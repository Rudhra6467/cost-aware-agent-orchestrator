"""Dependency-aware scheduler for CAOS execution sessions."""

from .execution_session import ExecutionSession, TaskStatus
from .task_graph import TaskGraph


class ExecutionScheduler:
    """Exposes only dependency-ready tasks for execution."""

    def __init__(self, graph: TaskGraph) -> None:
        self.graph = graph

    def ready_tasks(self, session: ExecutionSession) -> list[str]:
        completed = {task.task_id for task in session.tasks if task.status == TaskStatus.COMPLETED}
        running = {task.task_id for task in session.tasks if task.status == TaskStatus.RUNNING}
        ready = self.graph.ready(completed)
        return [task_id for task_id in ready if task_id not in running]

    def can_run(self, session: ExecutionSession, task_id: str) -> bool:
        return task_id in self.ready_tasks(session)
