"""Output formatters.

This module exposes simple helpers for turning :class:`~codeatlas.scanner.FileEntry`
objects into different textual representations.  The individual formatters live in
``text.py``, ``markdown.py`` and ``json_.py``.
"""

from .text import to_text
from .markdown import to_markdown
from .json_ import to_json

__all__ = ["to_text", "to_markdown", "to_json"]
