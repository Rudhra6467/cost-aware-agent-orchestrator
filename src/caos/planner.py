"""Transparent Zero-Cost and Lowest-Practical-Cost plan generation."""

from dataclasses import dataclass

from .enrichment import EnrichedTask
from .matching import CapabilityMatcher, ResourceCandidate
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
    """Greedy V1 planner; deliberately transparent and deterministic."""

    def __init__(self, matcher: CapabilityMatcher) -> None:
        self.matcher = matcher

    def generate(self, graph: TaskGraph, enriched: tuple[EnrichedTask, ...]) -> tuple[BuildPlan, BuildPlan]:
        graph.validate()
        enriched_by_id = {x.task_id: x for x in enriched}
        if set(enriched_by_id) != {x.task_id for x in graph.tasks}:
            raise ValueError("Enrichment must cover the complete DAG")

        zero_lines: list[PlanLine] = []
        hybrid_lines: list[PlanLine] = []
        free_tasks = 0
        for task in enriched:
            candidates = self.matcher.match(task)
            if not candidates:
                raise ValueError(f"No eligible resource for task {task.task_id}")
            free = next((c for c in candidates if c.resource.free_units >= self._units(task)), None)
            cheapest = min(candidates, key=lambda c: c.resource.effective_unit_cost)
            selected_free = free or cheapest
            zero_lines.append(self._line(task, selected_free, prefer_free=True))
            if free:
                free_tasks += 1
            hybrid_lines.append(self._line(task, cheapest, prefer_free=False))

        total_tasks = len(enriched)
        zero = BuildPlan("zero-cost", "Zero-Cost First", tuple(zero_lines), sum(x.estimated_cost for x in zero_lines), free_tasks / total_tasks if total_tasks else 1.0, ("Free capacity is treated as $0 only while the recorded quota is sufficient.", "V1 uses a greedy per-task choice; it is not a global optimum solver."))
        hybrid = BuildPlan("lowest-practical", "Lowest Practical Cost", tuple(hybrid_lines), sum(x.estimated_cost for x in hybrid_lines), sum(1 for x in hybrid_lines if x.estimated_cost == 0) / total_tasks if total_tasks else 1.0, ("Paid resources are considered only from the registered candidates.", "V1 does not yet model shared quota across tasks or parallel execution."))
        return zero, hybrid

    @staticmethod
    def _units(task: EnrichedTask) -> float:
        return max(1.0, task.estimated_tokens / 1000.0)

    @classmethod
    def _line(cls, task: EnrichedTask, candidate: ResourceCandidate, prefer_free: bool) -> PlanLine:
        units = cls._units(task)
        resource = candidate.resource
        free = min(units, resource.free_units)
        paid_units = max(0.0, units - free)
        cost = paid_units * resource.unit_cost
        if prefer_free and free >= units:
            cost = 0.0
            reason = "Uses sufficient recorded free capacity."
        elif prefer_free:
            reason = "Free capacity is insufficient; remaining usage is priced at the registered unit cost."
        else:
            reason = "Selected by lowest reliability-adjusted unit cost among eligible candidates."
        return PlanLine(task.task_id, resource.resource_id, resource.provider, units, resource.free_units, cost, reason)
