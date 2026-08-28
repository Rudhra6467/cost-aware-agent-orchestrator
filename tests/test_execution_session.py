import pytest

from caos.execution_session import ExecutionSessionManager, ExecutionStatus, TaskStatus
from caos.planning_contract import PlanSummary


def plan():
    return PlanSummary(
        plan_id="zero-cost",
        label="Zero-Cost",
        monetary_cost=0.0,
        execution_minutes=30.0,
        quota_wait_minutes=0.0,
        critical_path=("build", "test"),
    )


def test_create_session_starts_ready_with_pending_tasks():
    manager = ExecutionSessionManager()
    session = manager.create("todo app", plan(), ["create app", "run tests"])

    assert session.status == ExecutionStatus.READY
    assert session.progress == 0.0
    assert [task.status for task in session.tasks] == [TaskStatus.PENDING, TaskStatus.PENDING]


def test_start_and_complete_tasks_moves_session_to_verification():
    manager = ExecutionSessionManager()
    session = manager.create("todo app", plan(), ["create app", "run tests"])

    manager.start(session.session_id)
    manager.complete_task(session.session_id, "task_1")
    session = manager.complete_task(session.session_id, "task_2")

    assert session.status == ExecutionStatus.VERIFYING
    assert session.completed_tasks == 2
    assert session.progress == 1.0


def test_unknown_task_is_rejected():
    manager = ExecutionSessionManager()
    session = manager.create("todo app", plan(), ["create app"])
    manager.start(session.session_id)

    with pytest.raises(KeyError, match="Unknown task"):
        manager.complete_task(session.session_id, "missing")
