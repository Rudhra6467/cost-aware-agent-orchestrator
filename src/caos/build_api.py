"""Application-facing controlled build contract.

The API plans first, requires an explicit BUILD decision, and then delegates
execution to the existing bounded ControlledBuilder. It never executes model-
returned shell commands directly.
"""

from __future__ import annotations

from typing import Any, Callable

from .builder import ControlledBuilder
from .planning_api import plan_from_request


def build_from_request(
    payload: dict[str, Any],
    pipeline_factory: Callable[[], Any],
    builder_factory: Callable[[Any], ControlledBuilder],
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be an object")

    decision = payload.get("decision", "BUILD")
    if decision != "BUILD":
        raise ValueError("Build requires an explicit BUILD decision")

    pipeline = pipeline_factory()
    plan = plan_from_request(payload, pipeline)
    builder = builder_factory(pipeline)

    tasks = pipeline.create_plan(
        payload["idea"].strip(),
        __import__("caos.cost_optimizer", fromlist=["CostPolicy"]).CostPolicy(
            budget_remaining=(payload.get("policy") or {}).get("budget_remaining"),
            minimum_capability=float((payload.get("policy") or {}).get("minimum_capability", 0.0)),
            prefer_free=bool((payload.get("policy") or {}).get("prefer_free", True)),
        ),
    ).tasks

    if not tasks:
        raise ValueError("No build tasks were produced")

    results = []
    for item in tasks:
        verification = payload.get("verification_command", ["python", "-m", "compileall", "."])
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
