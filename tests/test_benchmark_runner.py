from caos.benchmark_runner import BenchmarkTask, ExecutionMeasurement, run_benchmark


def test_runner_executes_same_task_set_through_both_policies():
    tasks = [BenchmarkTask("t1", "build endpoint"), BenchmarkTask("t2", "add tests")]

    def baseline(task):
        return ExecutionMeasurement(cost=1.0, success=True, latency_ms=100)

    def caos(task):
        return ExecutionMeasurement(cost=0.5, success=True, latency_ms=80, handoffs=1)

    report = run_benchmark(tasks, baseline, caos)
    assert report.baseline.runs == 2
    assert report.caos.runs == 2
    assert report.metrics["cost_savings_pct"] == 50.0
    assert report.optimization_valid


def test_runner_does_not_call_empty_benchmark():
    try:
        run_benchmark([], lambda _: None, lambda _: None)
    except ValueError as exc:
        assert "at least one task" in str(exc)
    else:
        raise AssertionError("empty benchmark should fail")
