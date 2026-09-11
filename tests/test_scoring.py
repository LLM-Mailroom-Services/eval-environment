"""Scorer unit tests — deterministic, gold-in/gold-out wiring checks."""

from __future__ import annotations

from evals import scoring


def test_classification_gold():
    scored = scoring.score_classification("contract", "contract")
    assert scored["class_correct"] == 1


def test_classification_alias_match():
    scored = scoring.score_classification("merger_agreement", "merger agreement")
    assert scored["class_correct"] == 1


def test_classification_miss():
    assert scoring.score_classification("correspondence", "contract")["class_correct"] == 0


def test_subclass_match():
    assert scoring.score_subclass("All_Cash", "all cash")["subclass_correct"] == 1
    assert scoring.score_subclass("all_stock", "all_cash")["subclass_correct"] == 0


def test_extraction_gold_in_gold_out():
    expected = {"parties": ["Acme Corp", "Beta LLC"], "payment_terms": "Net 30"}
    scored = scoring.score_extraction("contract", dict(expected), expected)
    assert scored["overall_score"] is not None and scored["overall_score"] > 0.5


def test_extraction_empty_expected():
    assert scoring.score_extraction("contract", {"a": 1}, {})["n_expected_fields"] == 0


def test_label_lists_f1():
    scored = scoring.score_label_lists(
        {"cuad_clause_labels": ["Termination", "Limitation of Liability"]},
        {"cuad_clause_labels": ["termination", "indemnification"]},
        "cuad_clause_labels",
    )
    assert scored["cuad_clause_labels_recall"] == 0.5
    assert 0 < scored["cuad_clause_labels_f1"] < 1


def test_decision_validity():
    assert scoring.score_decision("retry_extraction", ("accept_with_caveats", "retry_extraction", "human_review"))["decision_valid"] == 1
    assert scoring.score_decision("bogus", ("approved", "review"))["decision_valid"] == 0
    assert scoring.score_decision("review", ("approved", "review"), expected="review")["decision_agrees"] == 1


def test_judge_agreement():
    case = {"review_expected": True}
    assert scoring.score_judge({"completeness_label": "incomplete"}, case)["judge_agrees"] == 1
    assert scoring.score_judge({"completeness_label": "complete"}, case)["judge_agrees"] == 0


def test_arbiter_agreement_map():
    case = {"arbiter_outcome": "re_extract"}
    assert scoring.score_arbiter({"decision": "retry_extraction"}, case)["decision_agrees"] == 1
    assert scoring.score_arbiter({"decision": "human_review"}, case)["decision_agrees"] == 0


def test_intake_no_truncation():
    case = {"text": "line one\nline two"}
    result = {"cleaned": "line one line two", "triage": {"primary_doc_class": "contract"}}
    scored = scoring.score_intake(result, case)
    assert scored["no_truncation"] == 1
    assert scored["triage_agrees"] is None  # no expected class on this case


def test_pipeline_stage_agreement():
    case = {"expected_stage": "archived", "expected_doc_class": "contract", "expected_fields": {}}
    scored = scoring.score_pipeline({"stage": "archived", "doc_type": "contract"}, case)
    assert scored["stage_agrees"] == 1


def test_performance_row_and_summary():
    row = scoring.performance_row(123.4, {"prompt_tokens": 10, "completion_tokens": 5}, None)
    assert row["total_tokens"] == 15 and row["latency_ms"] == 123.4
    summary = scoring.summarize_performance([row, row])
    assert summary["tokens_prompt_total"] == 20
    assert summary["latency_ms_p95"] >= summary["latency_ms_mean"]


def test_summarize_scores_keys():
    rows = [
        {"scores": {"class_correct": 1}, "error": None},
        {"scores": {"class_correct": 0}, "error": "boom"},
    ]
    summary = scoring.summarize_scores(rows)
    assert summary["n"] == 2 and summary["errors"] == 1 and "class_accuracy" in summary
