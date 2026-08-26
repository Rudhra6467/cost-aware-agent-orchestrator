"""End-to-end orchestration for a controlled benchmark run."""

from dataclasses import dataclass
from typing import Callable

from .benchmark_manifest import BenchmarkManifest, ManifestVerificationReport, verify_manifest
from .benchmark_runner import BenchmarkTask, ExecutionMeasurement
from .benchmark_workspace import BenchmarkWorkspaceManager, Workspace


@dataclass(frozen=True)
class HarnessRun:
    run_id: str
    workspace: Workspace
    measurements: tuple[ExecutionMeasurement, ...]
    verification: ManifestVerificationReport

    @property
    def passed(self) -> bool:
        return self.verification.passed and all(item.success for item in self.measurements)


def execute_harness(
    run_id: str,
    tasks: list[BenchmarkTask],
    manifest: BenchmarkManifest,
    executor: Callable[[BenchmarkTask, Workspace], ExecutionMeasurement],
    workspace_manager: BenchmarkWorkspaceManager,
) -> HarnessRun:
    """Create a clean workspace, execute all frozen tasks, then verify the result."""
    if not tasks:
        raise ValueError("Harness requires at least one task")

    workspace = workspace_manager.reset(run_id)
    measurements = tuple(executor(task, workspace) for task in tasks)
    verification = verify_manifest(workspace.path, manifest)
    return HarnessRun(run_id, workspace, measurements, verification)
