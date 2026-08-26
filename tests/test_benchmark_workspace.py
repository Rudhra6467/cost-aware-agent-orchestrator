from caos.benchmark_workspace import BenchmarkWorkspaceManager


def test_workspace_reset_is_isolated(tmp_path):
    manager = BenchmarkWorkspaceManager(tmp_path)
    first = manager.reset("run-001")
    (first.path / "generated.txt").write_text("old")
    second = manager.reset("run-001")
    assert second.path.exists()
    assert not (second.path / "generated.txt").exists()


def test_workspace_rejects_path_traversal(tmp_path):
    manager = BenchmarkWorkspaceManager(tmp_path)
    try:
        manager.reset("../escape")
    except ValueError:
        pass
    else:
        raise AssertionError("path traversal should be rejected")
