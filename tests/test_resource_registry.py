from datetime import date

from caos.resource_registry import ResourceRecord, ResourceRegistry


def test_registry_preserves_evidence_and_can_filter_capability():
    registry = ResourceRegistry()
    registry.add(
        ResourceRecord(
            resource_id="example",
            provider="Example",
            name="Example Free Model",
            category="llm",
            capabilities=("coding", "research"),
            quality_score=7.0,
            reliability_score=0.9,
            context_capacity=32000,
            input_cost_per_1k=0.0,
            output_cost_per_1k=0.0,
            free_tier_notes="Legitimate published free allocation.",
            availability_status="available",
            evidence_url="https://example.com/docs",
            last_verified_at=date(2026, 8, 25),
            confidence=0.8,
        )
    )

    matches = registry.by_capability("coding")

    assert len(matches) == 1
    assert matches[0].evidence_url.endswith("/docs")
    assert matches[0].last_verified_at == date(2026, 8, 25)
