from caos.budget_gate import BudgetPolicy, evaluate_budget
from caos.execution_plan import ExecutionPlan, PlannedTask


def plan(cost):
    return ExecutionPlan((PlannedTask("t1", "r1", "provider", cost, 1.0, "source", "test"),), cost)


def test_approves_plan_within_budget():
    decision = evaluate_budget(plan(0.10), BudgetPolicy(0.50))
    assert decision.approved


def test_rejects_plan_above_budget():
    decision = evaluate_budget(plan(0.60), BudgetPolicy(0.50))
    assert not decision.approved


def test_zero_cost_policy_rejects_paid_plan():
    decision = evaluate_budget(plan(0.01), BudgetPolicy(0.50, zero_cost_only=True))
    assert not decision.approved


def test_zero_cost_policy_accepts_free_plan():
    decision = evaluate_budget(plan(0.0), BudgetPolicy(0.50, zero_cost_only=True))
    assert decision.approved
