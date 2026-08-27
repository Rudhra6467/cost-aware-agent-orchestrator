"""Evaluate generated CAOS variants against one dependency graph."""

from dataclasses import dataclass
from datetime import datetime

from .execution import ExecutionAssumptions, ExecutionCostModel, ExecutionEstimate
from .quota_scheduler import QuotaScheduler, QuotaWindow, ScheduledTask
from .simulation import ExecutionSimulator, SimTask, SimulationResult
from .variant_policy import VariantPolicy, VariantPolicyGenerator


@dataclass(frozen=True)
class VariantEvaluation:
    policy: VariantPolicy
    simulation: SimulationResult
    execution: ExecutionEstimate
    quota_schedule: tuple[ScheduledTask, ...]
    total_wait_minutes: float


class VariantSimulationEngine:
    """Run policy allocations through execution and quota models before comparison."""

    def __init__(self, policy_generator: VariantPolicyGenerator) -> None:
        self.policy_generator = policy_generator
        self.simulator = ExecutionSimulator()
        self.cost_model = ExecutionCostModel()
        self.quota_scheduler = QuotaScheduler()

    def evaluate(self, policy, tasks, ledger, windows, execution=ExecutionAssumptions(), now: datetime | None = None):
        result = self.policy_generator.optimize(policy, tasks, ledger)
        sim_tasks = tuple(SimTask(t.task_id, execution.average_task_minutes, tuple(getattr(t, "dependencies", ()))) for t in tasks)
        simulation = self.simulator.simulate(sim_tasks)
        scheduled = []
        for assignment in result.assignments:
            resource_windows = windows.get(assignment.resource_id, ())
            if resource_windows:
                scheduled.append(self.quota_scheduler.schedule(
                    assignment.task_id,
                    assignment.free_units + assignment.paid_units,
                    execution.average_task_minutes,
                    resource_windows,
                    now,
                ))
        wait = sum(x.waited_minutes for x in scheduled)
        return VariantEvaluation(policy, simulation, self.cost_model.estimate(result, execution), tuple(scheduled), wait)
