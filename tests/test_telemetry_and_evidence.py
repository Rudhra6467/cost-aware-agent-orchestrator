from datetime import datetime, timedelta, timezone

from caos.resource_evidence import ResourceEvidence
from caos.telemetry import ExecutionTelemetry
from caos.telemetry_store import TelemetryStore


def test_telemetry_persists_and_summarizes():
    store = TelemetryStore()
    store.record(ExecutionTelemetry.now(
        run_id="r1", task_id="t1", agent_id="a1", estimated_cost=0.01,
        actual_cost=0.005, input_tokens=100, output_tokens=200,
        latency_ms=500, retries=1, handoffs=0, verification_passed=True,
    ))
    summary = store.summary()
    assert summary["executions"] == 1
    assert summary["actual_cost"] == 0.005
    assert summary["output_tokens"] == 200


def test_resource_evidence_can_be_marked_stale():
    old = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    evidence = ResourceEvidence(
        provider_id="p", model_id="m", capability="coding",
        input_price_per_1k=0, output_price_per_1k=0,
        free_quota_description="daily", rate_limit_description="limited",
        source_url="https://example.com", observed_at=old,
    )
    assert evidence.is_stale(3600)
