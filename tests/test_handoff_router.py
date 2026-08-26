import json

from caos.handoff import HandoffState
from caos.handoff_manifest import HandoffManifest
from caos.handoff_router import HandoffRouter
from caos.provider_health import ProviderHealth, ProviderHealthRegistry, ProviderState


def test_manifest_round_trip_and_integrity():
    state = HandoffState(
        project_id="demo",
        objective="build api",
        completed_tasks=("schema",),
        pending_tasks=("routes",),
    )
    manifest = HandoffManifest.create(
        state,
        reason="429 quota",
        source_agent="agent-a",
        target_capability="coding",
    )
    restored = HandoffManifest.from_json(manifest.to_json())
    assert restored.state == state
    assert restored.integrity_sha256 == manifest.integrity_sha256


def test_manifest_detects_tampering():
    state = HandoffState("demo", "build api")
    manifest = HandoffManifest.create(
        state, reason="quota", source_agent="a", target_capability="coding"
    )
    payload = json.loads(manifest.to_json())
    payload["state"]["objective"] = "tampered"
    try:
        HandoffManifest.from_json(json.dumps(payload))
    except ValueError:
        pass
    else:
        raise AssertionError("tampering should be detected")


def test_router_selects_healthy_fallback():
    health = ProviderHealthRegistry()
    health.update(ProviderHealth("agent-a", ProviderState.RATE_LIMITED, 0))
    health.update(ProviderHealth("agent-b", ProviderState.HEALTHY, 5))
    health.update(ProviderHealth("agent-c", ProviderState.HEALTHY, 2))

    decision = HandoffRouter(health).route(
        HandoffState("demo", "build api"),
        source_agent="agent-a",
        target_capability="coding",
        reason="429 quota",
    )
    assert decision.target_provider == "agent-b"
