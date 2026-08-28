"""Structured context snapshots for agent handoff and recovery."""

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class HandoffState:
    """Portable project state that another agent can consume."""

    project_id: str
    objective: str
    completed_tasks: tuple[str, ...] = ()
    pending_tasks: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()
    files_changed: tuple[str, ...] = ()
    known_errors: tuple[str, ...] = ()
    current_output: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    changed_files: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.changed_files and not self.files_changed:
            object.__setattr__(self, "files_changed", self.changed_files)
        elif self.files_changed and not self.changed_files:
            object.__setattr__(self, "changed_files", self.files_changed)

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)

    @classmethod
    def from_json(cls, value: str) -> "HandoffState":
        data = json.loads(value)
        files = tuple(data.get("files_changed", data.get("changed_files", ())))
        return cls(
            project_id=data["project_id"], objective=data["objective"],
            completed_tasks=tuple(data.get("completed_tasks", ())),
            pending_tasks=tuple(data.get("pending_tasks", ())),
            decisions=tuple(data.get("decisions", ())), files_changed=files,
            known_errors=tuple(data.get("known_errors", ())),
            current_output=data.get("current_output", ""),
            metadata=dict(data.get("metadata", {})), changed_files=files,
        )

    def compact_prompt(self) -> str:
        return (
            f"PROJECT: {self.project_id}\nOBJECTIVE: {self.objective}\n"
            f"COMPLETED: {', '.join(self.completed_tasks) or 'none'}\n"
            f"PENDING: {', '.join(self.pending_tasks) or 'none'}\n"
            f"DECISIONS: {'; '.join(self.decisions) or 'none'}\n"
            f"FILES: {', '.join(self.files_changed) or 'none'}\n"
            f"ERRORS: {'; '.join(self.known_errors) or 'none'}\n"
            f"LAST OUTPUT:\n{self.current_output}"
        )
