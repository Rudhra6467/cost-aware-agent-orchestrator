from datetime import datetime, timedelta, timezone

from caos.quota import QuotaState
from caos.quota_forecast import forecast_plan_usage, forecast_quota


def test_forecast_detects_future_quota_exhaustion():
    now = datetime.now(timezone.utc)
    quota = QuotaState("r1", 100, 80, reset_at=now + timedelta(hours=2))
    projection = forecast_quota(quota, 25, now)
    assert projection.remaining_before == 20
    assert projection.remaining_after == 0
    assert projection.exhausted
    assert projection.reset_in_seconds == 7200


def test_forecast_plan_usage_handles_multiple_resources():
    quotas = {
        "a": QuotaState("a", 100, 20),
        "b": QuotaState("b", 50, 10),
    }
    projections = forecast_plan_usage({"a": 30, "b": 5}, quotas)
    assert [p.resource_id for p in projections] == ["a", "b"]
    assert projections[0].exhausted
    assert not projections[1].exhausted
