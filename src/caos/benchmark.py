"""Deterministic benchmark primitives for comparing routing policies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    policy: str
    runs: int
    total_cost: float
    average_cost: float
    success_rate: float
    average_latency_ms: float
    total_retries: int
    total_handoffs: int


class BenchmarkAccumulator:
    def __init__(self, policy: str) -> None:
        self.policy = policy
        self._costs: list[float] = []
        self._successes = 0
        self._latencies: list[int] = []
        self._retries = 0
        self._handoffs = 0

    def add(self, *, cost: float, success: bool, latency_ms: int, retries: int = 0, handoffs: int = 0) -> None:
        if cost < 0 or latency_ms < 0 or retries < 0 or handoffs < 0:
            raise ValueError("benchmark measurements cannot be negative")
        self._costs.append(cost)
        self._successes += int(success)
        self._latencies.append(latency_ms)
        self._retries += retries
        self._handoffs += handoffs

    def result(self) -> BenchmarkResult:
        runs = len(self._costs)
        if runs == 0:
            raise ValueError("Benchmark has no runs")
        return BenchmarkResult(
            policy=self.policy,
            runs=runs,
            total_cost=sum(self._costs),
            average_cost=sum(self._costs) / runs,
            success_rate=self._successes / runs,
            average_latency_ms=sum(self._latencies) / runs,
            total_retries=self._retries,
            total_handoffs=self._handoffs,
        )


def compare(baseline: BenchmarkResult, caos: BenchmarkResult) -> dict[str, float]:
    if baseline.total_cost <= 0:
        raise ValueError("Baseline cost must be positive")
    return {
        "cost_savings_pct": (baseline.total_cost - caos.total_cost) / baseline.total_cost * 100,
        "success_rate_delta_pct": (caos.success_rate - baseline.success_rate) * 100,
        "latency_change_pct": ((caos.average_latency_ms - baseline.average_latency_ms)
                               / baseline.average_latency_ms * 100
                               if baseline.average_latency_ms else 0.0),
    }


def optimization_is_valid(baseline: BenchmarkResult, caos: BenchmarkResult) -> bool:
    """Cost savings count only when CAOS preserves success rate."""
    return caos.total_cost <= baseline.total_cost and caos.success_rate >= baseline.success_rate
