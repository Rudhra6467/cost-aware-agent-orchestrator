"""Application-facing planning service for CAOS."""

from dataclasses import dataclass
from typing import Any

from .constraints import UserConstraints
from .decision import Decision
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
        result = self.planner.plan(blueprint, request.constraints)
        return result

    @staticmethod
    def request_from_dict(payload: dict[str, Any]) -> PlanningRequest:
        idea = str(payload.get("idea", "")).strip()
        raw = payload.get("constraints") or {}
        constraints = UserConstraints(
            budget=float(raw.get("budget", 0)),
            quality_threshold=float(raw.get("quality_threshold", 0.7)),
            max_build_days=raw.get("max_build_days"),
        )
        return PlanningRequest(idea, constraints)
