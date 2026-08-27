"""Evidence and provenance primitives for resource research."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ResourceEvidence:
    evidence_id: str
    resource_id: str
    source_url: str
    source_type: str
    observed_at: datetime
    claim: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not self.source_url.startswith(("https://", "http://")):
            raise ValueError("Evidence source URL must be HTTP(S)")
        if not 0 <= self.confidence <= 1:
            raise ValueError("Evidence confidence must be between 0 and 1")
        if self.observed_at.tzinfo is None:
            raise ValueError("Evidence timestamp must be timezone-aware")

    @property
    def age_days(self) -> int:
        return max(0, (datetime.now(timezone.utc) - self.observed_at.astimezone(timezone.utc)).days)


class EvidenceRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ResourceEvidence] = {}

    def add(self, evidence: ResourceEvidence) -> None:
        if evidence.evidence_id in self._items:
            raise ValueError(f"Duplicate evidence ID: {evidence.evidence_id}")
        self._items[evidence.evidence_id] = evidence

    def for_resource(self, resource_id: str) -> tuple[ResourceEvidence, ...]:
        return tuple(x for x in self._items.values() if x.resource_id == resource_id)

    def freshest(self, resource_id: str) -> ResourceEvidence | None:
        items = self.for_resource(resource_id)
        return max(items, key=lambda x: x.observed_at) if items else None
