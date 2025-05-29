"""Plain text formatter."""

from __future__ import annotations

from typing import Iterable

from ..scanner import FileEntry


def _format_entry(entry: FileEntry) -> str:
    """Return a string representation of ``entry`` in plain text."""

    line = f"{entry.path.as_posix()} (size={entry.size})"
    if entry.content is None:
        return line
    return f"{line}\n{entry.content}"


def to_text(entries: Iterable[FileEntry]) -> str:
    """Return ``entries`` serialized as a plain text document."""

    return "\n".join(_format_entry(e) for e in entries)

