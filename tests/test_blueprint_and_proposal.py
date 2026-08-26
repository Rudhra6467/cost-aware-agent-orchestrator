from caos.blueprint import BlueprintEngine, BlueprintStatus
from caos.cost_optimizer import CostOption
from caos.proposal import ProposalEngine


def test_blueprint_creates_reviewable_layers():
    blueprint = BlueprintEngine().analyze("Build an AI workout tracking app")
    assert blueprint.status == BlueprintStatus.DRAFT
    assert {layer.name for layer in blueprint.layers} >= {
        "Frontend", "Backend", "Database", "Infrastructure"
    }
    assert "AI/model service" in blueprint.layers[-1].components


def test_approval_requires_questions_to_be_resolved():
    engine = BlueprintEngine()
    blueprint = engine.analyze("Build app")
    approved = engine.apply_user_decision(blueprint, "approve")
    assert approved.status == BlueprintStatus.NEEDS_CLARIFICATION


def test_proposal_contains_build_and_diy_paths():
    blueprint = BlueprintEngine().analyze("Build an expense tracker")
    selected = CostOption(
        agent_id="free",
        agent_name="Free Agent",
        estimated_cost=0.0,
        capability=8.0,
        reliability=0.9,
        availability=0.9,
        is_free=True,
        rationale="free",
    )
    proposal = ProposalEngine().create(blueprint, selected)
    assert proposal.estimated_cost == 0.0
    assert proposal.recommendation == "Let CAOS Build It"
    assert proposal.diy_steps
