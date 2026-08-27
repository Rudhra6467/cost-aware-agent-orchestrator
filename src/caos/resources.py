"""Provider/resource registry primitives used by the cost optimizer."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Resource:
    resource_id: str
    provider: str
    name: str
    capabilities: tuple[str, ...]
    unit: str
    unit_cost: float
    free_units: float = 0.0
    reliability: float = 1.0
    quality: float = 1.0
    freshness_days: int = 0
    enabled: bool = True

    @property
    def effective_unit_cost(self) -> float:
        """Expected cost per unit after reliability adjustment."""
        if self.reliability <= 0:
            return float("inf")
        return self.unit_cost / self.reliability

    def can_satisfy(self, capability: str) -> bool:
        return self.enabled and capability.lower() in {x.lower() for x in self.capabilities}


class ResourceRegistry:
    def __init__(self, resources: Iterable[Resource] = ()) -> None:
        self._resources: dict[str, Resource] = {}
        for resource in resources:
            self.add(resource)

    def add(self, resource: Resource) -> None:
        if resource.resource_id in self._resources:
            raise ValueError(f"Duplicate resource ID: {resource.resource_id}")
        if not 0 <= resource.reliability <= 1 or not 0 <= resource.quality <= 1:
            raise ValueError("Reliability and quality must be between 0 and 1")
        if resource.unit_cost < 0 or resource.free_units < 0:
            raise ValueError("Cost and free units cannot be negative")
        self._resources[resource.resource_id] = resource

    def get(self, resource_id: str) -> Resource:
        return self._resources[resource_id]

    def match(self, capability: str, minimum_quality: float = 0.0) -> list[Resource]:
        return sorted(
            (r for r in self._resources.values() if r.can_satisfy(capability) and r.quality >= minimum_quality),
            key=lambda r: (r.effective_unit_cost, -r.quality, -r.reliability),
        )

    def all(self) -> tuple[Resource, ...]:
        return tuple(self._resources.values())
