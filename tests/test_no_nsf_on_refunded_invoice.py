"""`no-nsf-on-refunded-invoice` on the REG11868556 fixture: the PAD invoice was refunded in full, then the bank
returned the debit and pay-queue raised an NSF. Changed values below are hypothetical variants for the rule."""

from __future__ import annotations

from rcm_core.detectors import run_detector
from rcm_payments.detectors import DETECTORS
from rcm_payments.sources import FixtureSource
from tests.conftest import FIXTURE

PADR_FILE = "settlement file with the PADR (name not recorded)"


def run(bundle, source, as_of):
    return run_detector(DETECTORS["no-nsf-on-refunded-invoice"], bundle, source, as_of, {"files": [PADR_FILE]})


def test_reg11868556_nsf_on_a_refunded_invoice(bundle, as_of):
    result = run(bundle, FixtureSource(FIXTURE), as_of)
    assert [f.entity for f in result.findings] == ["REG11868556"]
    evidence = result.findings[0].evidence
    assert [n["invoice_id"] for n in evidence["nsf_records"]] == [11919233]
    assert {c["credit_memo"] for c in evidence["applied_credits"]} == {"22622"}


def test_no_nsf_record_is_fine(bundle, as_of, fixture_data, write_fixture):
    fixture_data["nsf_records"] = []
    assert run(bundle, FixtureSource(write_fixture(fixture_data)), as_of).findings == []


def test_unrefunded_invoice_gets_a_normal_nsf(bundle, as_of, fixture_data, write_fixture):
    fixture_data["invoices"][0]["refund"] = None
    assert run(bundle, FixtureSource(write_fixture(fixture_data)), as_of).findings == []


def test_partial_refund_is_flagged(bundle, as_of, fixture_data, write_fixture):
    # A partial refund still gets the full NSF treatment today; the topic lists it as a cause.
    fixture_data["invoices"][0]["refund"] = "10.00"
    assert [f.entity for f in run(bundle, FixtureSource(write_fixture(fixture_data)), as_of).findings] == ["REG11868556"]
