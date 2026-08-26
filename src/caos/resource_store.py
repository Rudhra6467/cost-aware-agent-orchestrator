"""SQLite persistence for resource observations."""

import sqlite3
from dataclasses import asdict
from datetime import datetime

from .resource_discovery import ResourceObservation


class ResourceStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS resource_observations (
                resource_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                capabilities TEXT NOT NULL,
                source TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                free INTEGER NOT NULL,
                estimated_unit_cost REAL NOT NULL,
                confidence REAL NOT NULL,
                available INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def save(self, observation: ResourceObservation) -> None:
        self.connection.execute(
            """INSERT INTO resource_observations
            (resource_id, provider, capabilities, source, observed_at, free,
             estimated_unit_cost, confidence, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (observation.resource_id, observation.provider,
             ",".join(sorted(observation.capabilities)), observation.source,
             observation.observed_at.isoformat(), int(observation.free),
             observation.estimated_unit_cost, observation.confidence,
             int(observation.available)),
        )
        self.connection.commit()

    def load_recent(self, max_age_seconds: float = 86_400) -> list[ResourceObservation]:
        rows = self.connection.execute(
            "SELECT resource_id, provider, capabilities, source, observed_at, free, estimated_unit_cost, confidence, available FROM resource_observations"
        ).fetchall()
        observations = []
        for row in rows:
            observation = ResourceObservation(
                resource_id=row[0], provider=row[1], capabilities=frozenset(filter(None, row[2].split(","))),
                source=row[3], observed_at=datetime.fromisoformat(row[4]), free=bool(row[5]),
                estimated_unit_cost=row[6], confidence=row[7], available=bool(row[8]),
            )
            if observation.age_seconds <= max_age_seconds:
                observations.append(observation)
        return observations
