"""Route a failed execution to an eligible alternative resource."""

from __future__ import annotations

from dataclasses import dataclass

from .handoff import HandoffState
from .handoff_manifest import HandoffManifest
from .provider_health import ProviderHealthRegistry


@dataclass(frozen=True)
class HandoffDecision:
    target_provider: str | None
    manifest: HandoffManifest
    reason: str


class HandoffRouter:
    def __init__(self, health: ProviderHealthRegistry) -> None:
        self.health = health

    def route(
        self,
        state: HandoffState,
        *,
        source_agent: str,
        target_capability: str,
        reason: str,
    ) -> HandoffDecision:
        candidates = [item for item in self.health.eligible() if item.provider_id != source_agent]
        candidates.sort(key=lambda item: (item.remaining_requests is None, -(item.remaining_requests or 0)))
        target = candidates[0].provider_id if candidates else None
        manifest = HandoffManifest.create(
            state,
            reason=reason,
            source_agent=source_agent,
            target_capability=target_capability,
        )
        return HandoffDecision(target, manifest, reason if target else "No eligible fallback provider")
