"""SQLite state store for CAOS orchestration telemetry, evidence and handoffs."""

import json
import sqlite3
from pathlib import Path
from typing import Any


class StateStore:
    """Persist orchestration state independently of Git software artifacts."""

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
                task_id TEXT PRIMARY KEY, description TEXT NOT NULL,
                status TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL,
                agent_id TEXT NOT NULL, status TEXT NOT NULL,
                input_tokens INTEGER NOT NULL DEFAULT 0, output_tokens INTEGER NOT NULL DEFAULT 0,
                cost_usd REAL NOT NULL DEFAULT 0, error TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS handoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT NOT NULL,
                from_agent_id TEXT NOT NULL, to_agent_id TEXT, state_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS resource_evidence (
                resource_id TEXT PRIMARY KEY, provider TEXT NOT NULL, resource_name TEXT NOT NULL,
                evidence_json TEXT NOT NULL, observed_at TEXT NOT NULL,
                confidence REAL NOT NULL
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
        self._run("INSERT OR REPLACE INTO tasks(task_id, description, status) VALUES (?, ?, ?)", (task_id, description, status))

    def record_execution(self, **execution: Any) -> None:
        self._run(
            "INSERT INTO executions(task_id, agent_id, status, input_tokens, output_tokens, cost_usd, error) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (execution["task_id"], execution["agent_id"], execution["status"], execution.get("input_tokens", 0), execution.get("output_tokens", 0), execution.get("cost_usd", 0.0), execution.get("error")),
        )

    def record_handoff(self, project_id: str, from_agent_id: str, state_json: str, to_agent_id: str | None = None) -> None:
        self._run("INSERT INTO handoffs(project_id, from_agent_id, to_agent_id, state_json) VALUES (?, ?, ?, ?)", (project_id, from_agent_id, to_agent_id, state_json))

    def record_resource_evidence(self, resource_id: str, provider: str, resource_name: str, evidence: dict[str, Any], observed_at: str, confidence: float) -> None:
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        self._run(
            "INSERT OR REPLACE INTO resource_evidence(resource_id, provider, resource_name, evidence_json, observed_at, confidence) VALUES (?, ?, ?, ?, ?, ?)",
            (resource_id, provider, resource_name, json.dumps(evidence, sort_keys=True), observed_at, confidence),
        )

    def get_resource_evidence(self, resource_id: str) -> dict[str, Any] | None:
        db = self._connect()
        row = db.execute("SELECT * FROM resource_evidence WHERE resource_id = ?", (resource_id,)).fetchone()
        if self._memory_connection is None:
            db.close()
        if row is None:
            return None
        return {"resource_id": row["resource_id"], "provider": row["provider"], "resource_name": row["resource_name"], "evidence": json.loads(row["evidence_json"]), "observed_at": row["observed_at"], "confidence": row["confidence"]}

    def execution_count(self) -> int:
        db = self._connect(); count = int(db.execute("SELECT COUNT(*) FROM executions").fetchone()[0])
        if self._memory_connection is None: db.close()
        return count

    def handoff_count(self) -> int:
        db = self._connect(); count = int(db.execute("SELECT COUNT(*) FROM handoffs").fetchone()[0])
        if self._memory_connection is None: db.close()
        return count
