from datetime import datetime, timedelta, timezone

from caos.quota import QuotaState, quota_health


def test_remaining_quota_and_health():
    quota = QuotaState("r1", 100, 25)
    assert quota.remaining == 75
    assert quota.available
    assert quota_health(quota) == 0.75


def test_limited_resource_is_unavailable():
    quota = QuotaState("r1", 100, 100, limited=True)
    assert quota.remaining == 0
    assert not quota.available
    assert quota_health(quota) == 0.0


def test_reset_countdown_is_nonnegative():
    now = datetime.now(timezone.utc)
    quota = QuotaState("r1", 100, 25, reset_at=now + timedelta(seconds=10))
    assert 0 <= quota.reset_in_seconds(now) <= 10
