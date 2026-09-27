"""Braintrust Experiments + HF corpus dataset linkage for eval runs.

Keeps the existing Logger (``init_logger``) for nested LLM spans while opening
a per-run Experiment. Dataset-document upserts are intentionally off: Braintrust
rows are specialist (or node) invocations, not corpus documents.

Scoring on Braintrust stays minimal — see ``scoring.sink_score_metrics``.
"""

from __future__ import annotations

import os
from typing import Any

import structlog

from . import scoring
from .tracing import doc_text_sha256, public_case_ref

logger = structlog.get_logger(__name__)

_active_experiment: Any | None = None
_dataset_handle: Any | None = None
_record_id_by_sha: dict[str, str] = {}


def experiments_enabled(mock: bool, backend: str) -> bool:
    if mock or backend != "braintrust":
        return False
    if not os.environ.get("BRAINTRUST_API_KEY"):
        return False
    mode = (os.environ.get("BRAINTRUST_EXPERIMENTS") or "auto").strip().lower()
    if mode in {"0", "false", "off", "none", "disabled"}:
        return False
    if mode in {"1", "true", "on", "enabled"}:
        return True
    return True  # auto: on for real Braintrust eval runs


def current_experiment() -> Any | None:
    return _active_experiment


def dataset_record_id(case: dict[str, Any]) -> str | None:
    return _record_id_by_sha.get(doc_text_sha256(case))


def _dataset_name(revision: str) -> str:
    custom = os.environ.get("BRAINTRUST_DATASET_NAME")
    if custom:
        return custom
    short = (revision or "unknown")[:8]
    return f"mailroom-hf-{short}"


def _dataset_input(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_ref": public_case_ref(case),
        "chars": len(str(case.get("text") or "")),
    }


def _dataset_expected(case: dict[str, Any]) -> dict[str, Any]:
    """Ground truth for the Experiment UI (not copied to live span inputs)."""
    out: dict[str, Any] = {}
    if case.get("expected_doc_class"):
        out["expected_doc_class"] = case.get("expected_doc_class")
    if case.get("expected_subclass"):
        out["expected_subclass"] = case.get("expected_subclass")
    if case.get("expected_fields"):
        out["expected_fields"] = case.get("expected_fields")
    return out


def _dataset_metadata(case: dict[str, Any], prov: dict[str, Any]) -> dict[str, Any]:
    return {
        "hf_repo": prov.get("repo") or prov.get("id") or "Lucius-Morningstar/mailroom-dataset",
        "hf_revision": prov.get("revision"),
        "hf_config": case.get("config") or prov.get("config"),
        "hf_split": case.get("split") or prov.get("split"),
        "filename": case.get("filename"),
        "corpus_case_id": case.get("id"),
    }


