"""Project-level quota forecasting for a planned task sequence."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .quota import QuotaState


@dataclass(frozen=True)
class QuotaProjection:
    resource_id: str
    planned_units: int
    remaining_before: int | None
    remaining_after: int | None
    exhausted: bool
    reset_in_seconds: float | None


def forecast_quota(
    quota: QuotaState,
    planned_units: int,
    now: datetime | None = None,
) -> QuotaProjection:
    if planned_units < 0:
        raise ValueError("planned_units cannot be negative")
    remaining = quota.remaining
    after = None if remaining is None else max(0, remaining - planned_units)
    exhausted = False if remaining is None else planned_units > remaining
    return QuotaProjection(
        resource_id=quota.resource_id,
        planned_units=planned_units,
        remaining_before=remaining,
        remaining_after=after,
        exhausted=exhausted,
        reset_in_seconds=quota.reset_in_seconds(now or datetime.now(timezone.utc)),
    )


def forecast_plan_usage(
    usage_by_resource: dict[str, int],
    quotas: dict[str, QuotaState],
    now: datetime | None = None,
) -> list[QuotaProjection]:
    return [
        forecast_quota(quotas[resource_id], units, now)
        for resource_id, units in usage_by_resource.items()
        if resource_id in quotas
    ]
