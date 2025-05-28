import sys
from pathlib import Path

# Ensure the src directory is on the path when running tests without installing
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from codeatlas import extractor


def test_read_full_file(tmp_path: Path) -> None:
    file_path = tmp_path / "hello.txt"
    file_path.write_text("hello world", encoding="utf-8")

    text, truncated = extractor.extract_text(file_path)

    assert text == "hello world"
    assert truncated is False


def test_truncate_file(tmp_path: Path) -> None:
    file_path = tmp_path / "long.txt"
    file_path.write_text("abcdef", encoding="utf-8")

    text, truncated = extractor.extract_text(file_path, max_bytes=3)

    assert text == "abc"
    assert truncated is True


def test_encoding_detection(tmp_path: Path) -> None:
    file_path = tmp_path / "latin1.txt"
    # word caf\xe9 encoded in latin-1
    file_path.write_bytes("caf\xe9".encode("latin-1"))

    text, truncated = extractor.extract_text(file_path)

    assert text == "café"
    assert truncated is False
