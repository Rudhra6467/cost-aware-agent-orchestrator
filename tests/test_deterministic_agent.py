from pathlib import Path

from caos.deterministic_agent import DeterministicAgent
from caos.execution_session import ExecutionTask, TaskRole


def test_deterministic_agent_writes_auditable_artifact(tmp_path: Path):
    agent = DeterministicAgent(tmp_path)
    task = ExecutionTask("task_1", "create fixture", TaskRole.DEVELOPER)

    result = agent.execute(task, {"artifact": "result.txt"})

    assert result.success is True
    artifact = tmp_path / "result.txt"
    assert artifact.exists()
    content = artifact.read_text(encoding="utf-8")
    assert "task_id: task_1" in content
    assert "role: developer" in content
    assert "agent: deterministic-local" in content
    assert result.output == content


def test_deterministic_agent_cannot_escape_workspace(tmp_path: Path):
    agent = DeterministicAgent(tmp_path)
    task = ExecutionTask("task_1", "safe", TaskRole.ANALYST)

    result = agent.execute(task, {"artifact": "../outside.txt"})

    assert result.success is True
    assert (tmp_path / "outside.txt").exists()
    assert not (tmp_path.parent / "outside.txt").exists()
