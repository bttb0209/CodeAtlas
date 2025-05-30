"""Unit tests for the Textual user interface.

These tests exercise the key bindings and state persistence logic used by the
``AtlasTUI`` application.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from codeatlas.tui import AtlasTUI
from textual import events


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

    def test_double_click_event_handler_exists(self) -> None:
        """Test that the double-click event handler exists and is callable."""
        app = AtlasTUI()
        
        # Check if the general click handler exists (this should handle directory tree clicks)
        self.assertTrue(hasattr(app, 'on_click'), 
                       "on_click handler should exist")
        
        # Check if it's callable
        handler = getattr(app, 'on_click')
        self.assertTrue(callable(handler), 
                       "on_click should be callable")
        
        # The old specific handler should not exist anymore
        self.assertFalse(hasattr(app, 'on_directory_tree_click'),
                        "on_directory_tree_click should not exist (replaced by general on_click)")
        
        # Test the method signature by creating a mock event
        mock_event = MagicMock(spec=events.Click)
        mock_event.chain = 2  # Double-click
        mock_event.sender = None  # Not the directory tree, so should be ignored
        
        # This should not raise an exception and should not do anything
        try:
            handler(mock_event)
        except AttributeError as e:
            if "call_later" in str(e):
                # This is expected if app context is not set up
                pass
            else:
                raise


if __name__ == "__main__":  # pragma: no cover - manual execution
    unittest.main()
