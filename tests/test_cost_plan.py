from datetime import datetime, timezone

from caos.cost_plan import build_plan
from caos.performance_evidence import PerformanceEvidence
from caos.quota import QuotaState
from caos.resource_discovery import ResourceDiscovery, ResourceObservation
from caos.task_constraints import ResourceQuality, TaskConstraints


def test_build_plan_assigns_eligible_resources_and_tracks_cost():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free", "free-model", frozenset({"coding"}), "registry", now, True, 0.0, 0.9),
        ResourceObservation("paid", "paid-model", frozenset({"coding"}), "registry", now, False, 0.01, 0.9),
    ])
    quality = {"free": ResourceQuality(0.95, 0.95, "high"), "paid": ResourceQuality(0.95, 0.99, "high")}
    history = {
        "free": PerformanceEvidence("free", 10, 1, 1, 0, 1, 0),
        "paid": PerformanceEvidence("paid", 10, 1, 1, 0.01, 1, 0),
    }
    quotas = {"free": QuotaState("free", 100, 10), "paid": QuotaState("paid", 100, 0)}
    plan = build_plan([("t1", TaskConstraints("coding", min_quality=.9, security_level="high"))], discovery, quality, history, quotas)
    assert plan.feasible
    assert plan.tasks[0].resource_id == "free"
    assert plan.estimated_api_cost == 0
