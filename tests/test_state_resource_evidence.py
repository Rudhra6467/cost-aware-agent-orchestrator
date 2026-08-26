from caos.state import StateStore


def test_resource_evidence_round_trip():
    store = StateStore(":memory:")
    store.record_resource_evidence(
        resource_id="model-a",
        provider="provider-a",
        resource_name="Model A",
        evidence={"input_cost_per_1k": 0.0, "free_quota": "documented"},
        observed_at="2026-08-26T12:00:00Z",
        confidence=0.95,
    )
    evidence = store.get_resource_evidence("model-a")
    assert evidence["provider"] == "provider-a"
    assert evidence["evidence"]["input_cost_per_1k"] == 0.0
    assert evidence["confidence"] == 0.95
