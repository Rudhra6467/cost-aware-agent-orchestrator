"""Dependency-aware task graphs for CAOS execution sessions."""

from dataclasses import dataclass, field

from .execution_session import ExecutionTask, TaskRole
from .planning_contract import PlanSummary, PlanningResponse


@dataclass(frozen=True)
class TaskNode:
    task_id: str
    role: TaskRole
    description: str
    depends_on: tuple[str, ...] = ()


@dataclass
class TaskGraph:
    nodes: dict[str, TaskNode] = field(default_factory=dict)

    def add(self, node: TaskNode) -> None:
        if node.task_id in self.nodes:
            raise ValueError(f"Duplicate task: {node.task_id}")
        missing = [dependency for dependency in node.depends_on if dependency not in self.nodes]
        if missing:
            raise ValueError(f"Unknown task dependencies: {', '.join(missing)}")
        self.nodes[node.task_id] = node

    def ready(self, completed: set[str]) -> list[TaskNode]:
        return [
            node for node in self.nodes.values()
            if node.task_id not in completed and all(dep in completed for dep in node.depends_on)
        ]

    def validate(self) -> None:
        for node in self.nodes.values():
            if node.task_id in node.depends_on:
                raise ValueError(f"Task cannot depend on itself: {node.task_id}")

    def as_session_tasks(self) -> list[tuple[TaskRole, str]]:
        return [(node.role, node.description) for node in self.nodes.values()]


class TaskGraphBuilder:
    """Builds a deterministic graph from an approved planning response."""

    def build(self, response: PlanningResponse, plan: PlanSummary) -> TaskGraph:
        graph = TaskGraph()
        graph.add(TaskNode("task_1", TaskRole.ANALYST, "Analyze the requested outcome and constraints"))
        graph.add(TaskNode("task_2", TaskRole.DEVELOPER, f"Execute the {plan.label} implementation plan", ("task_1",)))
        graph.add(TaskNode("task_3", TaskRole.REVIEWER, "Review the implementation against the selected plan", ("task_2",)))
        graph.add(TaskNode("task_4", TaskRole.VERIFIER, "Verify the result against the requested outcome", ("task_3",)))
        if "DIY" in response.next_actions:
            graph.add(TaskNode("task_5", TaskRole.HANDOFF, "Prepare a clear implementation handoff", ("task_4",)))
        graph.validate()
        return graph
