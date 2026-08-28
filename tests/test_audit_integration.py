from caos.agent_catalog import AgentCapability, AgentCatalog, TaskRequirements
from caos.audit_trail import AuditTrail
from caos.execution_engine import AgentRegistry, AgentResult
from caos.execution_runtime import ExecutionRuntime
from caos.execution_session import ExecutionSessionManager, TaskRole
from caos.planning_contract import PlanSummary
from caos.task_graph import TaskGraph, TaskNode


class Agent:
    name = "developer"

    def execute(self, task, context):
        return AgentResult(True, output="ok")


def test_runtime_emits_session_selection_and_task_events():
    sessions = ExecutionSessionManager()
    plan = PlanSummary("p1", "Build", 0, 10, 0, ("build",))
    session = sessions.create("demo", plan, [(TaskRole.DEVELOPER, "build")])
    audit = AuditTrail()
    runtime = ExecutionRuntime(
        sessions,
        TaskGraph([TaskNode("task_1", TaskRole.DEVELOPER, "build")]),
        AgentCatalog([AgentCapability("developer", frozenset({TaskRole.DEVELOPER}), frozenset({"general"}), cost=0.01, quality=0.9)]),
        AgentRegistry([Agent()]),
        audit,
    )

    runtime.start(session.session_id)
    runtime.run_next(session.session_id, {"task_1": TaskRequirements(TaskRole.DEVELOPER, frozenset({"general"}))})

    assert [event.event_type for event in audit.for_session(session.session_id)] == [
        "SESSION_STARTED",
        "AGENT_SELECTED",
        "TASK_STARTED",
        "TASK_COMPLETED",
    ]
