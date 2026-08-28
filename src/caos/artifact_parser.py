"""Parse a conservative file-oriented response from a coding agent."""

from __future__ import annotations

import re

from .project_workspace import WorkspaceFile


_FILE_RE = re.compile(
    r"(?:^|\n)FILE:\s*([^\n]+)\n```[^\n]*\n(.*?)\n```(?:\n|$)",
    re.DOTALL,
)


def parse_file_artifacts(output: str) -> list[WorkspaceFile]:
    """Extract explicit FILE artifacts and reject unsafe paths."""
    if not output:
        return []
    files: list[WorkspaceFile] = []
    for match in _FILE_RE.finditer(output):
        path = match.group(1).strip()
        content = match.group(2)
        parts = path.replace("\\", "/").split("/")
        if path and not path.startswith(("/", "\\")) and ".." not in parts:
            files.append(WorkspaceFile(path=path, content=content))
    return files
