"""Small application-facing planning contract built on the existing CAOS pipeline."""

from dataclasses import asdict
from typing import Any

from .cost_optimizer import CostPolicy
from .pipeline import CostAwarePipeline


def plan_from_request(
    payload: dict[str, Any],
    pipeline: CostAwarePipeline,
) -> dict[str, Any]:
    """Translate a user request into a stable, UI/API-friendly plan response."""
    if not isinstance(payload, dict):
        raise ValueError("Request body must be an object")

    idea = payload.get("idea")
    if not isinstance(idea, str) or not idea.strip():
        raise ValueError("idea must be a non-empty string")

    raw_policy = payload.get("policy") or {}
    if not isinstance(raw_policy, dict):
        raise ValueError("policy must be an object")

    policy = CostPolicy(
        budget_remaining=(
            None if raw_policy.get("budget_remaining") is None
            else float(raw_policy["budget_remaining"])
        ),
        minimum_capability=float(raw_policy.get("minimum_capability", 0.0)),
        prefer_free=bool(raw_policy.get("prefer_free", True)),
    )

    plan = pipeline.create_plan(idea.strip(), policy)
    return {
        "idea": idea.strip(),
        "understanding": plan.blueprint.summary,
        "blueprint": {
            "status": plan.blueprint.status.value,
            "summary": plan.blueprint.summary,
            "assumptions": list(plan.blueprint.assumptions),
            "layers": [
                {
                    "name": layer.name,
                    "purpose": layer.purpose,
                    "components": list(layer.components),
                }
                for layer in plan.blueprint.layers
            ],
        },
        "tasks": [
            {
                "task_id": item.task.task_id,
                "description": item.task.description,
                "required_capability": item.task.required_capability,
                "recommended": asdict(item.recommended),
                "alternatives": [asdict(option) for option in item.options[1:]],
            }
            for item in plan.tasks
        ],
        "recommendation": {
            "action": "BUILD",
            "title": plan.proposal.title,
            "resource": plan.proposal.selected_resource,
            "estimated_cost": plan.proposal.estimated_cost,
            "estimated_time_minutes": plan.proposal.estimated_time_minutes,
            "rationale": list(plan.proposal.rationale),
        },
        "diy": {"steps": list(plan.proposal.diy_steps)},
    }
