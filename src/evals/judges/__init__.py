"""Local LLM-as-judge engine — post-hoc scoring of logged runs, zero sinks.

Reads a run's ``cases.jsonl`` from the experiment log, re-loads each case's
text from the pinned corpus (verified against the case row's
``doc_text_sha256``), and judges any dimension with the FROZEN lineage's
judge rubrics (``judge_v1``, ``judge_classification_v1``,
``judge_correctness_v1``, ``pipeline_verdict_v1``, ``pipeline_quality_v1``).

Judgments append to the run dir as ``judgments.jsonl`` and surface as a
follow-up run-summary record (``experiment_log.record_judging``) — history
stays append-only. ``--mock`` mode derives deterministic verdicts from the
stored deterministic scores (no network, CI-safe).
"""

from __future__ import annotations

import json
from typing import Any

import structlog

from .. import experiment_log
from ..cases import load_cases
from ..prompts import registry as prompts_registry
from ..prompts.lineage import resolve
from ..scoring import sha256_text

logger = structlog.get_logger(__name__)

DIMENSIONS: tuple[str, ...] = (
    "classification",   # judge_classification_v1 — class audit vs GT
    "completeness",     # judge_v1 — extraction completeness vs source text
    "correctness",      # judge_correctness_v1 — fabrication/accuracy audit
    "verdict",          # pipeline_verdict_v1 — CORRECT/PARTIAL/MISS vs GT
    "quality",          # pipeline_quality_v1 — 0.0-1.0 quality score
)

DIMENSION_PROMPT_KEY: dict[str, str] = {
    "classification": "judge-classification_v1",
    "completeness": "judge_v1",
    "correctness": "judge-correctness_v1",
    "verdict": "pipeline_verdict_v1",
    "quality": "pipeline_quality_v1",
}


def _load_case_text(case_row: dict[str, Any]) -> str | None:
    """Re-load a case's text from the pinned corpus, sha-verified.

    Returns None when the text cannot be verified (judge marks the row
    'text_unavailable' rather than guessing).
    """
    filename = case_row.get("filename")
    if not filename:
        return None
    expected_sha = case_row.get("doc_text_sha256")
    try:
        cases, _prov = load_cases("full")
    except Exception:
        logger.warning("judge_corpus_load_failed", exc_info=True)
        return None
    for case in cases:
        if case.get("filename") == filename:
            text = str(case.get("text") or "")
            if expected_sha and sha256_text(text) != expected_sha:
                logger.warning("judge_text_sha_mismatch", filename=filename)
                return None
            return text
    return None


def _judge_client(model: str | None):
    """The judge LLM client — the pipeline's own provider layer (taxonomy
    ``judge`` mapping by default). Returns (client, model)."""
    from llm.client import get_llm

    client, resolved = get_llm("judge")
    return client, model or resolved


def _call_judge(client: Any, model: str, system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """One structured judge call (JSON object out; retry handled upstream)."""
    user_payload = f"{user_prompt}\n\nRespond with a single JSON object."
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
    except Exception:
        # Some providers require the literal word "json" in the prompt for
        # response_format=json_object — the payload above satisfies it, but
        # hard-fail-soft: retry once without the response_format constraint
        # and parse defensively.
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt + "\nReply with ONLY a JSON object."},
                {"role": "user", "content": user_payload},
            ],
            temperature=0.1,
        )
    content = response.choices[0].message.content or "{}"
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content.removeprefix("json")
    return json.loads(content)


def _mock_verdict(dimension: str, case_row: dict[str, Any]) -> dict[str, Any]:
    """Deterministic mock judge derived from the stored deterministic scores.

    CI-safe stand-in for the LLM judge: the verdict follows the deterministic
    scorer's verdict so mock judging exercises the full judging pipeline
    (parse → record → log) without a network.
    """
    scores = case_row.get("scores") or {}
    if dimension == "classification":
        correct = scores.get("class_correct")
        return {"classification_correct": "correct" if correct else "incorrect", "classification_quality": 1.0 if correct else 0.0}
    if dimension == "completeness":
        overall = scores.get("overall_score")
        label = "complete" if (overall or 0) >= 0.95 else ("partial" if (overall or 0) >= 0.5 else "incomplete")
        return {"completeness": overall if overall is not None else 0.0, "completeness_label": label}
    if dimension == "correctness":
        overall = scores.get("overall_score")
        label = "accurate" if (overall or 0) >= 0.95 else ("partial" if (overall or 0) >= 0.5 else "inaccurate")
        return {"extraction_correctness": overall if overall is not None else 0.0, "extraction_correctness_label": label}
    if dimension == "verdict":
        overall = scores.get("overall_score")
        stage_ok = scores.get("stage_agrees")
        if overall is None and stage_ok is None:
            return {"verdict": "MISS"}
        if (overall or 0) >= 0.95 and stage_ok != 0:
            return {"verdict": "CORRECT"}
        if (overall or 0) >= 0.5:
            return {"verdict": "PARTIAL"}
        return {"verdict": "MISS"}
    if dimension == "quality":
        overall = scores.get("overall_score")
        return {"quality": overall if overall is not None else 0.0}
    raise ValueError(f"unknown dimension {dimension!r}")


