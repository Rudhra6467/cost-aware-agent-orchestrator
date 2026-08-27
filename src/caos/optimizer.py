"""Whole-DAG feasibility and cost optimization baseline."""

from dataclasses import dataclass

from .enrichment import EnrichedTask
from .matching import CapabilityMatcher, ResourceCandidate
from .ledger import UsageLedger


@dataclass(frozen=True)
class Assignment:
    task_id: str
    resource_id: str
    free_units: float
    paid_units: float
    cost: float
    feasible: bool
    reason: str


@dataclass(frozen=True)
class OptimizationResult:
    assignments: tuple[Assignment, ...]
    total_cost: float
    fully_free: bool
    unfulfilled_tasks: tuple[str, ...]


class GlobalOptimizer:
    """Deterministic baseline that allocates shared free quota across a task set."""

    def __init__(self, matcher: CapabilityMatcher) -> None:
        self.matcher = matcher

    @staticmethod
    def units(task: EnrichedTask) -> float:
        return max(1.0, task.estimated_tokens / 1000.0)

    def optimize(self, tasks: tuple[EnrichedTask, ...], ledger: UsageLedger) -> OptimizationResult:
        assignments: list[Assignment] = []
        unfulfilled: list[str] = []
        # Most constrained tasks first: fewer eligible resources means fewer alternatives.
        ordered = sorted(tasks, key=lambda task: (len(self.matcher.match(task)), task.task_id))
        for task in ordered:
            candidates = self.matcher.match(task)
            if not candidates:
                unfulfilled.append(task.task_id)
                continue
            units = self.units(task)
            selected = self._select(candidates, ledger, units)
            resource = selected.resource
            free = min(units, ledger.remaining(resource.resource_id))
            paid = units - free
            cost = paid * resource.unit_cost
            if free:
                ledger.reserve(resource.resource_id, free)
            assignments.append(Assignment(task.task_id, resource.resource_id, free, paid, cost, True, self._reason(resource, free, paid)))
        total = sum(x.cost for x in assignments)
        return OptimizationResult(tuple(assignments), total, bool(assignments) and all(x.paid_units == 0 for x in assignments) and not unfulfilled, tuple(unfulfilled))

    @staticmethod
    def _select(candidates: list[ResourceCandidate], ledger: UsageLedger, units: float) -> ResourceCandidate:
        def score(candidate: ResourceCandidate) -> tuple:
            remaining = ledger.remaining(candidate.resource.resource_id)
            free_possible = min(units, remaining)
            paid = units - free_possible
            cost = paid * candidate.resource.unit_cost
            return (cost, candidate.resource.effective_unit_cost, -candidate.resource.quality, -candidate.resource.reliability)
        return min(candidates, key=score)

    @staticmethod
    def _reason(resource, free: float, paid: float) -> str:
        if paid == 0:
            return "All estimated usage fits within currently available shared free quota."
        if free > 0:
            return "Shared free quota is partially available; only the spillover is paid."
        return "Shared free quota is exhausted or unavailable; paid capacity is required."
