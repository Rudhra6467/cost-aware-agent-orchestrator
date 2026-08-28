"""Shared task primitives used by the project DAG planner."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: str
    description: str
    category: str
    min_input_tokens: int
    max_output_tokens: int
    complexity: float = 1.0
    dependencies: tuple[str, ...] = ()
