import pytest

from caos.dag import topological_order
from caos.models import Task


def test_topological_order_respects_dependencies():
    tasks = [
        Task(task_id="b", description="B", dependencies=("a",)),
        Task(task_id="a", description="A"),
    ]

    ordered = topological_order(tasks)

    assert [task.task_id for task in ordered] == ["a", "b"]


def test_cycle_is_rejected():
    tasks = [
        Task(task_id="a", description="A", dependencies=("b",)),
        Task(task_id="b", description="B", dependencies=("a",)),
    ]

    with pytest.raises(ValueError, match="cycle"):
        topological_order(tasks)
