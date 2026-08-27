"""Match enriched project tasks to eligible resources with evidence awareness."""

from dataclasses import dataclass

from .enrichment import EnrichedTask
from .evidence import EvidenceRegistry
from .resources import Resource, ResourceRegistry


@dataclass(frozen=True)
class ResourceCandidate:
    task_id: str
    resource: Resource
    evidence_count: int
    freshest_evidence_age_days: int | None
    evidence_confidence: float


class CapabilityMatcher:
    def __init__(self, resources: ResourceRegistry, evidence: EvidenceRegistry) -> None:
        self.resources = resources
        self.evidence = evidence

    def match(self, task: EnrichedTask, minimum_quality: float = 0.0) -> list[ResourceCandidate]:
        candidates: dict[str, Resource] = {}
        for capability in task.capabilities:
            for resource in self.resources.match(capability, minimum_quality):
                candidates[resource.resource_id] = resource

        result = []
        for resource in candidates.values():
            items = self.evidence.for_resource(resource.resource_id)
            freshest = self.evidence.freshest(resource.resource_id)
            confidence = max((item.confidence for item in items), default=0.0)
            result.append(ResourceCandidate(
                task.task_id,
                resource,
                len(items),
                freshest.age_days if freshest else None,
                confidence,
            ))
        return sorted(result, key=self._sort_key)

    @staticmethod
    def _sort_key(candidate: ResourceCandidate) -> tuple:
        resource = candidate.resource
        # Prefer free capacity first, then lower reliability-adjusted cost,
        # stronger quality/reliability, and fresher evidence.
        has_free = resource.free_units > 0
        freshness = candidate.freshest_evidence_age_days
        return (
            not has_free,
            resource.effective_unit_cost,
            -resource.quality,
            -resource.reliability,
            freshness if freshness is not None else 10**9,
        )
