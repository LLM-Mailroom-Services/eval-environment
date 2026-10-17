"""Trace evidence survives decomposition without invoking an LLM or mutating prompts."""

from __future__ import annotations

from copy import deepcopy

import pytest
from prompt_engineer import decompose


def _failure(**overrides):
    return {
        "filename": "contract.txt",
        "expected_doc_class": "contract",
        "prediction": {"doc_type": "correspondence"},
        "scores": {"overall_score": 0.3},
        **overrides,
    }


def test_decompose_preserves_trace_evidence_and_expected_fields_without_mutation():
    row = _failure(
        braintrust={"project": "test-project", "experiment": "run-a", "span_id": "span-a"},
        trace_excerpt={"reasoning": "Inferred the wrong document class", "output_confidence": 0.9},
        expected_fields={"parties": ["Synthetic Company"]},
    )
    before = deepcopy(row)

    result = decompose([row])

    assert result == {
        "n_failures": 1,
        "by_class": {"contract": 1},
        "by_type": {"low_score": 1},
        "examples": {
            "contract": [
                {
                    "filename": "contract.txt",
                    "expected": "contract",
                    "predicted": "correspondence",
                    "scores": {"overall_score": 0.3},
                    "braintrust": row["braintrust"],
                    "trace_excerpt": row["trace_excerpt"],
                    "expected_fields": row["expected_fields"],
                }
            ]
        },
    }
    assert row == before


@pytest.mark.parametrize("empty", [None, {}])
def test_decompose_omits_absent_optional_evidence_from_legacy_manifests(empty):
    result = decompose([_failure(braintrust=empty, trace_excerpt=empty, expected_fields=empty)])
    assert result["examples"]["contract"] == [
        {
            "filename": "contract.txt",
            "expected": "contract",
            "predicted": "correspondence",
            "scores": {"overall_score": 0.3},
        }
    ]


def test_decompose_focus_filters_counts_and_evidence_before_example_limit():
    rows = [_failure(expected_doc_class="correspondence") for _ in range(201)]
    rows += [_failure(trace_excerpt={"reasoning": "focused evidence"})]

    result = decompose(rows, focus="contract")

    assert result["n_failures"] == 1
    assert result["by_class"] == {"contract": 1}
    assert result["by_type"] == {"low_score": 1}
    assert result["examples"]["contract"][0]["trace_excerpt"] == {"reasoning": "focused evidence"}


def test_decompose_limits_evidence_examples_but_counts_all_failures():
    rows = [_failure(filename=f"{i}.txt", braintrust={"span_id": f"span-{i}"}) for i in range(7)]
    result = decompose(rows)

    assert result["n_failures"] == 7
    assert result["by_class"] == {"contract": 7}
    assert [ex["braintrust"]["span_id"] for ex in result["examples"]["contract"]] == [
        f"span-{i}" for i in range(5)
    ]


def test_decompose_keeps_trace_evidence_for_runtime_errors_and_missing_predictions():
    row = _failure(
        error="provider failure", prediction=None, trace_excerpt={"reasoning": "partial evidence"}
    )
    result = decompose([row])

    assert result["by_type"] == {"runtime_error": 1}
    example = result["examples"]["contract"][0]
    assert example["predicted"] is None
    assert example["trace_excerpt"] == {"reasoning": "partial evidence"}


def test_decompose_empty_focus_returns_empty_summary():
    assert decompose([_failure()], focus="insurance_claim") == {
        "n_failures": 0,
        "by_class": {},
        "by_type": {},
        "examples": {},
    }
