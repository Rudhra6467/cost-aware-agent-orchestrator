"""Provider-neutral agent catalog and requirement-aware selection scoring."""

from dataclasses import dataclass

from .agent_policy import AgentProfile
from .execution_session import ExecutionTask, TaskRole


@dataclass(frozen=True)
class AgentCapability:
    name: str
    roles: frozenset[TaskRole]
    capabilities: frozenset[str] = frozenset()
    cost: float = 0.0
    quality: float = 0.5
    latency: float = 1.0
    reliability: float = 1.0

    def profile(self) -> AgentProfile:
        return AgentProfile(self.name, self.roles, cost_tier=int(self.cost * 1000))


@dataclass(frozen=True)
class TaskRequirements:
    role: TaskRole
    capabilities: frozenset[str] = frozenset()
    min_quality: float = 0.0
    max_cost: float | None = None


@dataclass(frozen=True)
class AgentScore:
    agent: AgentCapability
    score: float
    reasons: tuple[str, ...]


class AgentCatalog:
    """Ranks capable agents while keeping selection deterministic and explainable."""

    def __init__(self, agents: list[AgentCapability]) -> None:
        self.agents = tuple(agents)

    def rank(self, requirements: TaskRequirements) -> list[AgentScore]:
        scored: list[AgentScore] = []
        for agent in self.agents:
            if requirements.role not in agent.roles:
                continue
            if not requirements.capabilities.issubset(agent.capabilities):
                continue
            if agent.quality < requirements.min_quality:
                continue
            if requirements.max_cost is not None and agent.cost > requirements.max_cost:
                continue

            capability_match = len(requirements.capabilities) / max(len(agent.capabilities), 1)
            score = (
                capability_match * 0.35
                + agent.quality * 0.30
                + agent.reliability * 0.20
                + (1.0 / max(agent.latency, 0.01)) * 0.05
                + (1.0 / max(agent.cost, 0.01)) * 0.10 if agent.cost > 0 else 1.0
            )
            reasons = (
                f"supports role {requirements.role.value}",
                f"quality={agent.quality:.2f}",
                f"reliability={agent.reliability:.2f}",
                f"cost={agent.cost:.4f}",
            )
            scored.append(AgentScore(agent, score, reasons))

        return sorted(scored, key=lambda item: (-item.score, item.agent.name))

    def select(self, requirements: TaskRequirements) -> AgentScore:
        ranked = self.rank(requirements)
        if not ranked:
            raise LookupError(f"No agent satisfies requirements for role: {requirements.role.value}")
        return ranked[0]
