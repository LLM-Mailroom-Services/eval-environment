"""Ground GEPA OBSERVE manifests in the Braintrust specialist trace backlog."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

SPECIALIST_TASKS: frozenset[str] = frozenset(
    {
        "correspondence",
        "insurance_claims",
        "contracts",
        "merger_agreement",
        "corporate_records",
    }
)

SPECIALIST_AGENT: dict[str, str] = {
    "correspondence": "correspondence_specialist",
    "insurance_claims": "insurance_claims_specialist",
    "contracts": "contracts_specialist",
    "merger_agreement": "merger_agreement_specialist",
    "corporate_records": "corporate_records_specialist",
}


def _experiment_name(run: dict[str, Any]) -> str | None:
    trace = run.get("trace_ids") or {}
    if trace.get("backend") != "braintrust":
        return None
    exp = trace.get("experiment")
    if exp:
        return str(exp)
    return run.get("run_id")


def discover_braintrust_specialist_runs(runs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Index real Braintrust specialist eval runs from the experiment log."""
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        if run.get("mode") != "real":
            continue
        task = str(run.get("task") or "")
        if task not in SPECIALIST_TASKS:
            continue
        exp = _experiment_name(run)
        if not exp:
            continue
        by_task[task].append(
            {
                "run_id": run.get("run_id"),
                "task": task,
                "model": run.get("model"),
                "prompt_version": run.get("prompt_version"),
                "experiment": exp,
                "trace_ids": run.get("trace_ids"),
                "metrics": run.get("metrics"),
            }
        )
    for task in by_task:
        by_task[task].sort(key=lambda r: str(r.get("run_id") or ""))
    return dict(by_task)


def _failure_score(ev: dict[str, Any]) -> float | None:
    scores = ev.get("scores") or {}
    overall = scores.get("overall_score")
    if overall is None:
        overall = (ev.get("metrics") or {}).get("overall_score")
    return float(overall) if isinstance(overall, (int, float)) else None


def _is_observe_failure(ev: dict[str, Any]) -> bool:
    if ev.get("error"):
        return True
    overall = _failure_score(ev)
    if overall is not None and overall < 0.8:
        return True
    scores = ev.get("scores") or {}
    return any(
        isinstance(v, (int, float)) and v == 0
        for k, v in scores.items()
        if k.endswith(("_correct", "_agrees", "_valid", "_ok"))
    )


def _reasoning_excerpt(llm_span: dict[str, Any], *, limit: int = 1200) -> str | None:
    output = llm_span.get("output")
    if not output:
        return None
    messages = output if isinstance(output, list) else [output]
    for block in messages:
        if not isinstance(block, dict):
            continue
        msg = block.get("message") if "message" in block else block
        if not isinstance(msg, dict):
            continue
        reasoning = msg.get("reasoning")
        if isinstance(reasoning, str) and reasoning.strip():
            text = reasoning.strip()
            return text if len(text) <= limit else text[: limit - 3] + "..."
    return None


def _parse_json_content(llm_span: dict[str, Any]) -> dict[str, Any] | None:
    output = llm_span.get("output")
    if not isinstance(output, list):
        return None
    for block in output:
        msg = (block or {}).get("message") if isinstance(block, dict) else None
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if isinstance(content, str) and content.strip().startswith("{"):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return None
    return None


def fetch_experiment_events(
    experiment_name: str,
    *,
    project: str | None = None,
    set_current: bool = False,
) -> list[dict[str, Any]]:
    """Load all rows from a readonly Braintrust experiment (network)."""
    import braintrust

    project = project or os.environ.get("BRAINTRUST_PROJECT", "Mailroom-Evals")
    exp = braintrust.init(
        project=project,
        experiment=experiment_name,
        open=True,
        set_current=set_current,
    )
    return list(exp.fetch())


def index_experiment_spans(events: list[dict[str, Any]]) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    """Map root eval spans by root_span_id; LLM spans by parent span_id."""
    roots: dict[str, dict] = {}
    llm_by_parent: dict[str, list[dict]] = defaultdict(list)
    for ev in events:
        attrs = ev.get("span_attributes") or {}
        span_type = attrs.get("type")
        if ev.get("is_root") and span_type == "eval":
            roots[str(ev.get("root_span_id"))] = ev
        elif span_type == "llm":
            parents = ev.get("span_parents") or []
            if parents:
                llm_by_parent[str(parents[0])].append(ev)
    return roots, llm_by_parent


def root_to_observe_row(
    root: dict[str, Any],
    *,
    run_id: str,
    llm_spans: list[dict] | None = None,
    project: str | None = None,
) -> dict[str, Any]:
    """Braintrust eval root → GEPA failure manifest row (+ trace grounding)."""
    meta = root.get("metadata") or {}
    inp = root.get("input") or {}
    out = root.get("output") or {}
    expected = root.get("expected") or {}
    extracted = out.get("extracted_data") if isinstance(out, dict) else None
    scores = root.get("scores") or (out.get("scores") if isinstance(out, dict) else {}) or {}

    case_ref = inp.get("case_ref") or meta.get("case_ref")
    filename = meta.get("filename") or _filename_from_case_ref(case_ref)

    llm_spans = llm_spans or []
    reasoning = None
    model = meta.get("model")
    for span in llm_spans:
        sm = (span.get("metadata") or {}).get("model")
        if sm:
            model = sm
        reasoning = _reasoning_excerpt(span) or reasoning

    parsed = _parse_json_content(llm_spans[0]) if llm_spans else None
    prediction = {
        "doc_type": meta.get("task", "").replace("eval:", "") or expected.get("expected_doc_class"),
        "extracted_data": extracted or parsed,
        "specialist": meta.get("specialist") or out.get("specialist"),
        "model": model,
        "prompt_key": meta.get("prompt_key") or meta.get("prompt_version"),
    }

    exp_name = meta.get("run_id") or run_id
    span_id = root.get("span_id")
    project = project or os.environ.get("BRAINTRUST_PROJECT", "Mailroom-Evals")

    return {
        "run_id": run_id,
        "case_id": case_ref,
        "filename": filename,
        "expected_doc_class": expected.get("expected_doc_class") or meta.get("expected_doc_class"),
        "expected_subclass": expected.get("expected_subclass"),
        "prediction": prediction,
        "scores": scores,
        "error": out.get("error") if isinstance(out, dict) else root.get("error"),
        "doc_text_sha256": inp.get("doc_text_sha256") or meta.get("doc_text_sha256"),
        "braintrust": {
            "project": project,
            "experiment": exp_name,
            "span_id": span_id,
            "root_span_id": root.get("root_span_id"),
            "prompt_version": meta.get("prompt_version"),
            "model": model,
        },
        "trace_excerpt": {
            "reasoning": reasoning,
            "output_confidence": (extracted or parsed or {}).get("confidence")
            if isinstance(extracted or parsed, dict)
            else None,
        },
        "expected_fields": expected.get("expected_fields"),
    }


