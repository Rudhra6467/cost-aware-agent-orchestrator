"""Generate cheaper execution-plan candidates under explicit constraints."""

from dataclasses import dataclass

from .budget_gate import BudgetPolicy
from .execution_plan import ExecutionPlan


@dataclass(frozen=True)
class ReplanResult:
    plan: ExecutionPlan
    changed: bool
    rationale: str


def replan_for_budget(plan: ExecutionPlan, policy: BudgetPolicy) -> ReplanResult:
    """Reduce cost only when a verified zero-cost alternative is represented."""
    if plan.estimated_total_cost <= policy.max_estimated_cost and not (policy.zero_cost_only and plan.estimated_total_cost > 0):
        return ReplanResult(plan, False, "Existing plan already satisfies the budget policy.")

    free_tasks = tuple(item for item in plan.tasks if item.estimated_cost == 0)
    if not free_tasks:
        return ReplanResult(plan, False, "No verified cheaper plan is currently represented in the execution plan.")

    free_cost = sum(item.estimated_cost for item in free_tasks)
    if policy.zero_cost_only and free_cost == 0:
        return ReplanResult(ExecutionPlan(free_tasks, free_cost), True, "Removed paid tasks to satisfy zero-cost-only policy; paid work must be replanned with verified alternatives.")

    if free_cost <= policy.max_estimated_cost:
        return ReplanResult(ExecutionPlan(free_tasks, free_cost), True, "Selected the already-planned zero-cost subset because it satisfies the configured budget.")

    return ReplanResult(plan, False, "No verified cheaper plan is currently represented in the execution plan.")
