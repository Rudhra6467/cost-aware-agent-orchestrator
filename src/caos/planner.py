"""First-pass dependency-aware task decomposition for M1."""

from .models import Task


def plan(project_request: str) -> list[Task]:
    """Convert a simple project request into a small executable task DAG."""
    request = project_request.strip()
    if not request:
        raise ValueError("Project request cannot be empty.")

    return [
        Task(
            task_id="task-001",
            description=f"Analyze requirements and define implementation steps for: {request}",
            required_capability="architecture",
            estimated_input_tokens=700,
            estimated_output_tokens=700,
            minimum_capability=5.0,
        ),
        Task(
            task_id="task-002",
            description=f"Implement the requested software: {request}",
            required_capability="coding",
            estimated_input_tokens=1500,
            estimated_output_tokens=2500,
            minimum_capability=6.0,
            dependencies=("task-001",),
        ),
    ]
