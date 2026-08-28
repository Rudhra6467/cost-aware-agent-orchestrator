import pytest

from caos.agent_catalog import AgentCapability, AgentCatalog, TaskRequirements
from caos.execution_engine import AgentRegistry, AgentResult
from caos.execution_runtime import ExecutionRuntime
from caos.execution_session import ExecutionSessionManager, ExecutionStatus, TaskRole
from caos.repair_engine import RepairEngine
from caos.task_graph import TaskGraph, TaskNode
from caos.verification import VerificationCheck, VerificationResult
from caos.planning_contract import PlanSummary


class RepairAgent:
    name = "repair-agent"

    def execute(self, task, context):
        return AgentResult(True, output="repair complete")


def make_runtime():
    sessions = ExecutionSessionManager()
    plan = PlanSummary("p1", "Build", 0, 10, 0, ("build",))
    session = sessions.create("demo", plan, [(TaskRole.DEVELOPER, "original")])
    graph = TaskGraph([TaskNode("task_1", TaskRole.DEVELOPER, "original")])
    catalog = AgentCatalog([
        AgentCapability("repair-agent", frozenset({TaskRole.DEVELOPER}), frozenset({"repair"}), cost=0.01, quality=0.9),
    ])
    runtime = ExecutionRuntime(sessions, graph, catalog, AgentRegistry([RepairAgent()]))
    return runtime, session


def failed_verification():
    return VerificationResult(False, (VerificationCheck("artifact", False, "missing"),))


def test_repair_attempts_are_bounded_and_history_is_retained():
    runtime, session = make_runtime()
    engine = RepairEngine(runtime, max_attempts=2)
    session.status = ExecutionStatus.REPAIRING

    first = engine.prepare(session.session_id, failed_verification())
    session.status = ExecutionStatus.REPAIRING
    second = engine.prepare(session.session_id, failed_verification())

    assert first.attempt == 1
    assert second.attempt == 2
    assert engine.attempts(session.session_id) == 2
    assert len(engine.history(session.session_id)) == 2

    session.status = ExecutionStatus.REPAIRING
    with pytest.raises(RuntimeError, match="Maximum repair attempts"):
        engine.prepare(session.session_id, failed_verification())
    assert session.status is ExecutionStatus.FAILED
