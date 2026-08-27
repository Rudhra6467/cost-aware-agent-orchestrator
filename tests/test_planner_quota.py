from datetime import datetime, timezone

from caos.dag import TaskGraph
from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry, ResourceEvidence
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.matching import CapabilityMatcher
from caos.models import Task
from caos.planner import CostPlanGenerator
from caos.resources import Resource, ResourceRegistry


def test_planner_spends_shared_free_quota_only_once():
    tasks = (
        Task("a", "A", "coding", 100, 100, 1),
        Task("b", "B", "coding", 100, 100, 1, dependencies=("a",)),
    )
    graph = TaskGraph(tasks, ())
    enriched = tuple(EnrichedTask(t.task_id, t.description, ("coding",), ("security",), ("test",), 100, 900) for t in tasks)
    resources = ResourceRegistry([Resource("free", "p", "Free", ("coding",), "1k", 0.01, free_units=1.0, quality=0.9)])
    evidence = EvidenceRegistry()
    evidence.add(ResourceEvidence("e", "free", "https://example.com", "pricing", datetime.now(timezone.utc), "quota", 1.0))
    ledger = UsageLedger((QuotaSnapshot("free", 1.0),))
    zero, _ = CostPlanGenerator(CapabilityMatcher(resources, evidence)).generate(graph, enriched, ledger)
    assert zero.total_cost == 0.01
    assert zero.free_coverage == 0.5
