"""Safe workspace lifecycle and verification harness for Benchmark 001."""

from dataclasses import dataclass
from pathlib import Path
import shutil

from .verification import VerificationResult, run_verification


@dataclass(frozen=True)
class Workspace:
    path: Path


class BenchmarkWorkspaceManager:
    """Create isolated, disposable benchmark workspaces."""

    def __init__(self, root: str | Path = "artifacts/benchmarks") -> None:
        self.root = Path(root)

    def reset(self, run_id: str) -> Workspace:
        if not run_id or any(part in run_id for part in ("/", "\\", "..")):
            raise ValueError("run_id must be a simple workspace identifier")
        workspace = self.root / run_id
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir(parents=True, exist_ok=False)
        return Workspace(workspace)

    def verify(self, workspace: Workspace, command: list[str], timeout_seconds: int = 120) -> VerificationResult:
        return run_verification(workspace.path, command, timeout_seconds)

    def destroy(self, workspace: Workspace) -> None:
        if workspace.path.exists():
            resolved = workspace.path.resolve()
            root = self.root.resolve()
            if root not in resolved.parents:
                raise ValueError("refusing to destroy a workspace outside benchmark root")
            shutil.rmtree(resolved)
