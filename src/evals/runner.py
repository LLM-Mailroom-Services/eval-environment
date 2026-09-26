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

import json
import subprocess
import time
from datetime import UTC
from pathlib import Path
from typing import Any

import structlog

from . import (
    comparison_report,
    decode_budget,
    experiment_log,
    scoring,
    tracing,
)
from . import invoke as invoke_mod
from .cases import load_cases
from .openrouter_roster import apply_model_override, validate_model_slug
from .preflight import run_preflight
from .prompts import registry as prompts_registry
from .registry import AGENT_CATALOG, TaskSpec, get_task
from .tasks.base import read_subset_manifest, write_scoring_suite, write_subset_manifest

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
    # Calibration tasks alias their eval node's scorer (same node, decision-
    # focused analysis downstream in evals.calibration.*) — the per-case
    # score surface is the node's own.
    scorer = _CALIBRATION_SCORER_ALIAS.get(scorer, scorer)
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


# Calibration scorer names → the eval scorer they reuse per case.
_CALIBRATION_SCORER_ALIAS: dict[str, str] = {
    "calibration_classify": "classification",
    "calibration_judge": "judge",
    "calibration_arbiter": "arbiter",
    "calibration_retry": "extraction",
    "calibration_boss": "boss",
    "calibration_intake": "intake",
    "calibration_archivist": "archivist",
}


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
    prompt_source: str = "frozen",
    concurrency: int = 1,
    run_dir: Path | None = None,
    dry_run: bool = False,
    pilot: bool = False,
    resume_run_id: str | None = None,
    require_trace_sink: bool = False,
    skip_preflight: bool = False,
    decode_profile: str | None = None,
) -> RunResult:
    """Execute one task. Returns the run summary + per-case rows."""
    spec = get_task(task_id)
    subset = subset or spec.default_subset

    # Preflight BEFORE any corpus load / prompt injection / LLM spend.
    # Real mode hard-fails on missing credentials, bad model/prompt/subset,
    # or an explicitly requested Braintrust sink without a key.
    preflight_report = None
    if not skip_preflight:
        preflight_report = run_preflight(
            spec,
            mock=mock,
            invoke_mode=invoke_mode,
            subset=subset,
            model=model,
            prompt_version=prompt_version,
            prompt_source=prompt_source,
            trace_backend=trace_backend,
            require_trace_sink=require_trace_sink,
        )
        if not preflight_report.ok:
            # Non-negotiable #1: every run logs — including failures. A
            # preflight-blocked run writes a failed run-summary line before
            # raising, so `--task all` storms stay visible in the log.
            _log_preflight_failure(spec, preflight_report, mock=mock)
        preflight_report.raise_if_failed()

    if invoke_mode == "agent" and not spec.supports_agent_mode:
        raise ValueError(f"task {spec.task_id} does not support agent-mode invocation")
    if model:
        validate_model_slug(model)
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

    # Prompt lineage: resolve + inject BEFORE any agent instantiation.
    # Default = the frozen mailroom-evals-v1 seed; --prompt-version pins an
    # explicit key; --prompt-source live-docclass|production opts out.
    prompt_keys: dict[str, str] = {}
    prompt_overrides: dict[str, str] = {}
    if prompt_version:
        from .prompts.lineage import resolve

        resolved = resolve(prompt_version)
        role = prompt_version.rsplit("_v", 1)[0]
        prompt_overrides[role] = resolved.key
        if resolved.lineage not in ("frozen", "mutation"):
            prompt_source = "live-docclass" if resolved.lineage == "live-docclass" else prompt_source
    prompt_keys = prompts_registry.activate(prompt_source, prompt_overrides)
    prompt_snapshot = prompts_registry.resolved_snapshot(prompt_keys)
    prompt_lineage = (
        "mutation" if any(v["lineage"] == "mutation" for v in prompt_snapshot.values())
        else prompt_source
    )
    # Injection stays active for the whole run (mock AND real): with
    # Braintrust/Phoenix as the provider, get_managed_prompt resolves the
    # local fallback path — exactly what activate() patched.

    # Resume: skip cases already recorded in a previous (interrupted) run and
    # append to that run's case file instead of starting a new run id.
    prior_ids: set[str] = set()
    if resume_run_id:
        prior = experiment_log.load_cases(resume_run_id)
        prior_ids = {row.get("case_id") for row in prior if row.get("case_id")}
        cases = [case for case in cases if case["id"] not in prior_ids]
        run_dir = run_dir or (experiment_log.experiments_dir() / resume_run_id)
        if not cases and not dry_run:
            # No-op resume: every case is already recorded. Appending another
            # summary line would fabricate a {"n": 0, "errors": 0} "success"
            # under the same run_id — report and stop instead.
            logger.info(
                "evals_resume_noop",
                run_id=resume_run_id,
                skipped_already_run=len(prior_ids),
            )
            return RunResult(
                {
                    "run_id": resume_run_id,
                    "noop_resume": True,
                    "skipped_already_run": len(prior_ids),
                },
                [],
            )
    if dry_run:
        cases = cases[:1]

    run_id = resume_run_id or experiment_log.new_run_id(spec.family, spec.name)
    effective_run_dir = run_dir or (experiment_log.experiments_dir() / run_id)
    effective_run_dir.mkdir(parents=True, exist_ok=True)
    (effective_run_dir / "wave_lock.json").write_text(
        json.dumps(
            {
                "task": spec.name,
                "task_id": spec.task_id,
                "model": model or DEFAULT_MODEL,
                "decode_profile": decode_profile,
                "prompt_version": prompt_version,
                "prompt_source": prompt_source,
                "sample": sample,
                "seed": seed,
                "subset": subset,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Lock the exact case set BEFORE any LLM spend (reproducibility).
    # On resume the manifest already exists in the run dir and is the locked
    # FULL case set — never truncate it with the not-yet-run remainder
    # (a partial resume used to overwrite it); read it back instead.
    if resume_run_id:
        subset_lock = read_subset_manifest(effective_run_dir)
    else:
        subset_lock = write_subset_manifest(
            cases,
            run_dir=effective_run_dir,
            provenance={**dataset_prov, "subset": subset, "seed": seed, "sample": sample, "n": n},
        )

    # Decode-profile state is declared before the summary so both the params
    # block and the execution block see it.
    thinking_recovered = 0
    budget_applied_outer: dict[str, Any] | None = None
    budget = decode_budget.get_profile(decode_profile)

    summary: dict[str, Any] = {
        "run_id": run_id,
        "family": spec.family,
        "task": spec.name,
        "invoke": invoke_mode,
        "mode": "mock" if mock else "real",
        "model": model or DEFAULT_MODEL,
        "prompt_version": prompt_version or (prompt_keys.get(spec.name.split(":")[0]) if prompt_keys else None),
        "prompt_lineage": prompt_lineage,
        "prompt_source": prompt_source,
        "prompt_versions": prompt_snapshot,
        "trace_backend": backend,
        "started_at": experiment_log.utc_now(),
        "preflight": preflight_report.as_dict() if preflight_report else None,
        "task_framing": (preflight_report.framing if preflight_report else None),
        "params": {
            "concurrency": concurrency,
            "sample": sample,
            "seed": seed,
            "n": n,
            "dry_run": dry_run,
            "scorer": spec.scorer,
            "resumed_from": resume_run_id,
            "skipped_already_run": len(prior_ids),
            "decode_profile": decode_profile,
            "decode_budget_applied": budget_applied_outer,
            "thinking_recovered": thinking_recovered,
        },
        "dataset": {
            **dataset_prov,
            "subset": subset,
            "repo": dataset_prov.get("repo"),
            "case_ids": subset_lock.get("case_ids"),
            "filenames": subset_lock.get("filenames"),
            "subset_manifest_path": subset_lock.get("manifest_json"),
            "subset_manifest_jsonl": subset_lock.get("manifest_jsonl"),
        },
    }

    case_rows: list[dict[str, Any]] = []
    error: str | None = None
    try:
        if not dry_run:
            with apply_model_override(model):
                with decode_budget.apply_decode_budget(budget) as budget_applied:
                    # NOTE: the applied map is captured AFTER the block (below)
                    # — config merges populate it lazily during execution.
                    with invoke_mod.Isolation():
                        tracing.apply_provider_env(backend)
                        if mock:
                            invoke_mod.install_mocks()
                        tracing.configure(backend)
                        bt_experiment: dict[str, Any] | None = None
                        if backend == "braintrust":
                            from .braintrust_experiment import begin_eval_run, end_eval_run, experiments_enabled

                            if experiments_enabled(mock, backend):
                                bt_experiment = begin_eval_run(
                                    run_id=run_id,
                                    task_id=spec.task_id,
                                    cases=cases,
                                    dataset_prov={**dataset_prov, **(summary.get("dataset") or {})},
                                    run_metadata=run_meta_stub(spec, summary),
                                )
                                if bt_experiment:
                                    summary["braintrust_experiment"] = bt_experiment
                        try:
                            case_rows = _execute_cases(
                                spec, cases, invoke_mode=invoke_mode, backend=backend,
                                mock=mock, model=model, prompt_version=prompt_version,
                                summary=summary,
                                run_dir=effective_run_dir,
                                run_id=run_id,
                            )
                            # Granite thinking envelopes zero cases at the JSON
                            # parse (issue #18 §4); strip + re-parse any
                            # _parse_error predictions before scoring.
                            for row in case_rows:
                                recovered_pred, did = decode_budget.recover_prediction(
                                    (row.get("prediction") or {})
                                    if isinstance(row.get("prediction"), dict) else None
                                )
                                if did and recovered_pred is not None:
                                    # Case rows carry the expected_* fields, so
                                    # they double as the scoring `case` argument.
                                    row["prediction"] = recovered_pred
                                    row["scores"] = _score_case(spec.name, spec.scorer, row, recovered_pred)
                                    thinking_recovered += 1
                        finally:
                            pass  # Braintrust finalize+flush after run summary is built
                        # Off-path writes (relations daemon, async-deferred audit/catalog
                        # coroutines) must land inside the isolated base dir — drain
                        # before the env is restored, for every task.
                        invoke_mod.drain_daemons(1.0 if spec.name == "pipeline_chain" else 0.5)
                    # Capture AFTER execution: the applied map fills lazily as
                    # agents consult the merged load_config during the run.
                    budget_applied_outer = dict(budget_applied)
                    # params dict was built pre-run — re-bind the final map.
                    summary["params"]["decode_budget_applied"] = budget_applied_outer
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        logger.exception("evals_run_failed", task=spec.task_id)
    finally:
        prompts_registry.deactivate()
        tracing.flush(backend)
        summary["flush"] = _flush_health(backend)

    summary["finished_at"] = experiment_log.utc_now()
    summary["duration_s"] = round(time.time() - started, 1)
    summary["error"] = error
    summary["metrics"] = scoring.summarize_scores(case_rows) if case_rows else {"n": 0, "errors": 0}
    summary["performance"] = scoring.summarize_performance(case_rows) if case_rows else {}
    if not summary["model"]:
        # Provenance: the model that actually dominated the run's token spend
        # (agent models resolve per-agent from the pipeline taxonomy).
        by_agent = (summary["performance"] or {}).get("by_agent") or {}
        dominant = max(
            by_agent.items(),
            key=lambda kv: kv[1].get("total_tokens") or 0,
            default=(None, {}),
        )[0]
        summary["model"] = ((by_agent.get(dominant) or {}).get("models") or [None])[0]
    trace_ids = _trace_ids(backend) or {}
    if summary.get("braintrust_experiment"):
        trace_ids = {**trace_ids, **summary["braintrust_experiment"]}
    summary["trace_ids"] = trace_ids or None
    summary["pipeline_git"] = _pipeline_git()
    summary["prompts_snapshot_path"] = _write_prompts_snapshot(summary, effective_run_dir)
    if case_rows:
        # Full scoring suite artifact (all deterministic keys). Sink spans carry
        # ESSENTIAL_SCORES only; this file + case rows are the complete surface.
        summary["scoring_suite"] = write_scoring_suite(
            case_rows,
            run_dir=effective_run_dir,
            scorer=spec.scorer,
            essential_on_sink=scoring.essential_rollup(spec.scorer, case_rows),
        )
    if spec.family == "calibration" and not error:
        summary["calibration"] = _calibration_block(spec, case_rows)

    # Run-level rollup span: the sink's per-run dashboard entry (essential
    # aggregates only). Emitted even on run error, so the sink shows the run.
    perf = summary.get("performance") or {}
    with tracing.run_span(backend, run_meta={**run_meta_stub(spec, summary)}) as span:
        span.set_output({
            "metrics": {k: summary["metrics"].get(k) for k in _essential_keys(spec)},
            "performance": perf,
            "duration_s": summary.get("duration_s"),
            "cost_usd_est_total": perf.get("cost_usd_est_total"),
            "cost_cap": summary.get("cost_cap"),
            "error": error,
        })
        rollup = scoring.essential_rollup(spec.scorer, case_rows)
        span.set_metrics({
            **scoring.sink_score_metrics(spec.scorer, rollup, max_scores=scoring.SINK_SCORE_METRICS_MAX),
            **({"ece": summary["calibration"]["ece"]}
               if isinstance(summary.get("calibration"), dict) and isinstance(summary["calibration"].get("ece"), (int, float)) else {}),
            **(
                {
                    "duration_s": float(summary["duration_s"]),
                    "cost_usd_est_total": float(perf["cost_usd_est_total"]),
                }
                if isinstance(summary.get("duration_s"), (int, float))
                and isinstance(perf.get("cost_usd_est_total"), (int, float))
                else {}
            ),
        })

    if backend == "braintrust" and summary.get("braintrust_experiment") and not dry_run:
        from .braintrust_experiment import end_eval_run, finalize_eval_run

        finalize_eval_run(summary)
        end_eval_run()

    # Comparison report (Modal-comparable, filed by model): emitted whenever a
    # decode profile drove the run and cases executed; never fails the run.
    if budget and case_rows and not dry_run:
        try:
            summary["params"]["decode_sampling"] = budget.get("sampling")
            summary["params"]["decode_call_timeout_s"] = budget.get("call_timeout_s")
            cap = comparison_report.cap_status(summary, budget)
            if cap:
                summary["cost_cap"] = cap
            report_file = comparison_report.write_report(summary, case_rows)
            summary["comparison_report"] = str(report_file) if report_file else None
        except Exception as exc:  # report is auxiliary — log and move on
            logger.warning("comparison_report_failed", task=spec.task_id, error=str(exc))
            summary["comparison_report"] = None

    written = experiment_log.write_run(summary, case_rows, run_dir=effective_run_dir)
    try:
        experiment_log.write_markdown()
    except Exception:
        logger.warning("evals_markdown_render_failed", exc_info=True)
    return RunResult(written, case_rows)


def _essential_keys(spec: TaskSpec) -> list[str]:
    return list(scoring.ESSENTIAL_SCORES.get(scoring.essential_scorer(spec.scorer), ()))


def _log_preflight_failure(
    spec: TaskSpec, report: Any, *, mock: bool
) -> None:
    """Append a failed run-summary line for a preflight-blocked run.

    Non-negotiable #1: every run logs — including failures. Preflight fires
    before the run try/except, so without this a blocked task (e.g. a missing
    real-mode credential across a ``--task all`` sweep) would be invisible in
    ``reports/experiment_log.jsonl``. Best-effort: a logging failure must not
    mask the original preflight error.
    """
    try:
        now = experiment_log.utc_now()
        run_id = experiment_log.new_run_id(spec.family, spec.name)
        summary: dict[str, Any] = {
            "run_id": run_id,
            "family": spec.family,
            "task": spec.name,
            "invoke": None,
            "mode": "mock" if mock else "real",
            "model": None,
            "trace_backend": "none",
            "started_at": now,
            "finished_at": now,
            "preflight": report.as_dict(),
            "params": {"blocked_by": "preflight"},
            "dataset": {"subset": report.resolved.get("subset"), "n_selected": 0},
            "metrics": {"n": 0, "errors": 0},
            "performance": {},
            "error": f"PreflightError: {'; '.join(f'{i.code}: {i.message}' for i in report.errors)}",
        }
        experiment_log.write_run(summary, [], run_dir=experiment_log.experiments_dir() / run_id)
        logger.warning("evals_preflight_failure_logged", run_id=run_id, task=spec.task_id)
    except Exception:
        logger.warning("evals_preflight_failure_log_failed", task=spec.task_id, exc_info=True)


def _flush_health(backend: str) -> dict[str, Any] | None:
    """Affirmative flush counters for the run record (dropped-event evidence)."""
    if backend not in ("braintrust", "phoenix"):
        return None
    try:
        from observability.tracing import flush_health

        return dict(flush_health())
    except Exception:
        return None


def _pipeline_git() -> str | None:
    """The llm-mailroom package's git commit (prompt provenance anchor)."""
    try:
        import pipeline

        pipeline_root = Path(pipeline.__file__).resolve().parents[2]
        out = subprocess.run(
            ["git", "-C", str(pipeline_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        return out.stdout.strip() or None
    except Exception:
        return None


def _write_prompts_snapshot(summary: dict[str, Any], run_dir: Path | None) -> str | None:
    """Persist the exact rendered prompts used by this run (reproducibility
    without any prompt-management service)."""
    try:
        from .prompts.lineage import resolve

        target_dir = run_dir or (experiment_log.experiments_dir() / summary["run_id"])
        target_dir.mkdir(parents=True, exist_ok=True)
        snapshot: dict[str, Any] = {
            "run_id": summary["run_id"],
            "prompt_lineage": summary.get("prompt_lineage"),
            "prompt_source": summary.get("prompt_source"),
            "pipeline_git": summary.get("pipeline_git"),
            "prompts": {},
        }
        for role, meta in (summary.get("prompt_versions") or {}).items():
            version = resolve(meta["key"])
            snapshot["prompts"][role] = {**meta, "text": version.text}
        path = target_dir / "prompts_snapshot.json"
        path.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
        return str(path)
    except Exception:
        logger.warning("evals_prompts_snapshot_failed", exc_info=True)
        return None


def run_meta_stub(spec: TaskSpec, summary: dict[str, Any]) -> dict[str, Any]:
    """Run-level metadata for the rollup span (mirrors per-case run_meta)."""
    return {
        "run_id": summary["run_id"],
        "task": spec.task_id,
        "family": spec.family,
        "invoke": summary["invoke"],
        "mode": summary["mode"],
        "model": summary["model"] or "pipeline-default",
        "prompt_version": summary.get("prompt_version") or _primary_prompt_key(spec, summary),
        "prompt_lineage": summary.get("prompt_lineage"),
        "dataset.config": summary["dataset"].get("config"),
        "dataset.split": summary["dataset"].get("split"),
        "dataset.revision": summary["dataset"].get("revision"),
        "subset": summary["dataset"].get("subset"),
        "tags": [spec.family, spec.name, summary["mode"], "run-rollup"],
    }


def _specialist_name(spec: TaskSpec, agent_usage: dict[str, Any] | None) -> str | None:
    """The specialist that evaluated this document (one agent per extraction case)."""
    catalog = AGENT_CATALOG.get(spec.node_name) or {}
    specialists = list(catalog.get("agents") or [])
    usage = agent_usage or {}
    hits = [name for name in specialists if name in usage]
    if len(hits) == 1:
        return hits[0]
    if hits:
        return hits[0]
    task_map = {
        "contracts": "contracts_specialist",
        "merger_agreement": "merger_agreement_specialist",
        "corporate_records": "corporate_records_specialist",
        "correspondence": "correspondence_specialist",
        "insurance_claims": "insurance_claims_specialist",
    }
    return task_map.get(spec.name)


def _primary_prompt_key(spec: TaskSpec, summary: dict[str, Any]) -> str | None:
    """The task's primary agent-role prompt key (span metadata provenance).

    ``summary["prompt_version"]`` only carries an explicit --prompt-version
    override; the per-role snapshot (prompt_versions) is what actually ran.
    """
    versions = summary.get("prompt_versions") or {}
    catalog = AGENT_CATALOG.get(spec.node_name) or {}
    for role in catalog.get("agents") or []:
        slot = versions.get(role)
        if isinstance(slot, dict) and slot.get("key"):
            return slot["key"]
    return None


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
    run_dir: Path | None = None,
    run_id: str | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    run_meta = {
        "run_id": summary["run_id"],
        "task": spec.task_id,
        "family": spec.family,
        "invoke": invoke_mode,
        "mode": summary["mode"],
        "model": model or summary["model"] or "pipeline-default",
        "prompt_version": summary.get("prompt_version") or _primary_prompt_key(spec, summary),
        "prompt_lineage": summary.get("prompt_lineage"),
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
            recovered_pred, recovered = decode_budget.recover_prediction(
                prediction if isinstance(prediction, dict) else None
            )
            if recovered and recovered_pred is not None:
                prediction = recovered_pred
                summary["params"]["thinking_recovered"] = int(
                    summary.get("params", {}).get("thinking_recovered") or 0
                ) + 1
            scores = {} if error else _score_case(spec.name, spec.scorer, case, prediction)
            usage = _last_usage()
            case_model = model or next(
                (m for slot in (usage or {}).get("by_agent", {}).values() for m in slot.get("models", [])),
                None,
            )
            if case_model:
                span.update_metadata({"model": case_model})
            perf = scoring.performance_row(latency, usage, case_model)
            span.set_output({"scores": scores, "error": error})
            # Span metrics: essentials; Braintrust experiment: one fully scored document row.
            span.set_metrics(scoring.essential_metrics(spec.scorer, scores))
            agent_usage = _agent_usage()
            specialist = _specialist_name(spec, agent_usage)
            tokens = {
                "prompt": perf["prompt_tokens"],
                "completion": perf["completion_tokens"],
                "total": perf["total_tokens"],
            }
            if backend == "braintrust":
                from .braintrust_experiment import log_case_scores

                log_case_scores(
                    case,
                    scorer=spec.scorer,
                    scores=scores,
                    error=error,
                    prediction=prediction if isinstance(prediction, dict) else None,
                    specialist=specialist,
                    latency_ms=perf["latency_ms"],
                    cost_usd=perf["cost_usd_est"],
                    tokens=tokens,
                )
            case_trace = getattr(span, "trace_ref", None)
        rows.append(
            {
                "case_id": case.get("id"),
                "filename": case.get("filename"),
                "specialist": specialist,
                "expected_doc_class": case.get("expected_doc_class"),
                "expected_subclass": case.get("expected_subclass"),
                "review_expected": case.get("review_expected"),
                "retry_expected": case.get("retry_expected"),
                "fixture_kind": case.get("fixture_kind"),
                "fixture_cell": case.get("calibration_cell"),
                "fixture_outcome": case.get("arbiter_outcome"),
                "failure_stage": case.get("failure_stage"),
                # sha256 of the exact text judged — enables verified post-hoc
                # text re-load from the pinned corpus (lean logs, full fidelity).
                "doc_text_sha256": scoring.sha256_text(str(case.get("text") or "")),
                "prediction": prediction or None,
                "scores": scores,
                "latency_ms": perf["latency_ms"],
                "tokens": tokens,
                "cost_usd": perf["cost_usd_est"],
                # per-agent token/call attribution for this case (the
                # accumulator's by_agent map — every agent that fired)
                "agent_usage": _agent_usage(),
                "trace": case_trace,
                "error": error,
            }
        )
        if run_dir is not None and run_id and not mock:
            experiment_log.append_case_row(run_dir, run_id, rows[-1])
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


def _agent_usage() -> dict[str, Any]:
    """Per-agent usage for the current case (the accumulator's by_agent map,
    with the ``unattributed`` bucket kept only when it is the sole content)."""
    usage = _last_usage() or {}
    by_agent = usage.get("by_agent") or {}
    if not by_agent:
        return {}
    if set(by_agent) == {"unattributed"}:
        return {}  # nothing agent-attributed to report
    return {agent: slot for agent, slot in by_agent.items()}
