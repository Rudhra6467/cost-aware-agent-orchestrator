"""Provider-neutral verification primitives for CAOS execution artifacts."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .execution_session import ExecutionSession, ExecutionStatus


@dataclass(frozen=True)
class VerificationCheck:
    name: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    checks: tuple[VerificationCheck, ...]
    evidence: tuple[str, ...] = ()


Check = Callable[[Path], VerificationCheck]


class ArtifactVerifier:
    """Runs bounded checks against artifacts produced by an execution session."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace).resolve()

    def verify(self, session: ExecutionSession, checks: list[Check]) -> VerificationResult:
        if session.status != ExecutionStatus.VERIFYING:
            raise ValueError("Session must be in verifying state")

        results: list[VerificationCheck] = []
        for check in checks:
            results.append(check(self.workspace))

        passed = bool(results) and all(check.passed for check in results)
        evidence = tuple(check.evidence for check in results if check.evidence)
        if passed:
            session.status = ExecutionStatus.COMPLETED
        else:
            session.status = ExecutionStatus.REPAIRING
            session.error = "Verification failed"
        return VerificationResult(passed, tuple(results), evidence)


def artifact_exists(filename: str) -> Check:
    def check(workspace: Path) -> VerificationCheck:
        path = (workspace / filename).resolve()
        try:
            path.relative_to(workspace)
        except ValueError:
            return VerificationCheck("artifact_exists", False, "artifact path escapes workspace")
        exists = path.is_file()
        return VerificationCheck("artifact_exists", exists, str(path) if exists else f"missing: {filename}")

    return check


def artifact_contains(filename: str, expected: str) -> Check:
    def check(workspace: Path) -> VerificationCheck:
        path = (workspace / filename).resolve()
        try:
            path.relative_to(workspace)
        except ValueError:
            return VerificationCheck("artifact_contains", False, "artifact path escapes workspace")
        if not path.is_file():
            return VerificationCheck("artifact_contains", False, f"missing: {filename}")
        content = path.read_text(encoding="utf-8")
        passed = expected in content
        return VerificationCheck("artifact_contains", passed, f"found expected content in {filename}" if passed else f"missing expected content in {filename}")

    return check
