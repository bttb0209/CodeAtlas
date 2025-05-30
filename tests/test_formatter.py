"""Unit tests for the formatter helpers.

These tests verify that the Markdown, JSON and plain text output functions
return the expected representations for a set of sample entries.
"""

import json
import unittest
from pathlib import Path

from codeatlas.formatter import to_markdown, to_json, to_text
from codeatlas.scanner import FileEntry


def sample_entries() -> list[FileEntry]:
    return [FileEntry(Path("foo.txt"), size=3, mtime=0.0, content="foo")]


class TestFormatter(unittest.TestCase):
    def test_to_text(self) -> None:
        out = to_text(sample_entries())
        self.assertIn("foo.txt", out)
        self.assertIn("foo", out)

    def test_to_markdown(self) -> None:
        out = to_markdown(sample_entries())
        self.assertIn("### foo.txt", out)
        self.assertIn("```", out)
        self.assertIn("foo", out)

    def test_to_json(self) -> None:
        out = to_json(sample_entries())
        data = json.loads(out)
        self.assertEqual(data[0]["path"], "foo.txt")
        self.assertEqual(data[0]["content"], "foo")


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
