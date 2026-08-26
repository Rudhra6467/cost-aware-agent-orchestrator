"""Dependency-agnostic quota-aware scheduling primitives."""

from dataclasses import dataclass

from .quota import QuotaState


@dataclass(frozen=True)
class ScheduledTask:
    task_id: str
    resource_id: str
    units: int
    starts_after_seconds: float = 0.0


@dataclass(frozen=True)
class ScheduleResult:
    tasks: tuple[ScheduledTask, ...]
    unscheduled_task_ids: tuple[str, ...]
    total_wait_seconds: float


def schedule_sequentially(
    tasks: list[tuple[str, int, str]],
    quotas: dict[str, QuotaState],
) -> ScheduleResult:
    """Pack tasks into currently available quotas, waiting until reset when known.

    V1 assumes tasks are already dependency-ordered. It never bypasses quotas.
    Tasks with unknown quota are eligible because CAOS has no evidence that they
    are exhausted; provider-specific enforcement remains authoritative.
    """
    remaining = {key: value.remaining for key, value in quotas.items()}
    reset = {key: value.reset_in_seconds() for key, value in quotas.items()}
    scheduled: list[ScheduledTask] = []
    unscheduled: list[str] = []
    elapsed = 0.0

    for task_id, units, resource_id in tasks:
        if units < 0:
            raise ValueError("units cannot be negative")
        if resource_id not in quotas:
            unscheduled.append(task_id)
            continue
        available = remaining[resource_id]
        if available is None:
            scheduled.append(ScheduledTask(task_id, resource_id, units, elapsed))
            continue
        if available >= units:
            remaining[resource_id] = available - units
            scheduled.append(ScheduledTask(task_id, resource_id, units, elapsed))
            continue
        wait = reset[resource_id]
        if wait is not None and wait > 0 and quotas[resource_id].limit is not None:
            elapsed += wait
            remaining[resource_id] = quotas[resource_id].limit
            reset[resource_id] = None
            remaining[resource_id] -= units
            scheduled.append(ScheduledTask(task_id, resource_id, units, elapsed))
        else:
            unscheduled.append(task_id)

    return ScheduleResult(tuple(scheduled), tuple(unscheduled), elapsed)
