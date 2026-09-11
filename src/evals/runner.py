"""Shared runner — executes any registered task spec end-to-end.

Pipeline per run: resolve trace backend → isolate MAILROOM_BASE_DIR →
install mocks (mock mode) → load cases for the subset → per case: span,
invoke (node|agent), score, performance → summarize → append to the
centralized experiment log → write the run report (JSON + MD).

Mock runs force tracing to ``none`` unless a backend was explicitly
requested (mocked clients are not wrappable). Tracing failures never fail
a run; they log warnings and surface in ``flush_health``.
"""

from __future__ import annotations

import time
from datetime import UTC
from pathlib import Path
from typing import Any

import structlog

from . import experiment_log, scoring, tracing
from . import invoke as invoke_mod
from .cases import load_cases
from .registry import TaskSpec, get_task

logger = structlog.get_logger(__name__)

DEFAULT_MODEL = None  # resolved from the pipeline's provider registry at invoke time


class RunResult:
    def __init__(self, summary: dict[str, Any], case_rows: list[dict[str, Any]]) -> None:
        self.summary = summary
        self.case_rows = case_rows

    @property
    def run_id(self) -> str:
        return self.summary["run_id"]


def _score_case(task: str, scorer: str, case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    doc_class = str(case.get("expected_doc_class") or "")
    if scorer == "intake":
        return scoring.score_intake(prediction, case)
    if scorer == "classification":
        out = scoring.score_classification(prediction.get("doc_type"), case.get("expected_doc_class"))
        out.update(scoring.score_subclass(
            prediction.get("doc_subclass") or prediction.get("contract_subtype"),
            case.get("expected_subclass"),
        ))
        return out
    if scorer == "extraction":
        out = scoring.score_extraction(doc_class, prediction.get("extracted_data") or prediction, case.get("expected_fields") or {})
        for key in ("cuad_clause_labels", "maud_clause_labels"):
            out.update(scoring.score_label_lists(
                prediction.get("extracted_data") or prediction,
                case.get("expected_fields") or {},
                key,
            ))
        return out
    if scorer == "judge":
        return scoring.score_judge(prediction, case)
    if scorer == "arbiter":
        return scoring.score_arbiter(prediction, case)
    if scorer == "boss":
        expected = "review" if case.get("review_expected") else None
        return scoring.score_decision(prediction.get("decision"), valid=("approved", "review"), expected=expected)
    if scorer == "archivist":
        return scoring.score_archivist(prediction, case)
    if scorer == "pipeline":
        return scoring.score_pipeline(prediction, case)
    return {}


def run_task(
    task_id: str,
    *,
    invoke_mode: str = "node",
    subset: str | None = None,
    sample: int | None = None,
    seed: int = 42,
    n: int | None = None,
    mock: bool = False,
    trace_backend: str | None = None,
    model: str | None = None,
    prompt_version: str | None = None,
    concurrency: int = 1,
    run_dir: Path | None = None,
    dry_run: bool = False,
    pilot: bool = False,
    resume_run_id: str | None = None,
) -> RunResult:
    """Execute one task. Returns the run summary + per-case rows."""
    spec = get_task(task_id)
    if invoke_mode == "agent" and not spec.supports_agent_mode:
        raise ValueError(f"task {spec.task_id} does not support agent-mode invocation")
    subset = subset or spec.default_subset
    backend = tracing.resolve_backend(trace_backend)
    if mock and trace_backend is None:
        backend = "none"  # mocked clients are not wrappable; keep CI hermetic
    started = time.time()

    if pilot:
        from .pilot import pilot_cases

        cases, dataset_prov = pilot_cases(task_id, seed=seed)
        subset = f"pilot-preset({subset})"
    else:
        cases, dataset_prov = load_cases(subset, sample=sample, seed=seed, n=n)

    # Resume: skip cases already recorded in a previous (interrupted) run and
    # append to that run's case file instead of starting a new run id.
    prior_ids: set[str] = set()
    if resume_run_id:
        prior = experiment_log.load_cases(resume_run_id)
        prior_ids = {row.get("case_id") for row in prior if row.get("case_id")}
        cases = [case for case in cases if case["id"] not in prior_ids]
        run_dir = run_dir or (experiment_log.experiments_dir() / resume_run_id)
    if dry_run:
        cases = cases[:1]

    summary: dict[str, Any] = {
        "run_id": resume_run_id or experiment_log.new_run_id(spec.family, spec.name),
        "family": spec.family,
        "task": spec.name,
        "invoke": invoke_mode,
        "mode": "mock" if mock else "real",
        "model": model or DEFAULT_MODEL,
        "prompt_version": prompt_version,
        "trace_backend": backend,
        "started_at": experiment_log.utc_now(),
        "params": {
            "concurrency": concurrency,
            "sample": sample,
            "seed": seed,
            "n": n,
            "dry_run": dry_run,
            "scorer": spec.scorer,
            "resumed_from": resume_run_id,
            "skipped_already_run": len(prior_ids),
        },
        "dataset": {
            **dataset_prov,
            "subset": subset,
            "repo": dataset_prov.get("repo"),
        },
    }

    case_rows: list[dict[str, Any]] = []
    error: str | None = None
    try:
        if not dry_run:
            with invoke_mod.Isolation():
                tracing.apply_provider_env(backend)
                if mock:
                    invoke_mod.install_mocks()
                tracing.configure(backend)
                case_rows = _execute_cases(
                    spec, cases, invoke_mode=invoke_mode, backend=backend,
                    mock=mock, model=model, prompt_version=prompt_version,
                    summary=summary,
                )
                # Off-path writes (relations daemon, async-deferred audit/catalog
                # coroutines) must land inside the isolated base dir — drain
                # before the env is restored, for every task.
                invoke_mod.drain_daemons(1.0 if spec.name == "pipeline_chain" else 0.5)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        logger.exception("evals_run_failed", task=spec.task_id)
    finally:
        tracing.flush(backend)

    summary["finished_at"] = experiment_log.utc_now()
    summary["duration_s"] = round(time.time() - started, 1)
    summary["error"] = error
    summary["metrics"] = scoring.summarize_scores(case_rows) if case_rows else {"n": 0, "errors": 0}
    summary["performance"] = scoring.summarize_performance(case_rows) if case_rows else {}
    summary["trace_ids"] = _trace_ids(backend)
    if spec.family == "calibration" and not error:
        summary["calibration"] = _calibration_block(spec, case_rows)

    written = experiment_log.write_run(summary, case_rows, run_dir=run_dir)
    try:
        experiment_log.write_markdown()
    except Exception:
        logger.warning("evals_markdown_render_failed", exc_info=True)
    return RunResult(written, case_rows)


def _calibration_block(spec: TaskSpec, case_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Run the node's calibration analyzer over the case rows + write the report."""
    from datetime import datetime

    from .calibration import arbiter, archivist, boss, classify, intake, judge, retry

    analyzers = {
        "calibration_classify": classify,
        "calibration_judge": judge,
        "calibration_arbiter": arbiter,
        "calibration_retry": retry,
        "calibration_boss": boss,
        "calibration_intake": intake,
        "calibration_archivist": archivist,
    }
    module = analyzers.get(spec.scorer)
    if module is None:
        return {}
    try:
        analysis = module.analyze(case_rows)
    except Exception:
        logger.exception("calibration_analyze_failed", task=spec.task_id)
        return {"error": "analyzer failed — see logs"}
    analysis["generated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    analysis["n_cases"] = len(case_rows)
    analysis["errors"] = sum(1 for r in case_rows if r.get("error"))
    try:
        json_path, md_path = _write_calibration_report(spec.name, analysis)
        analysis["report_paths"] = {"json": str(json_path), "md": str(md_path)}
    except Exception:
        logger.warning("calibration_report_write_failed", task=spec.task_id, exc_info=True)
    return analysis


def _write_calibration_report(task: str, analysis: dict[str, Any]):
    from .calibration.base import write_report

    return write_report(task, analysis)


def _trace_ids(backend: str) -> dict[str, Any] | None:
    if backend == "none":
        return None
    out: dict[str, Any] = {"backend": backend}
    if backend == "braintrust":
        import os

        out["project"] = os.environ.get("BRAINTRUST_PROJECT", "mailroom")
    elif backend == "phoenix":
        import os

        out["endpoint"] = os.environ.get("PHOENIX_ENDPOINT", "http://localhost:6006/v1/traces")
        out["project"] = os.environ.get("PHOENIX_PROJECT", "mailroom-evals")
    return out


def _execute_cases(
    spec: TaskSpec,
    cases: list[dict[str, Any]],
    *,
    invoke_mode: str,
    backend: str,
    mock: bool,
    model: str | None,
    prompt_version: str | None,
    summary: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    run_meta = {
        "run_id": summary["run_id"],
        "task": spec.task_id,
        "family": spec.family,
        "invoke": invoke_mode,
        "mode": summary["mode"],
        "model": model or summary["model"] or "pipeline-default",
        "prompt_version": prompt_version,
        "dataset.config": summary["dataset"].get("config"),
        "dataset.split": summary["dataset"].get("split"),
        "dataset.revision": summary["dataset"].get("revision"),
        "subset": summary["dataset"].get("subset"),
        "tags": [spec.family, spec.name, summary["mode"]],
    }
    for case in cases:
        timer = scoring.Timer()
        error: str | None = None
        prediction: dict[str, Any] = {}
        try:
            from pipeline.limits import reset_run_usage

            reset_run_usage()  # per-case token accounting
        except Exception:
            pass
        with tracing.case_span(backend, node_name=spec.node_name, case=case, run_meta=run_meta) as span:
            try:
                prediction = invoke_mod.invoke(spec.name, case, mode=invoke_mode) or {}
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                logger.warning("evals_case_failed", case=case.get("id"), error=error)
            latency = timer.ms()
            scores = {} if error else _score_case(spec.name, spec.scorer, case, prediction)
            usage = _last_usage()
            perf = scoring.performance_row(latency, usage, model)
            span.set_output({"scores": scores, "error": error})
            span.set_metrics({k: v for k, v in scores.items() if isinstance(v, (int, float))})
        rows.append(
            {
                "case_id": case.get("id"),
                "filename": case.get("filename"),
                "expected_doc_class": case.get("expected_doc_class"),
                "expected_subclass": case.get("expected_subclass"),
                "review_expected": case.get("review_expected"),
                "retry_expected": case.get("retry_expected"),
                "fixture_kind": case.get("fixture_kind"),
                "fixture_cell": case.get("calibration_cell"),
                "fixture_outcome": case.get("arbiter_outcome"),
                "failure_stage": case.get("failure_stage"),
                "prediction": prediction or None,
                "scores": scores,
                "latency_ms": perf["latency_ms"],
                "tokens": {
                    "prompt": perf["prompt_tokens"],
                    "completion": perf["completion_tokens"],
                    "total": perf["total_tokens"],
                },
                "cost_usd": perf["cost_usd_est"],
                "error": error,
            }
        )
        tracing.flush(backend)
    return rows


def _last_usage() -> dict[str, Any] | None:
    """Token usage recorded by the pipeline's run accumulator
    (``pipeline.limits.record_usage`` — every agent call lands there)."""
    try:
        from pipeline.limits import usage_summary

        usage = usage_summary()
        return dict(usage) if usage and usage.get("total") else None
    except Exception:
        return None
