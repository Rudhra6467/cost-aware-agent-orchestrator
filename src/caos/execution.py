"""Practical execution-cost model for CAOS plan comparison."""

from dataclasses import dataclass

from .comparison import PlanVariant
from .optimizer import OptimizationResult


@dataclass(frozen=True)
class ExecutionAssumptions:
    retry_rate: float = 0.05
    handoff_rate: float = 0.0
    handoff_cost_units: float = 0.0
    average_task_minutes: float = 30.0
    parallelism: int = 1
    switch_penalty_minutes: float = 2.0

    def __post_init__(self) -> None:
        for name in ("retry_rate", "handoff_rate"):
            value = getattr(self, name)
            if not 0 <= value < 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.handoff_cost_units < 0 or self.average_task_minutes <= 0 or self.parallelism <= 0 or self.switch_penalty_minutes < 0:
            raise ValueError("Execution assumptions must be non-negative and parallelism must be positive")


@dataclass(frozen=True)
class ExecutionEstimate:
    monetary_cost: float
    expected_retries: float
    expected_handoffs: float
    estimated_minutes: float
    practical_cost_score: float


class ExecutionCostModel:
    def estimate(self, result: OptimizationResult, assumptions: ExecutionAssumptions = ExecutionAssumptions()) -> ExecutionEstimate:
        task_count = len(result.assignments) + len(result.unfulfilled_tasks)
        expected_retries = task_count * assumptions.retry_rate
        expected_handoffs = max(0.0, task_count - 1) * assumptions.handoff_rate
        execution_units = sum(x.free_units + x.paid_units for x in result.assignments)
        retry_spend = result.total_cost * assumptions.retry_rate
        handoff_spend = expected_handoffs * assumptions.handoff_cost_units
        monetary = result.total_cost + retry_spend + handoff_spend
        minutes = (task_count * assumptions.average_task_minutes / assumptions.parallelism) + expected_handoffs * assumptions.switch_penalty_minutes
        score = monetary + (minutes / 60.0) * 0.0
        # Time is returned separately; monetary score remains interpretable as dollars.
        return ExecutionEstimate(monetary, expected_retries, expected_handoffs, minutes, score)

    def enrich_variant(self, variant: PlanVariant, assumptions: ExecutionAssumptions = ExecutionAssumptions()) -> tuple[PlanVariant, ExecutionEstimate]:
        estimate = self.estimate(variant.result, assumptions)
        return variant, estimate
