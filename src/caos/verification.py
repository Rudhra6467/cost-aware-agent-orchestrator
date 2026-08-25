"""Verification primitives for generated projects."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    command: tuple[str, ...]
    return_code: int
    stdout: str
    stderr: str


def run_verification(
    workspace: str | Path,
    command: list[str],
    timeout_seconds: int = 120,
) -> VerificationResult:
    """Run an explicit verification command inside the generated workspace."""
    try:
        completed = subprocess.run(
            command,
            cwd=Path(workspace),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return VerificationResult(
            passed=completed.returncode == 0,
            command=tuple(command),
            return_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
    except subprocess.TimeoutExpired as exc:
        return VerificationResult(
            passed=False,
            command=tuple(command),
            return_code=-1,
            stdout=exc.stdout or "",
            stderr=f"Verification timed out after {timeout_seconds}s",
        )
