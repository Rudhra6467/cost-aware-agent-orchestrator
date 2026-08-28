"""Project-planning DAG used by enrichment and cost-plan generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptanceCriterion:
    criterion_id: str
    description: str
    task_id: str


@dataclass(frozen=True)
class TaskGraph:
    tasks: tuple
    criteria: tuple = ()

    def validate(self) -> None:
        ids = {task.task_id for task in self.tasks}
        for task in self.tasks:
            unknown = [dep for dep in getattr(task, "dependencies", ()) if dep not in ids]
            if unknown:
                raise ValueError(f"Unknown task dependencies: {', '.join(unknown)}")
            if task.task_id in getattr(task, "dependencies", ()):
                raise ValueError(f"Task cannot depend on itself: {task.task_id}")
