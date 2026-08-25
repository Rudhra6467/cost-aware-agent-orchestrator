"""Deterministic, explainable first-pass agent selector."""

from .models import AgentProfile, Selection, Task


def estimate_cost(agent: AgentProfile, task: Task) -> float:
    """Estimate USD cost from the task's expected token usage."""
    return (
        task.estimated_input_tokens / 1000 * agent.cost_per_1k_input
        + task.estimated_output_tokens / 1000 * agent.cost_per_1k_output
    )


def capability_score(agent: AgentProfile, task: Task) -> float:
    """Return the capability score relevant to the task."""
    score = getattr(agent, f"{task.required_capability}_score", None)
    if score is None:
        score = agent.coding_score
    return float(score)


def select_agent(
    task: Task,
    agents: list[AgentProfile],
    budget_remaining: float | None = None,
) -> Selection:
    """Select the best feasible agent using cost, capability and reliability.

    This is intentionally a simple baseline. It is the algorithm we will
    benchmark and improve in later CAOS phases.
    """
    candidates: list[tuple[AgentProfile, float, float]] = []

    for agent in agents:
        if not agent.enabled or agent.context_window < task.context_required:
            continue

        capability = capability_score(agent, task)
        if capability < task.minimum_capability:
            continue

        cost = estimate_cost(agent, task)
        if budget_remaining is not None and cost > budget_remaining:
            continue

        # Higher capability/reliability/availability is better; lower cost is
        # better. A small epsilon prevents division by zero for free agents.
        utility = (
            (0.55 * capability / 10.0)
            + (0.25 * agent.reliability)
            + (0.20 * agent.availability)
        ) / (1.0 + cost)
        candidates.append((agent, cost, utility))

    if not candidates:
        raise ValueError("No feasible agent is available for this task and budget.")

    agent, cost, score = max(candidates, key=lambda item: item[2])
    capability = capability_score(agent, task)
    rationale = (
        f"Selected {agent.name}: capability={capability:.1f}/10, "
        f"reliability={agent.reliability:.2f}, availability={agent.availability:.2f}, "
        f"estimated_cost=${cost:.6f}."
    )
    return Selection(agent.agent_id, score, cost, rationale)
