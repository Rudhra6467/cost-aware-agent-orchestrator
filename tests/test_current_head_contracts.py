"""Regression contracts for the M1 build and handoff boundaries."""

from caos.handoff import HandoffState


def test_handoff_accepts_changed_files_alias():
    state = HandoffState(project_id="demo", objective="build an app", changed_files=("app.py",))
    assert state.files_changed == ("app.py",)


def test_handoff_exposes_canonical_files_changed():
    state = HandoffState(project_id="demo", objective="build an app", files_changed=("app.py",))
    assert state.changed_files == ("app.py",)
