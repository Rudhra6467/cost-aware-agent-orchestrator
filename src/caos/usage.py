"""Measured execution economics. Estimate and actual stay separate."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ExecutionUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0
    latency_ms: float = 0.0
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    currency: str = "USD"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def combine_usage(items: list[ExecutionUsage]) -> ExecutionUsage:
    if not items:
        return ExecutionUsage()
    return ExecutionUsage(
        input_tokens=sum(item.input_tokens for item in items),
        output_tokens=sum(item.output_tokens for item in items),
        requests=sum(item.requests for item in items),
        latency_ms=sum(item.latency_ms for item in items),
        estimated_cost=sum(item.estimated_cost for item in items),
        actual_cost=sum(item.actual_cost for item in items),
        currency=items[0].currency,
    )
