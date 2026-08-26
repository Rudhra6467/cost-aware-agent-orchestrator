import pytest

from caos.cost_model import TokenPrice, Usage, compare_costs


def test_token_price_estimates_input_and_output_cost():
    price = TokenPrice(input_per_1k=0.01, output_per_1k=0.03)
    assert price.estimate(Usage(input_tokens=1000, output_tokens=2000)) == pytest.approx(0.07)


def test_cost_comparison_reports_error():
    comparison = compare_costs(0.10, 0.08)
    assert comparison.absolute_error == pytest.approx(0.02)
    assert comparison.error_pct == pytest.approx(20.0)


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        compare_costs(-0.01, 0.0)
