"""Deterministic scorers + per-case performance accounting.

Scoring reuses the pipeline's own deterministic scorers wherever they exist
(``observability.classification_scoring`` / ``suite_scoring`` /
``field_scoring``) so eval numbers measure the same rubric the pipeline runs.
Performance (latency, tokens, cost) is recorded for every case — per-node
performance analysis is a first-class output, not an afterthought.
"""

from __future__ import annotations

import time
from typing import Any


class Timer:
    """Wall-clock timer for per-case latency accounting."""

    def __init__(self) -> None:
        self.start = time.perf_counter()

    def ms(self) -> float:
        return round((time.perf_counter() - self.start) * 1000.0, 1)


# ESSENTIAL_SCORES — the curated headline metrics forwarded to the trace sinks
# at run time (one to three per scorer family). The FULL score set stays in
# the experiment log's case rows; sinks carry tracing + essentials only, and
# the complete evaluation suite runs post hoc (evals.judges + score_run.py).
ESSENTIAL_SCORES: dict[str, tuple[str, ...]] = {
    "intake": ("no_truncation", "triage_agrees"),
    "classification": ("class_correct", "subclass_correct"),
    "extraction": ("overall_score", "needs_judge_review"),
    "judge": ("judge_agrees",),
    "arbiter": ("decision_valid", "decision_agrees"),
    "boss": ("decision_valid",),
    "archivist": ("archived_ok", "stage_ok"),
    "pipeline": ("stage_agrees", "class_correct"),
}


def essential_metrics(scorer: str, scores: dict[str, Any]) -> dict[str, float]:
    """Filter a score dict down to the family's essential span metrics."""
    wanted = ESSENTIAL_SCORES.get(scorer, ())
    return {
        key: float(value)
        for key, value in scores.items()
        if key in wanted and isinstance(value, (int, float)) and not isinstance(value, bool)
        or key in wanted and isinstance(value, bool)
    }


def essential_rollup(scorer: str, rows: list[dict[str, Any]]) -> dict[str, float]:
    """Mean essential metrics over a run's case rows (run-level rollup)."""
    out: dict[str, float] = {}
    for key in ESSENTIAL_SCORES.get(scorer, ()):
        values = [
            float((r.get("scores") or {}).get(key))
            for r in rows
            if isinstance((r.get("scores") or {}).get(key), (int, float))
        ]
        mean = _mean(values)
        if mean is not None:
            out[key] = mean
    return out


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 4) if values else None


def sha256_text(text: str) -> str:
    """sha256 of a case's exact text — the post-hoc re-load integrity key."""
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = max(0, min(len(ordered) - 1, round(0.95 * (len(ordered) - 1))))
    return round(ordered[idx], 1)


def score_classification(predicted: str | None, expected: str | None) -> dict[str, Any]:
    """Class accuracy via the pipeline's own matcher (aliases honored)."""
    from observability.classification_scoring import classes_match

    expected_class = expected or ""
    predicted_class = predicted or ""
    correct = int(classes_match(expected_class, predicted_class)) if expected_class else None
    return {
        "predicted_doc_class": predicted_class,
        "expected_doc_class": expected_class,
        "class_correct": correct,
    }


def score_subclass(predicted: str | None, expected: str | None) -> dict[str, Any]:
    """Exact subclass match (normalized, blank-tolerant)."""
    def norm(value: str | None) -> str:
        return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")

    expected_sub = norm(expected)
    predicted_sub = norm(predicted)
    correct = int(predicted_sub == expected_sub) if expected_sub else None
    return {
        "predicted_subclass": predicted or None,
        "expected_subclass": expected or None,
        "subclass_correct": correct,
    }


def score_extraction(doc_class: str, predicted: dict, expected: dict) -> dict[str, Any]:
    """Field-level extraction score via the pipeline's suite scorer."""
    if not expected:
        return {"overall_score": None, "n_expected_fields": 0}
    try:
        from llm_dojo_scoring.field_scoring import get_field_types
        from observability.suite_scoring import score_with_suite

        result, extras = score_with_suite(
            doc_class, predicted, expected, field_types=get_field_types(doc_class)
        )
    except Exception:
        return {"overall_score": None, "n_expected_fields": len(expected), "scorer_error": True}
    out: dict[str, Any] = {
        "overall_score": None if result.overall_score is None else round(float(result.overall_score), 4),
        "needs_judge_review": bool(result.needs_judge_review),
        "n_expected_fields": len(expected),
    }
    for key, value in extras.items():
        try:
            out[key] = round(float(value), 4)
        except (TypeError, ValueError):
            pass
    return out


