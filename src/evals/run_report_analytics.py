"""Sandbox-parity analytics blocks for human run reports.

Mirrors the sections in ``mailroom-sandbox/scripts/sand032/report.py`` (analyst
insights, strata, scoring-method notes, reproduce, artifacts). API-leg reports
omit Modal-only engine observations and SVG figures; strata + per-document
tables are the figure table views.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any

OVERALL_KEYS = ("overall_score", "overall_extraction_score", "accuracy", "exact_match", "score")
F1_KEYS = ("extraction_f1", "f1", "field_f1")


def _pick(scores: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = scores.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
    return None


def _overall_values(case_rows: list[dict[str, Any]]) -> list[float]:
    out: list[float] = []
    for row in case_rows:
        value = _pick(row.get("scores") or {}, OVERALL_KEYS)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            out.append(float(value))
    return out


def _latencies_s(case_rows: list[dict[str, Any]]) -> list[float]:
    return sorted(
        float(r["latency_ms"]) / 1000.0
        for r in case_rows
        if isinstance(r.get("latency_ms"), (int, float))
    )


def _ok_rows(case_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ok: list[dict[str, Any]] = []
    for row in case_rows:
        pred = row.get("prediction") or {}
        if row.get("error"):
            continue
        if isinstance(pred, dict) and pred.get("_parse_error"):
            continue
        ok.append(row)
    return ok


def _tokens(case_rows: list[dict[str, Any]]) -> tuple[int, int]:
    pt = ct = 0
    for row in case_rows:
        tok = row.get("tokens") if isinstance(row.get("tokens"), dict) else {}
        pt += int(tok.get("prompt") or 0)
        ct += int(tok.get("completion") or 0)
    return pt, ct


def render_analyst_insights(
    summary: dict[str, Any],
    case_rows: list[dict[str, Any]],
    *,
    wall: float | None,
    p50: float | None,
    p95: float | None,
) -> list[str]:
    """Bullet findings comparable to sandbox ``insights()``."""
    params = summary.get("params") or {}
    conc = int(params.get("concurrency") or 1)
    latencies = _latencies_s(case_rows)
    lat_sum = sum(latencies) if latencies else None
    ok = _ok_rows(case_rows)
    lines: list[str] = ["## Analyst insights & findings", ""]

    if wall and lat_sum:
        factor = lat_sum / wall
        pct_ideal = 100 * factor / conc if conc else 0
        lines.append(
            f"- **Concurrency efficiency:** Σ latency {lat_sum:.1f} s over wall {wall:.1f} s = "
            f"**{factor:.2f}×** effective parallelism at c{conc} "
            f"({pct_ideal:.0f}% of the ideal {conc}×)."
        )
    if ok and latencies:
        slow = max(ok, key=lambda r: float(r.get("latency_ms") or 0))
        slow_s = float(slow.get("latency_ms") or 0) / 1000.0
        share = (slow_s / wall * 100) if wall else None
        sub = slow.get("expected_subclass") or "?"
        doc_id = slow.get("case_id") or slow.get("filename") or "?"
        ratio = (p95 / p50) if p50 and p95 else None
        share_s = f"{share:.0f}%" if share is not None else "—"
        ratio_s = f"{ratio:.2f}" if ratio is not None else "—"
        lines.append(
            f"- **Tail:** slowest doc `{doc_id}` ({sub}) {slow_s:.1f} s = {share_s} of wall — "
            f"p95/p50 = {ratio_s}×."
        )
        pts = []
        for row in ok:
            if not isinstance(row.get("latency_ms"), (int, float)):
                continue
            tok = row.get("tokens") if isinstance(row.get("tokens"), dict) else {}
            prompt = int(tok.get("prompt") or 0)
            pts.append((prompt, float(row["latency_ms"]) / 1000.0))
        if len(pts) > 2:
            xs, ys = zip(*pts)
            try:
                r = statistics.correlation(xs, ys)
                bound = "prefill-bound" if r > 0.5 else "not prefill-dominated"
                lines.append(
                    f"- **Prompt length vs latency:** Pearson r = {r:.2f} across {len(pts)} docs ({bound})."
                )
            except statistics.StatisticsError:
                pass
        pt, ct = _tokens(ok)
        lines.append(
            f"- **Decode budget:** mean completion {ct / len(ok):.0f} tok/doc, "
            f"mean prompt {pt / len(ok):.0f} tok/doc."
        )
    by_sub: dict[str, list[float]] = defaultdict(list)
    for row in ok:
        score = _pick(row.get("scores") or {}, OVERALL_KEYS)
        if isinstance(score, (int, float)):
            by_sub[str(row.get("expected_subclass") or "?")].append(float(score))
    if len(by_sub) > 1:
        best = max(by_sub, key=lambda k: statistics.mean(by_sub[k]))
        worst = min(by_sub, key=lambda k: statistics.mean(by_sub[k]))
        lines.append(
            f"- **Subclass spread:** best `{best}` {statistics.mean(by_sub[best]):.3f} "
            f"(n={len(by_sub[best])}), worst `{worst}` {statistics.mean(by_sub[worst]):.3f} "
            f"(n={len(by_sub[worst])})."
        )
    zeros = sum(
        1
        for row in ok
        if _pick(row.get("scores") or {}, F1_KEYS) == 0
    )
    if ok:
        lines.append(
            f"- **Field-level extraction:** {zeros}/{len(ok)} docs have extraction F1 = 0 — "
            "when non-zero overall scores still appear, entity/structure components may carry the headline."
        )
    if len(lines) == 2:
        lines.append("- (insufficient scored rows for derived insights)")
    lines.append("")
    return lines


def render_strata(case_rows: list[dict[str, Any]]) -> list[str]:
    """Subclass strata table (sandbox ``Strata (subclass)`` section)."""
    by_sub: dict[str, list[float]] = defaultdict(list)
    for row in case_rows:
        score = _pick(row.get("scores") or {}, OVERALL_KEYS)
        if not isinstance(score, (int, float)):
            continue
        by_sub[str(row.get("expected_subclass") or "?")].append(float(score))
    if not by_sub:
        return []
    all_scores = [v for bucket in by_sub.values() for v in bucket]
    mean_all = statistics.mean(all_scores)
    lines = [
        "## Strata (subclass)",
        "",
        "| subclass | n | mean overall |",
        "| --- | ---: | ---: |",
    ]
    for key in sorted(by_sub, key=lambda k: (-len(by_sub[k]), k)):
        lines.append(f"| {key} | {len(by_sub[key])} | {statistics.mean(by_sub[key]):.4f} |")
    lines.append(f"| **total** | **{len(all_scores)}** | **{mean_all:.4f}** |")
    lines.append("")
    return lines


def _aggregate_score_key(case_rows: list[dict[str, Any]], key: str) -> int:
    total = 0
    for row in case_rows:
        val = (row.get("scores") or {}).get(key)
        if isinstance(val, bool):
            total += int(val)
        elif isinstance(val, (int, float)):
            total += int(val)
    return total


def render_scoring_method(summary: dict[str, Any], case_rows: list[dict[str, Any]]) -> list[str]:
    """Task-specific scoring narrative (CUAD / MAUD when metrics present)."""
    task = str(summary.get("task") or "")
    ok = _ok_rows(case_rows)
    if not ok:
        return []

    scores_list = [row.get("scores") or {} for row in ok]
    if task == "merger_agreement" or any("maud_" in k for s in scores_list for k in s):
        q = _aggregate_score_key(ok, "maud_questions")
        answered = _aggregate_score_key(ok, "maud_answered")
        correct = _aggregate_score_key(ok, "maud_correct")
        if q > 0:
            return [
                "## Scoring method — MAUD answer accuracy",
                "",
                "Hub merger rows carry ground truth as `maud_clause_labels` (LegalBench MAUD "
                "question → answer). Field F1 against the suite map is often 0 by construction; "
                "when MAUD aggregate keys are present on case rows they reflect "
                "**per-question MAUD accuracy** (unanswered counts as wrong).",
                "",
                "| metric | value |",
                "| --- | --- |",
                f"| labeled MAUD questions | {q} |",
                f"| answered | {answered} ({answered / q:.1%} coverage) |",
                f"| correct | {correct} → **micro accuracy {correct / q:.1%}** |",
                "",
            ]
        return [
            "## Scoring method — merger extraction",
            "",
            "Headline **overall_score** uses the pipeline extraction rubric on MAUD-labeled "
            "merger agreements; field F1 may be 0 when GT is label-native only.",
            "",
        ]

    if task == "contracts" or any(k.startswith("cuad_") for s in scores_list for k in s):
        tp = _aggregate_score_key(ok, "cuad_tp")
        fp = _aggregate_score_key(ok, "cuad_fp")
        fn = _aggregate_score_key(ok, "cuad_fn")
        if tp + fp + fn > 0:
            prec = tp / (tp + fp) if tp + fp else 0.0
            rec = tp / (tp + fn) if tp + fn else 0.0
            f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
            labeled = sum(
                1 for s in scores_list if s.get("cuad_presence_f1") is not None
            )
            return [
                "## Scoring method — CUAD clause detection",
                "",
                "Contract rows on the pinned corpus expose `cuad_clause_labels`; the suite field "
                "map may not align, so extraction F1 can be 0 while **CUAD category-presence** "
                "metrics (when emitted on case rows) describe clause recall.",
                "",
                "| metric | value |",
                "| --- | --- |",
                f"| docs with CUAD-style scores | {labeled} of {len(ok)} ok |",
                f"| micro precision / recall / F1 | {prec:.3f} / {rec:.3f} / **{f1:.3f}** |",
                "",
            ]
        return [
            "## Scoring method — CUAD contracts",
            "",
            "Headline **overall_score** uses the pipeline contracts extraction rubric. "
            "Pinned Hub contract GT is often CUAD label-native; pair with sandbox Modal reports "
            "for full CUAD micro-F1 when the scorer emits `cuad_*` keys on case rows.",
            "",
        ]
    return []


def render_figures_note() -> list[str]:
    return [
        "## Figures",
        "",
        "Static SVG charts (latency bar, subclass means) are generated in the Modal sandbox "
        "repo (`scripts/sand032/report.py` + `/dataviz`). This API-leg report keeps the "
        "**table views**: **Strata (subclass)** and **Per-document scores** below.",
        "",
    ]


def _task_cli(summary: dict[str, Any]) -> str:
    family = summary.get("family") or "eval"
    task = summary.get("task") or "classification"
    return f"{family}:{task}"


def render_reproduce(summary: dict[str, Any]) -> list[str]:
    """Shell commands to replay the run (API leg)."""
    params = summary.get("params") or {}
    run_id = summary.get("run_id") or "<run_id>"
    task = _task_cli(summary)
    mode_flag = "--real" if summary.get("mode") == "real" else "--mock"
    sample = params.get("sample")
    n = params.get("n")
    draw = f"--sample {sample}" if sample else (f"--n {n}" if n else "")
    seed = params.get("seed")
    seed_flag = f"--seed {seed}" if seed is not None else ""
    conc = params.get("concurrency")
    conc_flag = f"--concurrency {conc}" if conc else ""
    profile = params.get("decode_profile")
    profile_flag = f"--decode-profile {profile}" if profile else ""
    subset = (summary.get("dataset") or {}).get("subset")
    subset_flag = f'--subset "{subset}"' if subset else ""
    flags = " ".join(x for x in (mode_flag, draw, seed_flag, conc_flag, profile_flag, subset_flag) if x)
    lines = [
        "## Reproduce",
        "",
        "```bash",
        f"uv run python scripts/run_evals.py --task {task} {flags}".strip(),
        f"uv run python scripts/score_run.py --run-id {run_id} --recompute",
        "uv run python scripts/render_comparison_reports.py "
        f"--run-id {run_id}",
        "```",
        "",
    ]
    return lines


def _repo_rel(path: str) -> str:
    """Strip absolute workspace prefixes so committed reports stay portable."""
    p = path.replace("\\", "/")
    for marker in ("/eval-environment/", "/workspace/"):
        if marker in p:
            return p.split(marker, 1)[1]
    if p.startswith("/"):
        return p.lstrip("/")
    return p


def render_artifacts(summary: dict[str, Any]) -> list[str]:
    run_id = summary.get("run_id") or "<run_id>"
    dataset = summary.get("dataset") or {}
    manifest = dataset.get("subset_manifest_path") or f"data/experiments/{run_id}/subset_manifest.json"
    manifest = _repo_rel(str(manifest))
    lines = [
        "## Artifacts",
        "",
        "| path | role |",
        "| --- | --- |",
        f"| `reports/experiment_log.jsonl` | append-only run summary (this run_id) |",
        f"| `data/experiments/{run_id}/cases.jsonl` | per-case rows (scores, tokens, latency) |",
        f"| `{manifest}` | canonical draw fingerprint (filenames + content hashes) |",
        f"| `reports/experiment_log/{run_id}.md` | experiment-log markdown mirror |",
    ]
    comp = summary.get("comparison_report")
    if comp:
        lines.append(f"| `{_repo_rel(str(comp))}` | Modal-comparable API-leg write-up |")
    lines.append("")
    return lines


def headline_score_stats(case_rows: list[dict[str, Any]]) -> dict[str, float | None]:
    values = _overall_values(case_rows)
    if not values:
        return {"mean": None, "sd": None, "min": None, "max": None}
    sd = statistics.pstdev(values) if len(values) > 1 else 0.0
    return {
        "mean": statistics.mean(values),
        "sd": sd,
        "min": min(values),
        "max": max(values),
    }
