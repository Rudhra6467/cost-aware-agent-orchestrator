"""Constraint-aware resource selection."""

from .resource_discovery import ResourceDiscovery, ResourceObservation
from .task_constraints import ResourceQuality, TaskConstraints, satisfies_constraints


def choose_constrained_resource(
    constraints: TaskConstraints,
    discovery: ResourceDiscovery,
    quality_by_resource: dict[str, ResourceQuality],
    max_age_seconds: float = 86_400,
) -> ResourceObservation | None:
    candidates = discovery.candidates(constraints.required_capability, max_age_seconds)
    eligible = [
        resource for resource in candidates
        if resource.resource_id in quality_by_resource
        and satisfies_constraints(
            constraints,
            resource.estimated_unit_cost,
            quality_by_resource[resource.resource_id],
        )
    ]
    if not eligible:
        return None
    return min(eligible, key=lambda item: (item.estimated_unit_cost, -item.confidence))
