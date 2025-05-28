from codeatlas import cli


def test_cli_runs(tmp_path):
    assert cli.main(["--root", str(tmp_path)]) == 0
