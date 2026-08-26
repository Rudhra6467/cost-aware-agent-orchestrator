import pytest

from caos.benchmark import BenchmarkAccumulator, compare


def test_benchmark_aggregates_runs():
    b = BenchmarkAccumulator("baseline")
    b.add(cost=1.0, success=True, latency_ms=100)
    b.add(cost=3.0, success=False, latency_ms=300, retries=1)
    result = b.result()
    assert result.total_cost == 4.0
    assert result.average_cost == 2.0
    assert result.success_rate == 0.5
    assert result.total_retries == 1


def test_compare_reports_savings_and_quality_delta():
    baseline = BenchmarkAccumulator("baseline")
    baseline.add(cost=10, success=True, latency_ms=100)
    caos = BenchmarkAccumulator("caos")
    caos.add(cost=6, success=True, latency_ms=80)
    metrics = compare(baseline.result(), caos.result())
    assert metrics["cost_savings_pct"] == pytest.approx(40.0)
    assert metrics["success_rate_delta_pct"] == pytest.approx(0.0)
    assert metrics["latency_change_pct"] == pytest.approx(-20.0)
