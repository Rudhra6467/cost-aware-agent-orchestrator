from caos.execution_scheduler import ExecutionScheduler
from caos.execution_session import ExecutionSessionManager, TaskRole, TaskStatus
from caos.planning_contract import PlanSummary
from caos.task_graph import TaskGraph, TaskNode


def make_session():
    manager = ExecutionSessionManager()
    plan = PlanSummary("p1", "Test", 0, 10, 0, ("build",))
    session = manager.create(
        "test",
        plan,
        [
            (TaskRole.ANALYST, "analyze"),
            (TaskRole.DEVELOPER, "develop"),
            (TaskRole.VERIFIER, "verify"),
        ],
    )
    manager.start(session.session_id)
    return manager, session


def test_scheduler_only_exposes_dependency_ready_tasks():
    manager, session = make_session()
    graph = TaskGraph([
        TaskNode("task_1", TaskRole.ANALYST, "analyze"),
        TaskNode("task_2", TaskRole.DEVELOPER, "develop", ("task_1",)),
        TaskNode("task_3", TaskRole.VERIFIER, "verify", ("task_2",)),
    ])
    scheduler = ExecutionScheduler(graph)

    assert scheduler.ready_tasks(session) == ["task_1"]
    assert scheduler.can_run(session, "task_2") is False

    manager.complete_task(session.session_id, "task_1")
    assert scheduler.ready_tasks(session) == ["task_2"]

    manager.complete_task(session.session_id, "task_2")
    assert scheduler.ready_tasks(session) == ["task_3"]


def test_scheduler_does_not_repeat_running_tasks():
    manager, session = make_session()
    graph = TaskGraph([TaskNode("task_1", TaskRole.ANALYST, "analyze")])
    scheduler = ExecutionScheduler(graph)
    session.tasks[0].status = TaskStatus.RUNNING

    assert scheduler.ready_tasks(session) == []
