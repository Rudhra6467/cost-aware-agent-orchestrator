import pytest

from caos.planning_api import plan_from_request
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline


def make_pipeline():
    return CostAwarePipeline([
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
        AgentProfile(
            agent_id="paid-coder",
            name="Paid Coder",
            coding_score=0.95,
            architecture_score=0.90,
            context_window=16_000,
            cost_per_1k_input=0.001,
            cost_per_1k_output=0.002,
            reliability=0.95,
            availability=0.99,
        ),
    ])


def test_plan_from_request_returns_end_user_contract():
    response = plan_from_request(
        {"idea": "Build a simple fitness tracking app for home workouts"},
        make_pipeline(),
    )

    assert response["idea"]
    assert response["understanding"]
    assert response["blueprint"]["layers"]
    assert response["tasks"]
    assert response["recommendation"]["action"] == "BUILD"
    assert response["recommendation"]["resource"] == "Free Coder"
    assert response["diy"]["steps"]


def test_plan_from_request_rejects_missing_idea():
    with pytest.raises(ValueError, match="idea"):
        plan_from_request({}, make_pipeline())
