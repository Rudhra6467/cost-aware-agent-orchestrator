"""Parse a conservative file-oriented response from a coding agent."""

from __future__ import annotations

import re

from .project_workspace import WorkspaceFile


_FILE_RE = re.compile(r"(?:^|\n)FILE:\s*([^\n]+)\n```[^\n]*\n(.*?)\n```", re.DOTALL)


def parse_file_artifacts(output: str) -> list[WorkspaceFile]:
    """Extract FILE: path fenced-block artifacts from model output.

    The format is deliberately explicit so arbitrary prose cannot silently
    become a filesystem operation.
    """
    files: list[WorkspaceFile] = []
    for match in _FILE_RE.finditer(output):
        path = match.group(1).strip()
        content = match.group(2)
        if path and not path.startswith("/") and ".." not in path.split("/"):
            files.append(WorkspaceFile(path=path, content=content))
    return files
