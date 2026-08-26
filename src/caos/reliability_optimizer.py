"""Select resources using historical practical-cost evidence."""

from .performance_evidence import PerformanceEvidence
from .resource_discovery import ResourceDiscovery, ResourceObservation
from .task_constraints import ResourceQuality, TaskConstraints, satisfies_constraints


def expected_practical_cost(evidence: PerformanceEvidence) -> float:
    """Approximate expected spend for one successful execution.

    V1 uses verification success as the success denominator and a retry penalty.
    A zero-success resource is never considered finite.
    """
    if evidence.verification_rate <= 0:
        return float("inf")
    retry_factor = 1.0 + evidence.average_retries
    return evidence.average_cost * retry_factor / evidence.verification_rate


def choose_reliable_resource(
    constraints: TaskConstraints,
    discovery: ResourceDiscovery,
    quality_by_resource: dict[str, ResourceQuality],
    historical: dict[str, PerformanceEvidence],
    max_age_seconds: float = 86_400,
) -> ResourceObservation | None:
    candidates = discovery.candidates(constraints.required_capability, max_age_seconds)
    eligible: list[ResourceObservation] = []
    for resource in candidates:
        quality = quality_by_resource.get(resource.resource_id)
        evidence = historical.get(resource.resource_id)
        if quality is None or evidence is None:
            continue
        if satisfies_constraints(constraints, resource.estimated_unit_cost, quality):
            eligible.append(resource)
    if not eligible:
        return None

    return min(
        eligible,
        key=lambda item: (
            expected_practical_cost(historical[item.resource_id]),
            item.estimated_unit_cost,
            -item.confidence,
        ),
    )
