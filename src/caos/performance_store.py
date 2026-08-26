"""SQLite persistence for execution outcomes and derived performance evidence."""

import sqlite3
from datetime import datetime, timezone

from .performance_evidence import ExecutionOutcome, PerformanceEvidence, summarize_outcomes


class PerformanceStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS execution_outcomes (
                resource_id TEXT NOT NULL,
                success INTEGER NOT NULL,
                verification_passed INTEGER NOT NULL,
                cost REAL NOT NULL,
                latency_seconds REAL NOT NULL,
                retries INTEGER NOT NULL,
                observed_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def record(self, outcome: ExecutionOutcome) -> None:
        self.connection.execute(
            """INSERT INTO execution_outcomes
            (resource_id, success, verification_passed, cost, latency_seconds, retries, observed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (outcome.resource_id, int(outcome.success), int(outcome.verification_passed),
             outcome.cost, outcome.latency_seconds, outcome.retries,
             datetime.now(timezone.utc).isoformat()),
        )
        self.connection.commit()

    def evidence(self) -> dict[str, PerformanceEvidence]:
        rows = self.connection.execute(
            "SELECT resource_id, success, verification_passed, cost, latency_seconds, retries FROM execution_outcomes"
        ).fetchall()
        outcomes = [ExecutionOutcome(r[0], bool(r[1]), bool(r[2]), r[3], r[4], r[5]) for r in rows]
        return summarize_outcomes(outcomes)
