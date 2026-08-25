from caos.agents import MockAgentExecutor
from caos.models import AgentProfile
from caos.orchestrator import CAOSOrchestrator
from caos.state import StateStore


def test_orchestrator_runs_plan_and_persists_execution():
    agents = [
        AgentProfile(
            agent_id="planner-free",
            name="Planner Free",
            coding_score=5.0,
            architecture_score=7.0,
            research_score=7.0,
            reliability=0.95,
            availability=0.95,
        ),
        AgentProfile(
            agent_id="coder-free",
            name="Coder Free",
            coding_score=8.0,
            architecture_score=6.0,
            reliability=0.90,
            availability=0.90,
        ),
    ]
    store = StateStore(":memory:")
    orchestrator = CAOSOrchestrator(
        agents,
        {
            "planner-free": MockAgentExecutor("planner-free"),
            "coder-free": MockAgentExecutor("coder-free"),
        },
        store,
    )

    result = orchestrator.run("Build a tiny expense API", budget=0.0)

    assert result.succeeded
    assert len(result.executions) == 2
    assert result.estimated_cost == 0.0
    assert result.actual_cost == 0.0
    assert store.execution_count() == 2
