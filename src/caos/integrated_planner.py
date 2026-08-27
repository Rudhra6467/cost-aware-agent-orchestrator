"""Integrated CAOS planning facade: constraints, optimization, execution and comparison."""

from dataclasses import dataclass

from .comparison import PlanComparison, PlanComparisonEngine, PlanVariant
from .constraints import UserConstraints
from .execution import ExecutionAssumptions, ExecutionCostModel, ExecutionEstimate
from .optimizer import GlobalOptimizer, OptimizationResult
from .quota_scheduler import QuotaScheduler, QuotaWindow, ScheduledTask


@dataclass(frozen=True)
class IntegratedPlan:
    optimization: OptimizationResult
    execution: ExecutionEstimate
    comparison: PlanComparison | None
    scheduled_tasks: tuple[ScheduledTask, ...]


class IntegratedPlanner:
    """Single orchestration entry point for the current planning primitives."""

    def __init__(self, optimizer: GlobalOptimizer) -> None:
        self.optimizer = optimizer
        self.execution_model = ExecutionCostModel()
        self.comparison_engine = PlanComparisonEngine()
        self.quota_scheduler = QuotaScheduler()

    def plan(
        self,
        tasks,
        ledger,
        constraints: UserConstraints,
        execution: ExecutionAssumptions = ExecutionAssumptions(),
        variants: tuple[PlanVariant, ...] = (),
        quota_windows: dict[str, tuple[QuotaWindow, ...]] | None = None,
    ) -> IntegratedPlan:
        optimization = self.optimizer.optimize(tasks, ledger)
        execution_estimate = self.execution_model.estimate(optimization, execution)
        comparison = self.comparison_engine.compare(variants, constraints) if variants else None

        scheduled: list[ScheduledTask] = []
        if quota_windows:
            for assignment in optimization.assignments:
                windows = quota_windows.get(assignment.resource_id, ())
                if windows:
                    units = assignment.free_units + assignment.paid_units
                    scheduled.append(self.quota_scheduler.schedule(assignment.task_id, units, execution.average_task_minutes, windows))

        return IntegratedPlan(optimization, execution_estimate, comparison, tuple(scheduled))
