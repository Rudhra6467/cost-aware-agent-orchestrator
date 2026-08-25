from caos.cost_optimizer import CostPolicy, rank_cost_options, recommend_lowest_practical_cost
from caos.models import AgentProfile, Task


AGENTS = [
    AgentProfile(
        agent_id="free",
        name="Free Capable Agent",
        coding_score=7.5,
        reliability=0.90,
        availability=0.95,
        cost_per_1k_input=0.0,
        cost_per_1k_output=0.0,
    ),
    AgentProfile(
        agent_id="cheap",
        name="Cheap Strong Agent",
        coding_score=9.0,
        reliability=0.98,
        availability=0.98,
        cost_per_1k_input=0.0002,
        cost_per_1k_output=0.0004,
    ),
]


def test_free_first_option_is_preferred_when_capable():
    task = Task(
        task_id="t1",
        description="Build API",
        minimum_capability=7.0,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )

    recommendation = recommend_lowest_practical_cost(task, AGENTS)

    assert recommendation.agent_id == "free"
    assert recommendation.is_free is True
    assert recommendation.estimated_cost == 0.0


def test_free_option_is_rejected_when_below_quality_threshold():
    task = Task(
        task_id="t2",
        description="Build security-sensitive API",
        minimum_capability=8.0,
    )

    recommendation = recommend_lowest_practical_cost(task, AGENTS)

    assert recommendation.agent_id == "cheap"
    assert recommendation.is_free is False
    assert recommendation.estimated_cost > 0


def test_budget_can_eliminate_paid_option():
    task = Task(
        task_id="t3",
        description="Build API",
        minimum_capability=8.0,
    )

    options = rank_cost_options(task, AGENTS, CostPolicy(budget_remaining=0.0))

    assert options == []
