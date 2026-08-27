import pytest

from caos.ledger import QuotaSnapshot, UsageLedger


def test_remaining_quota_accounts_for_consumed_and_reserved():
    ledger = UsageLedger((QuotaSnapshot("free", 100, consumed_units=20, reserved_units=10),))
    assert ledger.remaining("free") == 70


def test_reserve_prevents_double_counting_free_quota():
    ledger = UsageLedger((QuotaSnapshot("free", 100),))
    ledger.reserve("free", 70)
    assert ledger.remaining("free") == 30
    with pytest.raises(ValueError):
        ledger.reserve("free", 31)


def test_consume_updates_shared_state():
    ledger = UsageLedger((QuotaSnapshot("free", 100),))
    ledger.consume("free", 60)
    assert ledger.remaining("free") == 40
