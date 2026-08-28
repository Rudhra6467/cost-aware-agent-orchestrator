"""Execution-session foundation for turning an approved CAOS plan into work."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .planning_contract import PlanSummary


class ExecutionStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    REPAIRING = "repairing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionTask:
    task_id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str | None = None


@dataclass
class ExecutionSession:
    session_id: str
    plan_id: str
    plan_label: str
    idea: str
    status: ExecutionStatus = ExecutionStatus.READY
    tasks: list[ExecutionTask] = field(default_factory=list)
    completed_tasks: int = 0
    error: str | None = None

    @property
    def progress(self) -> float:
        if not self.tasks:
            return 0.0
        return self.completed_tasks / len(self.tasks)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["progress"] = self.progress
        for task in data["tasks"]:
            task["status"] = task["status"].value
        return data


class ExecutionSessionManager:
    """In-memory session store for the first execution vertical slice.

    Persistence is deliberately deferred until the execution lifecycle is proven.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, ExecutionSession] = {}

    def create(self, idea: str, plan: PlanSummary, tasks: list[str]) -> ExecutionSession:
        session = ExecutionSession(
            session_id=f"exec_{uuid4().hex[:12]}",
            plan_id=plan.plan_id,
            plan_label=plan.label,
            idea=idea,
            tasks=[ExecutionTask(f"task_{i + 1}", task) for i, task in enumerate(tasks)],
        )
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> ExecutionSession:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise KeyError(f"Unknown execution session: {session_id}") from exc

    def start(self, session_id: str) -> ExecutionSession:
        session = self.get(session_id)
        if session.status != ExecutionStatus.READY:
            raise ValueError("Only ready execution sessions can be started")
        session.status = ExecutionStatus.RUNNING
        return session

    def complete_task(self, session_id: str, task_id: str) -> ExecutionSession:
        session = self.get(session_id)
        task = next((t for t in session.tasks if t.task_id == task_id), None)
        if task is None:
            raise KeyError(f"Unknown task: {task_id}")
        if task.status == TaskStatus.COMPLETED:
            return session
        task.status = TaskStatus.COMPLETED
        session.completed_tasks = sum(t.status == TaskStatus.COMPLETED for t in session.tasks)
        if session.completed_tasks == len(session.tasks):
            session.status = ExecutionStatus.VERIFYING
        return session
