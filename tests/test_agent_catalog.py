import pytest

from caos.agent_catalog import AgentCapability, AgentCatalog, TaskRequirements
from caos.execution_session import TaskRole


def test_catalog_filters_and_ranks_agents():
    catalog = AgentCatalog([
        AgentCapability("cheap", frozenset({TaskRole.DEVELOPER}), frozenset({"python"}), cost=0.01, quality=0.70, reliability=0.95),
        AgentCapability("premium", frozenset({TaskRole.DEVELOPER}), frozenset({"python", "architecture"}), cost=0.10, quality=0.95, reliability=0.99),
        AgentCapability("wrong-role", frozenset({TaskRole.VERIFIER}), frozenset({"python"}), cost=0.0, quality=1.0),
    ])

    ranked = catalog.rank(TaskRequirements(TaskRole.DEVELOPER, frozenset({"python"}), min_quality=0.8))

    assert [item.agent.name for item in ranked] == ["premium"]


def test_catalog_rejects_capability_and_budget_mismatch():
    catalog = AgentCatalog([
        AgentCapability("python", frozenset({TaskRole.DEVELOPER}), frozenset({"python"}), cost=0.05, quality=0.9),
    ])

    with pytest.raises(LookupError):
        catalog.select(TaskRequirements(TaskRole.DEVELOPER, frozenset({"browser"}), max_cost=0.01))


def test_selection_is_deterministic_for_equal_scores():
    catalog = AgentCatalog([
        AgentCapability("alpha", frozenset({TaskRole.VERIFIER}), frozenset({"tests"}), cost=0.02, quality=0.8),
        AgentCapability("beta", frozenset({TaskRole.VERIFIER}), frozenset({"tests"}), cost=0.02, quality=0.8),
    ])

    assert catalog.select(TaskRequirements(TaskRole.VERIFIER, frozenset({"tests"}))).agent.name == "alpha"
