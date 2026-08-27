from caos.application_planner import ApplicationPlanner, Blueprint
from caos.planning_service import PlanningRequest
from caos.variant_policy import VariantPolicy
from caos.constraints import UserConstraints


class Analyzer:
    def analyze(self, idea):
        return Blueprint("A simple app blueprint", ("task-1",), ("Fixture analysis",))


class PolicyGenerator:
    policies = (VariantPolicy.ZERO_COST, VariantPolicy.LOWEST_PRACTICAL)


class Evaluation:
    def __init__(self, policy):
        self.policy = policy
        self.execution = type("E", (), {"monetary_cost": 0.0})()
        self.simulation = type("S", (), {"elapsed_minutes": 10.0, "critical_path": ("task-1",)})()
        self.total_wait_minutes = 0.0


class VariantEngine:
    policy_generator = PolicyGenerator()
    def evaluate(self, policy, tasks, ledger, windows):
        return Evaluation(policy)


def test_application_planner_composes_response():
    response = ApplicationPlanner(Analyzer(), VariantEngine(), ledger=None).plan(
        PlanningRequest("build an app", UserConstraints())
    )
    assert response.idea == "build an app"
    assert response.blueprint_summary == "A simple app blueprint"
    assert len(response.plans) == 2
    assert "BUILD" in response.next_actions
    assert "DIY" in response.next_actions
