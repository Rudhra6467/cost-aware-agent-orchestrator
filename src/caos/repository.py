"""Provider-neutral repository artifact interface.

GitHub integration belongs behind this boundary so orchestration logic remains
independent from a specific hosting provider.
"""

from abc import ABC, abstractmethod


class RepositoryWriter(ABC):
    @abstractmethod
    def write_file(self, path: str, content: str, message: str) -> str:
        """Persist a single project artifact and return a revision identifier."""
        raise NotImplementedError


class LocalRepositoryWriter(RepositoryWriter):
    """Repository writer for a local workspace; useful before Git integration."""

    def __init__(self, root: str):
        from .project_workspace import ProjectWorkspace

        self.workspace = ProjectWorkspace(root)

    def write_file(self, path: str, content: str, message: str) -> str:
        self.workspace.write_files([
            __import__("caos.project_workspace", fromlist=["WorkspaceFile"]).WorkspaceFile(path, content)
        ])
        return message
