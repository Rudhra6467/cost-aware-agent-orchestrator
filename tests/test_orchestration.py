from caos.agent_catalog import AgentCapability, AgentCatalog, TaskRequirements
from caos.execution_engine import AgentRegistry, AgentResult
from caos.execution_session import ExecutionSessionManager, TaskRole
from caos.orchestration import Orchestrator
from caos.planning_contract import PlanSummary


class Developer:
    name = "cheap-developer"

    def execute(self, task, context):
        return AgentResult(True, output="done")


def test_orchestrator_selects_records_and_executes_agent():
    sessions = ExecutionSessionManager()
    plan = PlanSummary("p1", "Test", 0, 10, 0, ("build",))
    session = sessions.create("test", plan, ["implement"])
    session.tasks[0].role = TaskRole.DEVELOPER
    sessions.start(session.session_id)

    catalog = AgentCatalog([
        AgentCapability("cheap-developer", frozenset({TaskRole.DEVELOPER}), frozenset({"python"}), cost=0.01, quality=0.9),
    ])
    agents = AgentRegistry([Developer()])
    orchestrator = Orchestrator(sessions, catalog, agents)

    decision, result = orchestrator.run_task(
        session.session_id,
        "task_1",
        TaskRequirements(TaskRole.DEVELOPER, frozenset({"python"}), min_quality=0.8),
    )

    assert result.success is True
    assert decision.agent_name == "cheap-developer"
    assert decision.task_id == "task_1"
    assert decision.reasons
    assert sessions.get(session.session_id).tasks[0].assigned_agent == "cheap-developer"
