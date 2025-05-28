from pathlib import Path

from codeatlas.scanner import FileEntry, scan

FIXTURE = Path(__file__).parent / "fixtures" / "simple_tree"


def test_scan_returns_all_files():
    entries = scan(FIXTURE)
    names = {entry.path.as_posix() for entry in entries}
    assert names == {"foo.txt", "sub/bar.txt", "sub/skip.log"}


def test_scan_respects_exclude():
    entries = scan(FIXTURE, exclude=["*.log"])
    names = {entry.path.as_posix() for entry in entries}
    assert names == {"foo.txt", "sub/bar.txt"}


def test_scan_include_patterns():
    entries = scan(FIXTURE, include=["*.txt"])
    names = {entry.path.as_posix() for entry in entries}
    assert names == {"foo.txt", "sub/bar.txt"}


def test_scan_with_contents():
    entries = scan(FIXTURE, include_contents=True)
    foo = next(e for e in entries if e.path.name == "foo.txt")
    assert foo.content == "foo\n"
