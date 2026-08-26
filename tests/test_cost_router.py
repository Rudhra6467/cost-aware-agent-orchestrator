from caos.cost_optimizer import CostPolicy
from caos.cost_router import CostAwareRouter
from caos.models import AgentProfile, Task
from caos.provider_health import ProviderHealth, ProviderHealthRegistry, ProviderState


def test_router_prefers_practical_quality_over_unusable_free_resource():
    task = Task("t1", "build endpoint", minimum_capability=0.5)
    agents = [
        AgentProfile("free", "Free", coding_score=0.55, reliability=0.50, context_window=32_000),
        AgentProfile("paid", "Paid", coding_score=0.95, reliability=0.98, cost_per_1k_output=0.01),
    ]
    decision = CostAwareRouter().route(task, agents, policy=CostPolicy(prefer_free=True))
    assert decision.agent_id == "free"


def test_health_filters_rate_limited_provider():
    task = Task("t1", "build endpoint")
    agents = [
        AgentProfile("a", "A", coding_score=1.0),
        AgentProfile("b", "B", coding_score=0.8),
    ]
    health = ProviderHealthRegistry()
    health.update(ProviderHealth("a", ProviderState.RATE_LIMITED, 0))
    health.update(ProviderHealth("b", ProviderState.HEALTHY, 3))
    decision = CostAwareRouter(health).route(task, agents)
    assert decision.agent_id == "b"
