import pytest

from caos.constraints import Autonomy
from caos.planning_service import PlanningService


def test_request_parses_all_user_controls():
    request = PlanningService.request_from_dict({
        "idea": "fitness app",
        "constraints": {
            "budget": 4,
            "quality_threshold": 0.85,
            "max_build_days": 3,
            "autonomy": "diy",
            "prefer_free": False,
        },
    })
    assert request.constraints.budget == 4
    assert request.constraints.quality_threshold == 0.85
    assert request.constraints.max_build_days == 3
    assert request.constraints.autonomy is Autonomy.DIY
    assert request.constraints.prefer_free is False


def test_invalid_autonomy_is_rejected():
    with pytest.raises(ValueError, match="Invalid constraints"):
        PlanningService.request_from_dict({"idea": "x", "constraints": {"autonomy": "unsafe"}})