def score_label_lists(predicted: dict, expected: dict, key: str) -> dict[str, Any]:
    """Set precision/recall/F1 over a GT label list (cuad/maud clause labels)."""
    want = expected.get(key)
    if not want:
        return {}
    want_set = {str(v).strip().lower() for v in _as_list(want)}
    got_set = {str(v).strip().lower() for v in _as_list(predicted.get(key))}
    if not want_set:
        return {}
    tp = len(want_set & got_set)
    precision = tp / len(got_set) if got_set else 0.0
    recall = tp / len(want_set)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        f"{key}_precision": round(precision, 4),
        f"{key}_recall": round(recall, 4),
        f"{key}_f1": round(f1, 4),
    }


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, (list, tuple)):
        return list(value)
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def score_decision(predicted: Any, valid: tuple[str, ...], expected: Any = None) -> dict[str, Any]:
    """Decision validity (and optional exact agreement) for judge/arbiter/boss."""
    decision = str(predicted or "").strip().lower()
    out: dict[str, Any] = {
        "decision": decision or None,
        "decision_valid": int(decision in valid),
    }
    if expected is not None:
        out["decision_agrees"] = int(decision == str(expected).strip().lower())
    return out


def score_intake(result: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Intake invariants: no truncation, normalized text, triage agreement."""
    from llm_dojo_scoring.intake import looks_messy

    original = str(case.get("text") or "")
    cleaned = str(result.get("cleaned") or result.get("doc_text") or original)
    triage = result.get("triage") or {}
    out: dict[str, Any] = {
        "no_truncation": int(len(cleaned) >= len(original) * 0.98),
        "messy_flag": int(bool(looks_messy(original))),
        "triage_class": triage.get("primary_doc_class"),
        "triage_agrees": None,
    }
    expected_class = case.get("expected_doc_class")
    if expected_class and triage.get("primary_doc_class"):
        out["triage_agrees"] = int(
            str(triage.get("primary_doc_class")).strip().lower()
            == str(expected_class).strip().lower()
        )
    return out


def score_archivist(result: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Archive conformance: manifest written, audit chained, sha256, stage."""
    out: dict[str, Any] = {
        "archived_ok": int(bool(result.get("archive_path"))),
        "audit_ok": int(bool(result.get("audit_entry"))),
        "sha256_ok": int(bool(result.get("sha256_ok", result.get("audit_entry")))),
        "stage_ok": int(str(result.get("stage") or "") == "archived"),
    }
    return out


def score_judge(prediction: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Judge verdict vs the fixture/case expectation (review_expected)."""
    label = str(prediction.get("completeness_label") or prediction.get("judge_verdict") or "")
    out: dict[str, Any] = {
        "judge_label": label or None,
        "judge_score": prediction.get("completeness"),
    }
    review_expected = case.get("review_expected")
    if review_expected is not None:
        # review_expected=True  -> judge should flag (partial/incomplete)
        # review_expected=False -> judge should pass (complete)
        flagged = label in ("partial", "incomplete")
        out["judge_agrees"] = int(flagged == bool(review_expected))
    return out


def score_arbiter(prediction: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """Arbiter decision validity + agreement with the fixture's arbiter_outcome."""
    scored = score_decision(
        prediction.get("decision"),
        valid=("accept_with_caveats", "retry_extraction", "human_review"),
    )
    outcome_map = {
        "stands": "accept_with_caveats",
        "re_extract": "retry_extraction",
        "escalate_human_review": "human_review",
    }
    expected_outcome = case.get("arbiter_outcome")
    if expected_outcome:
        scored["decision_agrees"] = int(
            scored["decision"] == outcome_map.get(str(expected_outcome).strip().lower(), "")
        )
    return scored


def score_pipeline(result: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    """End-to-end chained-run conformance vs expected_stage (+ class correctness)."""
    out: dict[str, Any] = {}
    expected_stage = case.get("expected_stage")
    final_stage = str(result.get("stage") or "")
    if expected_stage:
        out["stage_agrees"] = int(final_stage == str(expected_stage).strip().lower())
    out["final_stage"] = final_stage or None
    extracted = result.get("extracted_data") or {}
    expected_fields = case.get("expected_fields") or {}
    if expected_fields:
        doc_class = str(case.get("expected_doc_class") or "")
        out.update(score_extraction(doc_class, extracted, expected_fields))
    doc_type = result.get("doc_type")
    if case.get("expected_doc_class") and doc_type:
        out.update(score_classification(doc_type, case.get("expected_doc_class")))
    return out


def performance_row(latency_ms: float, usage: dict[str, Any] | None, model: str | None) -> dict[str, Any]:
    """Per-case performance record (tokens + estimated cost when model known)."""
    usage = usage or {}
    prompt = int(usage.get("prompt_tokens") or 0)
    completion = int(usage.get("completion_tokens") or 0)
    cost: float | None = None
    if model and (prompt or completion):
        try:
            from llm_dojo_scoring.cost import estimate_cost

            cost = estimate_cost(prompt, completion, model)
        except Exception:
            cost = None
    return {
        "latency_ms": round(float(latency_ms), 1),
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": prompt + completion,
        "cost_usd_est": round(cost, 6) if isinstance(cost, (int, float)) else None,
    }


def summarize_performance(rows: list[dict[str, Any]]) -> dict[str, Any]:
    latencies = [r["latency_ms"] for r in rows if isinstance(r.get("latency_ms"), (int, float))]
    prompt = sum(int(_row_tokens(r, "prompt")) for r in rows)
    completion = sum(int(_row_tokens(r, "completion")) for r in rows)
    costs = [
        r.get(cost_key)
        for r in rows
        for cost_key in ("cost_usd", "cost_usd_est")
        if isinstance(r.get(cost_key), (int, float))
    ]
    summary = {
        "latency_ms_mean": _mean([float(v) for v in latencies]),
        "latency_ms_p95": _p95([float(v) for v in latencies]),
        "tokens_prompt_total": prompt,
        "tokens_completion_total": completion,
        "cost_usd_est_total": round(sum(costs), 6) if costs else None,
    }
    by_agent = summarize_agent_usage([r.get("agent_usage") for r in rows if r.get("agent_usage")])
    if by_agent:
        summary["by_agent"] = by_agent
    return summary


def _row_tokens(row: dict[str, Any], which: str) -> float:
    """Token count from a case row — nested ``tokens`` dict or flat key."""
    tokens = row.get("tokens")
    if isinstance(tokens, dict):
        value = tokens.get(which)
        if isinstance(value, (int, float)):
            return value
    return row.get(f"{which}_tokens") or 0


def cost_for(prompt_tokens: int, completion_tokens: int, model: str | None) -> float | None:
    """Estimated USD cost for a token bundle (None when unpriceable)."""
    if not model or not (prompt_tokens or completion_tokens):
        return None
    try:
        from llm_dojo_scoring.cost import estimate_cost

        cost = estimate_cost(prompt_tokens, completion_tokens, model)
        return round(float(cost), 6) if isinstance(cost, (int, float)) else None
    except Exception:
        return None


def summarize_agent_usage(per_case_agent_usage: list[Any]) -> dict[str, dict[str, Any]]:
    """Aggregate per-case ``by_agent`` usage maps into a run-level catalog.

    Each per-case map is ``{agent: {calls, prompt_tokens, completion_tokens,
    total, models}}`` (the pipeline usage accumulator's per-agent shape).
    The aggregate adds estimated cost per agent (first model wins for
    pricing when an agent mixes models) and sorts agents by total spend.
    """
    agents: dict[str, dict[str, Any]] = {}
    for case_usage in per_case_agent_usage:
        if not isinstance(case_usage, dict):
            continue
        for agent, slot in case_usage.items():
            if not isinstance(slot, dict):
                continue
            entry = agents.setdefault(
                agent,
                {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "models": []},
            )
            entry["calls"] += int(slot.get("calls") or 0)
            entry["prompt_tokens"] += int(slot.get("prompt_tokens") or 0)
            entry["completion_tokens"] += int(slot.get("completion_tokens") or 0)
            entry["total_tokens"] += int(slot.get("total") or slot.get("total_tokens") or 0)
            for model in slot.get("models") or []:
                if model and model not in entry["models"]:
                    entry["models"].append(model)
    for agent, entry in agents.items():
        model = entry["models"][0] if entry["models"] else None
        entry["cost_usd_est"] = cost_for(entry["prompt_tokens"], entry["completion_tokens"], model)
    return dict(sorted(agents.items(), key=lambda kv: -kv[1]["total_tokens"]))


def summarize_scores(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Mean over every numeric score key present in the case rows.

    Rows may carry scores nested under ``scores`` (runner shape) or flat.
    """
    def scores_of(row: dict[str, Any]) -> dict[str, Any]:
        nested = row.get("scores")
        return {**nested, **{k: v for k, v in row.items() if k != "scores"}} if isinstance(nested, dict) else row

    keys: set[str] = set()
    for row in rows:
        keys.update(
            k for k, v in scores_of(row).items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)
            and (k.startswith(("class_", "subclass_", "overall_", "judge_", "decision_", "stage_", "archived_", "audit_", "sha256_", "triage_", "no_truncation", "messy_", "cuad_", "maud_", "key_")) or k.endswith(("_correct", "_valid", "_agrees", "_ok")))
        )
    out: dict[str, Any] = {"n": len(rows)}
    for key in sorted(keys):
        values = [
            float(scores_of(r)[key])
            for r in rows
            if isinstance(scores_of(r).get(key), (int, float)) and not isinstance(scores_of(r).get(key), bool)
        ]
        mean = _mean(values)
        if mean is not None:
            out[key.replace("correct", "accuracy")] = mean
    errors = sum(1 for r in rows if r.get("error"))
    out["errors"] = errors
    return out
