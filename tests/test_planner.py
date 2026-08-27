from datetime import datetime, timezone

from caos.dag import TaskGraph
from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry, ResourceEvidence
from caos.matching import CapabilityMatcher
from caos.models import Task
from caos.planner import CostPlanGenerator
from caos.resources import Resource, ResourceRegistry


def test_planner_generates_two_transparent_options():
    task = EnrichedTask("t", "coding", ("coding",), ("security",), ("test",), 100, 900)
    graph = TaskGraph((Task("t", "coding", "coding", 100, 900, 5.0),), ())
    resources = ResourceRegistry([
        Resource("free", "p", "Free", ("coding",), "1k_tokens", 0.0, free_units=1.0, reliability=0.9),
        Resource("paid", "p", "Paid", ("coding",), "1k_tokens", 0.01, quality=0.95),
    ])
    evidence = EvidenceRegistry()
    evidence.add(ResourceEvidence("e", "free", "https://example.com", "pricing", datetime.now(timezone.utc), "free", 1.0))
    matcher = CapabilityMatcher(resources, evidence)
    zero, hybrid = CostPlanGenerator(matcher).generate(graph, (task,))
    assert zero.name == "Zero-Cost First"
    assert hybrid.name == "Lowest Practical Cost"
    assert zero.total_cost == 0
    assert hybrid.total_cost == 0.01
