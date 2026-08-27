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
        hybrid_ledger = UsageLedger(tuple(base_ledger.snapshot(r.resource_id) for r in self.matcher.resources.all()))
        zero_lines: list[PlanLine] = []
        hybrid_lines: list[PlanLine] = []
        zero_free = hybrid_free = total_units = 0.0

        for task in enriched:
            candidates = self.matcher.match(task)
            if not candidates:
                raise ValueError(f"No eligible resource for task {task.task_id}")
            units = self._units(task)
            total_units += units

            free = next((c for c in candidates if zero_ledger.remaining(c.resource.resource_id) >= units), None)
            selected_zero = free or candidates[0]
            zero_lines.append(self._allocate_line(task, selected_zero, zero_ledger, "Zero-Cost First"))
            zero_free += self._reserve_free(zero_ledger, selected_zero, units)

            # For the hybrid plan, evaluate each candidate using the shared
            # quota currently remaining for that provider/resource.
            selected_hybrid = min(candidates, key=lambda c: self._marginal_cost(c, units, hybrid_ledger))
            hybrid_lines.append(self._allocate_line(task, selected_hybrid, hybrid_ledger, "Lowest Practical Cost"))
            hybrid_free += self._reserve_free(hybrid_ledger, selected_hybrid, units)

        zero = BuildPlan(
            "zero-cost", "Zero-Cost First", tuple(zero_lines),
            sum(x.estimated_cost for x in zero_lines), zero_free / total_units if total_units else 1.0,
            ("Free quota is shared across tasks through the usage ledger.", "V2 is a transparent greedy planner, not a global optimum solver."),
        )
        hybrid = BuildPlan(
            "lowest-practical", "Lowest Practical Cost", tuple(hybrid_lines),
            sum(x.estimated_cost for x in hybrid_lines), hybrid_free / total_units if total_units else 1.0,
            ("Free quota is shared across tasks through the usage ledger.", "V2 chooses the lowest marginal task cost from eligible candidates."),
        )
        return zero, hybrid

    @staticmethod
    def _units(task: EnrichedTask) -> float:
        return max(1.0, task.estimated_tokens / 1000.0)

    @staticmethod
    def _marginal_cost(candidate: ResourceCandidate, units: float, ledger: UsageLedger) -> float:
        free = min(units, ledger.remaining(candidate.resource.resource_id))
        return max(0.0, units - free) * candidate.resource.unit_cost

    @classmethod
    def _allocate_line(cls, task: EnrichedTask, candidate: ResourceCandidate, ledger: UsageLedger, plan_name: str) -> PlanLine:
        units = cls._units(task)
        resource = candidate.resource
        remaining = ledger.remaining(resource.resource_id)
        free = min(units, remaining)
        paid_units = max(0.0, units - free)
        cost = paid_units * resource.unit_cost
        if free >= units:
            reason = f"{plan_name}: uses sufficient shared free capacity."
        elif free > 0:
            reason = f"{plan_name}: consumes remaining shared free capacity and pays for the spillover."
        else:
            reason = f"{plan_name}: no free capacity remains; uses registered paid capacity."
        return PlanLine(task.task_id, resource.resource_id, resource.provider, units, remaining, cost, reason)

    @staticmethod
    def _reserve_free(ledger: UsageLedger, candidate: ResourceCandidate, units: float) -> float:
        free = min(units, ledger.remaining(candidate.resource.resource_id))
        if free > 0:
            ledger.reserve(candidate.resource.resource_id, free)
        return free
