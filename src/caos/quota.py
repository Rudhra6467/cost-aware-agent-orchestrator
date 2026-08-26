"""Quota and rate-limit state used by dynamic resource routing."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class QuotaState:
    resource_id: str
    limit: int | None
    used: int
    reset_at: datetime | None = None
    limited: bool = False

    @property
    def remaining(self) -> int | None:
        if self.limit is None:
            return None
        return max(0, self.limit - self.used)

    @property
    def available(self) -> bool:
        return not self.limited and (self.remaining is None or self.remaining > 0)

    def reset_in_seconds(self, now: datetime | None = None) -> float | None:
        if self.reset_at is None:
            return None
        now = now or datetime.now(timezone.utc)
        return max(0.0, (self.reset_at - now).total_seconds())


def quota_health(quota: QuotaState) -> float:
    """Return a conservative 0..1 health score from known quota state."""
    if not quota.available:
        return 0.0
    if quota.remaining is None or quota.limit in (None, 0):
        return 0.5
    return quota.remaining / quota.limit
