import pytest

from caos.cost_optimizer import CostPolicy
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline


AGENTS = [
    AgentProfile("free", "Free Coder", coding_score=0.65, architecture_score=0.55),
    AgentProfile("premium", "Premium Coder", coding_score=0.95, architecture_score=0.95,
                 cost_per_1k_input=0.01, cost_per_1k_output=0.02),
]


def test_pipeline_produces_dag_and_free_first_plan():
    plan = CostAwarePipeline(AGENTS).create_plan(
        "Build a workout tracking web app with recommendations that users can save."
    )
    assert len(plan.tasks) == 5
    assert plan.tasks[0].recommended.agent_id == "free"
    assert plan.tasks[0].task.dependencies == ()
    assert plan.tasks[1].task.dependencies == (plan.tasks[0].task.task_id,)
    assert plan.proposal.estimated_cost == 0


def test_pipeline_respects_budget():
    plan = CostAwarePipeline(AGENTS).create_plan(
        "Build a workout tracking web app with recommendations that users can save.",
        CostPolicy(budget_remaining=0),
    )
    assert all(item.recommended.is_free for item in plan.tasks)


def test_short_idea_requires_clarification():
    with pytest.raises(ValueError, match="needs clarification"):
        CostAwarePipeline(AGENTS).create_plan("Build an app")
