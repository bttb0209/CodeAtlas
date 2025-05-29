# CodeAtlas

*A lightweight CLI that scans a directory tree and emits a plain text summary.*

---

## ✨ Features

* **Recursive scan** – depth‑first walk from any root directory.
* **Content extraction** – inlines text‑based files with basic encoding detection.
* **Metadata tags** – records file size and modified time.
* **Include/Exclude patterns** – simple glob matching via `--include` and `--exclude`.
* **Plain text output** – results are printed line by line.

---

## Quick Start

```bash
# Install from PyPI (or clone the repo and install locally)
pip install codeatlas

# Scan a project and capture the first 20 kB of each text file
codeatlas --root ~/my/project --content --max-bytes 20000 > snapshot.txt
```

---

## CLI Usage

```bash
$ codeatlas --help
```

Outputs:

```
usage: codeatlas [-h] [--root ROOT] [--include INCLUDE] [--exclude EXCLUDE]
                 [--content] [--max-bytes MAX_BYTES]

options:
  -h, --help            show this help message and exit
  --root ROOT
  --include INCLUDE
  --exclude EXCLUDE
  --content
  --max-bytes MAX_BYTES
```

---

## TUI Usage

### When Installed from PyPI

```bash
codeatlas-tui
```

### Running Directly from Source

Install the TUI dependencies and launch the module with the `src` layout:

```bash
git clone https://github.com/bttb0209/codeatlas.git
cd codeatlas
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m codeatlas.tui
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
pip install -e .
```

---

## Development Guidelines

| Topic          | Standard                                                |
| -------------- | ------------------------------------------------------- |
| **Language**   | Python ≥ 3.9                                            |
| **Linting**    | [ruff](https://github.com/astral-sh/ruff)               |
| **Formatting** | [Black](https://github.com/psf/black)                   |
| **Docstrings** | NumPy style                                             |
| **Tests**      | `unittest`                                              |

---

## Contributing

1. Fork the repo and create a feature branch.
2. Follow the **Development Guidelines** above.
3. Ensure the test suite passes.
4. Submit a pull request describing **why** and **how** your change helps.
