"""End-to-end Phase 1→2 CAOS decision pipeline.

This module deliberately stops at a transparent proposal. It does not spend
money or execute generated code until a user-approved plan is returned.
"""

from __future__ import annotations

from dataclasses import dataclass

from .blueprint import BlueprintEngine, ProductBlueprint
from .cost_optimizer import CostOption, CostPolicy, rank_cost_options
from .models import AgentProfile, Task
from .proposal import BuildProposal, ProposalEngine


@dataclass(frozen=True)
class PlannedTask:
    task: Task
    options: tuple[CostOption, ...]
    recommended: CostOption


@dataclass(frozen=True)
class ProjectPlan:
    blueprint: ProductBlueprint
    tasks: tuple[PlannedTask, ...]
    proposal: BuildProposal


class CostAwarePipeline:
    """Connect blueprinting, task decomposition and resource optimization."""

    def __init__(self, agents: list[AgentProfile]) -> None:
        self.agents = agents
        self.blueprints = BlueprintEngine()
        self.proposals = ProposalEngine()

    def create_plan(
        self,
        raw_idea: str,
        policy: CostPolicy | None = None,
    ) -> ProjectPlan:
        blueprint = self.blueprints.analyze(raw_idea)
        if blueprint.open_questions:
            raise ValueError(
                "Blueprint needs clarification before cost planning: "
                + "; ".join(blueprint.open_questions)
            )
        blueprint = self.blueprints.apply_user_decision(blueprint, "approve")

        tasks = self._tasks_from_blueprint(blueprint)
        planned: list[PlannedTask] = []
        for task in tasks:
            options = rank_cost_options(task, self.agents, policy)
            if not options:
                raise ValueError(f"No feasible resource for task: {task.task_id}")
            planned.append(PlannedTask(task, tuple(options), options[0]))

        first = planned[0].recommended
        proposal = self.proposals.create(
            blueprint,
            first,
            [item.recommended for item in planned[1:]],
        )
        return ProjectPlan(blueprint, tuple(planned), proposal)

    @staticmethod
    def _tasks_from_blueprint(blueprint: ProductBlueprint) -> list[Task]:
        tasks: list[Task] = []
        previous: str | None = None
        for index, layer in enumerate(blueprint.layers, start=1):
            task_id = f"build-{index:02d}-{layer.name.lower().replace(' ', '-') }"
            capability = "architecture" if layer.name == "Infrastructure" else "coding"
            task = Task(
                task_id=task_id,
                description=f"Implement the {layer.name} layer: {', '.join(layer.components)}",
                required_capability=capability,
                minimum_capability=0.45,
                context_required=4_000,
                dependencies=(previous,) if previous else (),
                metadata={"blueprint_layer": layer.name},
            )
            tasks.append(task)
            previous = task_id
        return tasks
