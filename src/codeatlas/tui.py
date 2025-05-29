from __future__ import annotations

from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import DirectoryTree, Header, Footer, ListView, ListItem, Label

from .scanner import scan
from .formatter.text import to_text

try:
    import pyperclip
except Exception:  # pragma: no cover - fallback when pyperclip unavailable
    pyperclip = None


class PathItem(ListItem):
    """List item storing a filesystem path."""

    def __init__(self, path: Path) -> None:
        super().__init__(Label(path.as_posix()))
        self.path = path


class AtlasTUI(App):
    """Textual interface to select files and directories."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add", "Add target"),
        ("d", "remove", "Remove target"),
        ("c", "copy", "Copy to clipboard"),
        # Vim-like navigation bindings
        ("j", "move_down", "Cursor down"),
        ("k", "move_up", "Cursor up"),
        ("h", "move_left", "Collapse/parent"),
        ("l", "move_right", "Expand/toggle"),
    ]

    def __init__(self, root: Path | None = None) -> None:
        super().__init__()
        self.root = Path(root or ".").resolve()
        self.targets: list[Path] = []

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

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            self.dir_tree = DirectoryTree(self.root)
            self.list_view = ListView()
            yield self.dir_tree
            yield self.list_view
        yield Footer()

    def action_add(self) -> None:
        node = self.dir_tree.cursor_node
        if node and node.data:
            path = node.data.path
            if path not in self.targets:
                self.targets.append(path)
                self.list_view.append(PathItem(path))

    def action_remove(self) -> None:
        if self.list_view.index is not None:
            idx = self.list_view.index
            self.list_view.remove_items([idx])
            del self.targets[idx]

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
