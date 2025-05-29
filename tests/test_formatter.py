import json
from pathlib import Path

from codeatlas.formatter import to_text, to_markdown, to_json
from codeatlas.scanner import FileEntry


def sample_entries():
    return [FileEntry(Path('foo.txt'), size=3, mtime=0.0, content='foo')]


def test_to_text():
    out = to_text(sample_entries())
    assert 'foo.txt' in out
    assert 'foo' in out


def test_to_markdown():
    out = to_markdown(sample_entries())
    assert '### foo.txt' in out
    assert '```' in out
    assert 'foo' in out


def test_to_json():
    out = to_json(sample_entries())
    data = json.loads(out)
    assert data[0]['path'] == 'foo.txt'
    assert data[0]['content'] == 'foo'
