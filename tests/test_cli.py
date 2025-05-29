"""Tests for the command line interface."""

from __future__ import annotations

import tempfile
import unittest

from codeatlas import cli


class TestCLI(unittest.TestCase):
    """Unit tests for :mod:`codeatlas.cli`."""

    def test_cli_runs(self) -> None:
        """``main`` should return ``0`` for a minimal invocation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(cli.main(["--root", tmpdir]), 0)


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
