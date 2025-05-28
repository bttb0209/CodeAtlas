"""Utilities for reading and truncating text files."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple


def _detect_encoding(data: bytes) -> str:
    """Return the guessed encoding for *data*.

    The function tries UTF-8 first and falls back to latin-1. If the
    optional ``chardet`` package is available, it is used for detection.
    """
    try:
        import chardet  # type: ignore
    except Exception:
        chardet = None  # type: ignore

    if chardet is not None:
        result = chardet.detect(data)
        encoding = result.get("encoding")
        if encoding:
            return encoding

    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def extract_text(path: Path, max_bytes: int | None = None) -> Tuple[str, bool]:
    """Read text from ``path`` with optional byte truncation.

    Parameters
    ----------
    path:
        File to read.
    max_bytes:
        If given, at most this many bytes are read from the file. When the
        file is larger, the returned ``truncated`` flag is ``True``.

    Returns
    -------
    tuple[str, bool]
        Decoded text and a boolean indicating whether the file was truncated.
    """
    with open(path, "rb") as f:
        if max_bytes is not None:
            raw = f.read(max_bytes + 1)
        else:
            raw = f.read()

    truncated = max_bytes is not None and len(raw) > max_bytes
    if truncated:
        raw = raw[:max_bytes]

    encoding = _detect_encoding(raw)
    text = raw.decode(encoding, errors="replace")
    return text, truncated

