# Changelog

All notable changes to mailroom-evals are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
