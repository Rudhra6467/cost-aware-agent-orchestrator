"""Transparent decision engine for selecting a CAOS plan."""

from dataclasses import dataclass
from enum import Enum

from .constraints import UserConstraints
from .variant_simulation import VariantEvaluation


class DecisionReason(str, Enum):
    BUDGET = "budget"
    TIME = "time"
    FREE_USAGE = "free_usage"
    RELIABILITY = "reliability"
    PRACTICAL_COST = "practical_cost"


@dataclass(frozen=True)
class Decision:
    recommended: str
    reasons: tuple[DecisionReason, ...]
    explanation: str
    feasible: tuple[str, ...]
    rejected: tuple[str, ...]


class VariantDecisionEngine:
    """Choose a plan using explicit constraints and measurable evaluation fields."""

    def decide(self, evaluations: tuple[VariantEvaluation, ...], constraints: UserConstraints) -> Decision:
        if not evaluations:
            raise ValueError("At least one evaluation is required")
        feasible = []
        rejected = []
        for e in evaluations:
            cost = e.execution.monetary_cost
            days = (e.simulation.elapsed_minutes + e.total_wait_minutes) / 1440
            if constraints.budget is not None and cost > constraints.budget:
                rejected.append(e.policy.value)
            elif constraints.max_days is not None and days > constraints.max_days:
                rejected.append(e.policy.value)
            else:
                feasible.append(e)
        pool = feasible or list(evaluations)
        winner = min(pool, key=lambda e: (e.execution.monetary_cost, e.total_wait_minutes, e.simulation.elapsed_minutes))
        reasons = [DecisionReason.PRACTICAL_COST]
        if winner.execution.monetary_cost == 0:
            reasons.append(DecisionReason.FREE_USAGE)
        if constraints.max_days is not None:
            reasons.append(DecisionReason.TIME)
        if constraints.budget is not None:
            reasons.append(DecisionReason.BUDGET)
        explanation = self._explain(winner, reasons, bool(feasible))
        return Decision(winner.policy.value, tuple(reasons), explanation, tuple(e.policy.value for e in feasible), tuple(rejected))

    @staticmethod
    def _explain(winner, reasons, all_feasible: bool) -> str:
        prefix = "Recommended because it is the lowest practical-cost feasible option" if all_feasible else "No option satisfies every constraint; this is the lowest practical-cost fallback"
        return f"{prefix}. Estimated cost: ${winner.execution.monetary_cost:.2f}; execution: {winner.simulation.elapsed_minutes:.0f} minutes; quota waiting: {winner.total_wait_minutes:.0f} minutes."
