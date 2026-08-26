import pytest

from caos.consumption import estimate_consumption


def test_consumption_estimate_tracks_tokens_requests_and_tools():
    estimate = estimate_consumption(1000, 2000, 2, 3)
    assert estimate.total_tokens == 3000
    assert estimate.requests == 2
    assert estimate.tool_calls == 3


def test_consumption_rejects_negative_values():
    with pytest.raises(ValueError):
        estimate_consumption(-1, 10)
