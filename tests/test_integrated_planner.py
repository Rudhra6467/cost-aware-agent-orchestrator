from caos.constraints import UserConstraints
from caos.integrated_planner import IntegratedPlanner
from caos.optimizer import GlobalOptimizer
from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry
from caos.matching import CapabilityMatcher
from caos.resources import Resource, ResourceRegistry
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.quota_scheduler import QuotaWindow
from datetime import datetime, timezone


def test_integrated_planner_connects_core_layers():
    resources = ResourceRegistry([Resource("r", "p", "Resource", ("coding",), "1k", 0.01, free_units=10)])
    matcher = CapabilityMatcher(resources, EvidenceRegistry())
    optimizer = GlobalOptimizer(matcher)
    planner = IntegratedPlanner(optimizer)
    tasks = (EnrichedTask("t", "build", ("coding",), (), (), 1, 1000),)
    result = planner.plan(tasks, UsageLedger((QuotaSnapshot("r", 10),)), UserConstraints(budget=1), quota_windows={"r": (QuotaWindow("r", 10),)})
    assert result.optimization.total_cost == 0
    assert result.execution.estimated_minutes == 30
    assert result.scheduled_tasks[0].resource_id == "r"
