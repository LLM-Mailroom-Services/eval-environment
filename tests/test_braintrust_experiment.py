"""Braintrust experiment + dataset wiring (hermetic)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from evals import scoring
from evals.braintrust_experiment import (
    begin_eval_run,
    end_eval_run,
    experiments_enabled,
    finalize_eval_run,
    log_case_scores,
    sync_full_corpus_dataset,
)


class _KeyErrorGetattrExperiment:
    """Mimics braintrust.logger.Experiment's real (broken) __getattr__: it
    raises KeyError — not AttributeError — for unknown attribute names, so
    hasattr()/getattr(obj, name, default) do not fail closed and instead
    propagate the KeyError. Reproduces the live failure from run
    20260927T014814Z (finalize_eval_run crashed probing update_metadata)."""

    def __getattr__(self, name):
        raise KeyError(name)


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


def test_finalize_eval_run_survives_sdk_getattr_raising_keyerror():
    """hasattr(exp, "update_metadata") must not be used directly: the real
    SDK's __getattr__ raises KeyError, which hasattr() does not catch, and
    would otherwise blow up finalize_eval_run (caught only by the outer
    try/except as a warning, never crashing a run, but never attaching
    metadata either). This must resolve cleanly with no warning/log call."""
    exp = _KeyErrorGetattrExperiment()
    with patch("evals.braintrust_experiment._active_experiment", exp):
        with patch("evals.braintrust_experiment.logger") as mock_logger:
            finalize_eval_run(
                {
                    "run_id": "run-1",
                    "performance": {"cost_usd_est_total": 0.01},
                    "duration_s": 12.0,
                    "metrics": {"n": 2, "errors": 0},
                    "params": {"decode_profile": "qwen3-8b"},
                }
            )
    mock_logger.warning.assert_not_called()
    mock_logger.info.assert_called_once()
    assert mock_logger.info.call_args.args[0] == "braintrust_experiment_finalized"


def test_finalize_eval_run_calls_update_metadata_when_sdk_supports_it():
    exp = MagicMock()
    with patch("evals.braintrust_experiment._active_experiment", exp):
        finalize_eval_run(
            {
                "run_id": "run-1",
                "performance": {"cost_usd_est_total": 0.01},
                "duration_s": 12.0,
                "metrics": {"n": 2, "errors": 0},
                "params": {"decode_profile": "qwen3-8b"},
            }
        )
    exp.update_metadata.assert_called_once()
    call_kwargs = exp.update_metadata.call_args.args[0]
    assert call_kwargs["cost_usd_est_total"] == 0.01
    assert call_kwargs["n"] == 2


def test_finalize_eval_run_noop_without_active_experiment():
    with patch("evals.braintrust_experiment._active_experiment", None):
        finalize_eval_run({"run_id": "run-1"})  # must not raise


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


def test_sync_full_corpus_dataset_covers_both_splits_and_is_idempotent_by_id():
    """The full HF corpus (train + test) must land in the Braintrust
    Dataset keyed by the stable case id -- re-running upserts in place
    instead of duplicating rows, and no raw document text is sent."""
    train_cases = [
        {
            "id": "corpus:ground_truth:train:a.txt",
            "filename": "a.txt",
            "text": "SECRET DOCUMENT BODY",
            "expected_doc_class": "contract",
            "split": "train",
        }
    ]
    test_cases = [
        {
            "id": "corpus:ground_truth:test:b.txt",
            "filename": "b.txt",
            "text": "ANOTHER SECRET BODY",
            "expected_doc_class": "insurance_claim",
            "split": "test",
        }
    ]
    prov_train = {"revision": "deadbeef12345678", "repo": "Lucius-Morningstar/mailroom-dataset"}
    prov_test = {"revision": "deadbeef12345678", "repo": "Lucius-Morningstar/mailroom-dataset"}

    fake_dataset = MagicMock()

    def _load_cases(subset, **_kw):
        return (train_cases, prov_train) if subset == "full" else (test_cases, prov_test)

    with patch("evals.cases.load_cases", side_effect=_load_cases):
        with patch("braintrust.init_dataset", return_value=fake_dataset) as init_ds:
            result = sync_full_corpus_dataset(project="mailroom-evals")

    assert result == {
        "project": "mailroom-evals",
        "dataset": "mailroom-hf-deadbeef",
        "rows_train": 1,
        "rows_test": 1,
        "rows_total": 2,
        "revision": "deadbeef12345678",
    }
    init_ds.assert_called_once_with(project="mailroom-evals", name="mailroom-hf-deadbeef")
    assert fake_dataset.insert.call_count == 2
    ids = {c.kwargs["id"] for c in fake_dataset.insert.call_args_list}
    assert ids == {"corpus:ground_truth:train:a.txt", "corpus:ground_truth:test:b.txt"}
    for call in fake_dataset.insert.call_args_list:
        assert "SECRET" not in str(call.kwargs["input"])
        assert call.kwargs["input"]["case_ref"]
    fake_dataset.flush.assert_called_once()
