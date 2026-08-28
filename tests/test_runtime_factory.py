from pathlib import Path

from caos.planning_contract import PlanSummary, PlanningResponse
from caos.runtime_factory import create_runtime, requirements_for


def planning_response():
    plan = PlanSummary("p1", "Local Build", 0.0, 10.0, 0.0, ("build",))
    return PlanningResponse(
        idea="build a demo",
        blueprint_summary="demo",
        assumptions=(),
        plans=(plan,),
        recommendation="p1",
        reasons=(),
        explanation="local path",
        next_actions=("BUILD", "DIY"),
    )


def test_bootstrap_creates_complete_runtime(tmp_path: Path):
    response = planning_response()
    runtime, session = create_runtime(response, "p1", tmp_path)

    assert session.plan_id == "p1"
    assert runtime.ready_tasks(session.session_id) == ["task_1"]


def test_bootstrapped_runtime_executes_entire_graph(tmp_path: Path):
    response = planning_response()
    runtime, session = create_runtime(response, "p1", tmp_path)
    graph = runtime.scheduler.graph
    requirements = requirements_for(graph)
    runtime.start(session.session_id)

    while runtime.ready_tasks(session.session_id):
        runtime.run_next(session.session_id, requirements)

    final = runtime.sessions.get(session.session_id)
    assert final.status.value == "verifying"
    assert final.completed_tasks == len(final.tasks)
    assert len(list(tmp_path.glob("*.txt"))) == len(final.tasks)
