"""Bridge resource evidence into transparent cost-aware routing."""

from dataclasses import dataclass

from .models import Task
from .resource_discovery import ResourceDiscovery, ResourceObservation


@dataclass(frozen=True)
class ArbitrageDecision:
    task_id: str
    resource_id: str
    provider: str
    estimated_cost: float
    confidence: float
    evidence_source: str
    rationale: str


def choose_resource(task: Task, discovery: ResourceDiscovery, max_age_seconds: float = 86_400) -> ArbitrageDecision:
    """Choose the cheapest fresh resource capable of the task."""
    resource: ResourceObservation | None = discovery.cheapest(task.required_capability, max_age_seconds)
    if resource is None:
        raise ValueError(f"No fresh resource evidence satisfies task '{task.task_id}'")

    return ArbitrageDecision(
        task_id=task.task_id,
        resource_id=resource.resource_id,
        provider=resource.provider,
        estimated_cost=resource.estimated_unit_cost,
        confidence=resource.confidence,
        evidence_source=resource.source,
        rationale=(
            f"Selected {resource.resource_id} as the lowest-cost fresh resource "
            f"for capability '{task.required_capability}'."
        ),
    )
