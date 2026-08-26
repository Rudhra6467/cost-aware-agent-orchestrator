from caos.state import StateStore
from caos.usage import normalize_usage


def test_normalized_usage_is_persisted_as_execution():
    store = StateStore(":memory:")
    usage = normalize_usage(1000, 500, 0.01, 0.02)
    store.record_normalized_execution(usage, task_id="task-1", agent_id="agent-a")
    assert store.execution_count() == 1
    assert store.execution_cost_total() == 0.02
