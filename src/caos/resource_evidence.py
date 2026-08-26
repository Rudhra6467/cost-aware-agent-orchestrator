"""Evidence-backed resource records for volatile pricing and quota data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ResourceEvidence:
    provider_id: str
    model_id: str
    capability: str
    input_price_per_1k: float
    output_price_per_1k: float
    free_quota_description: str
    rate_limit_description: str
    source_url: str
    observed_at: str
    confidence: float = 1.0

    @classmethod
    def observed(cls, **kwargs) -> "ResourceEvidence":
        return cls(observed_at=datetime.now(timezone.utc).isoformat(), **kwargs)

    def is_stale(self, max_age_seconds: int, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        observed = datetime.fromisoformat(self.observed_at)
        return (now - observed).total_seconds() > max_age_seconds
