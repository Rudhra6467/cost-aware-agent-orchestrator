"""Time-aware scheduling around quota reset and rate-limit windows."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class QuotaWindow:
    resource_id: str
    available_units: float
    reset_at: datetime | None = None
    cooldown_until: datetime | None = None

    def usable_at(self, now: datetime, units: float) -> datetime | None:
        if self.available_units >= units and (self.cooldown_until is None or now >= self.cooldown_until):
            return now
        candidates = [x for x in (self.reset_at, self.cooldown_until) if x is not None and x > now]
        return min(candidates) if candidates else None


@dataclass(frozen=True)
class ScheduledTask:
    task_id: str
    resource_id: str
    start_at: datetime
    finish_at: datetime
    waited_minutes: float


class QuotaScheduler:
    """Select the earliest feasible resource while preferring free capacity."""

    def schedule(self, task_id: str, units: float, duration_minutes: float, windows: tuple[QuotaWindow, ...], now: datetime | None = None) -> ScheduledTask:
        now = now or datetime.now(timezone.utc)
        choices = []
        for window in windows:
            start = window.usable_at(now, units)
            if start is not None:
                choices.append((start, -window.available_units, window.resource_id))
        if not choices:
            raise ValueError("No resource has a known feasible availability window")
        start, _, resource_id = min(choices)
        finish = start + timedelta(minutes=duration_minutes)
        waited = max(0.0, (start - now).total_seconds() / 60)
        return ScheduledTask(task_id, resource_id, start, finish, waited)
