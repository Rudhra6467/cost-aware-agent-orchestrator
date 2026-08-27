"""Structured task enrichment with deterministic validation hooks."""

from dataclasses import dataclass

from .dag import TaskGraph


@dataclass(frozen=True)
class EnrichedTask:
    task_id: str
    description: str
    capabilities: tuple[str, ...]
    security_requirements: tuple[str, ...]
    acceptance_tests: tuple[str, ...]
    estimated_input_tokens: int
    estimated_output_tokens: int
    tool_calls: int = 0

    @property
    def estimated_tokens(self) -> int:
        return self.estimated_input_tokens + self.estimated_output_tokens


class TaskEnricher:
    """Deterministic baseline enrichment; LLM proposals can be validated against it."""

    def enrich(self, graph: TaskGraph) -> tuple[EnrichedTask, ...]:
        graph.validate()
        result = []
        for task in graph.tasks:
            capabilities = (task.category,)
            security = ("Protect secrets and credentials from source control",)
            tests = (f"Verify: {task.description}",)
            result.append(
                EnrichedTask(
                    task.task_id,
                    task.description,
                    capabilities,
                    security,
                    tests,
                    task.min_input_tokens,
                    task.max_output_tokens,
                    1,
                )
            )
        return tuple(result)


def validate_enrichment(graph: TaskGraph, enriched: tuple[EnrichedTask, ...]) -> None:
    graph_ids = {task.task_id for task in graph.tasks}
    enriched_ids = {task.task_id for task in enriched}
    if graph_ids != enriched_ids:
        raise ValueError("Enrichment must cover exactly the DAG tasks")
    for task in enriched:
        if not task.description.strip() or not task.capabilities:
            raise ValueError(f"Task {task.task_id} is missing required enrichment")
        if not task.acceptance_tests:
            raise ValueError(f"Task {task.task_id} has no acceptance tests")
        if task.estimated_input_tokens < 0 or task.estimated_output_tokens < 0:
            raise ValueError(f"Task {task.task_id} has invalid token estimates")
