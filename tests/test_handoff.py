from caos.handoff import HandoffState
from caos.state import StateStore


def test_handoff_state_round_trips():
    state = HandoffState(
        project_id="p1",
        objective="Build an API",
        completed_tasks=("task-001",),
        pending_tasks=("task-002",),
        decisions=("Use SQLite",),
        files_changed=("src/app.py",),
        known_errors=("test_x failed",),
        current_output="Implemented schema",
    )

    restored = HandoffState.from_json(state.to_json())

    assert restored == state
    assert "PENDING: task-002" in restored.compact_prompt()


def test_handoff_can_be_persisted():
    store = StateStore(":memory:")
    state = HandoffState(project_id="p1", objective="Build API")

    store.record_handoff("p1", "agent-a", state.to_json(), "agent-b")

    assert store.handoff_count() == 1
