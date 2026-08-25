from caos.state import StateStore


def test_state_store_records_execution():
    store = StateStore(":memory:")
    store.record_task("t1", "build api")
    store.record_execution(
        task_id="t1",
        agent_id="agent-a",
        status="succeeded",
        input_tokens=10,
        output_tokens=20,
        cost_usd=0.01,
    )
    assert store.execution_count() == 1
