import pytest

from caos.execution import ExecutionAssumptions, ExecutionCostModel
from caos.optimizer import Assignment, OptimizationResult


def test_execution_model_accounts_for_retries_and_handoffs():
    result = OptimizationResult((
        Assignment("a", "r1", 1, 0, 0.0, True, "free"),
        Assignment("b", "r2", 1, 2, 1.0, True, "paid"),
    ), 1.0, False, ())
    estimate = ExecutionCostModel().estimate(result, ExecutionAssumptions(retry_rate=0.1, handoff_rate=0.5, handoff_cost_units=0.2, average_task_minutes=20, parallelism=1, switch_penalty_minutes=2))
    assert estimate.expected_retries == pytest.approx(0.2)
    assert estimate.expected_handoffs == pytest.approx(0.5)
    assert estimate.monetary_cost == pytest.approx(1.2)
    assert estimate.estimated_minutes == pytest.approx(42)
