"""Braintrust Experiments + HF corpus dataset linkage for eval runs.

Keeps the existing Logger (``init_logger``) for nested LLM spans while opening
a per-run Experiment attached to a project Dataset that mirrors the pinned
Hugging Face mailroom corpus. Dataset rows upsert on ``doc_text_sha256`` so
re-runs do not multiply rows.

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
    """Open a Braintrust Experiment linked to the HF corpus dataset."""
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
        _dataset_handle = braintrust.init_dataset(
            project=project,
            name=ds_name,
            description="Pinned Lucius-Morningstar/mailroom-dataset eval rows",
            metadata={
                "hf_repo": dataset_prov.get("repo") or "Lucius-Morningstar/mailroom-dataset",
                "hf_revision": revision,
                "hf_config": dataset_prov.get("config"),
            },
        )
        for case in cases:
            sha = doc_text_sha256(case)
            try:
                rid = _dataset_handle.insert(
                    id=sha,
                    input=_dataset_input(case),
                    expected=_dataset_expected(case),
                    metadata=_dataset_metadata(case, dataset_prov),
                    tags=[
                        t
                        for t in (
                            case.get("split"),
                            case.get("expected_doc_class"),
                            task_id,
                        )
                        if t
                    ],
                )
                _record_id_by_sha[sha] = rid
            except Exception:
                logger.warning("braintrust_dataset_insert_failed", case_ref=public_case_ref(case), exc_info=True)

        meta = dict(run_metadata or {})
        meta.setdefault("hf_repo", dataset_prov.get("repo"))
        meta.setdefault("hf_revision", revision)
        meta.setdefault("hf_dataset_name", ds_name)

        _active_experiment = braintrust.init(
            project=project,
            experiment=run_id,
            description=f"mailroom-evals {task_id}",
            dataset=_dataset_handle,
            metadata=meta,
            tags=[task_id, "mailroom-evals"],
        )
        logger.info(
            "braintrust_experiment_opened",
            project=project,
            experiment=run_id,
            dataset=ds_name,
            n_cases=len(cases),
        )
        return {
            "project": project,
            "experiment": run_id,
            "dataset": ds_name,
            "dataset_records": len(_record_id_by_sha),
        }
    except Exception:
        logger.warning("braintrust_experiment_begin_failed", exc_info=True)
        _active_experiment = None
        return None


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
) -> None:
    """Attach minimal headline scores to the Experiment (quota-safe)."""
    exp = _active_experiment
    if exp is None:
        return
    headline = scoring.sink_score_metrics(scorer, scores)
    if not headline and not error:
        return
    try:
        exp.log(
            input=_dataset_input(case),
            output={"error": error} if error else {"ok": True},
            expected=_dataset_expected(case),
            scores=headline or None,
            error=error,
            dataset_record_id=dataset_record_id(case),
            metadata={"case_ref": public_case_ref(case)},
            allow_concurrent_with_spans=True,
        )
    except Exception:
        logger.warning("braintrust_experiment_case_log_failed", exc_info=True)
