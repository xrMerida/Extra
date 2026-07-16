# cleanwork

Interactive CLI tool for cleaning up `~/Desktop` and `~/Downloads`, inspired by `git rebase -i`.

## What it does

1. **Scans** `~/Desktop` and `~/Downloads` for all files
2. **Presents** an interactive, numbered list — you go through files one by one
3. For each file, you choose an action:
   - `p` — **pick**: move to `~/Documents` as-is
   - `r` — **rename**: move to `~/Documents` with a new filename
   - `d` — **delete**: permanently remove the file
   - `v` — **view**: preview the file contents (text or hex dump)
   - `s` — **skip**: leave the file where it is
   - `a` — **accept all**: pick all remaining files at once
   - `x` — **skip all**: skip all remaining files at once
   - `q` — **quit**: finish and apply changes
   - `l` — **list**: redisplay the file list
4. Shows a **confirmation summary** before applying
5. **Applies** all moves, renames, and deletions
6. Optionally **cleans** any leftover files from `~/Desktop` and `~/Downloads`

## Features

- Zero external dependencies (pure Python 3.10+)
- Colorful, terminal-friendly UI with ANSI formatting
- Handles filename collisions automatically (appends `_1`, `_2`, etc.)
- Supports text and binary file previews
- Confirmation prompts before any destructive action

## Installation

### Run directly (no install needed)

```bash
python -m cleanwork
```

### Install as a CLI command

```bash
cd cleanwork
pip install .
cleanwork
```

### Install in development mode

```bash
cd cleanwork
pip install -e .
```

## Project structure

```
cleanwork/
├── pyproject.toml          # Package metadata & build config
├── README.md
└── cleanwork/
    ├── __init__.py         # Version info
    ├── __main__.py         # Entry point (python -m cleanwork)
    ├── core.py             # File scanning, preview, and operations
    └── cli.py              # Interactive terminal UI
```

## Requirements

- Python 3.10+
- No external dependencies
