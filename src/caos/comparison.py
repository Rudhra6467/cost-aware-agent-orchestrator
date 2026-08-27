"""Compare alternative CAOS build plans against user constraints."""

from dataclasses import dataclass

from .constraints import UserConstraints
from .optimizer import OptimizationResult


@dataclass(frozen=True)
class PlanVariant:
    variant_id: str
    name: str
    result: OptimizationResult
    estimated_days: float | None = None
    score: float = 0.0


@dataclass(frozen=True)
class PlanComparison:
    variants: tuple[PlanVariant, ...]
    recommended_id: str | None
    rationale: str


class PlanComparisonEngine:
    """Rank feasible alternatives without pretending scores prove global optimality."""

    def compare(self, variants: tuple[PlanVariant, ...], constraints: UserConstraints) -> PlanComparison:
        if not variants:
            return PlanComparison((), None, "No plans were supplied.")

        def rank(v: PlanVariant) -> tuple:
            over_budget = v.result.total_cost > constraints.budget
            over_time = constraints.max_build_days is not None and v.estimated_days is not None and v.estimated_days > constraints.max_build_days
            quality_penalty = 0.0 if v.result.unfulfilled_tasks == () else 1.0
            # Hard constraint violations dominate; within feasible options prefer lower cost,
            # then higher free coverage, then faster delivery.
            return (
                over_budget,
                over_time,
                quality_penalty,
                v.result.total_cost,
                -self._free_coverage(v.result),
                v.estimated_days if v.estimated_days is not None else float("inf"),
            )

        ranked = tuple(sorted(variants, key=rank))
        best = ranked[0]
        rationale = self._rationale(best, constraints)
        return PlanComparison(ranked, best.variant_id, rationale)

    @staticmethod
    def _free_coverage(result: OptimizationResult) -> float:
        total = sum(x.free_units + x.paid_units for x in result.assignments)
        return sum(x.free_units for x in result.assignments) / total if total else 1.0

    def _rationale(self, variant: PlanVariant, constraints: UserConstraints) -> str:
        coverage = self._free_coverage(variant.result) * 100
        parts = [f"{variant.name} is the best-ranked option under the supplied constraints."]
        parts.append(f"Estimated cost is ${variant.result.total_cost:.2f} with {coverage:.0f}% free-capacity coverage.")
        if constraints.max_build_days is not None and variant.estimated_days is not None:
            parts.append(f"Estimated build time is {variant.estimated_days:g} days versus a {constraints.max_build_days:g}-day limit.")
        if variant.result.unfulfilled_tasks:
            parts.append("It still has unfulfilled tasks and therefore requires remediation before execution.")
        return " ".join(parts)
