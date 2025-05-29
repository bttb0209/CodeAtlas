import json
from codeatlas.tui import AtlasTUI


def test_vim_bindings_present():
    app = AtlasTUI()
    keys = {b[0] if isinstance(b, tuple) else b.key for b in app.BINDINGS}
    for key in ("j", "k", "h", "l", "r"):
        assert key in keys
    for action in ("move_up", "move_down", "move_left", "move_right", "refresh"):
        assert hasattr(app, f"action_{action}")


def test_state_persistence(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    root.mkdir()
    config_dir = tmp_path / "conf"
    monkeypatch.setenv("CODEATLAS_CONFIG_DIR", str(config_dir))
    state_file = config_dir / "state.json"
    state_file.parent.mkdir(parents=True)
    state_file.write_text("{}")

    stored = {str(root.resolve()): ["foo.txt"]}
    state_file.write_text(json.dumps(stored))

    app = AtlasTUI(root)
    assert app.targets == [root / "foo.txt"]

    app.targets.append(root / "bar.txt")
    app._save_current_state()
    new_state = json.loads(state_file.read_text())
    assert new_state[str(root.resolve())] == ["foo.txt", "bar.txt"]