def begin_eval_run(
    *,
    run_id: str,
    task_id: str,
    cases: list[dict[str, Any]],
    dataset_prov: dict[str, Any],
    run_metadata: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Open a Braintrust Experiment. Do not insert corpus documents as dataset rows."""
    global _active_experiment, _dataset_handle, _record_id_by_sha
    _active_experiment = None
    _dataset_handle = None
    _record_id_by_sha = {}

    try:
        import braintrust
    except Exception:
        logger.warning("braintrust_experiment_import_failed", exc_info=True)
        return None

    project = os.environ.get("BRAINTRUST_PROJECT", "mailroom")
    revision = str(dataset_prov.get("revision") or "")
    ds_name = _dataset_name(revision)

    try:
        meta = dict(run_metadata or {})
        meta.setdefault("hf_repo", dataset_prov.get("repo"))
        meta.setdefault("hf_revision", revision)
        meta.setdefault("hf_dataset_name", ds_name)
        meta["dataset_rows"] = "off"

        _active_experiment = braintrust.init(
            project=project,
            experiment=run_id,
            description=f"mailroom-evals {task_id}",
            metadata=meta,
            tags=[task_id, "mailroom-evals"],
        )
        logger.info(
            "braintrust_experiment_opened",
            project=project,
            experiment=run_id,
            dataset="off",
            n_cases=len(cases),
        )
        return {
            "project": project,
            "experiment": run_id,
            "dataset": None,
            "dataset_records": 0,
        }
    except Exception:
        logger.warning("braintrust_experiment_begin_failed", exc_info=True)
        _active_experiment = None
        return None


def finalize_eval_run(summary: dict[str, Any]) -> None:
    """Record wall time + cost on the Experiment without adding a non-document row."""
    exp = _active_experiment
    if exp is None:
        return
    perf = summary.get("performance") or {}
    duration = summary.get("duration_s")
    cost_total = perf.get("cost_usd_est_total")
    cap = summary.get("cost_cap") or {}
    try:
        extra = {
            "duration_s": duration,
            "cost_usd_est_total": cost_total,
            "cost_cap": cap,
            "n": (summary.get("metrics") or {}).get("n"),
            "errors": (summary.get("metrics") or {}).get("errors"),
            "decode_profile": (summary.get("params") or {}).get("decode_profile"),
        }
        # Prefer metadata merge when the SDK exposes it; never log a fake case.
        if hasattr(exp, "update_metadata"):
            exp.update_metadata(extra)
        logger.info(
            "braintrust_experiment_finalized",
            run_id=summary.get("run_id"),
            duration_s=duration,
            cost_usd_est_total=cost_total,
            cost_cap_status=cap.get("status"),
            document_rows=(summary.get("metrics") or {}).get("n"),
        )
    except Exception:
        logger.warning("braintrust_experiment_finalize_failed", exc_info=True)


def end_eval_run() -> None:
    global _active_experiment, _dataset_handle, _record_id_by_sha
    try:
        from observability.braintrust_setup import flush_braintrust

        flush_braintrust()
    except Exception:
        logger.warning("braintrust_experiment_flush_failed", exc_info=True)
    _active_experiment = None
    _dataset_handle = None
    _record_id_by_sha = {}


def log_case_scores(
    case: dict[str, Any],
    *,
    scorer: str,
    scores: dict[str, Any],
    error: str | None = None,
    prediction: dict[str, Any] | None = None,
    specialist: str | None = None,
    latency_ms: float | None = None,
    cost_usd: float | None = None,
    tokens: dict[str, Any] | None = None,
    span: Any | None = None,
) -> None:
    """Score the existing parent span for this specialist call.

    Must not call ``Experiment.log``: that opens a second row beside
    ``case_span``. Must not tag the row as a document.
    Nested LLM calls stay children of ``span``.
    """
    if span is None or not hasattr(span, "log_document_row"):
        logger.warning(
            "braintrust_experiment_case_log_skipped_no_span",
            case_ref=public_case_ref(case),
        )
        return
    row_scores = scoring.row_score_metrics(scores)
    extracted = None
    if isinstance(prediction, dict):
        extracted = prediction.get("extracted_data") or prediction
    try:
        span.log_document_row(
            output={
                "specialist": specialist,
                "extracted_data": extracted,
                "error": error,
                "scores": scores or {},
            },
            expected=_dataset_expected(case),
            scores=row_scores or None,
            error=error,
            metrics={
                k: float(v)
                for k, v in {
                    "latency_ms": latency_ms,
                    "cost_usd": cost_usd,
                    "prompt_tokens": (tokens or {}).get("prompt"),
                    "completion_tokens": (tokens or {}).get("completion"),
                }.items()
                if isinstance(v, (int, float))
            }
            or None,
            metadata={
                "case_ref": public_case_ref(case),
                "specialist": specialist,
                "scorer": scorer,
                "n_expected_fields": (scores or {}).get("n_expected_fields"),
                "filename": case.get("filename"),
            },
            tags=[t for t in (specialist, scorer) if t],
        )
    except Exception:
        logger.warning("braintrust_experiment_case_log_failed", exc_info=True)
