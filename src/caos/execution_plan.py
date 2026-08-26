"""Provider-neutral execution plan generated from cost-arbitrage decisions."""

from dataclasses import dataclass

from .cost_arbitrage import ArbitrageDecision, choose_resource
from .models import Task
from .resource_discovery import ResourceDiscovery


@dataclass(frozen=True)
class PlannedTask:
    task_id: str
    resource_id: str
    provider: str
    estimated_cost: float
    confidence: float
    evidence_source: str
    rationale: str


@dataclass(frozen=True)
class ExecutionPlan:
    tasks: tuple[PlannedTask, ...]
    estimated_total_cost: float


def build_execution_plan(
    tasks: list[Task],
    discovery: ResourceDiscovery,
    max_age_seconds: float = 86_400,
) -> ExecutionPlan:
    if not tasks:
        raise ValueError("Execution plan requires at least one task")

    decisions: list[ArbitrageDecision] = [
        choose_resource(task, discovery, max_age_seconds) for task in tasks
    ]
    planned = tuple(
        PlannedTask(
            task_id=d.task_id,
            resource_id=d.resource_id,
            provider=d.provider,
            estimated_cost=d.estimated_cost,
            confidence=d.confidence,
            evidence_source=d.evidence_source,
            rationale=d.rationale,
        )
        for d in decisions
    )
    return ExecutionPlan(planned, sum(item.estimated_cost for item in planned))
