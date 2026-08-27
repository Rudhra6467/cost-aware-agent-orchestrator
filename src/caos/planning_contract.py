"""Stable end-user planning contract for CAOS."""

from dataclasses import asdict, dataclass
from typing import Any

from .constraints import Autonomy, UserConstraints
from .decision import Decision
from .variant_simulation import VariantEvaluation


@dataclass(frozen=True)
class PlanSummary:
    plan_id: str
    label: str
    monetary_cost: float
    execution_minutes: float
    quota_wait_minutes: float
    critical_path: tuple[str, ...]


@dataclass(frozen=True)
class PlanningResponse:
    idea: str
    blueprint_summary: str
    assumptions: tuple[str, ...]
    plans: tuple[PlanSummary, ...]
    recommendation: str
    reasons: tuple[str, ...]
    explanation: str
    next_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_planning_response(
    idea: str,
    blueprint_summary: str,
    evaluations: tuple[VariantEvaluation, ...],
    decision: Decision,
    constraints: UserConstraints,
    assumptions: tuple[str, ...] = (),
) -> PlanningResponse:
    plans = tuple(
        PlanSummary(
            e.policy.value,
            _label(e.policy.value),
            e.execution.monetary_cost,
            e.simulation.elapsed_minutes,
            e.total_wait_minutes,
            e.simulation.critical_path,
        )
        for e in evaluations
    )
    actions = ("BUILD",) if constraints.autonomy == Autonomy.AUTONOMOUS else ("BUILD", "DIY")
    return PlanningResponse(
        idea=idea,
        blueprint_summary=blueprint_summary,
        assumptions=assumptions,
        plans=plans,
        recommendation=decision.recommended,
        reasons=tuple(r.value for r in decision.reasons),
        explanation=decision.explanation,
        next_actions=actions,
    )


def _label(plan_id: str) -> str:
    return {
        "zero-cost": "Zero-Cost",
        "lowest-practical-cost": "Lowest-Practical-Cost",
        "fastest-practical": "Fastest-Practical",
    }.get(plan_id, plan_id.replace("-", " ").title())
