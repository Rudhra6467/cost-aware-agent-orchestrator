"""Validation and execution ordering for CAOS task DAGs."""

from .models import Task


def topological_order(tasks: list[Task]) -> list[Task]:
    """Return tasks in dependency order and reject cycles/missing dependencies."""
    by_id = {task.task_id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("Task IDs must be unique.")

    for task in tasks:
        missing = [dep for dep in task.dependencies if dep not in by_id]
        if missing:
            raise ValueError(f"Task {task.task_id} has missing dependencies: {missing}")

    visiting: set[str] = set()
    visited: set[str] = set()
    ordered: list[Task] = []

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ValueError("Task dependency graph contains a cycle.")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in by_id[task_id].dependencies:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
        ordered.append(by_id[task_id])

    for task in tasks:
        visit(task.task_id)
    return ordered
