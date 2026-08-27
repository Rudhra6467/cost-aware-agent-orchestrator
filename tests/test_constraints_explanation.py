from caos.constraints import Autonomy, UserConstraints
from caos.explanation import PlanExplainer
from caos.optimizer import Assignment, OptimizationResult


def test_constraints_validate_budget_and_quality():
    assert UserConstraints(5, 0.9, 3, Autonomy.AUTONOMOUS).budget == 5


def test_explainer_flags_budget_overrun():
    result = OptimizationResult((Assignment("t", "r", 0, 2, 2.5, True, "paid"),), 2.5, False, ())
    explanation = PlanExplainer().explain(result, UserConstraints(budget=1))
    assert "exceeds" in explanation.warnings[0]
    assert explanation.recommendation
