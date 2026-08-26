"""Quota-aware resource selection."""

from .performance_evidence import PerformanceEvidence
from .quota import QuotaState, quota_health
from .resource_discovery import ResourceObservation
from .reliability_optimizer import expected_practical_cost
from .task_constraints import ResourceQuality, TaskConstraints, satisfies_constraints


def choose_quota_aware_resource(
    candidates: list[ResourceObservation],
    constraints: TaskConstraints,
    quality_by_resource: dict[str, ResourceQuality],
    historical: dict[str, PerformanceEvidence],
    quotas: dict[str, QuotaState],
) -> ResourceObservation | None:
    eligible: list[ResourceObservation] = []
    for resource in candidates:
        quality = quality_by_resource.get(resource.resource_id)
        evidence = historical.get(resource.resource_id)
        quota = quotas.get(resource.resource_id)
        if quality is None or evidence is None or quota is None or not quota.available:
            continue
        if satisfies_constraints(constraints, resource.estimated_unit_cost, quality):
            eligible.append(resource)

    if not eligible:
        return None

    return min(
        eligible,
        key=lambda item: (
            expected_practical_cost(historical[item.resource_id]),
            -quota_health(quotas[item.resource_id]),
            item.estimated_unit_cost,
            -item.confidence,
        ),
    )
