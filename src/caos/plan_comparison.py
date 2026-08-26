"""Compare complete execution plans rather than isolated resources."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanOption:
    plan_id: str
    estimated_cost: float
    estimated_wait_seconds: float
    risk_score: float
    verified_success_probability: float
    description: str = ""

    def __post_init__(self) -> None:
        if self.estimated_cost < 0 or self.estimated_wait_seconds < 0:
            raise ValueError("cost and wait cannot be negative")
        if not 0 <= self.risk_score <= 1:
            raise ValueError("risk_score must be between 0 and 1")
        if not 0 <= self.verified_success_probability <= 1:
            raise ValueError("success probability must be between 0 and 1")


def rank_plans(options: list[PlanOption]) -> list[PlanOption]:
    """Rank feasible alternatives by cost, then risk and success probability."""
    return sorted(
        options,
        key=lambda option: (
            option.estimated_cost,
            option.risk_score,
            -option.verified_success_probability,
            option.estimated_wait_seconds,
        ),
    )


def cheapest_feasible(options: list[PlanOption], budget: float | None = None) -> PlanOption | None:
    eligible = [o for o in options if budget is None or o.estimated_cost <= budget]
    return rank_plans(eligible)[0] if eligible else None
