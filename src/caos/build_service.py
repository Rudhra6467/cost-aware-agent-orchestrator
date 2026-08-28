"""Bridge approved planning decisions into execution sessions."""

from dataclasses import dataclass

from .execution_session import ExecutionSession, ExecutionSessionManager
from .planning_contract import PlanSummary, PlanningResponse


@dataclass(frozen=True)
class BuildRequest:
    idea: str
    plan_id: str


class BuildService:
    """Creates deterministic execution sessions from an approved plan.

    This layer deliberately does not execute agents. It converts the selected
    planning result into an explicit task graph that later execution adapters
    can consume.
    """

    def __init__(self, sessions: ExecutionSessionManager | None = None) -> None:
        self.sessions = sessions or ExecutionSessionManager()

    def create_session(self, response: PlanningResponse, request: BuildRequest) -> ExecutionSession:
        if request.idea != response.idea:
            raise ValueError("Build idea must match the planning response")

        plan = next((p for p in response.plans if p.plan_id == request.plan_id), None)
        if plan is None:
            raise ValueError(f"Unknown plan: {request.plan_id}")

        tasks = self._tasks_for(response, plan)
        return self.sessions.create(response.idea, plan, tasks)

    @staticmethod
    def _tasks_for(response: PlanningResponse, plan: PlanSummary) -> list[str]:
        tasks = [
            "Understand the requested outcome and constraints",
            f"Execute the {plan.label} implementation plan",
            "Run verification against the requested outcome",
        ]
        if "DIY" in response.next_actions:
            tasks.insert(1, "Prepare a clear implementation handoff")
        return tasks
