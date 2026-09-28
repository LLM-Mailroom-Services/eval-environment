"""Per-document-type charts for the API leg, from the viewer snapshot.

Renders the reports hub's API views, plus the classifier views it has for
ModernBERT, as static SVG from ``web/data/snapshot.json`` (the same run
summaries and case rows the Vercel viewer reads):

- extraction score by document type, one bar per model
- per-document extraction scores (one dot per document, tick = mean)
- per-subclass extraction scores, pooled over models
- API cost per document by type and model
- LLM sorter: doc-class confusion matrix per model
- LLM sorter: subclass accuracy and the collapse signal (share of a class's
  predictions on its single most common subclass)
- LLM sorter: reliability diagram of stated confidence against accuracy, with ECE
- surrogate ALE of latency on extraction score, per document type

Each (task, model) is charted from its latest real run on the frozen prompt
lineage with at least ``MIN_N`` scored cases and no run error, so GEPA
mutation A/B runs never stand in for a model's baseline. Everything is computed from the
snapshot; nothing is hand-entered.

    python scripts/render_report_charts.py            # write web/data/charts + reports/charts/README.md
    python scripts/render_report_charts.py --check    # exit 1 if the committed charts are stale
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from evals.viz import svgcharts as sc

MIN_N = 20
CLS_MIN_N = 100  # the LLM sorter comparison uses the n = 100 runs only
BIN_MIN_N = 5  # reliability bins with fewer documents are not drawn
TASKS = ["correspondence", "insurance_claims", "corporate_records", "contracts", "merger_agreement"]
TASK_LABEL = {"correspondence": "Correspondence", "insurance_claims": "Insurance claims",
              "corporate_records": "Corporate records", "contracts": "Contracts", "merger_agreement": "Merger agreements"}
CLASSES = ["correspondence", "insurance_claim", "corporate_record", "contract", "merger_agreement"]
CLASS_LABEL = {"correspondence": "Correspondence", "insurance_claim": "Insurance claim",
               "corporate_record": "Corporate record", "contract": "Contract", "merger_agreement": "Merger agreement"}
MODEL_LABEL = {"deepseek/deepseek-v4.1-flash": "DeepSeek V4.1 Flash", "ibm-granite/granite-4.2-8b": "Granite 4.2 8B",
               "qwen/qwen3-8b": "Qwen3 8B", "qwen/qwen3.7-flash": "Qwen3.7 Flash"}
MODEL_COLOR = {"deepseek/deepseek-v4.1-flash": sc.GREEN, "ibm-granite/granite-4.2-8b": sc.ORANGE,
               "qwen/qwen3-8b": sc.BLUE, "qwen/qwen3.7-flash": "#8a5cd6"}
CONF_BINS = [0.0, 0.5, 0.8, 0.9, 0.95, 0.99, 1.0001]


def model_label(m: str) -> str:
    return MODEL_LABEL.get(m, m.split("/")[-1])


def model_color(m: str) -> str:
    return MODEL_COLOR.get(m, sc.GREY)


def latest_runs(snap: dict) -> dict[tuple[str, str], dict]:
    """{(task, model): run} for the latest usable real run of each pair.

    Only frozen-lineage runs count: GEPA mutation runs score candidate
    prompts, not the model's baseline. A resumed run appears once per segment
    under one run_id; the record with the most scored cases wins.
    """
    best: dict[tuple[str, str], dict] = {}
    for r in snap["runs"]:
        n = (r.get("metrics") or {}).get("n") or 0
        floor = CLS_MIN_N if r.get("task") == "classification" else MIN_N
        if r.get("mode") != "real" or r.get("error") or not r.get("model") or n < floor \
                or r.get("prompt_lineage") != "frozen":
            continue
        if r["run_id"] not in snap.get("cases", {}):
            continue
        key = (r["task"], r["model"])
        cur = best.get(key)
        if cur is None or (r["started_at"], n) > (cur["started_at"], cur["metrics"]["n"]):
            best[key] = r
    return best


def _models(runs: dict, task_pred) -> list[str]:
    return sorted({m for (t, m) in runs if task_pred(t)}, key=model_label)


def classification_stats(cases: list[dict]) -> dict:
    conf: dict[str, Counter] = defaultdict(Counter)
    sub: dict[str, dict] = {}
    for c in cases:
        s = c["scores"]
        conf[s["expected_doc_class"]][s.get("predicted_doc_class") or "unknown"] += 1
    for cls in CLASSES:
        rows = [c["scores"] for c in cases if c["scores"]["expected_doc_class"] == cls and c["scores"].get("class_correct")]
        if rows:
            pred, true = Counter(r.get("predicted_subclass") for r in rows), Counter(r.get("expected_subclass") for r in rows)
            sub[cls] = {"n": len(rows), "correct": sum(bool(r.get("subclass_correct")) for r in rows),
                        "top_pred": pred.most_common(1)[0], "top_true": true.most_common(1)[0]}
    return {"confusion": conf, "subclass": sub}


def reliability(cases: list[dict]) -> dict | None:
    """Binned stated confidence vs doc-class accuracy, and ECE over the bins."""
    pts = [(float(c["prediction"]["confidence"]), 1.0 if c["scores"].get("class_correct") else 0.0)
           for c in cases if isinstance((c.get("prediction") or {}).get("confidence"), (int, float))]
    if len(pts) < MIN_N:
        return None
    bins = []
    for lo, hi in zip(CONF_BINS[:-1], CONF_BINS[1:], strict=True):
        b = [p for p in pts if lo <= p[0] < hi]
        if len(b) >= BIN_MIN_N:
            bins.append({"conf": sum(p[0] for p in b) / len(b), "acc": sum(p[1] for p in b) / len(b), "n": len(b)})
    in_bins = sum(b["n"] for b in bins)
    ece = sum(b["n"] * abs(b["acc"] - b["conf"]) for b in bins) / in_bins if in_bins else None
    return {"bins": bins, "ece": ece, "n": len(pts), "n_binned": in_bins} if bins else None


def latency_ale(task_runs: list[dict], cases: dict) -> dict | None:
    from evals.viz import ale

    rows = [{"lat": math.log2(max(c["latency_ms"], 1.0) / 1000), "score": c["scores"]["overall_score"], "model": r["model"]}
            for r in task_runs for c in cases[r["run_id"]]
            if isinstance(c.get("latency_ms"), (int, float)) and isinstance(c["scores"].get("overall_score"), (int, float))]
    if len(rows) < 30:
        return None
    try:
        return ale.ale(rows, "score", ["lat"], "lat", cat="model", kind="ridge", boot=200)
    except ValueError:
        return None


def render(snap: dict) -> dict[str, tuple[str, str]]:
    """Returns {filename: (caption, svg)} in gallery order."""
    runs, cases = latest_runs(snap), snap["cases"]
    out: dict[str, tuple[str, str]] = {}
    ext_models = _models(runs, lambda t: t in TASKS)
    tasks = [t for t in TASKS if any((t, m) in runs for m in ext_models)]

    def ext(t, m, f):
        r = runs.get((t, m))
        return f(r) if r else None

    cap = "Extraction score by document type"
    out["extraction_score_by_type.svg"] = (cap, sc.grouped_bars(
        cap, [TASK_LABEL[t] for t in tasks],
        [(model_label(m), model_color(m), [ext(t, m, lambda r: r["metrics"].get("overall_score")) for t in tasks])
         for m in ext_models],
        ymax=1.0, fmt=lambda v: f"{v:.2f}", tick_fmt=lambda t: f"{t:.1f}",
        subtitle=f"Mean overall_score of each model's latest real frozen-prompt run (n ≥ {MIN_N}) per type"))

    cap = "Per-document extraction scores"
    out["extraction_per_document.svg"] = (cap, sc.strips(
        cap, [(TASK_LABEL[t], [(model_label(m), model_color(m),
                                [c["scores"]["overall_score"] for c in cases[runs[(t, m)]["run_id"]]
                                 if isinstance(c["scores"].get("overall_score"), (int, float))])
                               for m in ext_models if (t, m) in runs]) for t in tasks],
        subtitle="One dot per document, tick = mean. Wide strips = scores vary document to document"))

    groups = []
    for t in tasks:
        by_sub: dict[str, list[float]] = defaultdict(list)
        for m in ext_models:
            if (t, m) in runs:
                for c in cases[runs[(t, m)]["run_id"]]:
                    if isinstance(c["scores"].get("overall_score"), (int, float)) and c.get("expected_subclass"):
                        by_sub[c["expected_subclass"]].append(c["scores"]["overall_score"])
        rows = sorted(((k, v) for k, v in by_sub.items() if len(v) >= 3), key=lambda kv: -sum(kv[1]) / len(kv[1]))
        if rows:
            groups.append((TASK_LABEL[t], [(f"{k.replace('_', ' ')} (n={len(v)})", sc.BLUE, v) for k, v in rows]))
    cap = "Extraction score by subclass"
    out["extraction_by_subclass.svg"] = (cap, sc.strips(
        cap, groups, label_w=230,
        subtitle="All models pooled; subclasses with at least 3 scored documents, highest mean first"))

    def cost_per_doc(r):
        perf, n = r.get("performance") or {}, r["metrics"].get("n") or 0
        c = perf.get("cost_usd_total", perf.get("cost_usd_est_total"))
        return c / n if isinstance(c, (int, float)) and n else None

    cap = "API cost per document"
    out["cost_per_document.svg"] = (cap, sc.grouped_bars(
        cap, [TASK_LABEL[t] for t in tasks],
        [(model_label(m), model_color(m), [ext(t, m, cost_per_doc) for t in tasks]) for m in ext_models],
        fmt=lambda v: f"${v * 1000:.2f}", tick_fmt=lambda t: f"${t * 1000:.1f}",
        subtitle="US dollars per 1,000 documents (labels), from each run's cost total over its scored cases"))

    cls_models = _models(runs, lambda t: t == "classification")
    stats = {m: classification_stats(cases[runs[("classification", m)]["run_id"]]) for m in cls_models}
    for m in cls_models:
        conf = stats[m]["confusion"]
        extra = sorted({p for row in conf.values() for p in row if p not in CLASSES})
        cols = CLASSES + extra
        n = runs[("classification", m)]["metrics"]["n"]
        slug = m.split("/")[-1]
        cap = f"LLM sorter confusion matrix · {model_label(m)}"
        out[f"classification_confusion_{slug}.svg"] = (cap, sc.heatmap(
            cap, [CLASS_LABEL[c] for c in CLASSES], [CLASS_LABEL.get(c, c) for c in cols],
            [[conf[t][p] for p in cols] for t in CLASSES],
            subtitle=f"n = {n} documents. Rows = expected class, columns = predicted; shade = share of the row"))

    if cls_models:
        have = [c for c in CLASSES if any(c in stats[m]["subclass"] for m in cls_models)]

        def sub_val(m, c, f):
            s = stats[m]["subclass"].get(c)
            return f(s) if s else None

        cap = "LLM sorter subclass accuracy"
        out["classification_subclass.svg"] = (cap, sc.grouped_bars(
            cap, [CLASS_LABEL[c] for c in have],
            [(model_label(m), model_color(m), [sub_val(m, c, lambda s: s["correct"] / s["n"]) for c in have])
             for m in cls_models], ymax=1.0, tick_fmt=lambda t: f"{t:.1f}", ref=(0.75, "P0 subclass gate 0.75"),
            subtitle=f"n = {CLS_MIN_N} runs. Documents whose class was right; share with the right subclass"))
        ref = stats[cls_models[0]]["subclass"]
        cap = "LLM sorter collapse signal"
        out["classification_collapse.svg"] = (cap, sc.grouped_bars(
            cap, [CLASS_LABEL[c] for c in have],
            [(model_label(m), model_color(m), [sub_val(m, c, lambda s: s["top_pred"][1] / s["n"]) for c in have])
             for m in cls_models]
            + [("most common true subclass", sc.GREY,
                [ref[c]["top_true"][1] / ref[c]["n"] if c in ref else None for c in have])],
            ymax=1.0, tick_fmt=lambda t: f"{t:.1f}", labels=False,
            subtitle="Share of each class's subclass predictions on its single most common answer; far above grey = collapse"))

        rel = {m: reliability(cases[runs[("classification", m)]["run_id"]]) for m in cls_models}
        rel = {m: r for m, r in rel.items() if r}
        if rel:
            series = [{"name": "perfect calibration", "color": sc.GREY, "x": [0.5, 1.0], "y": [0.5, 1.0], "dash": "4 3"}]
            series += [{"name": model_label(m), "color": model_color(m),
                        "x": [b["conf"] for b in r["bins"]], "y": [b["acc"] for b in r["bins"]]} for m, r in rel.items()]
            cap = "LLM sorter calibration"
            out["classification_calibration.svg"] = (cap, sc.lines(
                cap, series, x_label="stated confidence (bin mean)", y_label="doc-class accuracy",
                y_range=(0.5, 1.0), y_fmt=lambda t: f"{t:.1f}", x_fmt=lambda t: f"{t:.2f}",
                subtitle="ECE " + ", ".join(f"{model_label(m)} {r['ece']:.3f}" for m, r in rel.items())
                         + f" · bins with ≥ {BIN_MIN_N} docs · below diagonal = overconfident"))

    for t in tasks:
        a = latency_ale([runs[(t, m)] for m in ext_models if (t, m) in runs], cases)
        if not a:
            continue
        cap = f"ALE: latency on extraction score · {TASK_LABEL[t]}"
        out[f"ale_latency_{t}.svg"] = (cap, sc.lines(
            cap, [{"name": "ALE (90% bootstrap band)", "color": sc.BLUE, "x": a["x"], "y": a["ale"], "lo": a["lo"],
                   "hi": a["hi"]}],
            x_label="latency per document (s, log scale)", y_label="Δ score", rug=a["rug"],
            x_fmt=lambda v: f"{2 ** v:.0f}", y_fmt=lambda v: f"{v:+.2f}",
            subtitle=f"Ridge surrogate with model as a factor, n = {a['n']}, cross-validated {a['fit']['metric']} "
                     f"{a['fit']['value']}. Latency stands in for document length"))
    return out


def gallery_md(charts: dict[str, tuple[str, str]], snapshot_stamp: str, rel_dir: str) -> str:
    lines = ["# Eval charts", "",
             f"Generated by `scripts/render_report_charts.py` from `web/data/snapshot.json` "
             f"(snapshot {snapshot_stamp}). The same SVGs are served by the viewer's Charts tab.", ""]
    for name, (cap, _) in charts.items():
        lines += [f"## {cap}", "", f"![{cap}]({rel_dir}/{name})", ""]
    return "\n".join(lines)


def manifest(charts: dict[str, tuple[str, str]]) -> str:
    return json.dumps([{"file": k, "title": cap} for k, (cap, _) in charts.items()], indent=1, ensure_ascii=False) + "\n"


def outputs(snap: dict, charts_dir: Path, gallery: Path) -> dict[Path, str]:
    """Every file the renderer owns, with its expected content."""
    charts = render(snap)
    import os

    rel = os.path.relpath(charts_dir, gallery.parent).replace(os.sep, "/")
    files = {charts_dir / k: svg for k, (_, svg) in charts.items()}
    files[charts_dir / "index.json"] = manifest(charts)
    files[gallery] = gallery_md(charts, snap.get("generated_at", "?"), rel)
    return files
