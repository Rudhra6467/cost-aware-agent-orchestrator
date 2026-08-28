from caos.audit_trail import AuditTrail, ExecutionEvent


def test_audit_trail_preserves_order_and_filters_by_task():
    trail = AuditTrail()
    trail.record(ExecutionEvent("exec_1", "TASK_CREATED", "task_1"))
    trail.record(ExecutionEvent("exec_1", "AGENT_SELECTED", "task_1", "cheap-agent", cost=0.01))
    trail.record(ExecutionEvent("exec_1", "TASK_COMPLETED", "task_1", "cheap-agent", result="success"))
    trail.record(ExecutionEvent("exec_1", "VERIFICATION_FAILED", "task_1", evidence=("missing artifact",)))

    events = trail.for_session("exec_1")
    task_events = trail.for_task("exec_1", "task_1")

    assert [event.event_type for event in events] == [
        "TASK_CREATED",
        "AGENT_SELECTED",
        "TASK_COMPLETED",
        "VERIFICATION_FAILED",
    ]
    assert len(task_events) == 4
    assert task_events[1].agent_name == "cheap-agent"
    assert task_events[1].cost == 0.01
    assert task_events[3].evidence == ("missing artifact",)


def test_audit_trail_is_empty_for_unknown_session():
    assert AuditTrail().for_session("unknown") == ()
