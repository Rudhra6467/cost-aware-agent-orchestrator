from datetime import datetime, timedelta, timezone

from caos.resource_discovery import ResourceDiscovery, ResourceObservation


def observation(resource_id, cost, age_seconds=0, confidence=1.0):
    return ResourceObservation(
        resource_id=resource_id,
        provider="test-provider",
        capabilities=frozenset({"coding"}),
        source="https://example.invalid/pricing",
        observed_at=datetime.now(timezone.utc) - timedelta(seconds=age_seconds),
        free=cost == 0,
        estimated_unit_cost=cost,
        confidence=confidence,
    )


def test_cheapest_eligible_resource_wins():
    registry = ResourceDiscovery([observation("paid", 0.01), observation("free", 0.0)])
    assert registry.cheapest("coding").resource_id == "free"


def test_stale_resource_is_not_presented_as_current():
    registry = ResourceDiscovery([observation("stale", 0.0, age_seconds=90_000)])
    assert registry.cheapest("coding") is None


def test_higher_confidence_breaks_equal_cost_tie():
    registry = ResourceDiscovery([observation("low", 0.0, confidence=0.4), observation("high", 0.0, confidence=0.9)])
    assert registry.cheapest("coding").resource_id == "high"
