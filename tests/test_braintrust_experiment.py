"""Braintrust experiment + dataset wiring (hermetic)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from evals import scoring
from evals.braintrust_experiment import (
    begin_eval_run,
    end_eval_run,
    experiments_enabled,
    log_case_scores,
)


def test_experiments_disabled_for_mock():
    assert experiments_enabled(True, "braintrust") is False
    assert experiments_enabled(False, "none") is False


def test_sink_score_metrics_caps_headline_count():
    scores = {
        "overall_score": 0.8,
        "needs_judge_review": 0.0,
        "extraction_f1": 0.5,
    }
    out = scoring.sink_score_metrics("extraction", scores, max_scores=1)
    assert out == {"overall_score": 0.8}


@patch("braintrust.init")
@patch("braintrust.init_dataset")
def test_begin_eval_run_does_not_insert_document_rows(mock_init_dataset, mock_init, monkeypatch):
    monkeypatch.setenv("BRAINTRUST_API_KEY", "test-key")
    monkeypatch.setenv("BRAINTRUST_PROJECT", "Mailroom-Evals")

    dataset = MagicMock()
    dataset.insert.return_value = "rec-1"
    mock_init_dataset.return_value = dataset
    mock_init.return_value = MagicMock()

    case = {
        "id": "corpus:ground_truth:train:secret.pdf",
        "text": "hello",
        "filename": "secret.pdf",
        "expected_doc_class": "contract",
        "config": "ground_truth",
        "split": "train",
    }
    info = begin_eval_run(
        run_id="run-1",
        task_id="eval:contracts",
        cases=[case],
        dataset_prov={"repo": "Lucius-Morningstar/mailroom-dataset", "revision": "46a4d3c240a"},
    )
    assert info is not None
    assert info["dataset"] is None
    assert info["dataset_records"] == 0
    mock_init_dataset.assert_not_called()
    dataset.insert.assert_not_called()
    mock_init.assert_called_once()
    assert mock_init.call_args.kwargs.get("dataset") is None
    end_eval_run()


def test_log_case_scores_one_fully_scored_document_row():
    exp = MagicMock()
    span = MagicMock()
    with patch("evals.braintrust_experiment._active_experiment", exp):
        case = {"id": "x", "text": "doc", "expected_doc_class": "contract", "filename": "a.pdf"}
        log_case_scores(
            case,
            scorer="extraction",
            scores={
                "overall_score": 0.7,
                "needs_judge_review": True,
                "extraction_f1": 0.2,
                "n_expected_fields": 6,
            },
            prediction={"extracted_data": {"parties": ["Acme"]}},
            specialist="contracts_specialist",
            latency_ms=12.0,
            cost_usd=0.001,
            tokens={"prompt": 10, "completion": 4},
            span=span,
        )
    exp.log.assert_not_called()
    span.log_document_row.assert_called_once()
    kw = span.log_document_row.call_args.kwargs
    assert kw["scores"]["overall_score"] == 0.7
    assert kw["scores"]["extraction_f1"] == 0.2
    assert kw["scores"]["needs_judge_review"] == 1.0
    assert "n_expected_fields" not in kw["scores"]
    assert kw["output"]["specialist"] == "contracts_specialist"
    assert kw["output"]["extracted_data"] == {"parties": ["Acme"]}
    assert kw["metadata"]["specialist"] == "contracts_specialist"
    assert "document" not in kw["tags"]


def test_log_case_scores_skips_without_parent_span():
    exp = MagicMock()
    with patch("evals.braintrust_experiment._active_experiment", exp):
        log_case_scores(
            {"id": "x", "text": "doc"},
            scorer="extraction",
            scores={"overall_score": 1.0},
            specialist="contracts_specialist",
        )
    exp.log.assert_not_called()
