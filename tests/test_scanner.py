"""Tests for directory scanning utilities."""

from __future__ import annotations

import unittest
from pathlib import Path

from codeatlas.scanner import scan


FIXTURE = Path(__file__).parent / "fixtures" / "simple_tree"


class TestScanner(unittest.TestCase):
    """Unit tests for :mod:`codeatlas.scanner`."""

    def test_scan_returns_all_files(self) -> None:
        entries = scan(FIXTURE)
        names = {entry.path.as_posix() for entry in entries}
        self.assertEqual(names, {"foo.txt", "sub/bar.txt", "sub/skip.log"})

    def test_scan_respects_exclude(self) -> None:
        entries = scan(FIXTURE, exclude=["*.log"])
        names = {entry.path.as_posix() for entry in entries}
        self.assertEqual(names, {"foo.txt", "sub/bar.txt"})

    def test_scan_include_patterns(self) -> None:
        entries = scan(FIXTURE, include=["*.txt"])
        names = {entry.path.as_posix() for entry in entries}
        self.assertEqual(names, {"foo.txt", "sub/bar.txt"})

    def test_scan_with_contents(self) -> None:
        entries = scan(FIXTURE, include_contents=True)
        foo = next(e for e in entries if e.path.name == "foo.txt")
        self.assertEqual(foo.content, "foo\n")


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
