"""Provider-neutral usage normalization for CAOS telemetry."""

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float


def normalize_usage(input_tokens: int, output_tokens: int, input_price_per_1k: float, output_price_per_1k: float) -> NormalizedUsage:
    values = (input_tokens, output_tokens, input_price_per_1k, output_price_per_1k)
    if any(value < 0 for value in values):
        raise ValueError("usage and pricing values cannot be negative")
    cost = (input_tokens / 1000) * input_price_per_1k + (output_tokens / 1000) * output_price_per_1k
    return NormalizedUsage(input_tokens, output_tokens, input_tokens + output_tokens, cost)
