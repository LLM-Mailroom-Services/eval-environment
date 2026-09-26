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
def test_begin_eval_run_upserts_dataset_rows(mock_init_dataset, mock_init, monkeypatch):
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
    assert info["dataset"] == "mailroom-hf-46a4d3c2"
    dataset.insert.assert_called_once()
    call_kw = dataset.insert.call_args.kwargs
    assert "Co" not in str(call_kw["input"])
    assert call_kw["expected"]["expected_doc_class"] == "contract"
    mock_init.assert_called_once()
    end_eval_run()


def test_log_case_scores_uses_headline_only():
    exp = MagicMock()
    with patch("evals.braintrust_experiment._active_experiment", exp):
        case = {"id": "x", "text": "doc", "expected_doc_class": "contract"}
        log_case_scores(
            case,
            scorer="extraction",
            scores={"overall_score": 0.7, "needs_judge_review": 1.0, "extraction_f1": 0.2},
        )
    exp.log.assert_called_once()
    logged = exp.log.call_args.kwargs["scores"]
    assert logged.get("overall_score") == 0.7
    assert "extraction_f1" not in logged
