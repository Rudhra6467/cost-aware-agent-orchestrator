"""Cost + capability + health aware resource routing.

The score is intentionally explainable. CAOS should minimize practical cost,
not blindly choose the lowest sticker price.
"""

from __future__ import annotations

from dataclasses import dataclass

from .cost_optimizer import CostOption, CostPolicy, rank_cost_options
from .models import AgentProfile, Task
from .provider_health import ProviderHealthRegistry


@dataclass(frozen=True)
class RouteDecision:
    agent_id: str
    estimated_cost: float
    expected_total_cost: float
    score: float
    rationale: str


class CostAwareRouter:
    def __init__(self, health: ProviderHealthRegistry | None = None) -> None:
        self.health = health

    def route(
        self,
        task: Task,
        agents: list[AgentProfile],
        *,
        policy: CostPolicy | None = None,
        handoff_penalty: float = 0.0,
    ) -> RouteDecision:
        policy = policy or CostPolicy()
        options = rank_cost_options(task, agents, policy)
        if self.health is not None:
            healthy = {item.provider_id for item in self.health.eligible()}
            options = [item for item in options if item.agent_id in healthy]
        if not options:
            raise ValueError("No healthy, legitimate resource satisfies the task constraints.")

        # The user-facing policy is explicitly free-first. Once a legitimate
        # free option satisfies the task constraints, do not silently replace
        # it with a paid provider merely because a weighted score favors it.
        if policy.prefer_free:
            free_options = [item for item in options if item.is_free]
            if free_options:
                options = free_options

        scored: list[RouteDecision] = []
        for option in options:
            expected = option.estimated_cost + handoff_penalty * (1.0 - option.reliability)
            quality = 0.6 * option.capability + 0.4 * option.reliability
            score = quality / (1.0 + expected)
            scored.append(
                RouteDecision(
                    option.agent_id,
                    option.estimated_cost,
                    expected,
                    score,
                    self._rationale(option, expected),
                )
            )
        return max(scored, key=lambda item: item.score)

    @staticmethod
    def _rationale(option: CostOption, expected: float) -> str:
        price = "free" if option.is_free else f"${option.estimated_cost:.6f} estimated"
        return (
            f"Selected {price} resource: capability={option.capability:.2f}, "
            f"reliability={option.reliability:.2f}, expected practical cost="
            f"${expected:.6f}."
        )