def _filename_from_case_ref(case_ref: str | None) -> str | None:
    if not case_ref:
        return None
    # corpus:ground_truth:train:path/to/file → file basename
    if ":" in case_ref:
        tail = case_ref.split(":", 3)[-1]
        if tail.startswith("doc#"):
            return tail
        return tail.replace("/", os.sep).split("/")[-1] if "/" in tail else tail
    return case_ref


def failures_from_experiment(
    experiment_name: str,
    *,
    run_id: str | None = None,
    project: str | None = None,
) -> list[dict[str, Any]]:
    run_id = run_id or experiment_name
    events = fetch_experiment_events(experiment_name, project=project)
    roots, llm_by_parent = index_experiment_spans(events)
    rows: list[dict[str, Any]] = []
    for root in roots.values():
        if not _is_observe_failure(root):
            continue
        sid = str(root.get("span_id"))
        rows.append(
            root_to_observe_row(
                root,
                run_id=run_id,
                llm_spans=llm_by_parent.get(sid, []),
                project=project,
            )
        )
    return rows


def merge_observe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dedupe on case_id; keep the row with the lowest overall_score (worst miss)."""
    best: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row.get("case_id") or row.get("filename") or "")
        if not key:
            continue
        prev = best.get(key)
        if prev is None:
            best[key] = row
            continue
        s_new = (_failure_score({"scores": row.get("scores")}) or 1.0)
        s_old = (_failure_score({"scores": prev.get("scores")}) or 1.0)
        if s_new < s_old:
            best[key] = row
        elif s_new == s_old:
            # accumulate source runs for provenance
            src = prev.setdefault("source_run_ids", [prev.get("run_id")])
            if row.get("run_id") and row["run_id"] not in src:
                src.append(row["run_id"])
    return list(best.values())


def build_task_backlog_manifest(
    task: str,
    run_entries: list[dict[str, Any]],
    *,
    project: str | None = None,
) -> list[dict[str, Any]]:
    """Merge failure rows across every Braintrust experiment for one specialist task."""
    merged: list[dict[str, Any]] = []
    for entry in run_entries:
        exp = entry.get("experiment") or entry.get("run_id")
        if not exp:
            continue
        try:
            rows = failures_from_experiment(str(exp), run_id=str(entry.get("run_id")), project=project)
            merged.extend(rows)
        except Exception:
            logger.warning("gepa_braintrust_fetch_failed", task=task, experiment=exp, exc_info=True)
    return merge_observe_rows(merged)


def enrich_manifest_from_braintrust(
    manifest_rows: list[dict[str, Any]],
    *,
    experiment_name: str,
    project: str | None = None,
) -> list[dict[str, Any]]:
    """Attach Braintrust reasoning excerpts to existing score_run failure rows."""
    events = fetch_experiment_events(experiment_name, project=project)
    roots, llm_by_parent = index_experiment_spans(events)
    by_sha: dict[str, dict] = {}
    by_case: dict[str, dict] = {}
    for r in roots.values():
        inp = r.get("input") or {}
        meta = r.get("metadata") or {}
        sha = inp.get("doc_text_sha256") or meta.get("doc_text_sha256")
        if sha:
            by_sha[str(sha)] = r
        ref = inp.get("case_ref") or meta.get("case_ref")
        if ref:
            by_case[str(ref)] = r

    out: list[dict[str, Any]] = []
    for row in manifest_rows:
        root = by_sha.get(str(row.get("doc_text_sha256") or "")) or by_case.get(str(row.get("case_id") or ""))
        if not root:
            out.append(row)
            continue
        sid = str(root.get("span_id"))
        enriched = root_to_observe_row(
            root,
            run_id=str(row.get("run_id") or experiment_name),
            llm_spans=llm_by_parent.get(sid, []),
            project=project,
        )
        out.append({**row, "braintrust": enriched.get("braintrust"), "trace_excerpt": enriched.get("trace_excerpt")})
    return out


def write_backlog_index(
    by_task: dict[str, list[dict[str, Any]]],
    path: Path,
    *,
    manifest_stats: dict[str, int] | None = None,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "gepa-braintrust-backlog-index",
        "version": 1,
        "project": os.environ.get("BRAINTRUST_PROJECT", "Mailroom-Evals"),
        "tasks": {
            task: {
                "n_runs": len(entries),
                "runs": entries,
                "n_failures_merged": (manifest_stats or {}).get(task),
            }
            for task, entries in sorted(by_task.items())
        },
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
