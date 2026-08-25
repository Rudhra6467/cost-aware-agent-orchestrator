"""Minimal SQLite state store for CAOS orchestration telemetry."""

import sqlite3
from pathlib import Path
from typing import Any


class StateStore:
    """Persist tasks and execution records independently of Git artifacts."""

    def __init__(self, path: str | Path = "state/caos.db") -> None:
        self.path = str(path)
        self._memory_connection: sqlite3.Connection | None = None
        if self.path == ":memory:":
            self._memory_connection = sqlite3.connect(":memory:")
            self._memory_connection.row_factory = sqlite3.Row
        else:
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        if self._memory_connection is not None:
            return self._memory_connection
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        db = self._connect()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                status TEXT NOT NULL,
                input_tokens INTEGER NOT NULL DEFAULT 0,
                output_tokens INTEGER NOT NULL DEFAULT 0,
                cost_usd REAL NOT NULL DEFAULT 0,
                error TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        db.commit()
        if self._memory_connection is None:
            db.close()

    def _run(self, query: str, params: tuple[Any, ...] = ()) -> None:
        db = self._connect()
        db.execute(query, params)
        db.commit()
        if self._memory_connection is None:
            db.close()

    def record_task(self, task_id: str, description: str, status: str = "pending") -> None:
        self._run(
            "INSERT OR REPLACE INTO tasks(task_id, description, status) VALUES (?, ?, ?)",
            (task_id, description, status),
        )

    def record_execution(self, **execution: Any) -> None:
        self._run(
            """INSERT INTO executions
            (task_id, agent_id, status, input_tokens, output_tokens, cost_usd, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                execution["task_id"],
                execution["agent_id"],
                execution["status"],
                execution.get("input_tokens", 0),
                execution.get("output_tokens", 0),
                execution.get("cost_usd", 0.0),
                execution.get("error"),
            ),
        )

    def execution_count(self) -> int:
        db = self._connect()
        count = int(db.execute("SELECT COUNT(*) FROM executions").fetchone()[0])
        if self._memory_connection is None:
            db.close()
        return count
