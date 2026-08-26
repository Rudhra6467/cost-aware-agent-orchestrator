"""Controlled build loop: execute artifacts, verify, diagnose failures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .artifact_parser import parse_file_artifacts
from .agents import AgentExecutor
from .models import TaskStatus
from .project_workspace import ProjectWorkspace
from .repair import FailureDiagnosis, classify_failure
from .verification import VerificationResult, run_verification


@dataclass(frozen=True)
class BuildAttempt:
    attempt: int
    files_written: int
    verification: VerificationResult
    diagnosis: FailureDiagnosis | None


@dataclass(frozen=True)
class BuildResult:
    passed: bool
    attempts: tuple[BuildAttempt, ...]
    final_output: str


class ControlledBuilder:
    """Build generated artifacts with bounded verification attempts.

    The builder intentionally does not execute arbitrary commands returned by a
    model. Verification is supplied by the orchestration policy.
    """

    def __init__(self, executor: AgentExecutor, workspace: str | Path):
        self.executor = executor
        self.workspace = ProjectWorkspace(workspace)

    def build(self, task, verification_command: list[str], max_attempts: int = 2) -> BuildResult:
        attempts: list[BuildAttempt] = []
        prompt = task.description
        final_output = ""

        for attempt_number in range(1, max_attempts + 1):
            result = self.executor.execute(task, prompt)
            final_output = result.output
            if result.status == TaskStatus.FAILED:
                diagnosis = classify_failure(result.error or "provider failure")
                verification = VerificationResult(False, tuple(), 1, "", result.error or "provider failure")
                attempts.append(BuildAttempt(attempt_number, 0, verification, diagnosis))
                if not diagnosis.retryable:
                    break
                prompt = f"Repair the previous failure and return corrected files.\nFailure: {diagnosis.summary}\n{result.error or ''}"
                continue

            files = parse_file_artifacts(result.output)
            written = self.workspace.write_files(files)
            verification = run_verification(self.workspace.root, verification_command)
            diagnosis = None if verification.passed else classify_failure(verification.stderr, verification.return_code)
            attempts.append(BuildAttempt(attempt_number, len(written), verification, diagnosis))
            if verification.passed:
                return BuildResult(True, tuple(attempts), final_output)
            if not diagnosis or not diagnosis.retryable:
                break
            prompt = (
                "Repair the generated project. Return only corrected FILE artifacts.\n"
                f"Verification failure:\n{verification.stderr}\n{verification.stdout}"
            )

        return BuildResult(False, tuple(attempts), final_output)
