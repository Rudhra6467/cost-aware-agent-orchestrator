"""User-controlled budget and execution approval gate."""

from dataclasses import dataclass

from .execution_plan import ExecutionPlan


@dataclass(frozen=True)
class BudgetPolicy:
    max_estimated_cost: float
    zero_cost_only: bool = False

    def __post_init__(self) -> None:
        if self.max_estimated_cost < 0:
            raise ValueError("max_estimated_cost cannot be negative")


@dataclass(frozen=True)
class BudgetDecision:
    approved: bool
    reason: str
    estimated_cost: float


def evaluate_budget(plan: ExecutionPlan, policy: BudgetPolicy) -> BudgetDecision:
    cost = plan.estimated_total_cost
    if policy.zero_cost_only and cost > 0:
        return BudgetDecision(False, "Plan contains paid execution under a zero-cost-only policy.", cost)
    if cost > policy.max_estimated_cost:
        return BudgetDecision(False, "Estimated cost exceeds the user's maximum budget.", cost)
    return BudgetDecision(True, "Plan is within the user's configured budget policy.", cost)
