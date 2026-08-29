"""SQLite persistence for plans and BUILD records. Survives process restart."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class ProductStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS plans (
                    idea TEXT PRIMARY KEY,
                    body TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS builds (
                    session_id TEXT PRIMARY KEY,
                    idea TEXT NOT NULL,
                    body TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def save_plan(self, idea: str, body: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO plans(idea, body) VALUES (?, ?)",
                (idea.strip(), json.dumps(body)),
            )

    def load_plan(self, idea: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute("SELECT body FROM plans WHERE idea = ?", (idea.strip(),)).fetchone()
        return json.loads(row[0]) if row else None

    def save_build(self, session_id: str, idea: str, body: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO builds(session_id, idea, body) VALUES (?, ?, ?)",
                (session_id, idea.strip(), json.dumps(body)),
            )

    def load_build(self, session_id: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute("SELECT body FROM builds WHERE session_id = ?", (session_id,)).fetchone()
        return json.loads(row[0]) if row else None
