from caos.budget_gate import BudgetPolicy
from caos.execution_plan import ExecutionPlan, PlannedTask
from caos.replanner import replan_for_budget


def task(task_id, cost):
    return PlannedTask(task_id, "resource", "provider", cost, 1.0, "source", "test")


def test_replanner_selects_verified_free_subset_when_budget_is_exceeded():
    result = replan_for_budget(
        ExecutionPlan((task("free", 0.0), task("paid", 0.20)), 0.20),
        BudgetPolicy(0.05),
    )
    assert result.changed
    assert result.plan.estimated_total_cost == 0.0
    assert [x.task_id for x in result.plan.tasks] == ["free"]


def test_replanner_does_not_claim_a_solution_when_none_is_verified():
    result = replan_for_budget(
        ExecutionPlan((task("paid", 0.20),), 0.20),
        BudgetPolicy(0.05),
    )
    assert not result.changed
    assert result.plan.estimated_total_cost == 0.20


def test_replanner_respects_zero_cost_only():
    result = replan_for_budget(
        ExecutionPlan((task("free", 0.0), task("paid", 0.20)), 0.20),
        BudgetPolicy(1.00, zero_cost_only=True),
    )
    assert result.changed
    assert result.plan.estimated_total_cost == 0.0
