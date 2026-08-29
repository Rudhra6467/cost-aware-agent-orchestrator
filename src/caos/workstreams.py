"""Eight-session planning taxonomy. Checklist, not eight products."""

from __future__ import annotations

from dataclasses import asdict, dataclass


SESSIONS = (
    (1, "Product & architecture", "North Star and acceptance checks are written down"),
    (2, "Experience & content", "The primary user action can be demonstrated"),
    (3, "Data", "Records can be written and read back"),
    (4, "Backend", "One API path serves the North Star action"),
    (5, "Frontend", "The same action is usable in a browser"),
    (6, "Integration", "Frontend, API, and data agree on one contract"),
    (7, "Verification", "An automated check fails if the North Star action breaks"),
    (8, "Operate", "Runbook for host, secrets, and logs"),
)


@dataclass(frozen=True)
class WorkstreamLine:
    session_id: int
    session: str
    decision: str
    task: str
    resource: str
    tier: str
    estimated_cost: float
    option_b: str
    done_when: str

    def to_dict(self) -> dict:
        return asdict(self)


def is_notes_api(idea: str) -> bool:
    text = idea.lower()
    return any(token in text for token in ("note", "notes")) and any(
        token in text for token in ("api", "search", "store", "endpoint")
    )


def plan_workstreams(idea: str, prefer_free: bool = True) -> tuple[WorkstreamLine, ...]:
    """Keep only sessions the idea needs. Session 8 stays dropped in v0."""
    notes = is_notes_api(idea)
    local = ("local-deterministic", "local", 0.0, "assumed-free-llm")
    free = ("assumed-free-llm", "free-assumed", 0.0, "assumed-paid-llm ~$0.02")
    resource = local if prefer_free else free

    def line(session_id: int, decision: str, task: str, done_when: str, use=resource) -> WorkstreamLine:
        name = SESSIONS[session_id - 1][1]
        res, tier, cost, option = use
        if decision == "drop":
            res, tier, cost, option = ("—", "dropped", 0.0, "parked until slice 1 is green")
            task = task or "Not required for this idea"
        return WorkstreamLine(session_id, name, decision, task, res, tier, cost, option, done_when)

    if notes:
        return (
            line(1, "keep", "Write North Star: store a note, search it back", "Acceptance checks exist"),
            line(2, "drop", "No dashboard in v0", "Skipped"),
            line(3, "keep", "In-memory or SQLite note records", "POST writes a note"),
            line(4, "keep", "POST /notes and GET /notes/search", "Search returns stored text"),
            line(5, "drop", "No browser UI in v0", "Skipped"),
            line(6, "keep", "One JSON contract for create + search", "Contract matches tests"),
            line(7, "keep", "pytest: create a note, search finds it", "test_notes.py passes"),
            line(8, "drop", "No host, CDN, or IAM", "Parked"),
        )

    needs_data = any(token in idea.lower() for token in ("store", "save", "database", "db", "record"))
    needs_api = any(token in idea.lower() for token in ("api", "endpoint", "backend", "server"))
    needs_ui = any(token in idea.lower() for token in ("ui", "frontend", "dashboard", "page", "website"))
    return (
        line(1, "keep", "Write the outcome and the single automated check", "Acceptance checks exist"),
        line(2, "keep" if needs_ui else "drop", "Primary user flow", "Flow can be shown" if needs_ui else "Skipped"),
        line(3, "keep" if needs_data else "drop", "Define how records persist", "Read after write" if needs_data else "Skipped"),
        line(4, "keep" if needs_api else "drop", "Smallest backend path", "Endpoint works" if needs_api else "Skipped"),
        line(5, "keep" if needs_ui else "drop", "Smallest view of the action", "Action is usable" if needs_ui else "Skipped"),
        line(6, "keep" if (needs_api or needs_ui) else "drop", "Wire the pieces that exist", "Contract holds" if (needs_api or needs_ui) else "Skipped"),
        line(7, "keep", "One automated check for the North Star action", "Check passes"),
        line(8, "drop", "No production host in v0", "Parked"),
    )
