from datetime import datetime, timezone

from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry, ResourceEvidence
from caos.matching import CapabilityMatcher
from caos.optimizer import GlobalOptimizer
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.resources import Resource, ResourceRegistry


def test_global_optimizer_accounts_for_shared_quota_and_spillover():
    resources = ResourceRegistry([
        Resource("free", "p", "Free", ("coding",), "1k_tokens", 0.01, free_units=10, quality=0.8),
        Resource("paid", "p", "Paid", ("coding",), "1k_tokens", 0.02, quality=0.9),
    ])
    evidence = EvidenceRegistry()
    evidence.add(ResourceEvidence("e1", "free", "https://example.com", "pricing", datetime.now(timezone.utc), "quota", 1))
    matcher = CapabilityMatcher(resources, evidence)
    tasks = (
        EnrichedTask("a", "a", ("coding",), (), (), 1, 9000),
        EnrichedTask("b", "b", ("coding",), (), (), 1, 6000),
    )
    result = GlobalOptimizer(matcher).optimize(tasks, UsageLedger((QuotaSnapshot("free", 10),)))
    assert sum(x.free_units for x in result.assignments) == 10
    assert sum(x.paid_units for x in result.assignments) == 5
    assert result.total_cost == 0.1
    assert result.fully_free is False
