"""Extraction GT scoping — empty / other-class Hub union must not penalize."""

from __future__ import annotations

import numpy as np
import pandas as pd

from evals import cases, extraction_scope, scoring


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


# --- issue #18: numpy-array GT cells must classify, not crash ---------------
# `cases._case_from_row` reads rows via `DataFrame.to_dict(orient="records")`,
# so schema-v9 list-typed parquet cells arrive as `numpy.ndarray`. The old
# `if value in _EMPTY` membership test compared element-wise and `bool()` on the
# result raised "The truth value of an empty array is ambiguous".


def test_is_empty_gt_ndarray_cases():
    assert extraction_scope.is_empty_gt(np.array([])) is True
    assert extraction_scope.is_empty_gt(np.array([], dtype=object)) is True
    assert extraction_scope.is_empty_gt(np.array([[], []])) is True
    assert extraction_scope.is_empty_gt(np.array(["a"])) is False
    assert extraction_scope.is_empty_gt(np.array([0])) is False
    assert extraction_scope.is_empty_gt(np.array([[0], [0]])) is False
    assert extraction_scope.is_empty_gt(np.array(["a", "b"])) is False


def test_is_empty_gt_ndarray_zero_dim():
    assert extraction_scope.is_empty_gt(np.array(0)) is False
    assert extraction_scope.is_empty_gt(np.array(0.0)) is False
    assert extraction_scope.is_empty_gt(np.array("")) is True
    assert extraction_scope.is_empty_gt(np.array("a")) is False


def test_is_empty_gt_pandas_series():
    assert extraction_scope.is_empty_gt(pd.Series([], dtype=object)) is True
    assert extraction_scope.is_empty_gt(pd.Series(["a"])) is False
    assert extraction_scope.is_empty_gt(pd.Series([0])) is False
    assert extraction_scope.is_empty_gt(pd.Series([None])) is True
    assert extraction_scope.is_empty_gt(pd.Series([None, "a"])) is False


def test_is_empty_gt_missing_sentinels():
    assert extraction_scope.is_empty_gt(pd.NA) is True
    assert extraction_scope.is_empty_gt(pd.NaT) is True
    assert extraction_scope.is_empty_gt(float("nan")) is True
    assert extraction_scope.is_empty_gt(np.float64("nan")) is True
    assert extraction_scope.is_empty_gt(np.array([np.nan])) is True


def test_is_empty_gt_zero_is_stated():
    """Numeric zero / False are stated values — never absence."""
    for stated in (0, 0.0, "$0", False, np.int64(0), np.float64(0.0)):
        assert extraction_scope.is_empty_gt(stated) is False, stated


def test_is_empty_gt_legacy_values_unchanged():
    assert extraction_scope.is_empty_gt(None) is True
    assert extraction_scope.is_empty_gt("") is True
    assert extraction_scope.is_empty_gt("   ") is True
    assert extraction_scope.is_empty_gt("{}") is False  # literal, not a dict
    assert extraction_scope.is_empty_gt([]) is True
    assert extraction_scope.is_empty_gt(()) is True
    assert extraction_scope.is_empty_gt({}) is True
    assert extraction_scope.is_empty_gt([[], {}]) is True
    assert extraction_scope.is_empty_gt([[], ["a"]]) is False
    assert extraction_scope.is_empty_gt(["a", {}]) is False
    assert extraction_scope.is_empty_gt("claim-1") is False
    assert extraction_scope.is_empty_gt({"a": None}) is False
    assert extraction_scope.is_empty_gt(42) is False


def test_applicable_expected_fields_drops_ndarray_placeholders():
    row = {
        "sender": "Acme Legal",
        "recipient": "Beta LLC",
        "denial_reasons": np.array([], dtype=object),
        "supporting_documents": pd.Series([], dtype=object),
        "claim_number": pd.NA,
        "claimed_amount": float("nan"),
    }
    scoped = extraction_scope.applicable_expected_fields("correspondence", row)
    assert scoped == {"sender": "Acme Legal", "recipient": "Beta LLC"}


def test_applicable_expected_fields_keeps_numeric_ndarray():
    """An array holding 0 is a stated value — the union-key alias must fire."""
    row = {"sender": "X", "claimed_amount": np.array([0])}
    scoped = extraction_scope.applicable_expected_fields("correspondence", row)
    assert "claimed_amount" not in scoped  # not in the correspondence allow-list
    assert scoped["demand_amount"] == [0]  # alias copied a stated value


def test_cases_is_empty_container_array_and_missing_sentinels():
    assert cases._is_empty_container(np.array([], dtype=object)) is True
    assert cases._is_empty_container(pd.Series([], dtype=object)) is True
    assert cases._is_empty_container(np.array(["a"])) is False
    assert cases._is_empty_container(np.array([0])) is False
    assert cases._is_empty_container(pd.NA) is True
    assert cases._is_empty_container(pd.NaT) is True
    assert cases._is_empty_container(float("nan")) is True
    assert cases._is_empty_container(0) is False


def test_expand_gt_fields_drops_ndarray_empties():
    row = {
        "filename": "f.txt",
        "expected": "insurance_claim",
        "gt_fields": {
            "denial_reasons": np.array([], dtype=object),
            "supporting_documents": np.array(["invoice.pdf"]),
            "claimed_amount": float("nan"),
            "claim_number": "C-1",
        },
    }
    expanded = cases._expand_gt_fields(row)
    assert "denial_reasons" not in expanded
    assert "claimed_amount" not in expanded
    assert expanded["claim_number"] == "C-1"
    assert list(expanded["supporting_documents"]) == ["invoice.pdf"]


def test_expected_fields_survives_ndarray_row():
    """End-to-end over the shapes `to_dict` produces (issue #18 repro)."""
    row = {
        "filename": "f.txt",
        "expected": "insurance_claim",
        "claim_number": "C-1",
        "denial_reasons": np.array([], dtype=object),
        "coverage_determination": pd.Series([], dtype=object),
        "supporting_documents": np.array(["invoice.pdf"]),
    }
    fields = cases._expected_fields(row)
    assert fields.get("claim_number") == "C-1"
    assert "denial_reasons" not in fields
    assert "coverage_determination" not in fields
    assert list(fields["supporting_documents"]) == ["invoice.pdf"]
