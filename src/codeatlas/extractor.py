"""Utilities for reading text files with basic encoding detection."""

from __future__ import annotations

from pathlib import Path

__all__ = ["read_text", "detect_encoding"]


def detect_encoding(data: bytes) -> str:
    """Return ``utf-8`` if ``data`` decodes successfully, else ``latin-1``."""
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def read_text(path: Path, max_bytes: int | None = None) -> str:
    """Read ``path`` and return decoded text.

    Parameters
    ----------
    path:
        The file to read.
    max_bytes:
        Maximum number of bytes to read. ``None`` means no limit.
    """
    num = max_bytes if max_bytes is not None else -1
    with path.open("rb") as fh:
        data = fh.read(num)

    encoding = detect_encoding(data)
    return data.decode(encoding, errors="replace")
