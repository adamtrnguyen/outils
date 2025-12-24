#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def yaml_quote(s: str) -> str:
    """Safely quote a YAML string."""
    s = str(s).replace('"', '\\"')
    return f'"{s}"'


def render_yaml_scalar(v: Any) -> str:
    """Render a scalar value for YAML."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return yaml_quote(str(v))


def dict_to_frontmatter(obj: Dict[str, Any], keep_order: List[str] | None = None) -> str:
    """
    Convert dict to YAML frontmatter.
    - Lists become YAML lists.
    - Dicts are JSON-stringified (simple + safe).
    """
    lines: List[str] = ["---"]

    # Choose key order: preferred list first, then remaining keys sorted.
    keys: List[str] = []
    if keep_order:
        for k in keep_order:
            if k in obj:
                keys.append(k)
    for k in sorted(obj.keys()):
        if k not in keys:
            keys.append(k)

    for k in keys:
        v = obj[k]

        if isinstance(v, list):
            lines.append(f"{k}:")
            if v:
                for item in v:
                    lines.append(f"  - {render_yaml_scalar(item)}")
            else:
                lines.append("  -")
        elif isinstance(v, dict):
            lines.append(f"{k}: {yaml_quote(json.dumps(v, ensure_ascii=False))}")
        else:
            lines.append(f"{k}: {render_yaml_scalar(v)}")

    lines.append("---")
    return "\n".join(lines)


def load_json_list(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Top-level JSON must be an array (list of objects).")
    out: List[Dict[str, Any]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a JSON object.")
        out.append(item)
    return out


# Matches YAML frontmatter only if it is at the very top of the file.
FRONTMATTER_RE = re.compile(r"^\s*---\s*\n.*?\n---\s*\n", re.DOTALL)


def write_or_update_frontmatter(md_path: Path, frontmatter: str, body_if_new: str = "") -> None:
    """
    If file exists and starts with YAML frontmatter, replace ONLY that block.
    If file exists without frontmatter, prepend frontmatter.
    If file doesn't exist, create with frontmatter + optional body.
    """
    frontmatter_block = frontmatter.rstrip() + "\n\n"

    if md_path.exists():
        text = md_path.read_text(encoding="utf-8")

        if FRONTMATTER_RE.match(text):
            updated = FRONTMATTER_RE.sub(frontmatter_block, text, count=1)
        else:
            updated = frontmatter_block + text.lstrip()

        md_path.write_text(updated, encoding="utf-8")
    else:
        md_path.write_text(frontmatter_block + body_if_new, encoding="utf-8")


def safe_output_name(raw_name: str) -> str:
    """
    Use the filename exactly as provided, but prevent directory traversal
    (e.g. '../something'). We only allow a basename, not paths.
    """
    name = str(raw_name).strip()
    # Convert any path to just the final component
    return Path(name).name


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a JSON list of objects into Markdown notes with YAML frontmatter."
    )
    parser.add_argument("-i", "--input", required=True, help="Input JSON file (array of objects).")
    parser.add_argument("-o", "--output", required=True, help="Output directory for .md files.")
    parser.add_argument(
        "--filename-field",
        default="file_name",
        help="Field to use for the output filename (default: file_name).",
    )
    parser.add_argument(
        "--body-field",
        default=None,
        help="Optional field to write as markdown body under the frontmatter (used only when creating new files).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, update frontmatter even when files already exist. Without this, existing files are skipped.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    objects = load_json_list(input_path)

    preferred_order = ["title", "chapter", "section", "page", "base", "concepts"]

    written = 0
    skipped = 0

    for idx, obj in enumerate(objects, start=1):
        raw_name = obj.get(args.filename_field)

        if raw_name is None or str(raw_name).strip() == "":
            raw_name = f"note-{idx}"

        base_name = safe_output_name(str(raw_name))
        if not base_name.lower().endswith(".md"):
            base_name = base_name + ".md"

        out_path = output_dir / base_name

        if out_path.exists() and not args.overwrite:
            skipped += 1
            continue

        # Keep file_name out of YAML frontmatter
        obj_for_yaml = dict(obj)
        obj_for_yaml.pop("file_name", None)

        frontmatter = dict_to_frontmatter(obj_for_yaml, keep_order=preferred_order)

        body_if_new = ""
        if args.body_field:
            bv = obj.get(args.body_field, "")
            if bv is None:
                bv = ""
            body_if_new = str(bv).rstrip() + "\n"

        write_or_update_frontmatter(out_path, frontmatter, body_if_new=body_if_new)
        written += 1

    print(f"Updated/created {written} markdown file(s) in: {output_dir}")
    if skipped:
        print(f"Skipped {skipped} existing file(s) (run with --overwrite to update frontmatter).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

