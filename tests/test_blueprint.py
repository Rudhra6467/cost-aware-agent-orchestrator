import pytest

from caos.blueprint import BlueprintEngine, BlueprintStatus


def test_blueprint_engine_decomposes_product_into_user_facing_layers():
    blueprint = BlueprintEngine().analyze("Build a workout app that recommends meals with AI")
    assert blueprint.raw_idea.startswith("Build a workout")
    assert [layer.name for layer in blueprint.layers] == ["Frontend", "Backend", "Database", "Infrastructure", "External Resources"]
    assert "AI/model service" in blueprint.layers[-1].components


def test_short_idea_requires_clarification_before_cost_planning():
    blueprint = BlueprintEngine().analyze("build an app")
    assert blueprint.open_questions
    result = BlueprintEngine().apply_user_decision(blueprint, "approve")
    assert result.status == BlueprintStatus.NEEDS_CLARIFICATION
    assert not result.ready_for_cost_planning


def test_complete_blueprint_can_be_approved():
    blueprint = BlueprintEngine().analyze("Build a customer support portal with tickets, accounts, search and email notifications")
    result = BlueprintEngine().apply_user_decision(blueprint, "1")
    assert result.status == BlueprintStatus.APPROVED
    assert result.ready_for_cost_planning


def test_empty_idea_is_rejected():
    with pytest.raises(ValueError):
        BlueprintEngine().analyze("   ")
