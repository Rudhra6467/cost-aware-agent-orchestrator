import pytest

from caos.usage import normalize_usage


def test_usage_is_normalized_to_common_units():
    usage = normalize_usage(1000, 500, 0.01, 0.02)
    assert usage.total_tokens == 1500
    assert usage.estimated_cost_usd == pytest.approx(0.02)


def test_negative_usage_is_rejected():
    with pytest.raises(ValueError):
        normalize_usage(-1, 0, 0.0, 0.0)
