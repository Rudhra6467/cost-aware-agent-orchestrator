from caos.models import AgentProfile, Task
from caos.selector import estimate_cost, select_agent


def test_free_agent_has_zero_estimated_cost():
    agent = AgentProfile(agent_id="a", name="Free", coding_score=8)
    task = Task(task_id="t", description="code", estimated_input_tokens=1000, estimated_output_tokens=2000)
    assert estimate_cost(agent, task) == 0.0


def test_selector_respects_budget():
    free = AgentProfile(agent_id="free", name="Free", coding_score=8)
    paid = AgentProfile(
        agent_id="paid",
        name="Paid",
        coding_score=9,
        cost_per_1k_input=1.0,
        cost_per_1k_output=1.0,
    )
    task = Task(task_id="t", description="code", minimum_capability=7)
    result = select_agent(task, [free, paid], budget_remaining=0.01)
    assert result.agent_id == "free"


def test_selector_rejects_insufficient_context():
    small = AgentProfile(agent_id="small", name="Small", coding_score=10, context_window=100)
    task = Task(task_id="t", description="code", context_required=1000)
    try:
        select_agent(task, [small])
    except ValueError as exc:
        assert "No feasible agent" in str(exc)
    else:
        raise AssertionError("Expected no feasible agent")
