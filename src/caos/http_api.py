"""Framework-neutral HTTP API adapter for the CAOS planning service.

A thin adapter keeps transport concerns out of the domain engines. A web framework
can map its POST handler to ``post_plan`` and serialize the returned dictionary.
"""

from dataclasses import asdict
from typing import Any

from .planning_service import PlanningService


class PlanningAPI:
    """Minimal API contract for ``POST /api/v1/plan``."""

    def __init__(self, service: PlanningService) -> None:
        self.service = service

    def post_plan(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        try:
            request = self.service.request_from_dict(payload)
            response = self.service.create_plan(request)
            if hasattr(response, "to_dict"):
                body = response.to_dict()
            elif hasattr(response, "__dataclass_fields__"):
                body = asdict(response)
            else:
                body = response
            return 200, body
        except ValueError as exc:
            return 400, {"error": "invalid_request", "message": str(exc)}
        except Exception as exc:
            return 500, {"error": "planning_failed", "message": str(exc)}
