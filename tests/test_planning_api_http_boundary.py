"""Regression test that isolates planning failures from HTTP serialization."""

from caos.cost_optimizer import CostPolicy
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline
from caos.planning_api import plan_from_request


def test_planning_contract_accepts_long_mvp_idea():
    pipeline = CostAwarePipeline([
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            coding_score=0.80,
            architecture_score=0.60,
            context_window=8_000,
            cost_per_1k_input=0,
            cost_per_1k_output=0,
            reliability=0.85,
            availability=0.95,
        ),
    ])

    result = plan_from_request(
        {"idea": "Build a simple fitness tracking application for home workouts"},
        pipeline,
    )

    assert result["recommendation"]["resource"] == "Free Coder"
    assert result["blueprint"]["status"] == "approved"
