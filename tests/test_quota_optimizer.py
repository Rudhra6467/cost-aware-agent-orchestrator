from datetime import datetime, timezone

from caos.performance_evidence import PerformanceEvidence
from caos.quota import QuotaState
from caos.quota_optimizer import choose_quota_aware_resource
from caos.resource_discovery import ResourceObservation
from caos.task_constraints import ResourceQuality, TaskConstraints


def test_quota_aware_router_avoids_exhausted_free_resource():
    now = datetime.now(timezone.utc)
    candidates = [
        ResourceObservation("free-a", "a", frozenset({"coding"}), "source-a", now, True, 0.0, 0.9),
        ResourceObservation("free-b", "b", frozenset({"coding"}), "source-b", now, True, 0.0, 0.9),
    ]
    quality = {r: ResourceQuality(0.9, 0.95, "high") for r in ("free-a", "free-b")}
    historical = {
        r: PerformanceEvidence(r, 10, 1.0, 1.0, 0.0, 5, 0.0)
        for r in ("free-a", "free-b")
    }
    quotas = {
        "free-a": QuotaState("free-a", 100, 100, limited=True),
        "free-b": QuotaState("free-b", 100, 10),
    }
    selected = choose_quota_aware_resource(
        candidates, TaskConstraints("coding", min_quality=0.8, security_level="high"), quality, historical, quotas
    )
    assert selected.resource_id == "free-b"
