"""Evidence-first resource discovery primitives for CAOS."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class ResourceObservation:
    resource_id: str
    provider: str
    capabilities: frozenset[str]
    source: str
    observed_at: datetime
    free: bool
    estimated_unit_cost: float
    confidence: float
    available: bool = True

    def __post_init__(self) -> None:
        if not self.resource_id or not self.provider or not self.source:
            raise ValueError("resource_id, provider, and source are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.estimated_unit_cost < 0:
            raise ValueError("estimated_unit_cost cannot be negative")

    @property
    def age_seconds(self) -> float:
        now = datetime.now(timezone.utc)
        observed = self.observed_at
        if observed.tzinfo is None:
            observed = observed.replace(tzinfo=timezone.utc)
        return max(0.0, (now - observed).total_seconds())


class ResourceDiscovery:
    """Collect and filter observations without pretending stale data is live truth."""

    def __init__(self, observations: Iterable[ResourceObservation] = ()) -> None:
        self._observations = list(observations)

    def add(self, observation: ResourceObservation) -> None:
        self._observations.append(observation)

    def candidates(self, capability: str, max_age_seconds: float = 86_400) -> list[ResourceObservation]:
        return [
            item for item in self._observations
            if capability in item.capabilities
            and item.available
            and item.age_seconds <= max_age_seconds
        ]

    def cheapest(self, capability: str, max_age_seconds: float = 86_400) -> ResourceObservation | None:
        candidates = self.candidates(capability, max_age_seconds)
        if not candidates:
            return None
        return min(candidates, key=lambda item: (item.estimated_unit_cost, -item.confidence))
