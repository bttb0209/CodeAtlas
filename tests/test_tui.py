from codeatlas.tui import AtlasTUI


def test_vim_bindings_present():
    app = AtlasTUI()
    keys = {b[0] if isinstance(b, tuple) else b.key for b in app.BINDINGS}
    for key in ("j", "k", "h", "l"):
        assert key in keys
    for action in ("move_up", "move_down", "move_left", "move_right"):
        assert hasattr(app, f"action_{action}")
