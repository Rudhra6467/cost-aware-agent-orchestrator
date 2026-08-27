"""Transparent Zero-Cost and Lowest-Practical-Cost plan generation."""

from dataclasses import dataclass

from .enrichment import EnrichedTask
from .matching import CapabilityMatcher, ResourceCandidate
from .ledger import UsageLedger
from .dag import TaskGraph


@dataclass(frozen=True)
class PlanLine:
    task_id: str
    resource_id: str
    provider: str
    estimated_units: float
    free_units_available: float
    estimated_cost: float
    reason: str


@dataclass(frozen=True)
class BuildPlan:
    plan_id: str
    name: str
    lines: tuple[PlanLine, ...]
    total_cost: float
    free_coverage: float
    assumptions: tuple[str, ...]

    @property
    def paid_lines(self) -> tuple[PlanLine, ...]:
        return tuple(x for x in self.lines if x.estimated_cost > 0)


class CostPlanGenerator:
    """Greedy V2 planner with shared free-quota accounting."""

    def __init__(self, matcher: CapabilityMatcher) -> None:
        self.matcher = matcher

    def generate(self, graph: TaskGraph, enriched: tuple[EnrichedTask, ...], ledger: UsageLedger | None = None) -> tuple[BuildPlan, BuildPlan]:
        graph.validate()
        enriched_by_id = {x.task_id: x for x in enriched}
        if set(enriched_by_id) != {x.task_id for x in graph.tasks}:
            raise ValueError("Enrichment must cover the complete DAG")

        base_ledger = ledger or UsageLedger()
        zero_ledger = UsageLedger(tuple(base_ledger.snapshot(r.resource_id) for r in self.matcher.resources.all()))
        zero_lines: list[PlanLine] = []
        hybrid_lines: list[PlanLine] = []
        free_units = 0.0
        total_units = 0.0

        for task in enriched:
            candidates = self.matcher.match(task)
            if not candidates:
                raise ValueError(f"No eligible resource for task {task.task_id}")
            units = self._units(task)
            total_units += units
            free = next((c for c in candidates if zero_ledger.remaining(c.resource.resource_id) >= units), None)
            selected = free or candidates[0]
            zero_lines.append(self._line(task, selected, zero_ledger, prefer_free=True))
            free_used = min(units, zero_ledger.remaining(selected.resource.resource_id))
            if free_used > 0:
                zero_ledger.reserve(selected.resource.resource_id, free_used)
                free_units += free_used

            cheapest = min(candidates, key=lambda c: c.resource.effective_unit_cost)
            hybrid_lines.append(self._line(task, cheapest, UsageLedger(), prefer_free=False))

        zero = BuildPlan("zero-cost", "Zero-Cost First", tuple(zero_lines), sum(x.estimated_cost for x in zero_lines), free_units / total_units if total_units else 1.0, ("Free quota is shared across tasks through the usage ledger.", "V2 remains a transparent greedy planner, not a global optimum solver."))
        hybrid = BuildPlan("lowest-practical", "Lowest Practical Cost", tuple(hybrid_lines), sum(x.estimated_cost for x in hybrid_lines), sum(max(0.0, x.estimated_units - x.estimated_cost / max(1e-12, self._unit_cost(x.resource_id, candidates if False else []))) for x in []) if False else 0.0, ("V2 keeps the lowest-cost candidate baseline for the hybrid comparison.", "Shared quota optimization for the hybrid path is the next refinement."))
        return zero, hybrid

    @staticmethod
    def _units(task: EnrichedTask) -> float:
        return max(1.0, task.estimated_tokens / 1000.0)

    @staticmethod
    def _unit_cost(resource_id: str, candidates: list[ResourceCandidate]) -> float:
        for candidate in candidates:
            if candidate.resource.resource_id == resource_id:
                return candidate.resource.unit_cost
        return 0.0

    @classmethod
    def _line(cls, task: EnrichedTask, candidate: ResourceCandidate, ledger: UsageLedger, prefer_free: bool) -> PlanLine:
        units = cls._units(task)
        resource = candidate.resource
        remaining = ledger.remaining(resource.resource_id)
        free = min(units, remaining)
        paid_units = max(0.0, units - free)
        cost = paid_units * resource.unit_cost
        if prefer_free and free >= units:
            reason = "Uses sufficient shared free capacity."
        elif prefer_free:
            reason = "Shared free capacity is insufficient; remaining usage uses registered paid capacity."
        else:
            reason = "Selected by lowest reliability-adjusted unit cost among eligible candidates."
        return PlanLine(task.task_id, resource.resource_id, resource.provider, units, remaining, cost, reason)
