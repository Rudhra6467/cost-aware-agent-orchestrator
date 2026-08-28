"""Bounded repair loop for failed CAOS verification."""

from dataclasses import dataclass

from .agent_catalog import TaskRequirements
from .execution_runtime import ExecutionRuntime, RuntimeStep
from .execution_session import ExecutionStatus, ExecutionTask, TaskRole
from .verification import VerificationResult


@dataclass(frozen=True)
class RepairPlan:
    task_id: str
    failed_checks: tuple[str, ...]
    description: str


class RepairEngine:
    """Turns failed verification evidence into an ordinary executable task."""

    def __init__(self, runtime: ExecutionRuntime) -> None:
        self.runtime = runtime
        self._plans: dict[str, RepairPlan] = {}

    def prepare(self, session_id: str, verification: VerificationResult) -> RepairPlan:
        session = self.runtime.sessions.get(session_id)
        if session.status != ExecutionStatus.REPAIRING:
            raise ValueError("Session must be repairing before preparing a repair")
        failed = tuple(check.name for check in verification.checks if not check.passed)
        if not failed:
            raise ValueError("Cannot prepare a repair without failed checks")
        task_id = f"repair_{len(session.tasks) + 1}"
        plan = RepairPlan(task_id, failed, "Repair failed verification checks: " + ", ".join(failed))
        session.tasks.append(ExecutionTask(task_id, plan.description, TaskRole.DEVELOPER))
        self._plans[session_id] = plan
        return plan

    def run(self, session_id: str, requirements: TaskRequirements, context: dict[str, str] | None = None) -> RuntimeStep:
        plan = self._plans.get(session_id)
        if plan is None:
            raise KeyError(f"No repair prepared for session: {session_id}")
        session = self.runtime.sessions.get(session_id)
        session.status = ExecutionStatus.RUNNING
        return self.runtime.orchestrator.run_task(session_id, plan.task_id, requirements, context)
