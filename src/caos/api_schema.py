"""Validation and normalization for the public planning API contract."""

from typing import Any


SUPPORTED_ACTIONS = {"BUILD", "DIY"}


def validate_plan_request(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Request body must be an object")
    idea = payload.get("idea")
    if not isinstance(idea, str) or not idea.strip():
        raise ValueError("idea must be a non-empty string")
    constraints = payload.get("constraints", {})
    if not isinstance(constraints, dict):
        raise ValueError("constraints must be an object")
    budget = constraints.get("budget")
    if budget is not None and (not isinstance(budget, (int, float)) or isinstance(budget, bool) or budget < 0):
        raise ValueError("budget must be a non-negative number")
    quality = constraints.get("quality_threshold")
    if quality is not None and (not isinstance(quality, (int, float)) or isinstance(quality, bool) or not 0 <= quality <= 1):
        raise ValueError("quality_threshold must be between 0 and 1")
    max_days = constraints.get("max_build_days")
    if max_days is not None and (not isinstance(max_days, (int, float)) or isinstance(max_days, bool) or max_days <= 0):
        raise ValueError("max_build_days must be greater than 0")
    return {"idea": idea.strip(), "constraints": dict(constraints)}


def validate_plan_response(body: dict[str, Any]) -> None:
    required = {"idea", "blueprint_summary", "assumptions", "plans", "recommendation", "reasons", "explanation", "next_actions"}
    missing = required - set(body)
    if missing:
        raise ValueError(f"planning response missing fields: {sorted(missing)}")
    if not isinstance(body["plans"], list):
        raise ValueError("plans must be a list")
    if not set(body["next_actions"]).issubset(SUPPORTED_ACTIONS):
        raise ValueError("next_actions contains unsupported action")
