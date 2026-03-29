# CLAUDE.md — outils

## Overview

Personal utility for converting JSON datasets into structured Markdown notes with YAML frontmatter. Used to generate Obsidian vault notes for textbooks, problem sets, and courses.

## Structure

```
src/outils/
├── __init__.py
└── main.py        — CLI entry point (outils command)
scripts/
├── extract_nc150.py  — NeetCode 150 data extractor
└── extract_sdp.py    — System Design Primer extractor
data/                  — JSON datasets (NC150, SDP, TADM, HTD, UDL, etc.)
notes/NC150/           — Generated NeetCode 150 markdown notes
```

## Key Commands

```bash
uv run outils -i data/NC150.json -o notes/NC150   # Generate notes from JSON
uv run python scripts/extract_nc150.py              # Extract NeetCode data
```

## Key Conventions

- Python 3.11+, hatchling build
- Uses playwright for web scraping, pypdf for PDF extraction
- JSON data files serve as input for note generation
- Generated notes target the Obsidian vault
