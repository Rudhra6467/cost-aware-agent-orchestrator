from datetime import datetime, timezone

from caos.cost_arbitrage import choose_resource
from caos.models import Task
from caos.resource_discovery import ResourceDiscovery, ResourceObservation


def test_task_routes_to_lowest_cost_fresh_resource():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("paid", "provider-a", frozenset({"coding"}), "source-a", now, False, 0.01, 0.9),
        ResourceObservation("free", "provider-b", frozenset({"coding"}), "source-b", now, True, 0.0, 0.8),
    ])
    decision = choose_resource(Task("t1", "write code"), discovery)
    assert decision.resource_id == "free"
    assert decision.estimated_cost == 0.0
    assert decision.evidence_source == "source-b"


def test_task_fails_closed_without_fresh_evidence():
    discovery = ResourceDiscovery([])
    try:
        choose_resource(Task("t1", "write code"), discovery)
    except ValueError as exc:
        assert "No fresh resource evidence" in str(exc)
    else:
        raise AssertionError("routing must fail closed without evidence")
