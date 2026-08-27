from datetime import datetime, timedelta, timezone

import pytest

from caos.evidence import EvidenceRegistry, ResourceEvidence


def evidence(eid, rid, days=0):
    return ResourceEvidence(eid, rid, "https://example.com/pricing", "pricing", datetime.now(timezone.utc) - timedelta(days=days), "Free quota is available", 0.95)


def test_evidence_is_grouped_and_freshest_is_selected():
    registry = EvidenceRegistry()
    registry.add(evidence("old", "model-a", 5))
    registry.add(evidence("new", "model-a", 1))
    assert registry.freshest("model-a").evidence_id == "new"
    assert len(registry.for_resource("model-a")) == 2


def test_evidence_requires_valid_url_and_timezone():
    with pytest.raises(ValueError):
        ResourceEvidence("x", "r", "example.com", "pricing", datetime.now(timezone.utc), "claim")
    with pytest.raises(ValueError):
        ResourceEvidence("y", "r", "https://example.com", "pricing", datetime.now(), "claim")
