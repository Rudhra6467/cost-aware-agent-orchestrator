from caos.execution_engine import AgentRegistry, AgentResult, ExecutionEngine
from caos.execution_session import ExecutionSessionManager, TaskStatus
from caos.planning_contract import PlanSummary


class FakeAgent:
    name = "developer"

    def execute(self, task, context):
        assert context["workspace"] == "fixture"
        return AgentResult(True, output=f"completed {task.task_id}")


class FailingAgent:
    name = "broken"

    def execute(self, task, context):
        return AgentResult(False, error="verification failed")


def session_manager():
    manager = ExecutionSessionManager()
    plan = PlanSummary("p1", "Test", 0, 10, 0, ("build",))
    session = manager.create("test", plan, ["first task"])
    manager.start(session.session_id)
    return manager, session


def test_engine_runs_task_through_named_agent():
    sessions, session = session_manager()
    engine = ExecutionEngine(sessions, AgentRegistry([FakeAgent()]))

    result = engine.run_task(session.session_id, "task_1", "developer", {"workspace": "fixture"})

    assert result.success is True
    assert sessions.get(session.session_id).tasks[0].status is TaskStatus.COMPLETED
    assert sessions.get(session.session_id).status.value == "verifying"


def test_engine_marks_session_failed_when_agent_fails():
    sessions, session = session_manager()
    engine = ExecutionEngine(sessions, AgentRegistry([FailingAgent()]))

    result = engine.run_task(session.session_id, "task_1", "broken")

    assert result.success is False
    assert sessions.get(session.session_id).tasks[0].status is TaskStatus.FAILED
    assert sessions.get(session.session_id).status.value == "failed"
    assert sessions.get(session.session_id).error == "verification failed"
