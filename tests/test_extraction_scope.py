"""Extraction GT scoping — empty / other-class Hub union must not penalize."""

from __future__ import annotations

from evals import extraction_scope, scoring


def test_applicable_expected_drops_empty_insurance_on_correspondence():
    raw = {
        "sender": "Acme Legal",
        "recipient": "Beta LLC",
        "claim_number": "",
        "denial_reasons": [],
        "policy_number": None,
        "claimed_amount": "",
    }
    scoped = extraction_scope.applicable_expected_fields("correspondence", raw)
    assert scoped == {"sender": "Acme Legal", "recipient": "Beta LLC"}


def test_applicable_expected_drops_other_class_non_empty_keys():
    raw = {
        "sender": "Acme",
        "claim_number": "887013387879564",
        "claim_type": "carrier",
    }
    scoped = extraction_scope.applicable_expected_fields("correspondence", raw)
    assert "claim_number" not in scoped
    assert scoped["sender"] == "Acme"


def test_symmetric_correspondence_keys_dropped_on_insurance_claim():
    raw = {
        "claim_number": "C-1",
        "sender": "Should Not Score",
        "demand_amount": 1000,
    }
    scoped = extraction_scope.applicable_expected_fields("insurance_claim", raw)
    assert scoped.get("claim_number") == "C-1"
    assert "sender" not in scoped
    assert "demand_amount" not in scoped


def test_hub_alias_claimed_amount_to_demand_amount_on_correspondence():
    raw = {"claimed_amount": "5000", "sender": "X"}
    scoped = extraction_scope.applicable_expected_fields("correspondence", raw)
    assert scoped.get("demand_amount") == "5000"
    assert "claimed_amount" not in scoped


def test_scope_predicted_drops_insurance_keys_on_correspondence():
    pred = {"sender": "A", "claim_number": "phantom"}
    scoped = extraction_scope.scope_predicted_fields("correspondence", pred)
    assert scoped == {"sender": "A"}


def test_correspondence_union_with_residual_empty_lists():
    """Hub rows may still carry ``[]`` union keys after hoist — scope drops them."""
    row = {
        "sender": "Counsel",
        "recipient": "Debtor",
        "denial_reasons": [],
        "supporting_documents": [],
    }
    scoped = extraction_scope.applicable_expected_fields("correspondence", row)
    assert scoped == {"sender": "Counsel", "recipient": "Debtor"}


def test_score_extraction_uses_scoped_field_count_without_suite():
    """When the suite is unavailable, n_expected_fields still reflects scoped GT."""
    unscoped = {
        "sender": "A",
        "recipient": "B",
        "claim_number": "X",
        "denial_reasons": [],
    }
    scored = scoring.score_extraction("correspondence", {}, unscoped)
    if scored.get("scorer_error"):
        assert scored["n_expected_fields"] == 2
    else:
        assert scored["n_expected_fields"] == 2
