from datetime import datetime, timezone

from caos.constrained_arbitrage import choose_constrained_resource
from caos.resource_discovery import ResourceDiscovery, ResourceObservation
from caos.task_constraints import ResourceQuality, TaskConstraints


def test_free_resource_is_selected_only_when_quality_constraints_are_met():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free", "a", frozenset({"coding"}), "source-a", now, True, 0.0, 0.9),
        ResourceObservation("cheap", "b", frozenset({"coding"}), "source-b", now, False, 0.01, 0.9),
    ])
    quality = {
        "free": ResourceQuality(0.70, 0.99, "standard"),
        "cheap": ResourceQuality(0.95, 0.99, "high"),
    }
    selected = choose_constrained_resource(
        TaskConstraints("coding", min_quality=0.90, security_level="high"),
        discovery,
        quality,
    )
    assert selected.resource_id == "cheap"


def test_no_resource_is_selected_when_constraints_cannot_be_satisfied():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free", "a", frozenset({"coding"}), "source", now, True, 0.0, 1.0),
    ])
    quality = {"free": ResourceQuality(0.80, 0.80, "standard")}
    assert choose_constrained_resource(TaskConstraints("coding", min_quality=0.95), discovery, quality) is None
