from caos.decision import DecisionReason, VariantDecisionEngine
from caos.execution import ExecutionEstimate
from caos.simulation import SimulationResult, TaskSchedule
from caos.variant_policy import VariantPolicy
from caos.variant_simulation import VariantEvaluation
from caos.constraints import UserConstraints


def evaluation(policy, cost, elapsed, wait=0):
    return VariantEvaluation(policy, SimulationResult((), (), elapsed, ()), ExecutionEstimate(cost, 0, 0, elapsed, cost), (), wait)


def test_decision_prefers_lowest_practical_cost_when_constraints_allow():
    result = VariantDecisionEngine().decide((
        evaluation(VariantPolicy.ZERO_COST, 0, 300),
        evaluation(VariantPolicy.LOWEST_PRACTICAL, 1, 120),
        evaluation(VariantPolicy.FASTEST_PRACTICAL, 3, 60),
    ), UserConstraints(budget=5, max_days=1))
    assert result.recommended == "zero-cost"
    assert DecisionReason.PRACTICAL_COST in result.reasons


def test_decision_rejects_over_budget_plan():
    result = VariantDecisionEngine().decide((
        evaluation(VariantPolicy.ZERO_COST, 0, 100),
        evaluation(VariantPolicy.LOWEST_PRACTICAL, 2, 80),
    ), UserConstraints(budget=1))
    assert "lowest-practical-cost" in result.rejected
    assert result.recommended == "zero-cost"
