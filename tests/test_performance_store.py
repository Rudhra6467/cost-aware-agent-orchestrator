import sqlite3

from caos.performance_evidence import ExecutionOutcome
from caos.performance_store import PerformanceStore


def test_performance_store_records_and_aggregates_outcomes():
    store = PerformanceStore(sqlite3.connect(":memory:"))
    store.record(ExecutionOutcome("r1", True, True, 0.01, 10, 0))
    store.record(ExecutionOutcome("r1", True, True, 0.02, 20, 1))
    evidence = store.evidence()["r1"]
    assert evidence.executions == 2
    assert evidence.verification_rate == 1.0
    assert evidence.average_cost == 0.015
    assert evidence.average_retries == 0.5
