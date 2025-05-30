"""Unit tests for the Textual user interface.

These tests exercise the key bindings and state persistence logic used by the
``AtlasTUI`` application.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codeatlas.tui import AtlasTUI


class TestTUI(unittest.TestCase):
    def test_vim_bindings_present(self) -> None:
        app = AtlasTUI()
        keys = {b[0] if isinstance(b, tuple) else b.key for b in app.BINDINGS}
        for key in ("j", "k", "h", "l", "r"):
            self.assertIn(key, keys)
        for action in (
            "move_up",
            "move_down",
            "move_left",
            "move_right",
            "refresh",
        ):
            self.assertTrue(hasattr(app, f"action_{action}"))

    def test_state_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            root = tmp_path / "proj"
            root.mkdir()
            config_dir = tmp_path / "conf"
            state_file = config_dir / "state.json"
            state_file.parent.mkdir(parents=True)
            state_file.write_text("{}")

            stored = {str(root.resolve()): ["foo.txt"]}
            state_file.write_text(json.dumps(stored))

            with patch.dict(os.environ, {"CODEATLAS_CONFIG_DIR": str(config_dir)}):
                app = AtlasTUI(root)
                self.assertEqual(app.targets, [root / "foo.txt"])

                app.targets.append(root / "bar.txt")
                app._save_current_state()
                new_state = json.loads(state_file.read_text())
                self.assertEqual(new_state[str(root.resolve())], ["foo.txt", "bar.txt"])


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
