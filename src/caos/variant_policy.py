"""Generate genuinely different resource-selection policies for CAOS plan variants."""

from dataclasses import dataclass
from enum import Enum

from .enrichment import EnrichedTask
from .matching import CapabilityMatcher, ResourceCandidate
from .ledger import UsageLedger
from .optimizer import Assignment, OptimizationResult, GlobalOptimizer


class VariantPolicy(str, Enum):
    ZERO_COST = "zero-cost"
    LOWEST_PRACTICAL = "lowest-practical-cost"
    FASTEST_PRACTICAL = "fastest-practical"


@dataclass(frozen=True)
class PolicyConfig:
    paid_cost_weight: float = 1.0
    quality_weight: float = 0.0
    reliability_weight: float = 0.0
    speed_weight: float = 0.0


class VariantPolicyGenerator:
    """Run the same task set through intentionally different optimization policies."""

    def __init__(self, matcher: CapabilityMatcher) -> None:
        self.matcher = matcher

    def optimize(self, policy: VariantPolicy, tasks: tuple[EnrichedTask, ...], ledger: UsageLedger) -> OptimizationResult:
        configs = {
            VariantPolicy.ZERO_COST: PolicyConfig(paid_cost_weight=1000.0, speed_weight=0.0),
            VariantPolicy.LOWEST_PRACTICAL: PolicyConfig(paid_cost_weight=1.0, quality_weight=0.25, reliability_weight=0.25),
            VariantPolicy.FASTEST_PRACTICAL: PolicyConfig(paid_cost_weight=0.15, quality_weight=0.35, reliability_weight=0.50, speed_weight=1.0),
        }
        config = configs[policy]
        assignments: list[Assignment] = []
        missing: list[str] = []
        local = UsageLedger(tuple(ledger.snapshots))
        for task in sorted(tasks, key=lambda x: (len(self.matcher.match(x)), x.task_id)):
            candidates = self.matcher.match(task)
            if not candidates:
                missing.append(task.task_id)
                continue
            units = GlobalOptimizer.units(task)
            selected = min(candidates, key=lambda c: self._score(c, local, units, config))
            resource = selected.resource
            free = min(units, local.remaining(resource.resource_id))
            paid = units - free
            if free:
                local.reserve(resource.resource_id, free)
            assignments.append(Assignment(task.task_id, resource.resource_id, free, paid, paid * resource.unit_cost, True, f"Selected by {policy.value} policy."))
        total = sum(a.cost for a in assignments)
        return OptimizationResult(tuple(assignments), total, bool(assignments) and not missing and all(a.paid_units == 0 for a in assignments), tuple(missing))

    @staticmethod
    def _score(candidate: ResourceCandidate, ledger: UsageLedger, units: float, config: PolicyConfig) -> tuple:
        r = candidate.resource
        remaining = ledger.remaining(r.resource_id)
        free = min(units, remaining)
        paid = units - free
        # Lower tuple values are preferred. Quality/reliability are rewards.
        return (
            paid * r.unit_cost * config.paid_cost_weight
            - r.quality * config.quality_weight
            - r.reliability * config.reliability_weight,
            r.effective_unit_cost,
            -r.quality,
            -r.reliability,
        )
