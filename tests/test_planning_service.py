import pytest

from caos.constraints import UserConstraints
from caos.planning_service import PlanningRequest, PlanningService


class Analyzer:
    def analyze(self, idea):
        return (idea,)


class Planner:
    def plan(self, blueprint, constraints):
        return {"idea": blueprint[0], "budget": constraints.budget}


def test_service_validates_idea_and_delegates():
    service = PlanningService(Analyzer(), Planner())
    result = service.create_plan(PlanningRequest("build an app", UserConstraints(budget=5)))
    assert result == {"idea": "build an app", "budget": 5}


def test_service_rejects_empty_idea():
    with pytest.raises(ValueError):
        PlanningService(Analyzer(), Planner()).create_plan(PlanningRequest("   "))


def test_request_from_dict_parses_constraints():
    request = PlanningService.request_from_dict({"idea": "x", "constraints": {"budget": 2, "quality_threshold": .8}})
    assert request.idea == "x"
    assert request.constraints.budget == 2
    assert request.constraints.quality_threshold == .8
