from pathlib import Path

from caos.artifact_parser import parse_file_artifacts
from caos.project_workspace import ProjectWorkspace, WorkspaceFile
from caos.verification import run_verification


def test_artifact_parser_is_explicit_and_safe():
    output = """Here are the files.\n\nFILE: app.py\n```python\nprint('ok')\n```\n\nFILE: ../bad.py\n```python\nprint('bad')\n```\n"""
    files = parse_file_artifacts(output)
    assert [(item.path, item.content) for item in files] == [("app.py", "print('ok')")]


def test_workspace_writes_generated_files(tmp_path: Path):
    workspace = ProjectWorkspace(tmp_path / "project")
    written = workspace.write_files([WorkspaceFile("app.py", "print('ok')")])
    assert written[0].exists()
    assert workspace.read_file("app.py") == "print('ok')"


def test_workspace_rejects_path_traversal(tmp_path: Path):
    workspace = ProjectWorkspace(tmp_path / "project")
    try:
        workspace.write_files([WorkspaceFile("../escape.txt", "bad")])
    except ValueError:
        pass
    else:
        raise AssertionError("path traversal should be rejected")


def test_verification_runner(tmp_path: Path):
    result = run_verification(tmp_path, ["python", "-c", "print('verified')"])
    assert result.passed is True
    assert "verified" in result.stdout
