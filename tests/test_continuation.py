from caos.agents import MockAgentExecutor
from caos.continuation import ContinuationCoordinator
from caos.handoff import HandoffState
from caos.provider_health import ProviderHealth, ProviderHealthRegistry, ProviderState


def test_rate_limited_agent_continues_with_fallback():
    health = ProviderHealthRegistry()
    health.update(ProviderHealth("agent-a", ProviderState.RATE_LIMITED, 0, 120, "429"))
    health.update(ProviderHealth("agent-b", ProviderState.HEALTHY, 10))

    b = MockAgentExecutor({})
    coordinator = ContinuationCoordinator({"agent-b": b}, health)
    state = HandoffState(
        project_id="demo",
        objective="build a task API",
        completed_tasks=("schema",),
        pending_tasks=("routes",),
        decisions=("use python",),
        files_changed=("models.py",),
    )

    result = coordinator.continue_after_failure(
        source_provider="agent-a",
        state=state,
        reason="429 quota exceeded",
    )

    assert result.handed_off is True
    assert result.target_provider == "agent-b"
    assert result.output is not None
    assert "routes" in result.target_prompt
    assert "models.py" in result.target_prompt
