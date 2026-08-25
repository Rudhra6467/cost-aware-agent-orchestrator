"""Free-first, legitimate cost optimization primitives for CAOS.

This module intentionally uses transparent deterministic rules. More advanced
optimization strategies will be benchmarked against this baseline.
"""

from dataclasses import dataclass

from .models import AgentProfile, Task
from .selector import capability_score, estimate_cost


@dataclass(frozen=True)
class CostPolicy:
    """User constraints and the optimizer's operating policy."""

    budget_remaining: float | None = None
    minimum_capability: float = 0.0
    prefer_free: bool = True
    free_cost_epsilon: float = 1e-12


@dataclass(frozen=True)
class CostOption:
    """One feasible execution option exposed to the user."""

    agent_id: str
    agent_name: str
    estimated_cost: float
    capability: float
    reliability: float
    availability: float
    is_free: bool
    rationale: str


def rank_cost_options(
    task: Task,
    agents: list[AgentProfile],
    policy: CostPolicy | None = None,
) -> list[CostOption]:
    """Return feasible options using a free-first, quality-aware policy.

    Free resources are preferred only when they meet the requested capability.
    This avoids the false assumption that $0 is always the most economical
    outcome.
    """
    policy = policy or CostPolicy()
    options: list[CostOption] = []

    for agent in agents:
        if not agent.enabled or agent.context_window < task.context_required:
            continue

        capability = capability_score(agent, task)
        required = max(task.minimum_capability, policy.minimum_capability)
        if capability < required:
            continue

        cost = estimate_cost(agent, task)
        if policy.budget_remaining is not None and cost > policy.budget_remaining:
            continue

        is_free = cost <= policy.free_cost_epsilon
        rationale = (
            "Legitimate free option meeting capability threshold."
            if is_free
            else "Paid/usage-priced option retained because it meets capability and budget constraints."
        )
        options.append(
            CostOption(
                agent_id=agent.agent_id,
                agent_name=agent.name,
                estimated_cost=cost,
                capability=capability,
                reliability=agent.reliability,
                availability=agent.availability,
                is_free=is_free,
                rationale=rationale,
            )
        )

    # Primary order: legitimate free options first; within each group prefer
    # higher reliability/capability, then lower price.
    options.sort(
        key=lambda option: (
            0 if policy.prefer_free and option.is_free else 1,
            -option.reliability,
            -option.capability,
            option.estimated_cost,
        )
    )
    return options


def recommend_lowest_practical_cost(
    task: Task,
    agents: list[AgentProfile],
    policy: CostPolicy | None = None,
) -> CostOption:
    """Choose the first option from the transparent free-first ranking."""
    options = rank_cost_options(task, agents, policy)
    if not options:
        raise ValueError("No legitimate feasible resource satisfies the task constraints.")
    return options[0]
