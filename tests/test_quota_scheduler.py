from datetime import datetime, timedelta, timezone

from caos.quota_scheduler import QuotaScheduler, QuotaWindow


def test_scheduler_uses_free_capacity_available_now():
    now = datetime(2026, 8, 27, 12, tzinfo=timezone.utc)
    result = QuotaScheduler().schedule(
        "task", 2, 15,
        (QuotaWindow("free", 4), QuotaWindow("later", 10, reset_at=now + timedelta(hours=1))),
        now,
    )
    assert result.resource_id == "free"
    assert result.waited_minutes == 0


def test_scheduler_waits_for_reset_when_no_current_capacity():
    now = datetime(2026, 8, 27, 12, tzinfo=timezone.utc)
    reset = now + timedelta(minutes=45)
    result = QuotaScheduler().schedule(
        "task", 2, 10,
        (QuotaWindow("free", 0, reset_at=reset),),
        now,
    )
    assert result.resource_id == "free"
    assert result.waited_minutes == 45
