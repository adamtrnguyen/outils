# Outils

Convert JSON datasets into structured Markdown notes with YAML frontmatter.

## Structure

- `data/`: JSON data files used as input.
- `scripts/`: Data extraction scripts (NeetCode, System Design Primer, etc.).
- `src/outils/`: Core Python package logic.
- `notes/`: (Recommended) Directory for generated Markdown notes.

## Installation

This project is managed with [uv](https://github.com/astral-sh/uv).

```bash
# Install dependencies
uv sync
```

## Usage

You can use the `outils` command directly via `uv run`.

### Basic Usage
```bash
uv run outils -i data/NC150.json -o notes/NC150
```

### Sync Usage
Use `--overwrite` to update existing frontmatter.
```bash
uv run outils -i data/NC150.json -o notes/NC150 --overwrite
```

## Data Extraction

New datasets can be generated using the scripts in `scripts/`:

```bash
# Extract NeetCode 150
uv run scripts/extract_nc150.py

# Extract System Design Primer
uv run scripts/extract_sdp.py
```
