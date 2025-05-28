"""Command line interface for CodeAtlas."""
from __future__ import annotations

import argparse
from pathlib import Path
from .scanner import scan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="codeatlas")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--include", action="append", default=None)
    parser.add_argument("--exclude", action="append", default=None)
    parser.add_argument("--content", action="store_true")
    parser.add_argument("--max-bytes", type=int, default=None)
    args = parser.parse_args(argv)

    entries = scan(
        args.root,
        include=args.include,
        exclude=args.exclude,
        include_contents=args.content,
        max_bytes=args.max_bytes,
    )
    for entry in entries:
        print(entry)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
