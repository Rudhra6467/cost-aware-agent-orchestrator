"""Human-readable explanations of CAOS planning trade-offs."""

from dataclasses import dataclass

from .constraints import UserConstraints
from .optimizer import OptimizationResult


@dataclass(frozen=True)
class PlanExplanation:
    headline: str
    summary: str
    recommendation: str
    tradeoffs: tuple[str, ...]
    warnings: tuple[str, ...]


class PlanExplainer:
    def explain(self, result: OptimizationResult, constraints: UserConstraints) -> PlanExplanation:
        warnings = []
        if result.unfulfilled_tasks:
            warnings.append(f"No eligible resource was found for: {', '.join(result.unfulfilled_tasks)}.")
        if result.total_cost > constraints.budget:
            warnings.append(f"Estimated cost ${result.total_cost:.2f} exceeds the user's ${constraints.budget:.2f} budget.")

        if result.fully_free:
            headline = "Your current plan fits within available free capacity."
        elif result.total_cost <= constraints.budget:
            headline = f"This plan is feasible at an estimated ${result.total_cost:.2f}."
        else:
            headline = f"The current plan needs about ${result.total_cost:.2f}, above the stated budget."

        paid = sum(x.paid_units for x in result.assignments)
        free = sum(x.free_units for x in result.assignments)
        total = free + paid
        coverage = (free / total * 100) if total else 100.0
        tradeoffs = (
            f"Estimated free-capacity coverage is {coverage:.0f}%.",
            f"Estimated paid usage is {paid:.1f} units.",
            "The estimate is based on registered resource data and current shared quota state.",
        )

        if result.unfulfilled_tasks:
            recommendation = "Resolve the unfulfilled capabilities before autonomous execution."
        elif result.total_cost <= constraints.budget:
            recommendation = "Proceed if the quality and evidence assumptions meet the user's acceptance criteria."
        else:
            recommendation = "Search for additional free capacity, relax non-essential requirements, or increase the budget."

        return PlanExplanation(headline, "CAOS selected resources across the project while respecting shared quota accounting.", recommendation, tradeoffs, tuple(warnings))
