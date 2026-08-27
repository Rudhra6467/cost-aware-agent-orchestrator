from caos.constraints import UserConstraints
from caos.enrichment import EnrichedTask
from caos.evidence import EvidenceRegistry
from caos.integrated_planner import IntegratedPlanner
from caos.matching import CapabilityMatcher
from caos.optimizer import GlobalOptimizer
from caos.resources import Resource, ResourceRegistry
from caos.ledger import QuotaSnapshot, UsageLedger
from caos.unified_planner import UnifiedExecutionPlanner


def test_unified_planner_generates_standard_variants_and_simulates_graph():
    registry = ResourceRegistry([Resource("r", "p", "Builder", ("coding",), "1k", 0.01, free_units=10)])
    optimizer = GlobalOptimizer(CapabilityMatcher(registry, EvidenceRegistry()))
    planner = UnifiedExecutionPlanner(IntegratedPlanner(optimizer))
    tasks = (
        EnrichedTask("a", "first", ("coding",), (), (), 1, 1000),
        EnrichedTask("b", "second", ("coding",), (), (), 1, 1000),
    )
    plan = planner.build_variants(tasks, UsageLedger((QuotaSnapshot("r", 10),)), UserConstraints())
    assert {v.variant_id for v in plan.comparison.variants} == {"zero-cost", "lowest-practical", "fastest-practical"}
    assert plan.simulations[0][1].elapsed_minutes == 30
