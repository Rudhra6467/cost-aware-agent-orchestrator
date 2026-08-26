"""Reproducible benchmark runner for baseline vs CAOS routing policies."""

from dataclasses import dataclass
from typing import Callable

from .benchmark import BenchmarkAccumulator, BenchmarkResult, compare, optimization_is_valid


@dataclass(frozen=True)
class BenchmarkTask:
    task_id: str
    description: str


@dataclass(frozen=True)
class ExecutionMeasurement:
    cost: float
    success: bool
    latency_ms: int
    retries: int = 0
    handoffs: int = 0


@dataclass(frozen=True)
class BenchmarkReport:
    baseline: BenchmarkResult
    caos: BenchmarkResult
    metrics: dict[str, float]
    optimization_valid: bool


def run_benchmark(
    tasks: list[BenchmarkTask],
    baseline_executor: Callable[[BenchmarkTask], ExecutionMeasurement],
    caos_executor: Callable[[BenchmarkTask], ExecutionMeasurement],
) -> BenchmarkReport:
    """Run identical tasks through both policies and compare aggregate outcomes."""
    if not tasks:
        raise ValueError("Benchmark requires at least one task")

    baseline = BenchmarkAccumulator("baseline")
    caos = BenchmarkAccumulator("caos")

    for task in tasks:
        b = baseline_executor(task)
        baseline.add(cost=b.cost, success=b.success, latency_ms=b.latency_ms, retries=b.retries, handoffs=b.handoffs)
        c = caos_executor(task)
        caos.add(cost=c.cost, success=c.success, latency_ms=c.latency_ms, retries=c.retries, handoffs=c.handoffs)

    baseline_result = baseline.result()
    caos_result = caos.result()
    return BenchmarkReport(
        baseline=baseline_result,
        caos=caos_result,
        metrics=compare(baseline_result, caos_result),
        optimization_valid=optimization_is_valid(baseline_result, caos_result),
    )
