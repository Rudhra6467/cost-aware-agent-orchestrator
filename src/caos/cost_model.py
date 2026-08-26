"""Cost estimation and prediction-vs-actual analysis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class TokenPrice:
    input_per_1k: float
    output_per_1k: float

    def estimate(self, usage: Usage) -> float:
        return (usage.input_tokens / 1000) * self.input_per_1k + (
            usage.output_tokens / 1000
        ) * self.output_per_1k


@dataclass(frozen=True)
class CostComparison:
    estimated: float
    actual: float

    @property
    def absolute_error(self) -> float:
        return abs(self.actual - self.estimated)

    @property
    def error_pct(self) -> float:
        if self.estimated == 0:
            return 0.0 if self.actual == 0 else float("inf")
        return self.absolute_error / abs(self.estimated) * 100


def compare_costs(estimated: float, actual: float) -> CostComparison:
    if estimated < 0 or actual < 0:
        raise ValueError("Costs cannot be negative")
    return CostComparison(estimated=estimated, actual=actual)
