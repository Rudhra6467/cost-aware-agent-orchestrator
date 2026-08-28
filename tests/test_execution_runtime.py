from caos.agent_catalog import AgentCapability, AgentCatalog, TaskRequirements
from caos.execution_engine import AgentRegistry, AgentResult
from caos.execution_runtime import ExecutionRuntime
from caos.execution_session import ExecutionSessionManager, TaskRole
from caos.planning_contract import PlanSummary
from caos.task_graph import TaskGraph, TaskNode


class Agent:
    name = "developer"

    def execute(self, task, context):
        return AgentResult(True, output=task.description)


def test_runtime_runs_only_dependency_ready_tasks():
    sessions = ExecutionSessionManager()
    plan = PlanSummary("p1", "Build", 0, 10, 0, ("build",))
    session = sessions.create("demo", plan, [(TaskRole.ANALYST, "analyze"), (TaskRole.DEVELOPER, "develop")])
    graph = TaskGraph([
        TaskNode("task_1", TaskRole.ANALYST, "analyze"),
        TaskNode("task_2", TaskRole.DEVELOPER, "develop", ("task_1",)),
    ])
    catalog = AgentCatalog([
        AgentCapability("developer", frozenset({TaskRole.ANALYST, TaskRole.DEVELOPER}), frozenset({"general"}), cost=0.01, quality=0.9),
    ])
    runtime = ExecutionRuntime(sessions, graph, catalog, AgentRegistry([Agent()]))
    runtime.start(session.session_id)

    requirements = {
        "task_1": TaskRequirements(TaskRole.ANALYST, frozenset({"general"})),
        "task_2": TaskRequirements(TaskRole.DEVELOPER, frozenset({"general"})),
    }

    assert runtime.ready_tasks(session.session_id) == ["task_1"]
    runtime.run_next(session.session_id, requirements)
    assert runtime.ready_tasks(session.session_id) == ["task_2"]
    runtime.run_next(session.session_id, requirements)
    assert sessions.get(session.session_id).status.value == "verifying"
