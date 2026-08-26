"""Evidence-backed resource registry for CAOS V1."""

from dataclasses import dataclass
from datetime import date, datetime, timezone


@dataclass(frozen=True)
class ResourceRecord:
    resource_id: str
    provider: str
    name: str
    category: str
    capabilities: tuple[str, ...]
    quality_score: float
    reliability_score: float
    context_capacity: int
    input_cost_per_1k: float
    output_cost_per_1k: float
    free_tier_notes: str
    availability_status: str
    evidence_url: str
    last_verified_at: date
    confidence: float

    def is_stale(self, max_age_days: int = 30, today: date | None = None) -> bool:
        if max_age_days < 0:
            raise ValueError("max_age_days cannot be negative")
        reference = today or datetime.now(timezone.utc).date()
        return (reference - self.last_verified_at).days > max_age_days

    def validate(self) -> None:
        if not 0 <= self.quality_score <= 1:
            raise ValueError("quality_score must be between 0 and 1")
        if not 0 <= self.reliability_score <= 1:
            raise ValueError("reliability_score must be between 0 and 1")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if self.context_capacity < 0:
            raise ValueError("context_capacity cannot be negative")
        if self.input_cost_per_1k < 0 or self.output_cost_per_1k < 0:
            raise ValueError("resource costs cannot be negative")
        if not self.evidence_url:
            raise ValueError("evidence_url is required")


class ResourceRegistry:
    """Registry with explicit evidence and freshness metadata."""

    def __init__(self, resources: list[ResourceRecord] | None = None) -> None:
        self._resources = {}
        for resource in resources or []:
            self.add(resource)

    def add(self, resource: ResourceRecord) -> None:
        resource.validate()
        self._resources[resource.resource_id] = resource

    def all(self) -> list[ResourceRecord]:
        return list(self._resources.values())

    def by_capability(self, capability: str, include_stale: bool = True) -> list[ResourceRecord]:
        return [
            resource
            for resource in self._resources.values()
            if capability in resource.capabilities
            and (include_stale or not resource.is_stale())
        ]

    def verified(self, max_age_days: int = 30) -> list[ResourceRecord]:
        return [r for r in self._resources.values() if not r.is_stale(max_age_days)]

    def get(self, resource_id: str) -> ResourceRecord | None:
        return self._resources.get(resource_id)
