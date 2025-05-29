"""Markdown formatter."""

from __future__ import annotations

from typing import Iterable

from ..scanner import FileEntry


def _format_entry(entry: FileEntry) -> str:
    """Return a string representation of ``entry`` as a Markdown section."""

    lines = [f"### {entry.path.as_posix()}", f"- size: {entry.size}"]
    if entry.content is not None:
        lines.append("```")
        lines.append(entry.content)
        lines.append("```")
    return "\n".join(lines)


def to_markdown(entries: Iterable[FileEntry]) -> str:
    """Return ``entries`` serialized as a Markdown document."""

    return "\n\n".join(_format_entry(e) for e in entries)

