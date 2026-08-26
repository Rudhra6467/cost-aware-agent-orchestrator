"""End-to-end provider handoff continuation primitives."""

from __future__ import annotations

from dataclasses import dataclass

from .agents import AgentExecutor
from .handoff import HandoffState
from .handoff_manifest import HandoffManifest
from .handoff_router import HandoffRouter
from .models import TaskStatus
from .provider_health import ProviderHealthRegistry


@dataclass(frozen=True)
class ContinuationResult:
    source_provider: str
    target_provider: str | None
    handed_off: bool
    target_prompt: str | None
    manifest: HandoffManifest
    output: str | None


class ContinuationCoordinator:
    """Convert a failed execution into a portable A→B continuation."""

    def __init__(self, executors: dict[str, AgentExecutor], health: ProviderHealthRegistry):
        self.executors = executors
        self.router = HandoffRouter(health)

    def continue_after_failure(
        self,
        *,
        source_provider: str,
        state: HandoffState,
        reason: str,
        target_capability: str = "coding",
    ) -> ContinuationResult:
        decision = self.router.route(
            state,
            source_agent=source_provider,
            target_capability=target_capability,
            reason=reason,
        )
        if decision.target_provider is None:
            return ContinuationResult(source_provider, None, False, None, decision.manifest, None)

        target_prompt = (
            "Continue the existing CAOS task from the handoff manifest below. "
            "Do not restart completed work. Preserve architecture and constraints.\n\n"
            + decision.manifest.to_json()
        )
        executor = self.executors[decision.target_provider]
        task = type("ContinuationTask", (), {
            "id": f"handoff:{state.project_id}",
            "description": target_prompt,
        })()
        result = executor.execute(task, target_prompt)
        output = result.output if result.status == TaskStatus.COMPLETED else None
        return ContinuationResult(
            source_provider,
            decision.target_provider,
            True,
            target_prompt,
            decision.manifest,
            output,
        )
