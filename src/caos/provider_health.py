"""Provider health and quota signals used by resource routing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProviderState(str, Enum):
    HEALTHY = "healthy"
    RATE_LIMITED = "rate_limited"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ProviderHealth:
    provider_id: str
    state: ProviderState = ProviderState.UNKNOWN
    remaining_requests: int | None = None
    reset_after_seconds: int | None = None
    last_error: str | None = None

    @property
    def eligible(self) -> bool:
        return self.state == ProviderState.HEALTHY and (
            self.remaining_requests is None or self.remaining_requests > 0
        )


class ProviderHealthRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ProviderHealth] = {}

    def update(self, health: ProviderHealth) -> None:
        self._items[health.provider_id] = health

    def get(self, provider_id: str) -> ProviderHealth | None:
        return self._items.get(provider_id)

    def eligible(self) -> tuple[ProviderHealth, ...]:
        return tuple(item for item in self._items.values() if item.eligible)
