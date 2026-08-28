from caos.build_api import build_from_request
from caos.models import AgentProfile, AgentResult, TaskStatus
from caos.pipeline import CostAwarePipeline
from caos.builder import ControlledBuilder


class FakeExecutor:
    def execute(self, task, prompt):
        return AgentResult(
            task_id=task.task_id,
            agent_id="fake",
            status=TaskStatus.SUCCEEDED,
            output="```file: main.py\nprint('hello')\n```",
        )


def make_pipeline():
    return CostAwarePipeline([
        AgentProfile("free", "Free", coding_score=0.9, architecture_score=0.7),
    ])


def make_builder(pipeline):
    import tempfile
    return ControlledBuilder(FakeExecutor(), tempfile.mkdtemp())


def test_build_from_request_runs_controlled_build(tmp_path):
    def factory(_pipeline):
        return ControlledBuilder(FakeExecutor(), tmp_path)

    result = build_from_request(
        {"idea": "Build a tiny Python app", "decision": "BUILD", "verification_command": ["python", "-m", "compileall", "."]},
        make_pipeline,
        factory,
    )

    assert result["status"] == "succeeded"
    assert result["tasks_attempted"] >= 1
    assert result["results"][0]["passed"] is True


def test_build_requires_explicit_build_decision():
    try:
        build_from_request({"idea": "Build an app", "decision": "DIY"}, make_pipeline, make_builder)
    except ValueError as exc:
        assert "BUILD" in str(exc)
    else:
        raise AssertionError("non-BUILD decision should fail")
