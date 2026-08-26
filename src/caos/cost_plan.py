"""Unified cost-aware execution planning primitives."""

from dataclasses import dataclass

from .performance_evidence import PerformanceEvidence
from .quota import QuotaState
from .quota_optimizer import choose_quota_aware_resource
from .resource_discovery import ResourceDiscovery
from .reliability_optimizer import expected_practical_cost
from .task_constraints import ResourceQuality, TaskConstraints


@dataclass(frozen=True)
class PlannedTask:
    task_id: str
    resource_id: str
    estimated_cost: float
    expected_practical_cost: float
    quota_remaining_before: int | None


@dataclass(frozen=True)
class ExecutionPlan:
    tasks: tuple[PlannedTask, ...]
    estimated_api_cost: float
    estimated_practical_cost: float
    feasible: bool
    reason: str | None = None


def build_plan(
    tasks: list[tuple[str, TaskConstraints]],
    discovery: ResourceDiscovery,
    quality_by_resource: dict[str, ResourceQuality],
    historical: dict[str, PerformanceEvidence],
    quotas: dict[str, QuotaState],
    budget: float | None = None,
) -> ExecutionPlan:
    planned: list[PlannedTask] = []
    api_total = 0.0
    practical_total = 0.0

    for task_id, constraints in tasks:
        candidates = discovery.candidates(constraints.required_capability, 86_400)
        selected = choose_quota_aware_resource(
            candidates, constraints, quality_by_resource, historical, quotas
        )
        if selected is None:
            return ExecutionPlan(tuple(planned), api_total, practical_total, False,
                                 f"No eligible resource for task {task_id}")
        evidence = historical[selected.resource_id]
        quota = quotas[selected.resource_id]
        if quota.remaining is not None and quota.remaining < 1:
            return ExecutionPlan(tuple(planned), api_total, practical_total, False,
                                 f"Insufficient quota for task {task_id}")
        task_cost = selected.estimated_unit_cost
        task_practical = expected_practical_cost(evidence)
        api_total += task_cost
        practical_total += task_practical
        planned.append(PlannedTask(task_id, selected.resource_id, task_cost,
                                   task_practical, quota.remaining))
        if budget is not None and practical_total > budget:
            return ExecutionPlan(tuple(planned), api_total, practical_total, False,
                                 "Budget exceeded")

    return ExecutionPlan(tuple(planned), api_total, practical_total, True)
