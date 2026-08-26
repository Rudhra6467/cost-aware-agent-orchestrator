"""Historical execution evidence used to estimate practical resource quality."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionOutcome:
    resource_id: str
    success: bool
    verification_passed: bool
    cost: float
    latency_seconds: float
    retries: int = 0

    def __post_init__(self) -> None:
        if self.cost < 0 or self.latency_seconds < 0 or self.retries < 0:
            raise ValueError("cost, latency, and retries cannot be negative")


@dataclass(frozen=True)
class PerformanceEvidence:
    resource_id: str
    executions: int
    success_rate: float
    verification_rate: float
    average_cost: float
    average_latency_seconds: float
    average_retries: float


def summarize_outcomes(outcomes: list[ExecutionOutcome]) -> dict[str, PerformanceEvidence]:
    grouped: dict[str, list[ExecutionOutcome]] = {}
    for outcome in outcomes:
        grouped.setdefault(outcome.resource_id, []).append(outcome)

    result: dict[str, PerformanceEvidence] = {}
    for resource_id, items in grouped.items():
        n = len(items)
        result[resource_id] = PerformanceEvidence(
            resource_id=resource_id,
            executions=n,
            success_rate=sum(x.success for x in items) / n,
            verification_rate=sum(x.verification_passed for x in items) / n,
            average_cost=sum(x.cost for x in items) / n,
            average_latency_seconds=sum(x.latency_seconds for x in items) / n,
            average_retries=sum(x.retries for x in items) / n,
        )
    return result
