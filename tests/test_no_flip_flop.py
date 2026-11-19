"""`no-flip-flop` on the REG11868556 fixture. Rows added below are hypothetical variants of the recorded history,
to exercise the rule; they aren't recorded values."""

from __future__ import annotations

from rcm_core.detectors import run_detector
from rcm_payments.detectors import DETECTORS
from rcm_payments.sources import FixtureSource
from tests.conftest import FIXTURE

PADR_FILE = "settlement file with the PADR (name not recorded)"
CMAP_FILE = "settlement file with the CMAP (name not recorded)"
NUMBER = "REG11868556"


def run(bundle, source, as_of, files):
    return run_detector(DETECTORS["no-flip-flop"], bundle, source, as_of, {"files": files})


def row(file, record_type, status, day, application_id=None):
    return {"file": file, "record_type": record_type, "source_txn": None, "target_type": "INV",
            "target_number": NUMBER, "target_status": status, "application_amount": None,
            "application_date": day, "application_id": application_id}


def add_file(data, key):
    data["files"].append({"key": key, "processed": True, "processed_on": None})


def test_single_return_is_the_normal_nsf_path(bundle, as_of):
    assert run(bundle, FixtureSource(FIXTURE), as_of, [PADR_FILE]).findings == []


def test_file_without_pad_rows_opens_nothing(bundle, as_of):
    assert run(bundle, FixtureSource(FIXTURE), as_of, [CMAP_FILE]).findings == []


def test_pad_payment_after_a_return_is_a_flip_flop(bundle, as_of, fixture_data, write_fixture):
    # PAD is stopped after a return and the customer pays by credit card, so a PAD debit after it is never expected.
    add_file(fixture_data, "later file")
    fixture_data["settlement_rows"].append(row("later file", "PADP", "Fully PAID", "2026-09-10"))
    result = run(bundle, FixtureSource(write_fixture(fixture_data)), as_of, ["later file"])
    assert [f.entity for f in result.findings] == [NUMBER]
    evidence = result.findings[0].evidence
    assert evidence["pattern"] == "R P"
    assert evidence["pad_payment_after_return"] is True
    assert evidence["returns"] == 1


def test_paid_returned_paid_returned(bundle, as_of, fixture_data, write_fixture):
    add_file(fixture_data, "earlier file")
    add_file(fixture_data, "later file")
    fixture_data["settlement_rows"] += [
        row("earlier file", "PADP", "Fully PAID", "2026-08-01"),
        row("later file", "PADP", "Fully PAID", "2026-09-10"),
        row("later file", "PADR", "Not PAID", "2026-09-20"),
    ]
    result = run(bundle, FixtureSource(write_fixture(fixture_data)), as_of, ["later file"])
    assert result.findings[0].evidence["pattern"] == "P R P R"
    assert result.findings[0].evidence["returns"] == 2


def test_return_delivered_twice(bundle, as_of, fixture_data, write_fixture):
    add_file(fixture_data, "later file")
    fixture_data["settlement_rows"].append(row("later file", "PADR", None, "2026-08-31"))
    result = run(bundle, FixtureSource(write_fixture(fixture_data)), as_of, ["later file"])
    assert [f.entity for f in result.findings] == [NUMBER]
    assert result.findings[0].evidence["pattern"] == "R R"


def test_pad_payment_before_the_return_is_normal(bundle, as_of, fixture_data, write_fixture):
    add_file(fixture_data, "earlier file")
    fixture_data["settlement_rows"].append(row("earlier file", "PADP", "Fully PAID", "2026-08-01"))
    assert run(bundle, FixtureSource(write_fixture(fixture_data)), as_of, [PADR_FILE]).findings == []


def test_rows_older_than_the_lookback_are_ignored(bundle, as_of, fixture_data, write_fixture):
    # The check's lookback is P90D; as_of is 2026-10-19, so a return before 2026-07-21 is outside it.
    add_file(fixture_data, "old file")
    fixture_data["settlement_rows"].append(row("old file", "PADR", "Not PAID", "2026-06-01"))
    assert bundle.check("no-flip-flop")["lookback"] == "P90D"
    assert run(bundle, FixtureSource(write_fixture(fixture_data)), as_of, [PADR_FILE]).findings == []
