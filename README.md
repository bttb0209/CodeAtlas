# CodeAtlas

*A lightweight CLI that "maps" a directory tree—paths, metadata, and (optionally) file contents—then emits a single, prompt‑ready text file for use with LLMs.*

---

## ✨ Features

* **Recursive scan** – depth‑first walk from any root directory.
* **Content extraction** – inlines text‑based files with automatic encoding detection (defaults to UTF‑8).
* **Metadata tags** – size, modified time, and custom key–value pairs per file.
* **Ignore / include patterns** – respects `.gitignore` syntax and supports `--exclude/--include` globs.
* **Multiple output modes**

  * Plain text (default)
  * Markdown (`--md`) with fenced code blocks
  * JSON (`--json`) for downstream tooling
* **Chunking** – splits oversized files or trees into token‑friendly pieces (`--- CHUNK n/m ---`).
* **Colorized preview** – ANSI‑styled tree for humans (`--color`).

---

## Quick Start

```bash
# Install from PyPI
pip install codeatlas

# Snapshot a project in Markdown, truncating each file to 20 kB
codeatlas --root ~/my/project --md --max-bytes 20000 > snapshot.md

# Paste or upload `snapshot.md` to ChatGPT / Claude / your internal model
```

---

## CLI Usage

```bash
$ codeatlas --help
Usage: codeatlas [OPTIONS]

Options:
  --root PATH             Root directory to scan (default: .)
  --md / --json           Output mode (plain text is default)
  --content               Include file contents (text files only)
  --max-bytes INTEGER     Truncate each file after N bytes
  --exclude PATTERN...    Glob(s) to skip (repeatable)
  --include PATTERN...    Limit scan to matching files
  --color                 ANSI colors for on-screen preview
  --save FILE             Write to FILE instead of stdout
  -h, --help              Show this message and exit
```

---

## Installation

### End Users

```bash
pip install codeatlas
```

### Contributors

```bash
git clone https://github.com/bttb0209/codeatlas.git
cd codeatlas
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```

---

## Development Guidelines

| Topic          | Standard                                                |
| -------------- | ------------------------------------------------------- |
| **Language**   | Python ≥ 3.9                                            |
| **Linting**    | [ruff](https://github.com/astral-sh/ruff) (`make lint`) |
| **Formatting** | [Black](https://github.com/psf/black) (`make format`)   |
| **Docstrings** | NumPy style                                             |
| **Tests**      | `pytest` + `pytest-cov` (`make test`)                   |

> **Tip:** pre‑commit hooks (`pre‑commit install`) will run ruff, Black, and tests automatically on each commit.

---

## Contributing

1. Fork the repo and create a feature branch.
2. Follow the **Development Guidelines** above.
3. Ensure `make lint format test` passes.
4. Submit a pull request—please describe **why** and **how** your change helps.

