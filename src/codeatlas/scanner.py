"""Directory scanning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class FileEntry:
    """Metadata for a single file."""

    path: Path
    size: int
    mtime: float
    content: str | None = None


def _matches(path: Path, patterns: Iterable[str] | None) -> bool:
    if not patterns:
        return True
    for pattern in patterns:
        if path.match(pattern):
            return True
    return False


def scan(
    root: Path,
    *,
    include: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    include_contents: bool = False,
    max_bytes: int | None = None,
) -> List[FileEntry]:
    """Recursively scan ``root`` and return a list of :class:`FileEntry`.

    Parameters
    ----------
    root:
        Directory to scan.
    include:
        Glob patterns to include (relative to ``root``). If ``None``, all files
        are included.
    exclude:
        Glob patterns to exclude. Checked after ``include``.
    include_contents:
        Whether to read file contents.
    max_bytes:
        If ``include_contents`` is ``True``, read at most this many bytes from
        each file.
    """
    root = Path(root)
    entries: List[FileEntry] = []

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_dir():
            continue
        if include is not None and not _matches(rel, include):
            continue
        if exclude is not None and _matches(rel, exclude):
            continue

        stat = path.stat()
        content: str | None = None
        if include_contents:
            num = max_bytes if max_bytes is not None else -1
            with path.open("rb") as fh:
                data = fh.read(num)
            content = data.decode("utf-8", errors="replace")

        entries.append(
            FileEntry(path=rel, size=stat.st_size, mtime=stat.st_mtime, content=content)
        )

    return entries
