"""First-class execution audit trail for CAOS."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ExecutionEvent:
    session_id: str
    event_type: str
    task_id: str | None = None
    agent_name: str | None = None
    cost: float | None = None
    result: str | None = None
    evidence: tuple[str, ...] = ()
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AuditTrail:
    """Append-only in-memory event store for execution decisions and outcomes."""

    def __init__(self) -> None:
        self._events: dict[str, list[ExecutionEvent]] = {}

    def record(self, event: ExecutionEvent) -> ExecutionEvent:
        self._events.setdefault(event.session_id, []).append(event)
        return event

    def for_session(self, session_id: str) -> tuple[ExecutionEvent, ...]:
        return tuple(self._events.get(session_id, ()))

    def for_task(self, session_id: str, task_id: str) -> tuple[ExecutionEvent, ...]:
        return tuple(event for event in self.for_session(session_id) if event.task_id == task_id)

    def to_dict(self, session_id: str) -> list[dict[str, Any]]:
        return [event.to_dict() for event in self.for_session(session_id)]
