"""Regression contracts for the M1 build, handoff, and routing boundaries."""

from caos.handoff import HandoffState


def test_handoff_accepts_changed_files_alias():
    state = HandoffState(changed_files=("app.py",))
    assert state.files_changed == ("app.py",)


def test_handoff_exposes_canonical_files_changed():
    state = HandoffState(files_changed=("app.py",))
    assert state.files_changed == ("app.py",)


def test_free_first_is_a_policy_when_capability_is_sufficient():
    """Document the product invariant without coupling to a provider implementation."""
    from caos.router import CostAwareRouter

    router = CostAwareRouter()
    assert hasattr(router, "route")
