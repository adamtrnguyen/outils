# Outils

Tools and data for research.

## Structure

- `data/`: JSON data files used as input.
- `src/`: Python source scripts (`main.py`) for processing data.
- `out/`: Directory for generated output (Markdown files).

## Usage

This project is managed with [uv](https://github.com/astral-sh/uv).

To run the converter script:

```bash
uv run src/main.py -i data/<input_file>.json -o out
```

Example:

```bash
uv run src/main.py -i data/COR.json -o out
```
