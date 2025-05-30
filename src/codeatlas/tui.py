"""Textual user interface for selecting files and directories.

This module provides a small wrapper around :mod:`textual` that lets a user
pick files or folders from a directory tree.  The selected paths are persisted
between sessions so that reports can be regenerated easily.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Any
import os
import json

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual import events
from textual.widgets import (
    DirectoryTree,
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
)

from .scanner import scan
from .formatter.text import to_text

CONFIG_ENV = "CODEATLAS_CONFIG_DIR"


def _state_file() -> Path:
    config_dir = Path(os.environ.get(CONFIG_ENV, Path.home() / ".codeatlas"))
    return config_dir / "state.json"


def _load_state() -> dict[str, list[str]]:
    path = _state_file()
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:  # pragma: no cover - malformed state
            return {}
    return {}


def _save_state(data: dict[str, list[str]]) -> None:
    path = _state_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


pyperclip: Any | None
try:
    import pyperclip as _pyperclip  # type: ignore

    pyperclip = _pyperclip
except Exception:  # pragma: no cover - fallback when pyperclip unavailable
    pyperclip = None


class PathItem(ListItem):
    """List item storing a filesystem path."""

    def __init__(self, path: Path) -> None:
        super().__init__(Label(path.as_posix()))
        self.path = path

    def on_click(
        self, event: events.Click
    ) -> None:  # pragma: no cover - UI interaction
        """Remove the item on double click."""
        if event.chain == 2:
            app = self.app
            if hasattr(app, "remove_path_item"):
                app.remove_path_item(self)
            event.stop()


class AtlasTUI(App):
    """Textual interface to select files and directories."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add", "Add target"),
        ("d", "remove", "Remove target"),
        ("c", "copy", "Copy to clipboard"),
        ("r", "refresh", "Refresh tree"),
        # Vim-like navigation bindings
        ("j", "move_down", "Cursor down"),
        ("k", "move_up", "Cursor up"),
        ("h", "move_left", "Collapse/parent"),
        ("l", "move_right", "Expand/toggle"),
    ]

    def __init__(self, root: Path | None = None) -> None:
        super().__init__()
        self.root = Path(root or ".").resolve()
        self._state = _load_state()
        stored = self._state.get(str(self.root), [])
        self.targets: list[Path] = [self.root / Path(p) for p in stored]

    def _save_current_state(self) -> None:
        self._state[str(self.root)] = [
            p.relative_to(self.root).as_posix() for p in self.targets
        ]
        _save_state(self._state)

    def _cursor_action(self, name: str) -> None:
        """Dispatch a cursor action to the focused widget."""

        widget = self.focused
        if widget is not None:
            method = getattr(widget, f"action_{name}", None)
            if method is not None:
                method()

    def action_move_up(self) -> None:
        self._cursor_action("cursor_up")

    def action_move_down(self) -> None:
        self._cursor_action("cursor_down")

    def action_move_left(self) -> None:
        if self.focused is self.dir_tree:
            self.dir_tree.action_cursor_parent()

    def action_move_right(self) -> None:
        if self.focused is self.dir_tree:
            self.dir_tree.action_toggle_node()

    def on_click(self, event: events.Click) -> None:
        """Handle click events, specifically double-clicks on directory tree."""
        # Check if it's a double-click on the directory tree
        if (
            event.chain == 2
            and hasattr(self, "dir_tree")
            and event.sender is self.dir_tree
        ):
            # Defer action until after the tree updates its selection
            self.call_later(self.action_add)
            event.stop()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            self.dir_tree = DirectoryTree(self.root)
            self.list_view = ListView()
            yield self.dir_tree
            yield self.list_view
        yield Footer()

    def on_mount(self) -> None:
        for path in self.targets:
            self.list_view.append(PathItem(path))

    def action_add(self) -> None:
        node = self.dir_tree.cursor_node
        if node and node.data:
            path = node.data.path
            if path not in self.targets:
                self.targets.append(path)
                self.list_view.append(PathItem(path))
                self._save_current_state()

    def action_remove(self) -> None:
        if self.list_view.index is not None:
            self._remove_index(self.list_view.index)

    def remove_path_item(self, item: PathItem) -> None:
        """Remove the specified path item."""
        items = list(self.list_view.query(PathItem))
        if item in items:
            idx = items.index(item)
            self._remove_index(idx)

    def _remove_index(self, idx: int) -> None:
        self.list_view.remove_items([idx])
        del self.targets[idx]
        self._save_current_state()

    def action_refresh(self) -> None:
        self.dir_tree.reload()

    async def action_quit(self) -> None:
        self._save_current_state()
        self.exit()

    def action_copy(self) -> None:
        text = self._build_report()
        if pyperclip is not None:
            pyperclip.copy(text)
            self.notify("Copied report to clipboard")
        else:  # pragma: no cover - clipboard fallback
            self.notify("pyperclip not available", severity="warning")

    def _build_report(self) -> str:
        patterns: list[str] = []
        for path in self.targets:
            rel = path.relative_to(self.root)
            if path.is_dir():
                patterns.append(rel.as_posix() + "/**")
            else:
                patterns.append(rel.as_posix())
        entries = scan(self.root, include=patterns, include_contents=True)
        return to_text(entries)


def main(argv: Iterable[str] | None = None) -> int:
    app = AtlasTUI()
    app.run()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
