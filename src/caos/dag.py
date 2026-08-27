"""Dependency-aware project graph construction and validation."""

from dataclasses import dataclass

from .blueprint import ProductBlueprint
from .models import Task


@dataclass(frozen=True)
class AcceptanceCriterion:
    criterion_id: str
    description: str
    task_id: str


@dataclass(frozen=True)
class TaskGraph:
    tasks: tuple[Task, ...]
    acceptance_criteria: tuple[AcceptanceCriterion, ...]

    def validate(self) -> None:
        by_id = {task.task_id: task for task in self.tasks}
        if len(by_id) != len(self.tasks):
            raise ValueError("Task IDs must be unique")
        for task in self.tasks:
            missing = set(task.dependencies) - set(by_id)
            if missing:
                raise ValueError(f"Task {task.task_id} has missing dependencies: {sorted(missing)}")

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise ValueError("Task graph contains a dependency cycle")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in by_id[task_id].dependencies:
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in by_id:
            visit(task_id)

    def ready_tasks(self, completed: set[str]) -> tuple[Task, ...]:
        return tuple(
            task for task in self.tasks
            if task.task_id not in completed and set(task.dependencies).issubset(completed)
        )


def topological_order(tasks: list[Task]) -> list[Task]:
    graph = TaskGraph(tuple(tasks), ())
    graph.validate()
    by_id = {task.task_id: task for task in tasks}
    ordered: list[Task] = []
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visited:
            return
        for dependency in by_id[task_id].dependencies:
            visit(dependency)
        visited.add(task_id)
        ordered.append(by_id[task_id])

    for task in tasks:
        visit(task.task_id)
    return ordered


class DagBuilder:
    """Deterministic baseline: blueprint -> executable planning DAG."""

    def build(self, blueprint: ProductBlueprint) -> TaskGraph:
        if not blueprint.raw_idea.strip():
            raise ValueError("Blueprint must contain an idea")

        tasks = (
            Task("task-001", f"Finalize requirements and acceptance criteria for: {blueprint.raw_idea}", "architecture", 700, 900, 5.0),
            Task("task-002", "Design application data model and persistence strategy", "architecture", 900, 1100, 5.0, dependencies=("task-001",)),
            Task("task-003", "Implement backend services and API contracts", "coding", 1600, 2800, 6.0, dependencies=("task-002",)),
            Task("task-004", "Implement frontend user flows and interface", "coding", 1400, 2600, 6.0, dependencies=("task-001",)),
            Task("task-005", "Integrate frontend, backend and external services", "coding", 1200, 2200, 6.0, dependencies=("task-003", "task-004")),
            Task("task-006", "Run automated tests and fix verified failures", "coding", 1300, 2200, 6.0, dependencies=("task-005",)),
            Task("task-007", "Verify acceptance criteria and prepare deployment", "architecture", 900, 1200, 5.0, dependencies=("task-006",)),
        )
        criteria = tuple(
            AcceptanceCriterion(f"AC-{i:03d}", description, task_id)
            for i, (description, task_id) in enumerate((
                ("Requirements are explicit and reviewable", "task-001"),
                ("Data model supports required product state", "task-002"),
                ("Backend behavior matches defined contracts", "task-003"),
                ("Primary user flows are functional", "task-004"),
                ("Integrated application works across components", "task-005"),
                ("Automated verification passes", "task-006"),
                ("All agreed acceptance criteria are verified", "task-007"),
            ), 1)
        )
        graph = TaskGraph(tasks, criteria)
        graph.validate()
        return graph
