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


def test_repair_uses_normal_orchestration_pipeline():
    sessions = ExecutionSessionManager()
    plan = PlanSummary("p1", "Build", 0, 10, 0, ("build",))
    session = sessions.create("demo", plan, [(TaskRole.DEVELOPER, "original")])
    session.status = ExecutionStatus.REPAIRING
    graph = TaskGraph([TaskNode("task_1", TaskRole.DEVELOPER, "original")])
    catalog = AgentCatalog([
        AgentCapability("repair-agent", frozenset({TaskRole.DEVELOPER}), frozenset({"repair"}), cost=0.01, quality=0.9),
    ])
    runtime = ExecutionRuntime(sessions, graph, catalog, AgentRegistry([RepairAgent()]))
    engine = RepairEngine(runtime)

    verification = VerificationResult(False, (VerificationCheck("artifact", False, "missing"),))
    repair = engine.prepare(session.session_id, verification)
    decision, result = engine.run(session.session_id, TaskRequirements(TaskRole.DEVELOPER, frozenset({"repair"})))

    assert repair.failed_checks == ("artifact",)
    assert decision.agent_name == "repair-agent"
    assert result.success is True
