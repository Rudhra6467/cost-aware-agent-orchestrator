from datetime import date, timedelta

import pytest

from caos.resource_registry import ResourceRecord, ResourceRegistry


def resource(**overrides):
    values = dict(
        resource_id="gemini-free",
        provider="provider-a",
        name="Example Free Model",
        category="coding",
        capabilities=("coding",),
        quality_score=0.8,
        reliability_score=0.9,
        context_capacity=32000,
        input_cost_per_1k=0.0,
        output_cost_per_1k=0.0,
        free_tier_notes="documented free quota",
        availability_status="healthy",
        evidence_url="https://example.com/pricing",
        last_verified_at=date.today(),
        confidence=0.9,
    )
    values.update(overrides)
    return ResourceRecord(**values)


def test_registry_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        ResourceRegistry([resource(confidence=1.2)])


def test_registry_can_exclude_stale_resources():
    registry = ResourceRegistry([
        resource(resource_id="fresh", last_verified_at=date.today()),
        resource(resource_id="old", last_verified_at=date.today() - timedelta(days=45)),
    ])
    assert {r.resource_id for r in registry.verified(30)} == {"fresh"}


def test_resource_staleness_is_explicit():
    assert resource(last_verified_at=date.today() - timedelta(days=31)).is_stale(30)
