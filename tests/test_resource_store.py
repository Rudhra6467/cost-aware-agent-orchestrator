import sqlite3
from datetime import datetime, timezone

from caos.resource_discovery import ResourceObservation
from caos.resource_store import ResourceStore


def test_resource_observation_round_trip():
    store = ResourceStore(sqlite3.connect(":memory:"))
    item = ResourceObservation(
        resource_id="gemini-free",
        provider="google",
        capabilities=frozenset({"coding", "reasoning"}),
        source="https://example.invalid/source",
        observed_at=datetime.now(timezone.utc),
        free=True,
        estimated_unit_cost=0.0,
        confidence=0.8,
    )
    store.save(item)
    loaded = store.load_recent()
    assert len(loaded) == 1
    assert loaded[0].resource_id == item.resource_id
    assert loaded[0].capabilities == item.capabilities
    assert loaded[0].confidence == item.confidence
