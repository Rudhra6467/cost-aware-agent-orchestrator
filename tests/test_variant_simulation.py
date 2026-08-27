from datetime import datetime, timedelta, timezone

from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.matching import CapabilityMatcher
from caos.resources import Resource, ResourceRegistry
from caos.quota_scheduler import QuotaWindow
from caos.variant_policy import VariantPolicy, VariantPolicyGenerator
from caos.variant_simulation import VariantSimulationEngine


def test_variant_evaluation_includes_quota_wait_and_execution_metrics():
    registry = ResourceRegistry([Resource("r", "p", "Builder", ("coding",), "unit", .01, free_units=0)])
    gen = VariantPolicyGenerator(CapabilityMatcher(registry, EvidenceRegistry()))
    engine = VariantSimulationEngine(gen)
    tasks = (EnrichedTask("t", "code", ("coding",), (), (), 1, 1000),)
    now = datetime(2026, 8, 27, 12, tzinfo=timezone.utc)
    windows = {"r": (QuotaWindow("r", 0, reset_at=now + timedelta(minutes=20)),)}
    evaluation = engine.evaluate(VariantPolicy.LOWEST_PRACTICAL, tasks, UsageLedger((QuotaSnapshot("r", 0),)), windows, now=now)
    assert evaluation.execution.monetary_cost > 0
    assert evaluation.total_wait_minutes == 20
    assert evaluation.simulation.elapsed_minutes == 30
