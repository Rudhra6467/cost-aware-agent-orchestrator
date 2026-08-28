"""Deterministic, provider-neutral policy for assigning execution roles."""

from dataclasses import dataclass

from .execution_session import ExecutionTask, TaskRole


@dataclass(frozen=True)
class AgentProfile:
    name: str
    roles: frozenset[TaskRole]
    cost_tier: int = 0


class AgentSelectionPolicy:
    """Selects the cheapest capable registered agent for each task role."""

    def __init__(self, agents: list[AgentProfile]) -> None:
        self.agents = tuple(agents)

    def select(self, task: ExecutionTask) -> AgentProfile:
        candidates = [agent for agent in self.agents if task.role in agent.roles]
        if not candidates:
            raise LookupError(f"No capable agent for role: {task.role.value}")
        return min(candidates, key=lambda agent: (agent.cost_tier, agent.name))

    def assign(self, tasks: list[ExecutionTask]) -> dict[str, str]:
        return {task.task_id: self.select(task).name for task in tasks}
