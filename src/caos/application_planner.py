"""Application-level planning composition for the CAOS vertical slice."""

from dataclasses import dataclass

from .decision import VariantDecisionEngine
from .planning_contract import PlanningResponse, build_planning_response
from .planning_service import PlanningRequest


@dataclass(frozen=True)
class Blueprint:
    summary: str
    tasks: tuple
    assumptions: tuple[str, ...] = ()


class ApplicationPlanner:
    """Compose blueprint analysis, variant evaluation, and decision into one response."""

    def __init__(self, analyzer, variant_engine, ledger, quota_windows=None):
        self.analyzer = analyzer
        self.variant_engine = variant_engine
        self.ledger = ledger
        self.quota_windows = quota_windows or {}
        self.decision_engine = VariantDecisionEngine()

    def plan(self, request: PlanningRequest) -> PlanningResponse:
        blueprint = self.analyzer.analyze(request.idea)
        evaluations = tuple(
            self.variant_engine.evaluate(policy, blueprint.tasks, self.ledger, self.quota_windows)
            for policy in self.variant_engine.policy_generator.policies
        )
        decision = self.decision_engine.decide(evaluations, request.constraints)
        return build_planning_response(
            request.idea,
            blueprint.summary,
            evaluations,
            decision,
            request.constraints,
            blueprint.assumptions,
        )
