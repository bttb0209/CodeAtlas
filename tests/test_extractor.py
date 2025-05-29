"""Tests for text extraction utilities."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from codeatlas.extractor import read_text


class TestExtractor(unittest.TestCase):
    """Unit tests for :mod:`codeatlas.extractor`."""

    def test_read_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "sample.txt"
            p.write_text("hello")
            self.assertEqual(read_text(p), "hello")

    def test_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "long.txt"
            p.write_text("abcdef")
            self.assertEqual(read_text(p, max_bytes=3), "abc")

    def test_non_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "latin1.txt"
            data = "café".encode("latin-1")
            p.write_bytes(data)
            self.assertEqual(read_text(p), "café")


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
