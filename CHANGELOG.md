# Changelog

All notable changes to mailroom-evals are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] — 2026-09-12

Prompt lineage, essential-sink scoring, and the full post-hoc suite.

### Added

- **Frozen prompt lineage `mailroom-evals-v1`** — 15 prompts (docclass
  lineage KANBAN-090 + intake production template + pipeline evaluator
  rubrics) snapshotted by `scripts/freeze_prompts.py` with sha256 manifest +
  pipeline git provenance; human-readable mirror under `prompts/`;
  drift check (`--check`).
- **Runtime prompt injection** — `evals.prompts.registry.activate()` patches
  the two verified choke points (`managed_prompt_lookup`, LangChain
  `PROMPT_VERSIONS`); default source = frozen v1; `--prompt-source` /
  `--prompt-version` flags; per-run provenance (`prompt_lineage`,
  `prompt_versions`, `pipeline_git`, `prompts_snapshot.json`).
- **Essential scores to sinks** — `ESSENTIAL_SCORES` per scorer family; only
  curated headline metrics reach spans; one `evals-run` rollup span per run.
- **Local LLM-as-judge engine** (`evals/judges/`) — post-hoc judging of
  logged runs with the frozen judge rubrics; case text re-loaded from the
  pinned corpus (verified via case-row `doc_text_sha256`); deterministic
  mock judges; `judgments.jsonl` + append-only follow-up run records.
- **`scripts/score_run.py`** — `--recompute`, `--judge`, `--all-runs`,
  `--export-failures` (the GEPA OBSERVE manifest).
- **`evals/analysis.py` + `scripts/compare_runs.py`** — local run
  aggregation, confusion matrices, A/B deltas with paired bootstrap CIs.
- **GEPA scaffold** — `evals/prompts/mutations.py` (four validation gates),
  `scripts/prompt_engineer.py` (DRAFT tool), `prompt-engineer` subagent +
  `PROMPT_ENGINEER_GEPA_PROVENANCE.md` (mechanics pinned to gepa-ai/gepa @
  `b265bf9`, arXiv 2507.19457).
- **Experiment-log schema v2** — `judging` block, case-row
  `doc_text_sha256`, prompt-lineage fields; v1 records stay valid.
- **Docs** — `docs/prompt-lineage.md`; README prompt-lineage + local-scoring
  sections; AGENTS.md non-negotiables 8–9; prompt-lineage skill.

### Changed

- Test suite grown to 70 tests (prompt lineage, judging, analysis).
- Sink spans now carry essential metrics only (full scores remain in the log).

## [0.1.0] — 2026-09-11

Initial release. Charter: [mailroom-issues #7](https://github.com/LLM-Mailroom-Services/mailroom-issues/issues/7).

### Added

- **Task registry** — 31 tasks across three families:
  - `eval:<node>` (12): intake, classification, contracts, merger_agreement,
    corporate_records, correspondence, insurance_claims, judge_arbiter,
    arbiter, boss, archivist, pipeline_chain.
  - `pilot:<node|chain>` (12): stratified micro-slice presets of every eval task.
  - `calibration:<node>` (7): classify, judge, arbiter, retry, boss, intake, archivist.
- **Corpus case loader** — `Lucius-Morningstar/mailroom-corpus` v8 pinned to
  `eafe1ab4`; `ground_truth` ⇆ `default` join on `filename`; subset grammar
  (`full/train/test/class:/subclass:/fixtures/bundles/streams/pilot/cuad/enron/claims`);
  stratified sampling; family corpora (docclass-pilot, CUAD, Enron, CMS claims).
- **Dual invocation modes** — node-level (raw graph node fns + `DocumentState`)
  and agent-level (agent classes); deterministic mock shim; per-run
  `MAILROOM_BASE_DIR` isolation with daemon-thread drain for the chained pipeline.
- **Deterministic scoring + performance accounting** — pipeline-native scorers
  plus per-case latency, token usage, and estimated cost.
- **Trace sinks** — Braintrust (key-set auto) → local Arize Phoenix → `none`;
  one node-named root span per case; runner sets `OBSERVABILITY_PROVIDER`.
- **Centralized experiment log** — schema v1 (`schemas/experiment_record.v1.json`),
  append-only JSONL index + rendered markdown + self-contained run dirs;
  `--resume` for interrupted runs; `--export csv|parquet`.
- **Calibration machinery** — reliability tables, ECE, threshold sweeps,
  bootstrap CIs, REPORT-ONLY threshold recommendations under `reports/calibration/`.
- **Project agent skills** (7) and **subagents** (5) under `.opencode/`.
- **Hermetic test suite** — 49 tests; full mock smoke across all 12 eval tasks.
