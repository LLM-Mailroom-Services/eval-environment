<div align="center">

# mailroom-evals

**Evaluation environment for the LLM-Mailroom — per-node performance evals, pilot scenarios, and calibration suites over the mailroom-corpus.**

One task registry for every LLM-based node in the 13-node LangGraph pipeline.
Two invocation modes (graph node or underlying agent). Traced to Braintrust or
local Arize Phoenix. Every run lands in one centralized, append-only
experiment log — machine-readable JSONL, human-readable markdown tables.

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Pipeline under test](https://img.shields.io/badge/pipeline-llm--mailroom%20v0.6.0-4C8CBF)](https://github.com/LLM-Mailroom-Services/Digital-Mailroom)
[![Dataset](https://img.shields.io/badge/dataset-Lucius--Morningstar%2Fmailroom--corpus%20v8-F5A623)](https://huggingface.co/datasets/Lucius-Morningstar/mailroom-corpus)
[![Tracing](https://img.shields.io/badge/tracing-Braintrust%20%7C%20Phoenix-8A2BE2)](#trace-sinks)
[![Tasks](https://img.shields.io/badge/tasks-31%20registered-2EA043)](#the-task-families)
[![Contributor](https://img.shields.io/badge/contributor-Exios66-blue)](https://github.com/Exios66)

</div>

| At a glance | |
|---|---|
| **Pipeline under test** | [`llm-mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom) — 13-node LangGraph state machine (pkg `mailroom`, resolved as a local editable path source) |
| **Dataset** | [`Lucius-Morningstar/mailroom-corpus`](https://huggingface.co/datasets/Lucius-Morningstar/mailroom-corpus) schema v8, **pinned** to revision `eafe1ab4` — 2,000 docs (1,792 train + 208 test) |
| **Task families** | `eval:<node>` (performance) · `pilot:<node\|chain>` (cheap validation) · `calibration:<node>` (edge-test + threshold recommendation) |
| **Invocation** | `--invoke node` (raw graph node fns with corpus-built `DocumentState`) or `--invoke agent` (agent classes directly) |
| **Trace sinks** | Braintrust (when `BRAINTRUST_API_KEY` is set) → local Arize Phoenix → `none` — never Langfuse (per [mailroom-issues #7](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/7)) |
| **Experiment log** | Append-only `reports/experiment_log.jsonl` + rendered `.md` + self-contained per-run dirs (`data/experiments/<run_id>/`) |
| **Mock mode** | Deterministic fake LLM — the full suite runs hermetic (zero network, zero spend) |

---

This repository consists of:

- **A task registry** (`src/evals/registry.py`) — 31 registered tasks across three families covering every LLM-based pipeline node: intake, classify (sorter), five extraction specialists (contracts, merger agreement, corporate records, correspondence, insurance claims), judge + arbiter, boss escalation, archivist, and the full chained pipeline.
- **A corpus case loader** (`src/evals/cases.py`) — the one data path onto `mailroom-corpus`: config joins (`ground_truth` ⇆ `default` on `filename`), the subset grammar (`full/train/test/class:/subclass:/fixtures/bundles/streams/pilot/cuad/enron/claims`), stratified sampling, and integrity verification.
- **Dual-mode invocation** (`src/evals/invoke.py`) — node-level measurement (call `classify_node`, `extract_node`, `judge_verify_node`, … with a faithful `DocumentState`) or agent-level measurement (call `SorterAgent`, specialists, `CompletenessJudge`, … directly), plus a deterministic mock shim and per-run `MAILROOM_BASE_DIR` isolation.
- **Deterministic scoring + performance accounting** (`src/evals/scoring.py`) — the pipeline's own scorers (`classes_match`, suite/field scoring) plus per-case latency, token usage, and cost: per-node performance analysis is a first-class output.
- **Trace-sink wiring** (`src/evals/tracing.py`) — one root span per case named after the node's stable observation name (`classify-document`, `judge-verify`, …), curated inputs (never raw document text), scorer metrics attached to spans.
- **A centralized experiment log** (`src/evals/experiment_log.py` + `schemas/experiment_record.v2.json`) — one versioned record schema for all families; strict JSONL for machines, rendered tables for humans.
- **A frozen prompt lineage** (`src/evals/prompts/` + `prompts/`) — `mailroom-evals-v1`, the official prompt version 1 snapshotted from the mailroom docclass lineage (KANBAN-090), injected into the pipeline at runtime with full provenance (sha256 + pipeline git commit per run) and drift detection — the seed for the GEPA prompt-mutation loop.
- **Local scoring self-sufficiency** (`src/evals/judges/`, `scripts/score_run.py`, `evals/analysis.py`) — the full evaluation suite runs post hoc from the experiment log: deterministic recompute, local LLM-as-judge over frozen rubrics, A/B comparisons with bootstrap CIs. Sinks carry tracing + essential scores only.
- **Calibration machinery** (`src/evals/calibration/`) — reliability tables, ECE, threshold sweeps, bootstrap CIs, and REPORT-ONLY threshold recommendations over the corpus's fixtures grid.
- **Project agent skills** (`.opencode/skills/`) — a tool router plus dedicated skills for the corpus, both trace sinks, the experiment log, calibration methodology, pipeline internals, and eval engineering; **subagents** (`.opencode/agents/`) for run execution, corpus curation, trace auditing, calibration analysis, and log hygiene.

## Contents

- [Getting started](#getting-started) — [Quick Start](#quick-start) · [Installation](#installation)
- [The task families](#the-task-families) — [Task catalog](#task-catalog) · [Invocation modes](#invocation-modes)
- [Datasets & subsets](#datasets--subsets) — [Ground-truth columns](#ground-truth-columns) · [Subset grammar](#subset-grammar)
- [Trace sinks](#trace-sinks)
- [The experiment log](#the-experiment-log)
- [Vercel viewer & dashboard](#vercel-viewer--dashboard)
- [Prompt lineage & GEPA](#prompt-lineage--gepa)
- [Scoring: essential in-sink, full post-hoc](#scoring-essential-in-sink-full-post-hoc)
- [Pilot scenarios](#pilot-scenarios)
- [Calibration scenarios](#calibration-scenarios)
- [Scoring & performance metrics](#scoring--performance-metrics)
- [Operations](#operations) — [Configuration](#configuration) · [Prompt iteration](#prompt-iteration) · [Testing](#testing) · [Project structure](#project-structure)
- [The Mailroom umbrella](#the-mailroom-umbrella)

## Getting started

### Quick Start

> [!NOTE]
> **Mock first, always.** `--mock` installs a deterministic fake LLM: the full
> suite — corpus loads, node invocation, scoring, tracing, experiment log —
> runs with zero network and zero spend. Reach for `--real` only after a mock
> pilot is green.

```bash
# 1. Install (resolves llm-mailroom as a local editable path source)
uv sync --extra dev

# 2. List the 31 registered tasks
uv run python scripts/run_evals.py --list

# 3. CI-grade smoke: every eval task, mock LLM, 2 cases each
uv run python scripts/run_evals.py --task all --mock --n 2

# 4. One node, node-mode invocation, a stratified real slice
uv run python scripts/run_evals.py --task eval:insurance_claims --real \
    --subset class:insurance_claim --sample 25 --seed 42

# 5. Pilot the full chained pipeline (stratified micro-slice + fixture pinch)
uv run python scripts/run_evals.py --task pilot:pipeline_chain --mock

# 6. Calibrate the sorter's confidence gate on the fixtures grid
uv run python scripts/run_evals.py --task calibration:classify --real

# 7. Read the results
uv run python scripts/render_experiment_log.py --validate
uv run python scripts/render_experiment_log.py
open reports/experiment_log.md
```

Every run prints a `run_id` (`<UTC stamp>-<family>-<task>`), appends one line
to `reports/experiment_log.jsonl`, and writes a self-contained directory under
`data/experiments/<run_id>/`.

### Installation

```bash
uv sync --extra dev        # recommended — resolves the path source + lockfile
pip install -e ".[dev]"    # or plain pip (uses the same path source)
```

The pipeline under test is resolved from the sibling checkout:

```toml
[tool.uv.sources]
mailroom = { path = "../Digital-Mailroom/packages/llm-mailroom", editable = true }
```

> **Moving machines?** Re-point `[tool.uv.sources]` at the new checkout (or a
> git source). Everything else in this repo is self-contained.

Real runs need `OPENROUTER_API_KEY` (the pipeline's provider registry resolves
per-agent models). See [Configuration](#configuration) for the full env table.

## The task families

| Family | Purpose | Data | Output |
|---|---|---|---|
| `eval:<node>` | **Performance analysis of individual nodes** — accuracy/quality metrics + per-case latency, tokens, cost | any subset up to the full 2,000-doc corpus | metrics + performance in the experiment log; one span per case in the trace sink |
| `pilot:<node\|chain>` | **Cheap validation** of wiring (corpus → invoke → score → trace → log) before full sweeps | stratified micro-slice (1 doc per class × subclass) + a fixtures pinch for decision nodes | same report shape, tagged `pilot` |
| `calibration:<node>` | **Edge-test + calibrate** node decision boundaries | the corpus `fixtures` grid (+ `bundles`/`streams` for intake) | reliability table, ECE, threshold curves, REPORT-ONLY threshold recommendations under `reports/calibration/` |

### Task catalog

| Task | Node observed | Default subset | Scorer focus |
|---|---|---|---|
| `eval:intake` | `intake` (`intake-document`) | `full` | no-truncation invariant, normalization, triage agreement |
| `eval:classification` | `classify` (`classify-document`) | `full` | doc-class accuracy, subclass accuracy |
| `eval:contracts` | `extract` (`extract-fields`) | `class:contract` | suite field score, CUAD clause-label P/R/F1 |
| `eval:merger_agreement` | `extract` | `class:merger_agreement` | suite field score, MAUD clause-label P/R/F1 |
| `eval:corporate_records` | `extract` | `class:corporate_record` | suite field score |
| `eval:correspondence` | `extract` | `class:correspondence` | suite field score |
| `eval:insurance_claims` | `extract` | `class:insurance_claim` | suite field score over the 13 insurance GT fields |
| `eval:judge_arbiter` | `judge_verify` (`judge-verify`) | `fixtures` | verdict agreement vs `review_expected` |
| `eval:arbiter` | `arbiter` (`arbitrate-verdict`) | `fixtures` | decision validity + agreement vs `arbiter_outcome` |
| `eval:boss` | `boss_escalation` (`adjudicate-conflict`) | `fixtures` | decision validity on conflicting fixtures |
| `eval:archivist` | `archive` (`archive-document`) | `fixtures` | manifest/audit/sha256/stage conformance (isolated base dir) |
| `eval:pipeline_chain` | full 13-node graph (`document-pipeline`) | `pilot` | terminal stage vs `expected_stage`, end-to-end class + extraction scores |

Each task also exists as `pilot:<name>`; the seven calibration tasks are
`calibration:classify|judge|arbiter|retry|boss|intake|archivist`.

### Invocation modes

```bash
--invoke node    # (default) raw graph node fns with a corpus-built DocumentState
--invoke agent   # underlying agent classes directly (agent_eval.py style)
```

- **node mode** builds a faithful `DocumentState` per case (ids, filename,
  `doc_text`, `file_path` materialized in the isolated base dir, `doc_type`
  from ground truth for extract dispatch) and calls the real node function —
  the same code path the pipeline runs, including judge gating and retry
  guards.
- **agent mode** calls the agent class directly — cheaper, and the right
  shape for prompt A/B iterations on one agent.
- `eval:pipeline_chain` runs the compiled graph via `run_pipeline()` and is
  node-mode only.

## Datasets & subsets

The one loading path is `evals.cases` → `pipeline.hf_corpus_loader`: the
`ground_truth` config (labels) joined to `default` (blind text) on
`filename`, **pinned** to revision `eafe1ab4c0d330d8f9c7a5fb254155e75d290828`,
with `content_sha256` verification. Never zip rows positionally — always join.

| config | train | test | contents |
|---|---|---|---|
| `default` | 1,792 | 208 | blind: `filename`, `doc_text`, `prompt`, `metadata` |
| `ground_truth` | 1,792 | 208 | labels + provenance (~60 columns) |
| `fixtures` | 26 | 6 | calibration cells (see [Calibration scenarios](#calibration-scenarios)) |
| `bundles` | 46 | 4 | duplicate/bundle families |
| `streams` | 58 | 4 | thread/stream scenarios |

Train + test = **2,000 docs = the full dataset**. Family corpora (via the
`hf_corpora` registry): `docclass-pilot` (138 stratified class × subclass),
`mailroom-cuad-contracts-full` (510), `enron-correspondence-dedup` (247k),
`cms-desynpuf-insurance-claims` (400).

### Ground-truth columns

| column | drives |
|---|---|
| `expected` | classify/sorter accuracy — `contract · merger_agreement · corporate_record · correspondence · insurance_claim` |
| `expected_subclass` | subclass accuracy (MAUD consideration, record type, …) |
| `expected_specialist` | extract-node dispatch verification |
| `expected_stage` | chained-pipeline terminal-stage conformance (`archived`, `review`, …) |
| `review_expected` / `retry_expected` | judge, arbiter, and retry calibration labels |
| insurance fields (`claim_number`, `policy_number`, `insurer`, `insured_party`, `claim_type`, `date_of_loss`, `date_filed`, `claimed_amount`, `adjuster`, `damages_description`, `coverage_determination`, `denial_reasons`, `supporting_documents`) | insurance-claims extraction scoring |
| `cuad_clause_labels` / `maud_clause_labels` | clause-label precision/recall/F1 |

### Subset grammar

```
full | train | test | class:<name> | subclass:<class>:<subclass>
fixtures | bundles | streams | pilot | cuad | enron | claims
```

Combine with `--sample N --seed S` (stratified by `expected`) and `--n N`
(hard cap). `full` = all 2,000 rows; `train`/`test` select the split; class
and subclass slices filter the train split.

## Trace sinks

Default order (`--trace-backend auto`): **Braintrust** when
`BRAINTRUST_API_KEY` is set → **local Arize Phoenix** (cost-free) → `none`.

```bash
# Braintrust
export BRAINTRUST_API_KEY=...
export BRAINTRUST_PROJECT=mailroom-evals

# Phoenix (local, zero spend)
phoenix serve                      # http://localhost:6006
uv run python scripts/run_evals.py --task eval:classify --real --trace-backend phoenix
```

- The runner sets `OBSERVABILITY_PROVIDER` to the resolved backend **before**
  any agent instantiation, so llm-mailroom's `get_llm` wraps the OpenAI client
  with the matching instrumentation — every LLM call inside a node auto-traces.
- One root span per case, named after the node's stable observation name;
  curated input (ids + class + char count, never raw text); scorer metrics
  attached to the span; `flush()` per case; failures warn, never fail a run.
- Langfuse is intentionally **not** a sink here — issue #7 names Phoenix
  and/or Braintrust.

## Vercel viewer & dashboard

`web/` is a zero-dependency static site — a **dedicated viewer of eval run
results** plus a **dashboard of the eval environment itself** — deployed on
Vercel via the GitHub integration (same pattern as the DMR dispatch board).

**Views**: Dashboard (health badges, runs/day sparkline, per-task status,
recent-activity feed) · Runs (filterable index of every recorded run) ·
**Trends** (per-task metric history over time — SVG chart, best/worst/mean,
mock-vs-real split) · **Compare** (A/B any two runs: metric deltas with
better/worse verdicts + per-case disagreement tables) · Run detail (metrics,
provenance, expected→predicted matrices for class AND subclass, failures-only
case filter) · Tasks (the 31-task catalog) · Corpus (the pinned revision +
subset grammar) · Prompts (frozen lineage browser + GEPA mutations) ·
Environment (health checks, command surface, skills/subagents,
non-negotiables). Project dashboard:
[Vercel → eval-environment](https://vercel.com/lucius-projects-54efe0bb/eval-environment/A5xZpmnPeh8RB2H2Pjn3acTtn4RS).

**Data flow**: the raw experiment log stays local (per `.gitignore`); the
viewer reads one tracked, generated snapshot:

```bash
uv run python scripts/export_site_snapshot.py          # regenerate web/data/snapshot.json
uv run python scripts/export_site_snapshot.py --check  # exit 1 if stale vs the log
```

Refresh discipline: whenever the experiment log changes, re-export and
commit the snapshot — the viewer then shows it on the next Vercel deploy.
The snapshot embeds run summaries + capped case rows (250/run), the task
catalog, corpus pin, prompt lineage manifest, and in-process health checks
(log validation + lineage drift), with a visible `generated_at` staleness
stamp in the header.

The viewer itself has a headless regression check (DOM-stubbed, no browser
needed — catches empty renders and leaked `undefined`/`NaN` across every
route):

```bash
node scripts/viewer_smoke.js
```

**Deployment** (one-time, via the already-configured Vercel account):
Vercel → Add New Project → import `LLM-Mailroom-Services/eval-environment`
→ framework **Other** (zero-config; root `vercel.json` rewrites `/` to the
viewer and serves `web/data/`) → Deploy. No env vars, no build command, no
functions. Every push to `main` redeploys.

## Prompt lineage & GEPA

Every eval run measures the **frozen `mailroom-evals-v1` lineage** — the
official prompt version 1 snapshotted from the mailroom docclass lineage
(KANBAN-090) plus the pipeline evaluator rubrics — injected into the live
pipeline at runtime (`--prompt-source frozen|live-docclass|production`,
`--prompt-version <key>` for explicit pins). Full details, the freeze/drift
workflow, and the GEPA mutation scaffold live in
[`docs/prompt-lineage.md`](docs/prompt-lineage.md).

```bash
uv run python scripts/freeze_prompts.py --check      # drift check vs the live pipeline
uv run python scripts/run_evals.py --task eval:classify --real \
    --subset class:contract --sample 50 --prompt-version sorter_v2   # a GEPA candidate A/B
```

Provenance is automatic: every run records `prompt_lineage`, per-agent
resolved keys + sha256s, the pipeline git commit, and a full
`prompts_snapshot.json` in the run dir.

## Scoring: essential in-sink, full post-hoc

**Sinks carry essential scores only** — one to three headline metrics per
case (`class_correct`, `overall_score`, `judge_agrees`, … per family in
`evals.scoring.ESSENTIAL_SCORES`) plus one run-level rollup span
(`evals-run`) with the essential aggregates. Everything else — the full
deterministic suite, LLM-as-judge across all dimensions, A/B analysis — runs
**post hoc, locally, from the experiment log**:

```bash
uv run python scripts/score_run.py --run-id <id> --recompute        # re-score with current scorers
uv run python scripts/score_run.py --run-id <id> --judge verdict,quality --mock   # local judges (frozen rubrics)
uv run python scripts/score_run.py --run-id <id> --export-failures data/manifests/<id>.failures.jsonl
uv run python scripts/compare_runs.py --a <baseline> --b <candidate> --md reports/comparisons/
```

Judgments use the **frozen** `judge_v1` / `judge-classification_v1` /
`judge-correctness_v1` / `pipeline_verdict_v1` / `pipeline_quality_v1`
rubrics, re-load case text from the pinned corpus (verified via the case
row's `doc_text_sha256`), and append `judgments.jsonl` to the run dir plus a
follow-up run-summary record — history stays append-only. `--mock` judges
derive deterministic verdicts from the stored scores (CI-safe, zero network).

## The experiment log

One canonical, versioned record schema (`schemas/experiment_record.v1.json`)
for all three families. Append-only; never overwrite.

```
reports/experiment_log.jsonl          # THE index — one line per RUN
reports/experiment_log.md             # rendered tables (rebuildable, idempotent)
data/experiments/<run_id>/cases.jsonl # one line per CASE (full fidelity)
data/experiments/<run_id>/summary.json# the same run summary, self-contained
```

- **Machine-readable**: strict JSONL, `schema_version` on every record,
  flat dotted keys (`pandas.json_normalize`-ready), `load_runs()` /
  `load_cases(run_id)` / `export_run(run_id, "csv"|"parquet")`.
- **Human-readable**: markdown is tables only — run index, per-run metadata,
  dataset provenance, metrics, performance, calibration sections, per-case
  results. Floats 4dp, bools ✓/✗, never raw JSON dumps.
- **Storable**: self-contained per-run dirs; env-overridable paths
  (`EXPERIMENT_LOG_PATH`, `EXPERIMENT_LOG_MD_PATH`, `EVALS_EXPERIMENTS_DIR`);
  git snapshot stamped per run; torn tails tolerated on load.
- **Cross-referenced**: every record carries the trace backend + ids, so log
  rows ↔ Braintrust/Phoenix traces join on `run_id`.
- Small runs (≤ 50 cases) inline their case rows into the central line;
  larger runs carry a `cases_ref` pointer.

Long runs are protected by `--resume <run_id>`: recorded cases are skipped
and the run dir is appended to, with the resume provenance stamped in
`params`.

## Pilot scenarios

A pilot is a task run over a **stratified micro-slice** — one document per
class × subclass stratum from `docclass-pilot`, plus a three-fixture pinch
for decision nodes (judge, arbiter, boss, archivist). Pilots exist to
validate the whole chain (corpus load → invocation → scoring → tracing →
experiment log) at near-zero cost:

```bash
uv run python scripts/run_evals.py --task pilot:classification --mock   # CI gate
uv run python scripts/run_evals.py --task pilot:pipeline_chain --real   # 5-doc chain pilot
```

Mock pilots are the CI gate; real pilots are the gate before any `full` run.

## Calibration scenarios

Calibration tasks edge-test a node's **decision boundaries** against the
corpus `fixtures` grid and emit threshold recommendations — report-only,
never auto-applied to pipeline configs.

The fixtures grid (26 train + 6 test) is purpose-built for this:

| column | values |
|---|---|
| `calibration_cell` | `correct_high` · `correct_low` · `wrong_high` · `wrong_low` (the 2×2 confidence grid) |
| `fixture_kind` | `conflicting`(6) · `retry_review`(5) · `low_confidence`(4) · `high_confidence`(3) · `incomplete`(3) · `ambiguous`(3) · `retry`(2) |
| `probes_confidence` | the confidence the sorter should emit (e.g. `0.985`, `0.895`) |
| `failure_stage` | `ingestion · classification · extraction · grouping · adjudication · archival` |
| `arbiter_outcome` | `stands` · `re_extract` · `escalate_human_review` |
| `review_expected` / `retry_expected` / `expected_stage` | gating labels (`review` / `archived`) |

| task | probes | key outputs |
|---|---|---|
| `calibration:classify` | 2×2 grid + low/high-confidence fixtures | reliability table, ECE, review-gate threshold rec vs `review_expected` |
| `calibration:judge` | `incomplete` fixtures + `review_expected` rows | completeness-threshold sweep, agreement CI |
| `calibration:arbiter` | `arbiter_outcome` cells | per-decision confusion, boundary recs |
| `calibration:retry` | `retry_expected` + `failure_stage` rows | per-stage coverage, retry-trigger threshold rec |
| `calibration:boss` | `conflicting` fixtures | decision validity, review-routing rate |
| `calibration:intake` | messy/ambiguous + `bundles` + `streams` | no-truncation violations, triage agreement CI |
| `calibration:archivist` | `failure_stage=archival` rows | manifest/audit/sha256/stage conformance rates |

Reports land under `reports/calibration/<task>/<stamp>.{json,md}` with
per-cell confusion, reliability table, ECE, threshold curves, bootstrap CIs,
and `recommended_thresholds` mapped to concrete config hints. Small cells get
"insufficient evidence" verdicts, not thresholds.

## Scoring & performance metrics

Scoring reuses the pipeline's own deterministic scorers wherever they exist —
`classes_match` for classification, the suite/field scorers for extraction —
so eval numbers measure the same rubric the pipeline runs. LLM-as-judge is
out of scope for v1 (the deterministic layer is the contract).

Every case records **performance** regardless of family:

| metric | meaning |
|---|---|
| `latency_ms` / `latency_ms_mean` / `latency_ms_p95` | wall-clock per case (node-mode = the node's own cost) |
| `tokens_prompt_total` / `tokens_completion_total` | via the pipeline's run accumulator (`pipeline.limits.record_usage`) |
| `cost_usd_est` | estimated per-case cost when the model's pricing is registered |

## Operations

### Configuration

| variable | used for | default |
|---|---|---|
| `OPENROUTER_API_KEY` | real LLM runs (`--real`) | — (required for real) |
| `BRAINTRUST_API_KEY` / `BRAINTRUST_PROJECT` | Braintrust sink | auto-selects Braintrust when set / `mailroom` |
| `PHOENIX_ENDPOINT` / `PHOENIX_PROJECT` / `PHOENIX_SERVICE_NAME` | Phoenix sink | `http://localhost:6006/v1/traces` / `mailroom-evals` |
| `EVALS_TRACE_BACKEND` | default backend without the CLI flag | `auto` |
| `OBSERVABILITY_PROVIDER` | set BY the runner — do not export | (resolved backend) |
| `HF_TOKEN` | optional headroom on Hub reads | anonymous (public, ungated) |
| `MAILROOM_HF_CACHE_DIR` | parquet cache root | `<base>/hf_cache/corpus` |
| `EXPERIMENT_LOG_PATH` / `EXPERIMENT_LOG_MD_PATH` / `EVALS_EXPERIMENTS_DIR` | log locations | `reports/experiment_log.{jsonl,md}` / `data/experiments` |
| `MAILROOM_BASE_DIR` | set BY the runner per run — isolation | (temp dir) |

> [!WARNING]
> Archive/intake/chain evals write real bins, manifests, SQLite catalogs, and
> audit chains. The runner isolates every run inside a temp `MAILROOM_BASE_DIR`
> and drains off-path daemon threads before restoring it — never run evals
> against a live data dir.

### Prompt iteration

Prompt versions are a first-class dimension of every record:

```bash
uv run python scripts/run_evals.py --task eval:classification --real \
    --subset class:contract --sample 50 --prompt-version sorter_docclass_v7
uv run python scripts/run_evals.py --task eval:classification --real \
    --subset class:contract --sample 50 --prompt-version sorter_docclass_v8
```

`prompt_version` rides the trace metadata, the experiment-log records, and
the report filenames — A/B comparisons are log filters, not new machinery.

### Testing

```bash
uv run pytest tests/ -q          # 49 tests, fully hermetic (no network, no tracing)
```

The suite covers the subset grammar, scorers (gold-in/gold-out), the
experiment-log round-trip, calibration machinery, trace-backend resolution,
registry completeness, and runner smoke (mock mode, stubbed cases).

### Project structure

```
eval-environment/
├── pyproject.toml                     # uv pkg "mailroom-evals"; mailroom = path source
├── schemas/experiment_record.v2.json  # the record contract (v1 records stay valid)
├── prompts/                           # frozen lineage mirror + manifest + mutations (generated)
├── src/evals/
│   ├── registry.py                    # 31 tasks: eval | pilot | calibration
│   ├── cases.py                       # corpus loading + subset grammar + stratified sampling
│   ├── invoke.py                      # node-level + agent-level invocation, mocks, isolation
│   ├── scoring.py                     # deterministic scorers + essential-sink curation + perf
│   ├── tracing.py                     # Braintrust → Phoenix → none; per-case + run-rollup spans
│   ├── runner.py                      # shared execution engine (CLI semantics)
│   ├── experiment_log.py              # append-only log + markdown renderer + export + judging
│   ├── pilot.py                       # stratified micro-slice presets
│   ├── analysis.py                    # local run aggregation + A/B comparisons (bootstrap CIs)
│   ├── judges/                        # local LLM-as-judge engine (post-hoc, mock judges)
│   ├── prompts/                       # frozen_v1 + lineage registry + runtime injection + GEPA gates
│   ├── tasks/                         # per-node task documentation
│   └── calibration/                   # base + 7 node analyzers (report-only)
├── scripts/
│   ├── run_evals.py                   # the eval CLI
│   ├── score_run.py                   # post-hoc local scoring (recompute / judge / failures)
│   ├── compare_runs.py                # A/B comparisons with bootstrap CIs
│   ├── freeze_prompts.py              # freeze the lineage + drift check
│   ├── prompt_engineer.py             # GEPA DRAFT tool (one surgical mutation per iteration)
│   └── render_experiment_log.py       # rebuild/validate the markdown log
├── tests/                             # hermetic pytest suite (70 tests)
├── .opencode/skills/                  # project skills (router + specialties)
└── .opencode/agents/                  # subagents (runner, corpus, traces, calibration, log, GEPA)
```

## The Mailroom umbrella

- [`Digital-Mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom) — the monorepo; `packages/llm-mailroom` is the pipeline under test.
- [`mailroom-issues`](https://github.com/LLM-Mailroom-Services/mailroom-issues) — the task tracker; issue #7 is this repo's charter.
- [`llm-entity-extraction`](https://github.com/Exios66/llm-entity-extraction) — the pattern repo for the runner design (sorter + contract-specialist evals).
- [`The-Mailroom`](https://github.com/LLM-Mailroom-Services/The-Mailroom) — the orchestrating front end.
