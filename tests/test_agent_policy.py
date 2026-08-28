import pytest

from caos.agent_policy import AgentProfile, AgentSelectionPolicy
from caos.execution_session import ExecutionTask, TaskRole


def test_selects_cheapest_capable_agent():
    policy = AgentSelectionPolicy([
        AgentProfile("premium-dev", frozenset({TaskRole.DEVELOPER}), cost_tier=2),
        AgentProfile("cheap-dev", frozenset({TaskRole.DEVELOPER}), cost_tier=0),
    ])
    task = ExecutionTask("task_1", "implement", TaskRole.DEVELOPER)

    assert policy.select(task).name == "cheap-dev"


def test_selection_is_deterministic_for_equal_cost():
    policy = AgentSelectionPolicy([
        AgentProfile("z-agent", frozenset({TaskRole.VERIFIER}), cost_tier=1),
        AgentProfile("a-agent", frozenset({TaskRole.VERIFIER}), cost_tier=1),
    ])
    task = ExecutionTask("task_1", "verify", TaskRole.VERIFIER)

    assert policy.select(task).name == "a-agent"


def test_missing_capability_is_rejected():
    policy = AgentSelectionPolicy([AgentProfile("developer", frozenset({TaskRole.DEVELOPER}))])
    task = ExecutionTask("task_1", "verify", TaskRole.VERIFIER)

    with pytest.raises(LookupError, match="No capable agent"):
        policy.select(task)
