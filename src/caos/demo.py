"""Run the provider-free M1 planning and selection demonstration."""

from .models import AgentProfile
from .planner import plan
from .selector import select_agent
from .state import StateStore


AGENTS = [
    AgentProfile(
        agent_id="planner-free",
        name="Planner Free Baseline",
        coding_score=5.0,
        architecture_score=7.0,
        research_score=7.0,
        context_window=32_000,
        availability=0.95,
        reliability=0.95,
    ),
    AgentProfile(
        agent_id="coder-free",
        name="Coder Free Baseline",
        coding_score=8.0,
        architecture_score=6.0,
        context_window=64_000,
        availability=0.90,
        reliability=0.90,
    ),
    AgentProfile(
        agent_id="premium-coder",
        name="Premium Coder Baseline",
        coding_score=9.5,
        architecture_score=8.5,
        context_window=128_000,
        cost_per_1k_input=0.002,
        cost_per_1k_output=0.008,
        availability=0.99,
        reliability=0.98,
    ),
]


def run(request: str, budget: float = 0.05) -> None:
    store = StateStore(":memory:")
    tasks = plan(request)

    print("CAOS M1 — first orchestration path")
    print(f"Budget: ${budget:.2f}\n")

    for task in tasks:
        store.record_task(task.task_id, task.description)
        selection = select_agent(task, AGENTS, budget_remaining=budget)
        budget -= selection.estimated_cost
        store.record_execution(
            task_id=task.task_id,
            agent_id=selection.agent_id,
            status="selected",
            cost_usd=selection.estimated_cost,
        )
        print(f"{task.task_id}: {task.description}")
        print(f"  → {selection.rationale}")
        print(f"  → Remaining budget: ${budget:.6f}\n")


if __name__ == "__main__":
    run("Build a small expense-tracking REST API")
