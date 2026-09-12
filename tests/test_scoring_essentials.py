"""scoring.py essentials — the sink-metric curation surface (non-negotiable 8).

The ESSENTIAL_SCORES dict is the complete span-metric surface; these tests
pin its shape and the filter/rollup behavior so full-score forwarding can
never creep back into spans.
"""

from __future__ import annotations

import pytest

from evals.scoring import (
    ESSENTIAL_SCORES,
    essential_metrics,
    essential_rollup,
    sha256_text,
)


def test_essential_scores_shape():
    families = {
        "intake", "classification", "extraction", "judge",
        "arbiter", "boss", "archivist", "pipeline",
    }
    assert set(ESSENTIAL_SCORES) == families
    for scorer, keys in ESSENTIAL_SCORES.items():
        assert 1 <= len(keys) <= 3, f"{scorer} carries {len(keys)} essentials (cap is 3)"
        assert len(set(keys)) == len(keys), f"{scorer} has duplicate essentials"


def test_essential_metrics_filters_to_family():
    scores = {
        "class_correct": 1,
        "subclass_correct": 0,
        "judge_agrees": False,          # belongs to the judge family, not classification
        "some_full_suite_metric": 0.5,  # must never reach spans
    }
    out = essential_metrics("classification", scores)
    assert out == {"class_correct": 1.0, "subclass_correct": 0.0}
    assert "some_full_suite_metric" not in out


def test_essential_metrics_unknown_scorer_is_empty():
    assert essential_metrics("nonexistent_scorer", {"class_correct": 1}) == {}


def test_essential_metrics_drops_non_numeric():
    scores = {"class_correct": 1, "predicted_doc_class": "contract"}
    assert essential_metrics("classification", scores) == {"class_correct": 1.0}


def test_essential_rollup_means():
    rows = [
        {"scores": {"class_correct": 1, "subclass_correct": 1}},
        {"scores": {"class_correct": 0, "subclass_correct": 0}},
        {"scores": {"class_correct": 1}},  # missing subclass_correct — skipped
        {"scores": {}},                    # no essentials — skipped
    ]
    rollup = essential_rollup("classification", rows)
    assert rollup["class_correct"] == pytest.approx(2 / 3, abs=1e-3)
    assert rollup["subclass_correct"] == 0.5


def test_essential_rollup_empty_rows():
    assert essential_rollup("classification", []) == {}
    assert essential_rollup("nonexistent_scorer", [{"scores": {"class_correct": 1}}]) == {}


def test_sha256_text_stable_and_sensitive():
    a = sha256_text("hello")
    assert a == sha256_text("hello")
    assert a != sha256_text("hello ")
    assert len(a) == 64
