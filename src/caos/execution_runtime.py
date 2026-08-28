"""High-level runtime that composes CAOS execution infrastructure."""

from dataclasses import dataclass

from .agent_catalog import AgentCatalog, TaskRequirements
from .audit_trail import AuditTrail, ExecutionEvent
from .execution_engine import AgentRegistry, AgentResult
from .execution_scheduler import ExecutionScheduler
from .execution_session import ExecutionSession, ExecutionSessionManager, ExecutionStatus
from .orchestration import Orchestrator, SelectionDecision
from .task_graph import TaskGraph


@dataclass(frozen=True)
class RuntimeStep:
    decision: SelectionDecision
    result: AgentResult


class ExecutionRuntime:
    """Single entry point for dependency-aware, cost-aware task execution."""

    def __init__(self, sessions: ExecutionSessionManager, graph: TaskGraph, catalog: AgentCatalog, agents: AgentRegistry, audit: AuditTrail | None = None) -> None:
        self.sessions = sessions
        self.audit = audit or AuditTrail()
        self.scheduler = ExecutionScheduler(graph)
        self.orchestrator = Orchestrator(sessions, catalog, agents, self.audit)

    def start(self, session_id: str) -> ExecutionSession:
        session = self.sessions.start(session_id)
        self.audit.record(ExecutionEvent(session_id, "SESSION_STARTED"))
        return session

    def ready_tasks(self, session_id: str) -> list[str]:
        return self.scheduler.ready_tasks(self.sessions.get(session_id))

    def run_next(self, session_id: str, requirements: dict[str, TaskRequirements], context: dict[str, str] | None = None) -> RuntimeStep:
        session = self.sessions.get(session_id)
        if session.status != ExecutionStatus.RUNNING:
            raise ValueError("Execution session must be running")
        ready = self.scheduler.ready_tasks(session)
        if not ready:
            raise ValueError("No executable tasks are ready")
        task_id = ready[0]
        task_requirements = requirements.get(task_id)
        if task_requirements is None:
            raise KeyError(f"Missing requirements for ready task: {task_id}")
        return RuntimeStep(*self.orchestrator.run_task(session_id, task_id, task_requirements, context))
