"""Application-facing planning service for CAOS."""

from dataclasses import dataclass
from typing import Any

from .constraints import Autonomy, UserConstraints
from .planning_contract import PlanningResponse


@dataclass(frozen=True)
class PlanningRequest:
    idea: str
    constraints: UserConstraints = UserConstraints()


class PlanningService:
    """Stable application boundary; domain engines can evolve behind it."""

    def __init__(self, analyzer, planner):
        self.analyzer = analyzer
        self.planner = planner

    def create_plan(self, request: PlanningRequest) -> PlanningResponse:
        if not request.idea or not request.idea.strip():
            raise ValueError("Idea is required")
        blueprint = self.analyzer.analyze(request.idea)
        return self.planner.plan(blueprint, request.constraints)

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
            budget = float(raw.get("budget", 0))
            quality = float(raw.get("quality_threshold", 0.7))
            max_days = raw.get("max_build_days")
            max_days = None if max_days is None else float(max_days)
            prefer_free = bool(raw.get("prefer_free", True))
            constraints = UserConstraints(
                budget=budget,
                quality_threshold=quality,
                max_build_days=max_days,
                autonomy=autonomy,
                prefer_free=prefer_free,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid constraints: {exc}") from exc
        return PlanningRequest(idea.strip(), constraints)
