from caos.comparison import PlanComparisonEngine, PlanVariant
from caos.constraints import UserConstraints
from caos.optimizer import Assignment, OptimizationResult


def result(cost, paid=0):
    return OptimizationResult((Assignment("t", "r", 1-paid, paid, cost, True, "test"),), cost, paid == 0, ())


def test_comparison_prefers_feasible_plan_over_cheaper_over_budget_plan():
    variants = (
        PlanVariant("free", "Zero-Cost", result(2.0, 1), estimated_days=2),
        PlanVariant("hybrid", "Hybrid", result(1.0), estimated_days=3),
    )
    comparison = PlanComparisonEngine().compare(variants, UserConstraints(budget=1.5))
    assert comparison.recommended_id == "hybrid"


def test_comparison_returns_no_plan_when_empty():
    comparison = PlanComparisonEngine().compare((), UserConstraints())
    assert comparison.recommended_id is None
