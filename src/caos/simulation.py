"""Dependency-aware execution simulation for CAOS."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimTask:
    task_id: str
    duration_minutes: float
    dependencies: tuple[str, ...] = ()
    handoff_minutes: float = 0.0

    def __post_init__(self) -> None:
        if self.duration_minutes <= 0 or self.handoff_minutes < 0:
            raise ValueError("Task duration must be positive and handoff time non-negative")


@dataclass(frozen=True)
class TaskSchedule:
    task_id: str
    start_minute: float
    finish_minute: float
    dependency_finish: float


@dataclass(frozen=True)
class SimulationResult:
    schedule: tuple[TaskSchedule, ...]
    critical_path: tuple[str, ...]
    elapsed_minutes: float
    blocked_tasks: tuple[str, ...]


class ExecutionSimulator:
    """Deterministic earliest-start scheduler for a validated DAG."""

    def simulate(self, tasks: tuple[SimTask, ...]) -> SimulationResult:
        by_id = {task.task_id: task for task in tasks}
        if len(by_id) != len(tasks):
            raise ValueError("Task IDs must be unique")
        for task in tasks:
            missing = [d for d in task.dependencies if d not in by_id]
            if missing:
                raise ValueError(f"Missing dependencies for {task.task_id}: {missing}")

        self._validate_acyclic(by_id)
        schedules: dict[str, TaskSchedule] = {}
        for task in self._topological(by_id):
            dep_finish = max((schedules[d].finish_minute for d in task.dependencies), default=0.0)
            start = dep_finish
            finish = start + task.duration_minutes + task.handoff_minutes
            schedules[task.task_id] = TaskSchedule(task.task_id, start, finish, dep_finish)

        elapsed = max((x.finish_minute for x in schedules.values()), default=0.0)
        terminal = max(schedules, key=lambda k: schedules[k].finish_minute, default=None)
        path: list[str] = []
        while terminal is not None:
            path.append(terminal)
            deps = by_id[terminal].dependencies
            terminal = max(deps, key=lambda d: schedules[d].finish_minute) if deps else None
        path.reverse()
        return SimulationResult(tuple(schedules.values()), tuple(path), elapsed, ())

    def _topological(self, by_id: dict[str, SimTask]) -> list[SimTask]:
        remaining = dict(by_id)
        result: list[SimTask] = []
        while remaining:
            ready = [task for task in remaining.values() if all(d not in remaining for d in task.dependencies)]
            if not ready:
                raise ValueError("Task graph contains a cycle")
            for task in sorted(ready, key=lambda x: x.task_id):
                result.append(task)
                del remaining[task.task_id]
        return result

    def _validate_acyclic(self, by_id: dict[str, SimTask]) -> None:
        self._topological(by_id)
