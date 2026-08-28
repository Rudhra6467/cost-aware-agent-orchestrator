"""Bounded deterministic agent used to prove the execution boundary."""

from dataclasses import dataclass
from pathlib import Path

from .execution_engine import AgentResult
from .execution_session import ExecutionTask


@dataclass(frozen=True)
class Artifact:
    path: str
    content: str


class DeterministicAgent:
    """A safe local agent that produces an auditable text artifact.

    It performs no shell commands, network access, or arbitrary code execution.
    """

    name = "deterministic-local"

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)

    def execute(self, task: ExecutionTask, context: dict[str, str]) -> AgentResult:
        self.workspace.mkdir(parents=True, exist_ok=True)
        filename = context.get("artifact", f"{task.task_id}.txt")
        path = self.workspace / Path(filename).name
        content = (
            f"task_id: {task.task_id}\n"
            f"role: {task.role.value}\n"
            f"description: {task.description}\n"
            f"agent: {self.name}\n"
        )
        path.write_text(content, encoding="utf-8")
        return AgentResult(True, output=content)
