"""JSON formatter."""

from __future__ import annotations

import json
from typing import Iterable

from ..scanner import FileEntry


def to_json(entries: Iterable[FileEntry]) -> str:
    """Return ``entries`` serialized as a JSON string."""

    data = [
        {
            "path": e.path.as_posix(),
            "size": e.size,
            "mtime": e.mtime,
            "content": e.content,
        }
        for e in entries
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)

