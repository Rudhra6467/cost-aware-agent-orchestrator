import pytest

from caos.resources import Resource, ResourceRegistry


def test_registry_matches_capability_and_orders_by_effective_cost():
    registry = ResourceRegistry([
        Resource("paid", "example", "Paid", ("coding",), "1k_tokens", 0.02, reliability=1.0, quality=0.9),
        Resource("free", "example", "Free", ("coding",), "1k_tokens", 0.0, free_units=10, reliability=0.8, quality=0.85),
    ])
    matches = registry.match("coding", minimum_quality=0.8)
    assert matches[0].resource_id == "free"


def test_registry_rejects_invalid_values():
    with pytest.raises(ValueError):
        ResourceRegistry([Resource("x", "p", "x", ("coding",), "unit", -1)])
