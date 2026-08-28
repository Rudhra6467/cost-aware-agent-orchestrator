"""Application-facing controlled build contract.

The API plans first, requires an explicit BUILD decision, and delegates
execution to the existing bounded ControlledBuilder.
"""

from __future__ import annotations

from typing import Any, Callable

from .builder import ControlledBuilder
from .cost_optimizer import CostPolicy
from .planning_api import plan_from_request


def build_from_request(
    payload: dict[str, Any],
    pipeline_factory: Callable[[], Any],
    builder_factory: Callable[[Any], ControlledBuilder],
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be an object")

    if payload.get("decision", "BUILD") != "BUILD":
        raise ValueError("Build requires an explicit BUILD decision")

    pipeline = pipeline_factory()
    plan = plan_from_request(payload, pipeline)
    policy_data = payload.get("policy") or {}
    if not isinstance(policy_data, dict):
        raise ValueError("policy must be an object")
    policy = CostPolicy(
        budget_remaining=policy_data.get("budget_remaining"),
        minimum_capability=float(policy_data.get("minimum_capability", 0.0)),
        prefer_free=bool(policy_data.get("prefer_free", True)),
    )
    planned = pipeline.create_plan(payload["idea"].strip(), policy)
    if not planned.tasks:
        raise ValueError("No build tasks were produced")

    builder = builder_factory(pipeline)
    verification = payload.get(
        "verification_command", ["python", "-m", "compileall", "."]
    )
    if not isinstance(verification, list) or not all(isinstance(x, str) for x in verification):
        raise ValueError("verification_command must be a list of strings")

    results = []
    for item in planned.tasks:
        result = builder.build(item.task, verification_command=list(verification))
        results.append(result)
        if not result.passed:
            break

    return {
        "idea": plan["idea"],
        "status": "succeeded" if all(r.passed for r in results) else "failed",
        "tasks_attempted": len(results),
        "results": [
            {
                "passed": result.passed,
                "attempts": [
                    {
                        "attempt": attempt.attempt,
                        "files_written": attempt.files_written,
                        "verification_passed": attempt.verification.passed,
                        "diagnosis": attempt.diagnosis.summary if attempt.diagnosis else None,
                    }
                    for attempt in result.attempts
                ],
            }
            for result in results
        ],
    }
