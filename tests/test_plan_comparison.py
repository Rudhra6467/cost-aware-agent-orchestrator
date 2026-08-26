import pytest

from caos.plan_comparison import PlanOption, cheapest_feasible, rank_plans


def test_rank_plans_prefers_lower_cost_then_lower_risk():
    options = [
        PlanOption("hybrid", 0.05, 0, 0.1, 0.99),
        PlanOption("free", 0.0, 300, 0.4, 0.90),
        PlanOption("free-risky", 0.0, 0, 0.8, 0.70),
    ]
    ranked = rank_plans(options)
    assert [o.plan_id for o in ranked] == ["free", "free-risky", "hybrid"]


def test_cheapest_feasible_respects_budget():
    options = [
        PlanOption("free", 0.0, 0, 0.5, 0.9),
        PlanOption("hybrid", 0.05, 0, 0.1, 0.99),
    ]
    assert cheapest_feasible(options, 0.01).plan_id == "free"
    assert cheapest_feasible(options, -0.01) is None