def judge_run(
    run_id: str,
    dimensions: list[str],
    *,
    mock: bool = False,
    judge_model: str | None = None,
) -> dict[str, Any]:
    """Judge one logged run post hoc. Appends judgments + a follow-up record."""
    for dimension in dimensions:
        if dimension not in DIMENSIONS:
            raise ValueError(f"unknown dimension {dimension!r}; known: {DIMENSIONS}")
    case_rows = experiment_log.load_cases(run_id)
    if not case_rows:
        raise KeyError(f"run {run_id!r} has no case rows to judge")

    # Judge prompts come from the FROZEN lineage (never a live fetch).
    prompts_registry.activate("frozen")
    try:
        prompt_versions = {
            dim: {"key": DIMENSION_PROMPT_KEY[dim], "sha256": resolve(DIMENSION_PROMPT_KEY[dim]).sha256}
            for dim in dimensions
        }
    finally:
        prompts_registry.deactivate()

    client = model = None
    if not mock:
        client, model = _judge_client(judge_model)

    judgments: list[dict[str, Any]] = []
    for row in case_rows:
        text = _load_case_text(row)
        for dimension in dimensions:
            if mock:
                verdict = _mock_verdict(dimension, row)
            elif text is None:
                verdict = {"error": "text_unavailable"}
            else:
                system_prompt = resolve(DIMENSION_PROMPT_KEY[dimension]).text
                user_prompt = json.dumps({
                    "document_text_excerpt": text[:20000],
                    "prediction": row.get("prediction"),
                    "expected": {
                        "doc_class": row.get("expected_doc_class"),
                        "subclass": row.get("expected_subclass"),
                        "expected_fields": None,  # GT fields ride the corpus, not the log
                    },
                }, default=str)
                try:
                    verdict = _call_judge(client, model, system_prompt, user_prompt)
                except Exception as exc:
                    verdict = {"error": f"{type(exc).__name__}: {exc}"}
            judgments.append({
                "run_id": run_id,
                "case_id": row.get("case_id"),
                "dimension": dimension,
                "verdict": verdict,
                "mock": mock,
                "text_available": text is not None,
                "error": row.get("error"),
            })

    # Persist: judgments.jsonl in the run dir + follow-up run-summary record.
    run_dir = experiment_log.experiments_dir() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    judgments_path = run_dir / "judgments.jsonl"
    with judgments_path.open("a", encoding="utf-8") as fh:
        for judgment in judgments:
            fh.write(json.dumps(judgment, default=str) + "\n")

    metrics = _judge_metrics(judgments)
    record = experiment_log.record_judging(
        run_id,
        dimensions=dimensions,
        judge_model="mock" if mock else model,
        mock=mock,
        metrics=metrics,
        prompt_versions=prompt_versions,
        judgments_ref=str(judgments_path),
    )
    return {"judgments": judgments, "metrics": metrics, "record": record, "judgments_ref": str(judgments_path)}


def _judge_metrics(judgments: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-dimension agreement rates over the judged rows."""
    out: dict[str, Any] = {"n": len({j.get("case_id") for j in judgments})}
    by_dim: dict[str, list[float]] = {}
    for judgment in judgments:
        dim = judgment["dimension"]
        verdict = judgment.get("verdict") or {}
        if not isinstance(verdict, dict) or verdict.get("error"):
            continue
        value = _positive(verdict)
        if value is not None:
            by_dim.setdefault(dim, []).append(float(value))
    for dim, values in sorted(by_dim.items()):
        out[f"{dim}_mean"] = round(sum(values) / len(values), 4) if values else None
    return out


def _positive(verdict: dict[str, Any]) -> float | None:
    """Map a verdict to 0/1 (categorical) or its numeric score."""
    for key, positive_values in (
        ("classification_correct", ("correct",)),
        ("completeness_label", ("complete",)),
        ("extraction_correctness_label", ("accurate",)),
        ("verdict", ("CORRECT",)),
    ):
        if key in verdict:
            value = verdict[key]
            if isinstance(value, (int, float)):
                return float(value)
            return 1.0 if str(value) in positive_values else 0.0
    for key in ("classification_quality", "completeness", "extraction_correctness", "quality"):
        if key in verdict and isinstance(verdict[key], (int, float)):
            return float(verdict[key])
    return None
