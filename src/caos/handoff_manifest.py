"""Versioned handoff manifests for switching execution resources."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from .handoff import HandoffState


@dataclass(frozen=True)
class HandoffManifest:
    schema_version: str
    reason: str
    source_agent: str
    target_capability: str
    state: HandoffState
    integrity_sha256: str

    @classmethod
    def create(
        cls,
        state: HandoffState,
        *,
        reason: str,
        source_agent: str,
        target_capability: str,
    ) -> "HandoffManifest":
        canonical = state.to_json().encode("utf-8")
        digest = hashlib.sha256(canonical).hexdigest()
        return cls("1.0", reason, source_agent, target_capability, state, digest)

    def to_json(self) -> str:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "reason": self.reason,
            "source_agent": self.source_agent,
            "target_capability": self.target_capability,
            "state": json.loads(self.state.to_json()),
            "integrity_sha256": self.integrity_sha256,
        }
        return json.dumps(payload, sort_keys=True)

    @classmethod
    def from_json(cls, value: str) -> "HandoffManifest":
        payload = json.loads(value)
        state = HandoffState.from_json(json.dumps(payload["state"], sort_keys=True))
        manifest = cls(
            payload["schema_version"],
            payload["reason"],
            payload["source_agent"],
            payload["target_capability"],
            state,
            payload["integrity_sha256"],
        )
        expected = hashlib.sha256(state.to_json().encode("utf-8")).hexdigest()
        if expected != manifest.integrity_sha256:
            raise ValueError("handoff state integrity check failed")
        return manifest


def write_manifest(path: str, manifest: HandoffManifest) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(manifest.to_json())


def read_manifest(path: str) -> HandoffManifest:
    with open(path, "r", encoding="utf-8") as handle:
        return HandoffManifest.from_json(handle.read())
