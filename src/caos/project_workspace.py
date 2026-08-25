"""Safe project workspace for generated software artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkspaceFile:
    path: str
    content: str


class ProjectWorkspace:
    """Write model-produced files inside a controlled project directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def write_files(self, files: list[WorkspaceFile]) -> list[Path]:
        written: list[Path] = []
        for item in files:
            target = (self.root / item.path).resolve()
            if self.root != target and self.root not in target.parents:
                raise ValueError(f"Unsafe workspace path: {item.path}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(item.content, encoding="utf-8")
            written.append(target)
        return written

    def read_file(self, path: str) -> str:
        target = (self.root / path).resolve()
        if self.root != target and self.root not in target.parents:
            raise ValueError(f"Unsafe workspace path: {path}")
        return target.read_text(encoding="utf-8")
