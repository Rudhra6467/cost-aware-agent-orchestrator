"""End-to-end deterministic CAOS orchestration loop for M1.

The orchestrator connects planning, free-first resource selection, execution,
and telemetry. Provider adapters remain replaceable behind AgentExecutor.
"""

from dataclasses import dataclass

from .agents import AgentExecutor
from .cost_optimizer import CostPolicy, CostOption, recommend_lowest_practical_cost
from .models import AgentProfile, ExecutionResult, TaskStatus
from .planner import plan
from .state import StateStore


@dataclass(frozen=True)
class TaskExecution:
    task_id: str
    option: CostOption
    result: ExecutionResult


@dataclass(frozen=True)
class ProjectExecution:
    request: str
    executions: tuple[TaskExecution, ...]
    estimated_cost: float
    actual_cost: float

    @property
    def succeeded(self) -> bool:
        return all(item.result.status == TaskStatus.SUCCEEDED for item in self.executions)


class CAOSOrchestrator:
    """Coordinate the current M1 planning → selection → execution loop."""

    def __init__(
        self,
        agents: list[AgentProfile],
        executors: dict[str, AgentExecutor],
        state_store: StateStore | None = None,
    ) -> None:
        self.agents = agents
        self.executors = executors
        self.state = state_store or StateStore(":memory:")

    def run(self, request: str, budget: float | None = None) -> ProjectExecution:
        tasks = plan(request)
        remaining = budget
        executions: list[TaskExecution] = []

        for task in tasks:
            self.state.record_task(task.task_id, task.description)
            option = recommend_lowest_practical_cost(
                task,
                self.agents,
                CostPolicy(budget_remaining=remaining),
            )

            executor = self.executors.get(option.agent_id)
            if executor is None:
                raise ValueError(f"No executor registered for selected resource: {option.agent_id}")

            result = executor.execute(task)
            actual_cost = self._actual_cost(option.agent_id, result)
            self.state.record_execution(
                task_id=result.task_id,
                agent_id=result.agent_id,
                status=result.status.value,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                cost_usd=actual_cost,
                error=result.error,
            )

            if remaining is not None:
                remaining -= actual_cost

            executions.append(TaskExecution(task.task_id, option, result))

        estimated_cost = sum(item.option.estimated_cost for item in executions)
        actual_cost = sum(
            self._actual_cost(item.option.agent_id, item.result) for item in executions
        )
        return ProjectExecution(request, tuple(executions), estimated_cost, actual_cost)

    def _actual_cost(self, agent_id: str, result: ExecutionResult) -> float:
        agent = next((candidate for candidate in self.agents if candidate.agent_id == agent_id), None)
        if agent is None:
            raise ValueError(f"Unknown agent profile: {agent_id}")
        return (
            result.input_tokens / 1000 * agent.cost_per_1k_input
            + result.output_tokens / 1000 * agent.cost_per_1k_output
        )
