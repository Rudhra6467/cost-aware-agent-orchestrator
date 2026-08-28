import pytest

from caos.build_service import BuildRequest, BuildService
from caos.planning_contract import PlanSummary, PlanningResponse


def response():
    plan = PlanSummary("zero-cost", "Zero-Cost", 0.0, 30.0, 0.0, ("build",))
    return PlanningResponse(
        idea="build a landing page",
        blueprint_summary="landing page",
        assumptions=(),
        plans=(plan,),
        recommendation="zero-cost",
        reasons=(),
        explanation="fits constraints",
        next_actions=("BUILD", "DIY"),
    )


def test_create_session_from_selected_plan():
    result = response()
    session = BuildService().create_session(result, BuildRequest(result.idea, "zero-cost"))

    assert session.plan_id == "zero-cost"
    assert session.idea == result.idea
    assert session.status.value == "ready"
    assert len(session.tasks) == 4
    assert session.tasks[0].description.startswith("Understand")
    assert session.tasks[-1].description.startswith("Run verification")


def test_unknown_plan_is_rejected():
    result = response()
    with pytest.raises(ValueError, match="Unknown plan"):
        BuildService().create_session(result, BuildRequest(result.idea, "missing"))


def test_mismatched_idea_is_rejected():
    result = response()
    with pytest.raises(ValueError, match="idea must match"):
        BuildService().create_session(result, BuildRequest("different", "zero-cost"))
