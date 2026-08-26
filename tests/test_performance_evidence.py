from caos.performance_evidence import ExecutionOutcome, summarize_outcomes


def test_summarizes_historical_execution_outcomes():
    evidence = summarize_outcomes([
        ExecutionOutcome("a", True, True, 0.0, 10, 0),
        ExecutionOutcome("a", True, False, 0.02, 20, 1),
        ExecutionOutcome("b", False, False, 0.01, 30, 2),
    ])
    assert evidence["a"].executions == 2
    assert evidence["a"].success_rate == 1.0
    assert evidence["a"].verification_rate == 0.5
    assert evidence["a"].average_cost == 0.01
    assert evidence["a"].average_retries == 0.5
    assert evidence["b"].success_rate == 0.0
