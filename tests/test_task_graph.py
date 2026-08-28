import pytest

from caos.execution_session import TaskRole
from caos.planning_contract import PlanSummary, PlanningResponse
from caos.task_graph import TaskGraph, TaskGraphBuilder, TaskNode


def response(actions=("BUILD", "DIY")):
    plan = PlanSummary("p1", "Test Plan", 0.01, 10, 0.1, ("build",))
    return PlanningResponse("test", "summary", (), (plan,), "p1", (), "explain", actions)


def test_builder_creates_dependency_ordered_graph():
    graph = TaskGraphBuilder().build(response(), response().plans[0])
    assert list(graph.nodes) == ["task_1", "task_2", "task_3", "task_4", "task_5"]
    assert graph.nodes["task_2"].depends_on == ("task_1",)
    assert graph.nodes["task_4"].role is TaskRole.VERIFIER
    assert [n.task_id for n in graph.ready(set())] == ["task_1"]
    assert [n.task_id for n in graph.ready({"task_1"})] == ["task_2"]


def test_diy_handoff_is_omitted_when_not_available():
    result = response(("BUILD",))
    graph = TaskGraphBuilder().build(result, result.plans[0])
    assert "task_5" not in graph.nodes


def test_graph_rejects_duplicate_tasks_and_missing_dependencies():
    graph = TaskGraph()
    graph.add(TaskNode("task_1", TaskRole.ANALYST, "first"))
    with pytest.raises(ValueError, match="Duplicate task"):
        graph.add(TaskNode("task_1", TaskRole.DEVELOPER, "duplicate"))
    with pytest.raises(ValueError, match="Unknown task dependencies"):
        graph.add(TaskNode("task_2", TaskRole.DEVELOPER, "bad", ("missing",)))
