"""Deterministic failure classification for the future repair loop."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FailureKind(str, Enum):
    TEST_FAILURE = "test_failure"
    DEPENDENCY_FAILURE = "dependency_failure"
    SYNTAX_ERROR = "syntax_error"
    TIMEOUT = "timeout"
    PROVIDER_RATE_LIMIT = "provider_rate_limit"
    PROVIDER_ERROR = "provider_error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FailureDiagnosis:
    kind: FailureKind
    retryable: bool
    handoff_recommended: bool
    summary: str


def classify_failure(stderr: str, return_code: int = 1) -> FailureDiagnosis:
    text = stderr.lower()
    if "429" in text or "rate limit" in text or "quota" in text:
        return FailureDiagnosis(FailureKind.PROVIDER_RATE_LIMIT, True, True, "Provider quota/rate limit detected.")
    if "timeout" in text or "timed out" in text:
        return FailureDiagnosis(FailureKind.TIMEOUT, True, False, "Verification exceeded the allowed time.")
    if "syntaxerror" in text:
        return FailureDiagnosis(FailureKind.SYNTAX_ERROR, True, False, "Generated code contains a syntax error.")
    if "modulenotfounderror" in text or "importerror" in text:
        return FailureDiagnosis(FailureKind.DEPENDENCY_FAILURE, True, False, "A dependency/import is unavailable.")
    if return_code != 0:
        return FailureDiagnosis(FailureKind.TEST_FAILURE, True, False, "The generated project failed verification.")
    return FailureDiagnosis(FailureKind.UNKNOWN, False, False, "Failure could not be classified.")
