"""Artifact and command acceptance manifest for Benchmark 001."""

from dataclasses import dataclass
from pathlib import Path

from .verification import VerificationResult, run_verification


@dataclass(frozen=True)
class ArtifactExpectation:
    path: str
    required: bool = True


@dataclass(frozen=True)
class BenchmarkManifest:
    artifacts: tuple[ArtifactExpectation, ...]
    verification_commands: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class ManifestVerificationReport:
    artifacts_present: bool
    missing_artifacts: tuple[str, ...]
    command_results: tuple[VerificationResult, ...]

    @property
    def passed(self) -> bool:
        return self.artifacts_present and all(result.passed for result in self.command_results)


def verify_manifest(workspace: str | Path, manifest: BenchmarkManifest) -> ManifestVerificationReport:
    root = Path(workspace).resolve()
    missing: list[str] = []
    for expectation in manifest.artifacts:
        if not expectation.required:
            continue
        candidate = (root / expectation.path).resolve()
        if root not in candidate.parents and candidate != root:
            raise ValueError(f"artifact path escapes workspace: {expectation.path}")
        if not candidate.exists() or not candidate.is_file():
            missing.append(expectation.path)

    results = tuple(run_verification(root, list(command)) for command in manifest.verification_commands)
    return ManifestVerificationReport(not missing, tuple(missing), results)
