import pytest

from caos.blueprint import BlueprintEngine
from caos.dag import DagBuilder, topological_order


def test_blueprint_becomes_dependency_aware_graph():
    blueprint = BlueprintEngine().analyze("Build a workout tracking app with recommendations")
    graph = DagBuilder().build(blueprint)
    graph.validate()
    assert len(graph.tasks) == 7
    assert graph.tasks[4].dependencies == ("task-003", "task-004")
    assert len(graph.acceptance_criteria) == 7


def test_ready_tasks_follow_dependencies():
    blueprint = BlueprintEngine().analyze("Build a small app")
    graph = DagBuilder().build(blueprint)
    ready = graph.ready_tasks({"task-001"})
    assert {task.task_id for task in ready} == {"task-002", "task-004"}


def test_topological_order_rejects_cycle():
    from caos.models import Task
    tasks = [Task("a", "A", dependencies=("b",)), Task("b", "B", dependencies=("a",))]
    with pytest.raises(ValueError, match="cycle"):
        topological_order(tasks)
