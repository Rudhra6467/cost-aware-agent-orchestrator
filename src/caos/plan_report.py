"""User-facing cost plan and DIY roadmap generation primitives."""

from dataclasses import dataclass

from .cost_optimizer import CostOption, CostPolicy, rank_cost_options
from .models import AgentProfile, Task
from .planner import plan


@dataclass(frozen=True)
class BuildPlan:
    request: str
    tasks: tuple[Task, ...]
    recommended: tuple[CostOption, ...]
    alternatives: tuple[tuple[CostOption, ...], ...]
    estimated_cost: float
    diy_steps: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "request": self.request,
            "tasks": [
                {
                    "id": task.task_id,
                    "description": task.description,
                    "dependencies": list(task.dependencies),
                }
                for task in self.tasks
            ],
            "recommended": [option.__dict__ for option in self.recommended],
            "alternatives": [
                [option.__dict__ for option in options] for options in self.alternatives
            ],
            "estimated_cost": self.estimated_cost,
            "diy_steps": list(self.diy_steps),
        }


def create_build_plan(
    request: str,
    agents: list[AgentProfile],
    budget: float | None = None,
) -> BuildPlan:
    """Create the first two-path CAOS plan: Build or DIY."""
    tasks = tuple(plan(request))
    remaining = budget
    recommended: list[CostOption] = []
    alternatives: list[tuple[CostOption, ...]] = []

    for task in tasks:
        options = rank_cost_options(task, agents, CostPolicy(budget_remaining=remaining))
        if not options:
            raise ValueError(f"No feasible resource options for {task.task_id}")
        recommended.append(options[0])
        alternatives.append(tuple(options[1:]))
        if remaining is not None:
            remaining -= options[0].estimated_cost

    diy_steps = tuple(
        [
            "Review the task graph and acceptance criteria.",
            "Create the recommended project structure locally.",
            *[f"Complete {task.task_id}: {task.description}" for task in tasks],
            "Run tests/build verification before considering the project complete.",
            "Record actual costs and replace resources if a cheaper practical option exists.",
        ]
    )

    return BuildPlan(
        request=request,
        tasks=tasks,
        recommended=tuple(recommended),
        alternatives=tuple(alternatives),
        estimated_cost=sum(option.estimated_cost for option in recommended),
        diy_steps=diy_steps,
    )
