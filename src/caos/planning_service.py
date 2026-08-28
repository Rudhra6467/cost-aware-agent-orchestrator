"""Application-facing planning service for CAOS."""

from dataclasses import dataclass, field
from typing import Any

from .constraints import Autonomy, UserConstraints
from .planning_contract import PlanningResponse


@dataclass(frozen=True)
class PlanningRequest:
    idea: str
    constraints: UserConstraints = field(default_factory=UserConstraints)


class PlanningService:
    """Stable application boundary; the concrete planner is injected."""

    def __init__(self, analyzer, planner):
        self.analyzer = analyzer
        self.planner = planner

    def create_plan(self, request: PlanningRequest) -> PlanningResponse:
        if not request.idea or not request.idea.strip():
            raise ValueError("Idea is required")
        return self.planner.plan(request)

    @staticmethod
    def request_from_dict(payload: dict[str, Any]) -> PlanningRequest:
        if not isinstance(payload, dict):
            raise ValueError("Request body must be an object")
        idea = payload.get("idea", "")
        if not isinstance(idea, str) or not idea.strip():
            raise ValueError("idea must be a non-empty string")
        raw = payload.get("constraints") or {}
        if not isinstance(raw, dict):
            raise ValueError("constraints must be an object")
        try:
            autonomy = Autonomy(str(raw.get("autonomy", Autonomy.CONTROLLED.value)))
            constraints = UserConstraints(
                budget=float(raw.get("budget", 0)),
                quality_threshold=float(raw.get("quality_threshold", 0.7)),
                max_build_days=None if raw.get("max_build_days") is None else float(raw["max_build_days"]),
                autonomy=autonomy,
                prefer_free=bool(raw.get("prefer_free", True)),
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid constraints: {exc}") from exc
        return PlanningRequest(idea.strip(), constraints)
