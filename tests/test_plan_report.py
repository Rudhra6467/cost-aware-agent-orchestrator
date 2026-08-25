from caos.models import AgentProfile
from caos.plan_report import create_build_plan


def test_build_plan_contains_build_and_diy_paths():
    agents = [
        AgentProfile(
            agent_id="free-architect",
            name="Free Architect",
            coding_score=6.0,
            architecture_score=8.0,
        ),
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            coding_score=8.0,
            architecture_score=6.0,
        ),
    ]

    report = create_build_plan("Build a small API", agents, budget=0.0)

    assert len(report.tasks) == 2
    assert len(report.recommended) == 2
    assert report.estimated_cost == 0.0
    assert any("tests" in step.lower() for step in report.diy_steps)
    assert report.to_dict()["request"] == "Build a small API"
