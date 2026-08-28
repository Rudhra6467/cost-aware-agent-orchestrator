"""Cost-aware agent selection integrated with task execution."""

from dataclasses import dataclass

from .agent_catalog import AgentCatalog, AgentScore, TaskRequirements
from .audit_trail import AuditTrail, ExecutionEvent
from .execution_engine import AgentRegistry, AgentResult
from .execution_session import ExecutionSessionManager, ExecutionTask


@dataclass(frozen=True)
class SelectionDecision:
    task_id: str
    agent_name: str
    score: float
    reasons: tuple[str, ...]


class Orchestrator:
    """Selects an agent, records the decision, then executes it."""

    def __init__(self, sessions: ExecutionSessionManager, catalog: AgentCatalog, agents: AgentRegistry, audit: AuditTrail | None = None) -> None:
        self.sessions = sessions
        self.catalog = catalog
        self.agents = agents
        self.audit = audit or AuditTrail()
        self.decisions: dict[str, SelectionDecision] = {}

    def run_task(self, session_id: str, task_id: str, requirements: TaskRequirements, context: dict[str, str] | None = None) -> tuple[SelectionDecision, AgentResult]:
        session = self.sessions.get(session_id)
        task = next((item for item in session.tasks if item.task_id == task_id), None)
        if task is None:
            raise KeyError(f"Unknown task: {task_id}")
        if task.role != requirements.role:
            raise ValueError("Task role does not match agent requirements")

        selected: AgentScore = self.catalog.select(requirements)
        decision = SelectionDecision(task_id, selected.agent.name, selected.score, selected.reasons)
        self.decisions[task_id] = decision
        self.audit.record(ExecutionEvent(session_id, "AGENT_SELECTED", task_id, selected.agent.name, evidence=selected.reasons))
        return decision, self._execute(session_id, task, selected.agent.name, context or {})

    def _execute(self, session_id: str, task: ExecutionTask, agent_name: str, context: dict[str, str]) -> AgentResult:
        session = self.sessions.get(session_id)
        if session.status.value != "running":
            raise ValueError("Execution session must be running")
        agent = self.agents.get(agent_name)
        task.assigned_agent = agent_name
        task.status = task.status.RUNNING
        self.audit.record(ExecutionEvent(session_id, "TASK_STARTED", task.task_id, agent_name))
        result = agent.execute(task, context)
        if result.success:
            self.sessions.complete_task(session_id, task.task_id)
            self.audit.record(ExecutionEvent(session_id, "TASK_COMPLETED", task.task_id, agent_name, result="success"))
        else:
            task.status = task.status.FAILED
            session.status = session.status.FAILED
            session.error = result.error or "Agent execution failed"
            self.audit.record(ExecutionEvent(session_id, "TASK_FAILED", task.task_id, agent_name, result=result.error or "Agent execution failed"))
        return result
