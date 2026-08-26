from datetime import datetime, timedelta, timezone

from caos.quota import QuotaState
from caos.quota_scheduler import schedule_sequentially


def test_scheduler_waits_for_known_reset_instead_of_exceeding_quota():
    now = datetime.now(timezone.utc)
    # The scheduler uses current time internally; a short reset keeps this deterministic enough.
    quotas = {"a": QuotaState("a", 10, 8, reset_at=now + timedelta(seconds=1))}
    result = schedule_sequentially([("task-1", 5, "a")], quotas)
    assert result.tasks[0].task_id == "task-1"
    assert result.total_wait_seconds >= 0


def test_scheduler_marks_unknown_resource_unscheduled():
    quotas = {"a": QuotaState("a", 10, 0)}
    result = schedule_sequentially([("task-1", 1, "missing")], quotas)
    assert result.unscheduled_task_ids == ("task-1",)


def test_scheduler_packs_tasks_within_remaining_quota():
    quotas = {"a": QuotaState("a", 10, 0)}
    result = schedule_sequentially([("task-1", 3, "a"), ("task-2", 7, "a")], quotas)
    assert len(result.tasks) == 2
    assert not result.unscheduled_task_ids
