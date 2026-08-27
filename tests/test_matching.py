from datetime import datetime, timezone

from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry, ResourceEvidence
from caos.matching import CapabilityMatcher
from caos.resources import Resource, ResourceRegistry


def test_matcher_prefers_available_free_capacity():
    resources = ResourceRegistry([
        Resource("paid", "p", "Paid", ("coding",), "unit", 0.01, quality=0.95),
        Resource("free", "p", "Free", ("coding",), "unit", 0.00, free_units=100, quality=0.8),
    ])
    evidence = EvidenceRegistry()
    evidence.add(ResourceEvidence("e1", "free", "https://example.com", "pricing", datetime.now(timezone.utc), "free quota", 0.9))
    task = EnrichedTask("t", "code", ("coding",), ("protect secrets",), ("test",), 10, 20)
    matches = CapabilityMatcher(resources, evidence).match(task)
    assert matches[0].resource.resource_id == "free"
    assert matches[0].evidence_count == 1


def test_matcher_exposes_missing_evidence():
    resources = ResourceRegistry([Resource("x", "p", "X", ("coding",), "unit", 0.0)])
    task = EnrichedTask("t", "code", ("coding",), ("security",), ("test",), 1, 1)
    matches = CapabilityMatcher(resources, EvidenceRegistry()).match(task)
    assert matches[0].evidence_count == 0
    assert matches[0].freshest_evidence_age_days is None
