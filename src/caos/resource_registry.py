"""Small evidence-backed resource registry for CAOS V1.

The first version is intentionally in-memory and provider-neutral. A later
migration will persist these records in SQLite and add evidence refresh.
"""

from dataclasses import dataclass
from datetime import date


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


class ResourceRegistry:
    """Registry with explicit evidence and freshness metadata."""

    def __init__(self, resources: list[ResourceRecord] | None = None) -> None:
        self._resources = {resource.resource_id: resource for resource in resources or []}

    def add(self, resource: ResourceRecord) -> None:
        self._resources[resource.resource_id] = resource

    def all(self) -> list[ResourceRecord]:
        return list(self._resources.values())

    def by_capability(self, capability: str) -> list[ResourceRecord]:
        return [
            resource
            for resource in self._resources.values()
            if capability in resource.capabilities
        ]

    def get(self, resource_id: str) -> ResourceRecord | None:
        return self._resources.get(resource_id)
