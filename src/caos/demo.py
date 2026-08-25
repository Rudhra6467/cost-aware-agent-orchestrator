"""Run a provider-free CAOS cost-aware orchestration demonstration."""

from .agents import MockAgentExecutor
from .models import AgentProfile
from .orchestrator import CAOSOrchestrator


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
    orchestrator = CAOSOrchestrator(
        AGENTS,
        {
            agent.agent_id: MockAgentExecutor(agent.agent_id)
            for agent in AGENTS
        },
    )
    result = orchestrator.run(request, budget=budget)

    print("CAOS — cost-aware orchestration")
    print(f"Request: {request}")
    print(f"Estimated cost: ${result.estimated_cost:.6f}")
    print(f"Actual cost:    ${result.actual_cost:.6f}")
    print(f"Succeeded:      {result.succeeded}\n")

    for execution in result.executions:
        print(f"{execution.task_id}: {execution.option.agent_name}")
        print(f"  {execution.option.rationale}")
        print(f"  Status: {execution.result.status.value}\n")


if __name__ == "__main__":
    run("Build a small expense-tracking REST API")
