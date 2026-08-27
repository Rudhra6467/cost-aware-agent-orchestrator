from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.matching import CapabilityMatcher
from caos.resources import Resource, ResourceRegistry
from caos.variant_policy import VariantPolicy, VariantPolicyGenerator


def test_zero_cost_prefers_free_resource():
    registry = ResourceRegistry([
        Resource("free", "p", "Free", ("coding",), "unit", 0.0, free_units=10, reliability=.8, quality=.8),
        Resource("paid", "p", "Paid", ("coding",), "unit", .01, free_units=0, reliability=1, quality=1),
    ])
    gen = VariantPolicyGenerator(CapabilityMatcher(registry, EvidenceRegistry()))
    task = (EnrichedTask("t", "code", ("coding",), (), (), 1, 1000),)
    result = gen.optimize(VariantPolicy.ZERO_COST, task, UsageLedger((QuotaSnapshot("free", 10), QuotaSnapshot("paid", 0))))
    assert result.assignments[0].resource_id == "free"


def test_policies_return_distinct_policy_metadata():
    assert VariantPolicy.ZERO_COST.value != VariantPolicy.FASTEST_PRACTICAL.value
