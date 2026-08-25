"""Provider-neutral execution interface for future LLM adapters."""

from abc import ABC, abstractmethod

from .models import ExecutionResult, Task


class AgentExecutor(ABC):
    """Adapter boundary between CAOS and a concrete AI provider."""

    agent_id: str

    @abstractmethod
    def execute(self, task: Task, context: str = "") -> ExecutionResult:
        """Execute a task and return a normalized result."""
        raise NotImplementedError


class MockAgentExecutor(AgentExecutor):
    """Deterministic executor used for local development and tests."""

    def __init__(self, agent_id: str = "mock-agent") -> None:
        self.agent_id = agent_id

    def execute(self, task: Task, context: str = "") -> ExecutionResult:
        output = (
            "MOCK EXECUTION\n"
            f"Task: {task.description}\n"
            f"Context supplied: {'yes' if context else 'no'}\n"
        )
        return ExecutionResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            status="succeeded",
            output=output,
            input_tokens=max(1, len(task.description.split())),
            output_tokens=max(1, len(output.split())),
        )
