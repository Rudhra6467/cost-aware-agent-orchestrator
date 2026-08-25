"""Core domain models for CAOS.

The first implementation deliberately keeps the models provider-agnostic.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentProfile:
    """Capabilities and economics used by the selector."""

    agent_id: str
    name: str
    coding_score: float
    architecture_score: float = 0.0
    research_score: float = 0.0
    context_window: int = 32_000
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    availability: float = 1.0
    reliability: float = 1.0
    enabled: bool = True


@dataclass(frozen=True)
class Task:
    """A dependency-aware unit of work that CAOS can route to an agent."""

    task_id: str
    description: str
    required_capability: str = "coding"
    estimated_input_tokens: int = 1_000
    estimated_output_tokens: int = 1_000
    minimum_capability: float = 0.0
    context_required: int = 4_000
    dependencies: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Selection:
    """A transparent agent-selection decision."""

    agent_id: str
    score: float
    estimated_cost: float
    rationale: str


@dataclass
class ExecutionResult:
    """Provider-neutral result returned by an execution adapter."""

    task_id: str
    agent_id: str
    status: TaskStatus
    output: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    error: str | None = None

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens
