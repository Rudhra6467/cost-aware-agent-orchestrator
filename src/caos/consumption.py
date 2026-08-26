"""Estimate resource consumption before execution."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConsumptionEstimate:
    input_tokens: int
    output_tokens: int
    requests: int = 1
    tool_calls: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


def estimate_consumption(
    input_tokens: int,
    output_tokens: int,
    requests: int = 1,
    tool_calls: int = 0,
) -> ConsumptionEstimate:
    values = (input_tokens, output_tokens, requests, tool_calls)
    if any(value < 0 for value in values):
        raise ValueError("consumption values cannot be negative")
    return ConsumptionEstimate(input_tokens, output_tokens, requests, tool_calls)
