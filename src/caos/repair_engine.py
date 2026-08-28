"""Bounded repair loop for failed CAOS verification."""

from dataclasses import dataclass

from .agent_catalog import TaskRequirements
from .execution_runtime import ExecutionRuntime, RuntimeStep
from .execution_session import ExecutionStatus, ExecutionTask, TaskRole
from .verification import VerificationResult


@dataclass(frozen=True)
class RepairPlan:
    task_id: str
    attempt: int
    failed_checks: tuple[str, ...]
    description: str


class RepairEngine:
    """Turns failed verification evidence into bounded executable repair tasks."""

    def __init__(self, runtime: ExecutionRuntime, max_attempts: int = 3) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.runtime = runtime
        self.max_attempts = max_attempts
        self._attempts: dict[str, int] = {}
        self._plans: dict[str, RepairPlan] = {}
        self._history: dict[str, list[VerificationResult]] = {}

    def prepare(self, session_id: str, verification: VerificationResult) -> RepairPlan:
        session = self.runtime.sessions.get(session_id)
        if session.status != ExecutionStatus.REPAIRING:
            raise ValueError("Session must be repairing before preparing a repair")
        failed = tuple(check.name for check in verification.checks if not check.passed)
        if not failed:
            raise ValueError("Cannot prepare a repair without failed checks")

        attempt = self._attempts.get(session_id, 0) + 1
        self._history.setdefault(session_id, []).append(verification)
        if attempt > self.max_attempts:
            session.status = ExecutionStatus.FAILED
            session.error = "Maximum repair attempts exhausted"
            raise RuntimeError("Maximum repair attempts exhausted")

        task_id = f"repair_{len(session.tasks) + 1}"
        plan = RepairPlan(
            task_id,
            attempt,
            failed,
            "Repair failed verification checks: " + ", ".join(failed),
        )
        session.tasks.append(ExecutionTask(task_id, plan.description, TaskRole.DEVELOPER))
        self._attempts[session_id] = attempt
        self._plans[session_id] = plan
        return plan

    def history(self, session_id: str) -> tuple[VerificationResult, ...]:
        return tuple(self._history.get(session_id, ()))

    def attempts(self, session_id: str) -> int:
        return self._attempts.get(session_id, 0)

    def run(self, session_id: str, requirements: TaskRequirements, context: dict[str, str] | None = None) -> RuntimeStep:
        plan = self._plans.get(session_id)
        if plan is None:
            raise KeyError(f"No repair prepared for session: {session_id}")
        session = self.runtime.sessions.get(session_id)
        session.status = ExecutionStatus.RUNNING
        return self.runtime.orchestrator.run_task(session_id, plan.task_id, requirements, context)
