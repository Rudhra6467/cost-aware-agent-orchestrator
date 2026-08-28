from caos.planning_api import plan_from_request
from caos.cost_optimizer import CostPolicy
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline


def make_pipeline():
    return CostAwarePipeline([
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            capabilities={"coding": 0.8, "architecture": 0.6},
            context_window=8000,
            input_cost_per_million=0,
            output_cost_per_million=0,
            reliability=0.85,
            availability=0.95,
        ),
        AgentProfile(
            agent_id="paid-coder",
            name="Paid Coder",
            capabilities={"coding": 0.95, "architecture": 0.9},
            context_window=16000,
            input_cost_per_million=1,
            output_cost_per_million=2,
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
    try:
        plan_from_request({}, make_pipeline())
    except ValueError as exc:
        assert "idea" in str(exc)
    else:
        raise AssertionError("missing idea should fail")
