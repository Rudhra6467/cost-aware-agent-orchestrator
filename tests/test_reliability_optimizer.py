from datetime import datetime, timezone

from caos.performance_evidence import PerformanceEvidence
from caos.reliability_optimizer import choose_reliable_resource, expected_practical_cost
from caos.resource_discovery import ResourceDiscovery, ResourceObservation
from caos.task_constraints import ResourceQuality, TaskConstraints


def test_expected_practical_cost_penalizes_retries_and_failures():
    good = PerformanceEvidence("good", 10, 1.0, 1.0, 0.01, 10, 0.0)
    fragile = PerformanceEvidence("fragile", 10, 1.0, 0.5, 0.0, 10, 2.0)
    assert expected_practical_cost(good) == 0.01
    assert expected_practical_cost(fragile) == 0.0


def test_reliability_optimizer_can_choose_free_verified_resource():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free", "a", frozenset({"coding"}), "source-a", now, True, 0.0, 0.9),
        ResourceObservation("paid", "b", frozenset({"coding"}), "source-b", now, False, 0.01, 0.9),
    ])
    quality = {
        "free": ResourceQuality(0.95, 0.98, "high"),
        "paid": ResourceQuality(0.95, 0.98, "high"),
    }
    historical = {
        "free": PerformanceEvidence("free", 20, 0.95, 0.90, 0.0, 8, 0.1),
        "paid": PerformanceEvidence("paid", 20, 0.99, 0.99, 0.01, 12, 0.0),
    }
    selected = choose_reliable_resource(TaskConstraints("coding", min_quality=0.9, security_level="high"), discovery, quality, historical)
    assert selected.resource_id == "free"
