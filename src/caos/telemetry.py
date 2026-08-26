"""Execution telemetry used to learn whether CAOS actually saves money."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json


@dataclass(frozen=True)
class ExecutionTelemetry:
    run_id: str
    task_id: str
    agent_id: str
    estimated_cost: float
    actual_cost: float
    input_tokens: int
    output_tokens: int
    latency_ms: int
    retries: int
    handoffs: int
    verification_passed: bool
    timestamp: str

    @classmethod
    def now(cls, **kwargs):
        return cls(timestamp=datetime.now(timezone.utc).isoformat(), **kwargs)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)
