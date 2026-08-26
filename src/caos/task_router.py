"""Task-DAG routing facade with auditable route decisions."""

from __future__ import annotations

from dataclasses import dataclass

from .cost_optimizer import CostPolicy
from .cost_router import CostAwareRouter, RouteDecision
from .models import AgentProfile, Task


@dataclass(frozen=True)
class TaskRoute:
    task_id: str
    decision: RouteDecision


class TaskRouter:
    def __init__(self, router: CostAwareRouter):
        self.router = router

    def route_ready_tasks(
        self,
        tasks: list[Task],
        completed_task_ids: set[str],
        agents: list[AgentProfile],
        *,
        policy: CostPolicy | None = None,
    ) -> list[TaskRoute]:
        routes: list[TaskRoute] = []
        for task in tasks:
            if task.task_id in completed_task_ids:
                continue
            if not set(task.dependencies).issubset(completed_task_ids):
                continue
            decision = self.router.route(task, agents, policy=policy)
            routes.append(TaskRoute(task.task_id, decision))
        return routes
