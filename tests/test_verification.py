from pathlib import Path

import pytest

from caos.execution_session import ExecutionSessionManager, ExecutionStatus, TaskRole
from caos.planning_contract import PlanSummary
from caos.verification import ArtifactVerifier, artifact_contains, artifact_exists


def make_verifying_session():
    manager = ExecutionSessionManager()
    plan = PlanSummary("p1", "Test", 0, 10, 0, ("build",))
    session = manager.create("demo", plan, [(TaskRole.DEVELOPER, "write artifact")])
    manager.start(session.session_id)
    manager.complete_task(session.session_id, "task_1")
    assert session.status == ExecutionStatus.VERIFYING
    return session


def test_verifier_passes_and_completes_session(tmp_path: Path):
    session = make_verifying_session()
    artifact = tmp_path / "task_1.txt"
    artifact.write_text("task_id: task_1\nagent: deterministic-local\n", encoding="utf-8")

    result = ArtifactVerifier(tmp_path).verify(
        session,
        [artifact_exists("task_1.txt"), artifact_contains("task_1.txt", "deterministic-local")],
    )

    assert result.passed is True
    assert len(result.checks) == 2
    assert session.status == ExecutionStatus.COMPLETED
    assert session.error is None


def test_verifier_failure_enters_repairing(tmp_path: Path):
    session = make_verifying_session()

    result = ArtifactVerifier(tmp_path).verify(session, [artifact_exists("missing.txt")])

    assert result.passed is False
    assert session.status == ExecutionStatus.REPAIRING
    assert session.error == "Verification failed"


def test_verifier_rejects_non_verifying_session(tmp_path: Path):
    manager = ExecutionSessionManager()
    plan = PlanSummary("p1", "Test", 0, 10, 0, ("build",))
    session = manager.create("demo", plan, ["task"])

    with pytest.raises(ValueError, match="verifying state"):
        ArtifactVerifier(tmp_path).verify(session, [artifact_exists("task.txt")])
