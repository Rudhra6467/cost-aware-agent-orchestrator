"""Provider-neutral execution engine for CAOS execution sessions."""

from dataclasses import dataclass
from typing import Protocol

from .execution_session import ExecutionSession, ExecutionSessionManager, ExecutionTask


@dataclass(frozen=True)
class AgentResult:
    success: bool
    output: str = ""
    error: str | None = None


class Agent(Protocol):
    name: str

    def execute(self, task: ExecutionTask, context: dict[str, str]) -> AgentResult: ...


class AgentRegistry:
    """Maps explicit agent names to provider-neutral agent implementations."""

    def __init__(self, agents: list[Agent] | None = None) -> None:
        self._agents = {agent.name: agent for agent in (agents or [])}

    def register(self, agent: Agent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> Agent:
        try:
            return self._agents[name]
        except KeyError as exc:
            raise KeyError(f"Unknown agent: {name}") from exc


class ExecutionEngine:
    """Executes assigned tasks without knowing the underlying model/provider."""

    def __init__(self, sessions: ExecutionSessionManager, agents: AgentRegistry) -> None:
        self.sessions = sessions
        self.agents = agents

    def run_task(self, session_id: str, task_id: str, agent_name: str, context: dict[str, str] | None = None) -> AgentResult:
        session = self.sessions.get(session_id)
        if session.status.value != "running":
            raise ValueError("Execution session must be running")

        task = next((item for item in session.tasks if item.task_id == task_id), None)
        if task is None:
            raise KeyError(f"Unknown task: {task_id}")

        agent = self.agents.get(agent_name)
        task.assigned_agent = agent_name
        task.status = task.status.RUNNING
        result = agent.execute(task, context or {})
        if result.success:
            self.sessions.complete_task(session_id, task_id)
        else:
            task.status = task.status.FAILED
            session.status = session.status.FAILED
            session.error = result.error or "Agent execution failed"
        return result
