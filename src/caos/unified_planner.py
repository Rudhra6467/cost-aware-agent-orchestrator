"""Generate and compare CAOS execution-plan variants from one project definition."""

from dataclasses import dataclass

from .comparison import PlanComparison, PlanComparisonEngine, PlanVariant
from .constraints import UserConstraints
from .execution import ExecutionAssumptions, ExecutionCostModel
from .integrated_planner import IntegratedPlanner
from .simulation import ExecutionSimulator, SimTask, SimulationResult


@dataclass(frozen=True)
class UnifiedPlan:
    comparison: PlanComparison
    simulations: tuple[tuple[str, SimulationResult], ...]


class UnifiedExecutionPlanner:
    """Build three standard strategy variants from the same DAG and compare them."""

    def __init__(self, integrated: IntegratedPlanner) -> None:
        self.integrated = integrated
        self.simulator = ExecutionSimulator()
        self.cost_model = ExecutionCostModel()
        self.comparator = PlanComparisonEngine()

    def build_variants(
        self,
        tasks,
        ledger,
        constraints: UserConstraints,
        execution: ExecutionAssumptions = ExecutionAssumptions(),
    ) -> UnifiedPlan:
        # The optimizer currently supplies the common baseline. Standard variants are
        # explicit strategy labels until provider/resource policy generation is added.
        baseline = self.integrated.optimizer.optimize(tasks, ledger)
        base_estimate = self.cost_model.estimate(baseline, execution)
        task_graph = tuple(
            SimTask(t.task_id, execution.average_task_minutes, tuple(getattr(t, "dependencies", ())))
            for t in tasks
        )
        simulation = self.simulator.simulate(task_graph)

        variants = (
            PlanVariant("zero-cost", "Zero-Cost", baseline, simulation.elapsed_minutes / 1440),
            PlanVariant("lowest-practical", "Lowest-Practical-Cost", baseline, simulation.elapsed_minutes / 1440),
            PlanVariant("fastest-practical", "Fastest-Practical", baseline, simulation.elapsed_minutes / 1440),
        )
        # Keep the three variants distinct in the API; full policy-specific resource
        # generation will replace this shared baseline in the next iteration.
        comparison = self.comparator.compare(variants, constraints)
        return UnifiedPlan(comparison, (("baseline", simulation),))
