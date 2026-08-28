from datetime import datetime, timezone

from caos.execution_plan import build_execution_plan
from caos.models import Task
from caos.resource_discovery import ResourceDiscovery, ResourceObservation


def test_execution_plan_routes_each_task_and_totals_cost():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free-code", "provider-a", frozenset({"coding"}), "source-a", now, True, 0.0, 0.9),
        ResourceObservation("cheap-research", "provider-b", frozenset({"research"}), "source-b", now, False, 0.002, 0.95),
    ])
    plan = build_execution_plan([
        Task("code", "write code", required_capability="coding"),
        Task("research", "research pricing", required_capability="research"),
    ], discovery)
    assert [item.resource_id for item in plan.tasks] == ["free-code", "cheap-research"]
    assert plan.estimated_total_cost == 0.002


def test_plan_preserves_evidence_provenance():
    now = datetime.now(timezone.utc)
    discovery = ResourceDiscovery([
        ResourceObservation("free", "provider", frozenset({"coding"}), "official-source", now, True, 0.0, 1.0),
    ])
    plan = build_execution_plan([Task("t1", "code")], discovery)
    assert plan.tasks[0].evidence_source == "official-source"
