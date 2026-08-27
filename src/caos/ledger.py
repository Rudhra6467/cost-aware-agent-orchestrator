"""Shared resource quota accounting for CAOS planning."""

from dataclasses import dataclass


@dataclass(frozen=True)
class QuotaSnapshot:
    resource_id: str
    free_units: float
    consumed_units: float = 0.0
    reserved_units: float = 0.0

    @property
    def remaining_units(self) -> float:
        return max(0.0, self.free_units - self.consumed_units - self.reserved_units)


class UsageLedger:
    def __init__(self, snapshots: tuple[QuotaSnapshot, ...] = ()) -> None:
        self._snapshots = {x.resource_id: x for x in snapshots}

    def snapshot(self, resource_id: str) -> QuotaSnapshot:
        return self._snapshots.get(resource_id, QuotaSnapshot(resource_id, 0.0))

    def reserve(self, resource_id: str, units: float) -> QuotaSnapshot:
        if units < 0:
            raise ValueError("Reservation cannot be negative")
        current = self.snapshot(resource_id)
        if units > current.remaining_units:
            raise ValueError(f"Insufficient free quota for {resource_id}: requested={units}, remaining={current.remaining_units}")
        updated = QuotaSnapshot(current.resource_id, current.free_units, current.consumed_units, current.reserved_units + units)
        self._snapshots[resource_id] = updated
        return updated

    def consume(self, resource_id: str, units: float) -> QuotaSnapshot:
        if units < 0:
            raise ValueError("Consumption cannot be negative")
        current = self.snapshot(resource_id)
        updated = QuotaSnapshot(current.resource_id, current.free_units, current.consumed_units + units, current.reserved_units)
        self._snapshots[resource_id] = updated
        return updated

    def remaining(self, resource_id: str) -> float:
        return self.snapshot(resource_id).remaining_units
