from pathlib import Path

from codeatlas.extractor import read_text, detect_encoding


def test_read_text(tmp_path: Path) -> None:
    p = tmp_path / "sample.txt"
    p.write_text("hello")
    assert read_text(p) == "hello"


def test_truncation(tmp_path: Path) -> None:
    p = tmp_path / "long.txt"
    p.write_text("abcdef")
    assert read_text(p, max_bytes=3) == "abc"


def test_non_utf8(tmp_path: Path) -> None:
    p = tmp_path / "latin1.txt"
    data = "café".encode("latin-1")
    p.write_bytes(data)
    assert read_text(p) == "café"
