from caos.constraints import UserConstraints
from caos.decision import Decision, DecisionReason
from caos.execution import ExecutionEstimate
from caos.planning_contract import build_planning_response
from caos.simulation import SimulationResult
from caos.variant_policy import VariantPolicy
from caos.variant_simulation import VariantEvaluation


def test_planning_response_exposes_build_and_diy_actions():
    evaluation = VariantEvaluation(
        VariantPolicy.ZERO_COST,
        SimulationResult((), ("a",), 30, ()),
        ExecutionEstimate(0, 0, 0, 30, 0),
        (),
        0,
    )
    decision = Decision("zero-cost", (DecisionReason.PRACTICAL_COST,), "Use free resources.", ("zero-cost",), ())
    response = build_planning_response(
        "Build a workout app", "Frontend + backend + database", (evaluation,), decision, UserConstraints()
    )
    assert response.recommendation == "zero-cost"
    assert response.next_actions == ("BUILD", "DIY")
    assert response.to_dict()["idea"] == "Build a workout app"
