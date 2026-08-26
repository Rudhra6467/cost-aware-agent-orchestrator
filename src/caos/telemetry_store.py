"""SQLite persistence for CAOS execution telemetry."""

from __future__ import annotations

import sqlite3
from .telemetry import ExecutionTelemetry


class TelemetryStore:
    def __init__(self, database_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(database_path)
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS execution_telemetry (
                run_id TEXT NOT NULL, task_id TEXT NOT NULL, agent_id TEXT NOT NULL,
                estimated_cost REAL NOT NULL, actual_cost REAL NOT NULL,
                input_tokens INTEGER NOT NULL, output_tokens INTEGER NOT NULL,
                latency_ms INTEGER NOT NULL, retries INTEGER NOT NULL,
                handoffs INTEGER NOT NULL, verification_passed INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )"""
        )
        self.connection.commit()

    def record(self, item: ExecutionTelemetry) -> None:
        self.connection.execute(
            "INSERT INTO execution_telemetry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (item.run_id, item.task_id, item.agent_id, item.estimated_cost,
             item.actual_cost, item.input_tokens, item.output_tokens, item.latency_ms,
             item.retries, item.handoffs, int(item.verification_passed), item.timestamp),
        )
        self.connection.commit()

    def summary(self) -> dict[str, float | int]:
        row = self.connection.execute(
            "SELECT COUNT(*), COALESCE(SUM(actual_cost),0), COALESCE(SUM(input_tokens),0), "
            "COALESCE(SUM(output_tokens),0), COALESCE(AVG(latency_ms),0), "
            "COALESCE(SUM(retries),0), COALESCE(SUM(handoffs),0) FROM execution_telemetry"
        ).fetchone()
        return {
            "executions": row[0], "actual_cost": row[1], "input_tokens": row[2],
            "output_tokens": row[3], "average_latency_ms": row[4],
            "retries": row[5], "handoffs": row[6],
        }
