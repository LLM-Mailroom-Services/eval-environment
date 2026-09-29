# Changelog

All notable changes to mailroom-evals are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **Report chart layout** (`src/evals/viz/svgcharts.py`) — long subtitles
  wrap instead of running off the right edge (classification calibration);
  legends are laid out by measured text width and carry the reference-line
  key, so they no longer collide with value labels (classification subclass);
  bar and heatmap labels are measured; confusion-matrix text is 10 px (was
  9.5). All 15 `web/data/charts` SVGs regenerated; data unchanged.
- **Broken link** in `RUN-03-MODERNBERT-HELDOUT-TEST-REPORT.md` to the
  held-out eval JSON.
- `scripts/render_comparison_reports.py` covers `qwen3.7-flash`, and its
  missing suite README `reports/api-comparisons/qwen3.7-flash/README.md` is
  added (12 canonical stems, 550 case rows, 809 LLM calls, $0.579319). It was
  rendered by `render_model_suite_readme` from the committed experiment log;
  every row matches its canonical report (run id, score, calls, cost).
- **Resumed-run wall time** — API-leg reports label `duration_s` as the resume
  segment only when `params.skipped_already_run` > 0, and omit the
  serial-vs-batched ratio (it divided a 100-case latency sum by a 1-case wall
  time on `20260927T101544Z-eval-classification`). Dated correction notes on
  that run and on the `qwen3-8b` merger run, which was served by
  `qwen/qwen3.7-flash`.

### Changed

- **Report excellence (sandbox parity)** — API-leg comparison reports, calibration
  write-ups, and `compare_runs` markdown now include analyst insights, strata,
  scoring-method context (CUAD/MAUD), reproduce/artifacts blocks aligned with
  `mailroom-sandbox/scripts/sand032/report.py`. Regenerate API reports via
  `scripts/render_comparison_reports.py`.
- **Corpus pin → v9.1** — document and skill citations for
  `Lucius-Morningstar/mailroom-dataset` now target revision
  `ed7576b676343e0b402ec5412cded301e629bdee` (supersedes GT-closure
  `46a4d3c240a36671cde0182fff4960f6b8b73aca`; Hub tag `v9.1` not published
  yet). Eval harness runtime still reads `FULL_CORPUS_REVISION` from the
  `mailroom` dependency until the coordinated llm-mailroom pin lands
  ([#57](https://github.com/LLM-Mailroom-Services/eval-environment/issues/57)).

## [0.5.0] — 2026-09-27

SAND-027 Leg B (OpenRouter API) vs Modal parity, Braintrust experiment rows,
comparison-report tree, and experiment-log schema v3.

### Added

- **OpenRouter model roster** — `config/openrouter_models.yaml` (incl.
  `qwen/qwen3-8b`, `qwen/qwen3.7-flash`, `ibm-granite/granite-4.2-8b` with
  live-verified pricing). `--list-models` / `--model` validate slugs, apply a
  uniform OpenRouter override for the run, and price tokens from the roster.
- **Direct specialist OpenRouter path** — `src/evals/specialist_llm.py` runs
  extraction specialists via designated frozen prompts + OpenRouter chat
  completions (no LangChain specialist classes); merger agreements support
  model-specific source-chunk limits and per-chunk JSON retries.
- **Decode comparison profiles** — `qwen3-8b` and `granite-4.2-8b` profiles
  (`src/evals/decode_budget.py`): per-agent completion budgets, IBM Granite
  sampling (`T=1.0`, `top_p=0.95`, `seed=42`), 600 s call timeout, wave cost
  caps; profile sampling reaches the specialist direct-client path.
- **Modal-comparable API reports** — `reports/api-comparisons/<model>/<task>/`
  with immutable `runs/<run_id>.md`, canonical `RUN-<wave>-<CLASS>-<MODEL>-REPORT.md`
  stems, [INDEX.md](reports/api-comparisons/INDEX.md), per-model suite READMEs,
  and **[API-LEG-MASTER-REPORT.md](reports/api-comparisons/API-LEG-MASTER-REPORT.md)**
  (Qwen vs Granite paired deltas + superseded-run index). Regenerate via
  `scripts/render_comparison_reports.py`.
- **OpenRouter + Braintrust runbook** — `docs/openrouter-braintrust-runbook.md`
  (N=20 waves, concurrency reliability, one-coverage-call vs chunking policy,
  Granite validation gates).
- **Braintrust experiment integration** — one scored row per document in
  Braintrust experiments; optional full-corpus Dataset sync
  (`scripts/sync_braintrust_dataset.py`); HF corpus linked to experiments with
  minimal essential span metrics.
- **SAND-027 orchestration** — `scripts/sand027_n20_orchestrate.py`,
  `sand027_n20_waves.sh`, Qwen concurrency-8 rerun helpers; resume-safe wave
  locks; canonical subset draws under `data/manifests/subset-draws/` (#20).
- **Archived production specialists (`*_v0`)** — verbose pre-concise freeze in
  `prompts/archive/` + `archived_production.py`; opt in with
  `--prompt-source archived` or `--prompt-version <role>_v0`.
- **Contracts Modal v33 twin** — `contracts_specialist_v33` archive prompt for
  sandbox parity experiments.
- **Cloud agent environment** — `.cursor/environment.json`,
  `scripts/cloud-agent-install.sh`; CI installs via uv with comparison-report
  snapshot checks.
- **Experiment-log detail files** — short `reports/experiment_log.md` index plus
  per-run `reports/experiment_log/<run_id>.md` write-ups.

### Changed

- **Frozen extraction specialists (concise baseline)** — four specialist v1
  prompts align with sandbox simplified lineage (`97c0f940194f`); promote via
  `scripts/promote_sandbox_specialist.py upgrade-frozen-specialists`.
- **Experiment log schema v3** — `schema_version: 3` (v1/v2 records remain
  valid); richer run summaries (`performance.cost_usd_total` /
  `cost_usd_est_total`, `expected_cost_usd`, comparison-report paths).
- **Specialist concurrency** — real eval waves can run documents concurrently
  (`--concurrency`); runner aggregates per-agent usage and re-prices runs from
  aggregate tokens (not summed rounded per-case costs).
- **Git tracking policy** — `reports/` (experiment log, api-comparisons,
  calibration) tracked; `data/experiments/` and raw tee logs gitignored again.
- **Viewer snapshot** — `export_site_snapshot.py` unwraps prompt mutation JSON;
  snapshot refreshed for 60+ logged runs.

### Fixed

- **Qwen concurrency garble** — retry once on successful but non-JSON
  completions; **one retry slot per coverage chunk** (not one shared slot per
  document).
- **Merger chunk policy** — `CHUNK_CHARS` / `LARGE_COMPLETION_MODELS` scoped by
  doc class (48K multi-chunk for `qwen/qwen3-8b` merger only; Granite ~280K
  context-safe spans; correspondence/insurance never source-chunked on pinned
  draws). Comparison reports flag high call counts vs chunking misconfiguration.
- **Granite compliance** — mandated sampling on specialist wire calls;
  correspondence 16K completion budget after N=20 evidence; merger rerun
  supersedes accidental 48K-chunk Granite wave (~170 calls).
- **Truncated merger JSON** — treat 8k-digit integer overflow / truncated JSON
  as parse misses; disable Qwen thinking on chunked merger path where required.
- **Braintrust rows** — one document row per specialist case (no duplicate
  experiment rows); resume matches model/prompt wave lock.
- **Trace hygiene** — sanitize case refs in trace metadata (#30); checkpointed
  case rows not rewritten at run close.
- **Comparison report costs** — expected vs actual vs roster-estimated cost
  columns; run configuration and serial-vs-batched wall proof in API reports.

### Validation

- **275** hermetic tests (`uv run pytest tests/ -q`).
- SAND-027 Leg B N=20 suites logged for **qwen/qwen3-8b** and
  **ibm-granite/granite-4.2-8b** (six specialist/classification tasks, seed 42,
  Braintrust `Mailroom-Evals`); master report and suite READMEs committed under
  `reports/api-comparisons/`.

## [0.4.0] — 2026-09-13

v9 corpus alignment (`mailroom-dataset` GT-closure `46a4d3c2`), silent-failure
remediation, and tracking restoration.

### Added

- **v9 GT expansion** — schema v9 moved the 13 insurance GT fields plus
  `cuad_clause_labels`/`maud_clause_labels` into a nested `gt_fields` JSON
  payload; `evals.cases._expand_gt_fields` now hoists it (inner JSON-array
  strings parsed, empty containers skipped) so insurance extraction and
  clause-label scoring are live again (insurance extraction_f1 0.55–0.90 on
  the validation sweep vs hard-zero before).
- **LangChain LLM tracing** — `evals.tracing` installs a Braintrust callback
  handler (langchain-core ≥1.x `register_configure_hook`), closing the gap
  where `wrap_openai` only traced raw OpenAI clients: sorter/specialist/judge
  `Chat Completion` spans now nest under their case spans with token metrics
  (verified live: 3/3 nested).
- **Per-case trace refs** — case rows now carry `trace`
  (`{backend, span_id, root_span_id}`) written from the open case span — the
  log ↔ trace cross-reference the schema documented but never populated.
- **Flush health** — run summaries record `flush` (provider, flush_ok,
  flush_failures) so dropped events are affirmatively verifiable per record.
- **Span metadata provenance** — case/rollup spans now carry the task's
  primary role prompt key (`prompt_version`, e.g. `sorter_v1`), the resolved
  per-case model, and `dataset.revision` on the run rollup.
- **`scorer_errors` run metric** — cases whose suite scorer crashed
  (`scorer_error: True`) surface at run level instead of hiding per case.
- **Rehydrated experiment log** — `reports/experiment_log.jsonl` +
  `data/experiments/` were lost with the checkout (gitignored); restored
  113 historical run summaries + 1,292 case rows from the tracked snapshot,
  each annotated `params.reconstructed_from_snapshot`.

### Changed

- **Corpus pin → v9 GT-closure** — `Lucius-Morningstar/mailroom-dataset`
  revision `46a4d3c2` (3,302 docs; default 2,979/323, fixtures 26/6, bundles
  47/3, streams 59/3; v8 parent `mailroom-corpus` @ `eafe1ab4` stays frozen
  for lineage). Updated AGENTS.md, README, skills, agents, and the pin test.
- **Snapshot projection** — run records now keep `trace_ids`, `judging`,
  `pipeline_git`, and `prompt_versions` so judging follow-up rows are
  distinguishable from their originals and trace cross-references survive.

### Fixed

- **Archivist silent zeros** — verification searched the archive for the RAW
  corpus filename while staging flattens it (`/`→`_`), so `sha256_ok`
  scored 0 on every real run with a pathed filename (25/25 and 32/32). Now
  matches the flattened name, returns a real `archive_path` (was a
  stringified bool), and verifies content integrity (archived bytes hash to
  the case text) — `sha256_ok = 1.0` verified live.
- **Empty-GT clause scoring** — `score_label_lists` treated the v9 "no
  annotations" convention (`{}`/`[]` JSON strings) as a phantom token and
  scored F1 0.0; empty payloads now skip, JSON objects contribute annotated
  keys, and calibration essential metrics resolve their eval-node alias.
- **No-op resume pollution** — `--resume` on a fully-recorded run appended a
  fake `{"n": 0, "errors": 0}` summary under the same run_id; it now returns
  a `noop_resume` marker without logging.
- **run_id collisions** — `new_run_id()` guards same-second collisions with
  a deterministic `-a<N>` suffix (torn-tail tolerant).
- **GEPA failure predicate** — `score_run.py --export-failures` precedence
  rewritten explicitly and counts `scorer_error` cases as failures.
- **GT catalog fallback** — `cases.py` no longer swallows catalog failures
  silently (logged warning instead of bare `except: pass`).
- **Family corpora fail loudly** — `--subset cuad/enron` raise on 0-case
  loads (Hub-side parquet conversion currently failed/pending) instead of
  silently running empty; family corpora accept registry revisions.

### Validation

- 141 tests green (17 new regression tests for the fixes above).
- Mock gates: 12-task sweep + previously-broken paths
  (`pilot:classification` FileNotFoundError, `calibration:classify` /
  `pilot:pipeline_chain` invoke-mode ValueErrors) all clean.
- Real sweep (qwen/qwen3.7-flash, Braintrust `Mailroom-Evals`): 5/5 passed —
  classification 1.0, insurance_claims overall 0.78, merger 0.46, archivist
  sha256 1.0, calibration:classify report generated — ≈$0.04 total.
- Trace audit: 39/39 case roots present with full metadata; llm-span nesting
  fixed and verified; flush healthy.

## [0.3.0] — 2026-09-12

Real-mode preflight complete: full baseline sweep, calibration sweep, live judges.

### Added

- **Real baseline sweep** — all 12 `eval:*` tasks on real LLM calls
  (qwen/qwen3.7-flash via OpenRouter, 25 cases/task, seed 42): intake
  triage 1.0, classification 0.96, boss 1.0, pipeline_chain 1.0,
  insurance_claims 0.726, corporate_records 0.655, correspondence 0.58,
  contracts 0.566, merger_agreement 0.45, judge_agrees 0.2 / arbiter
  decision_agrees 0.333 (fixture-boundary tasks — agreement CIs recorded).
  Total spend $0.23.
- **Real calibration sweep** — all 7 `calibration:*` tasks with analyzers +
  REPORT-ONLY threshold recommendations (review_gate 0.05, retry_trigger
  0.25, judge_flag_max_completeness 0.05 @ F2 0.65).
- **Live post-hoc judges** — real LLM judging of baseline runs
  (classification 0.93, contracts verdict 1.0, merger_agreement verdict
  0.36); judge client hardened (json-in-prompt fallback + fence stripping).
- **Judge calibration realism** — judge probes now run the real class
  specialist (extract → judge chain) instead of empty/synthetic input;
  gate forced into the class's ambiguous band for review-expected cells.

### Fixed

- **GT scoring surface** — `evals.cases` now emits the pipeline's canonical
  flattened shape (`cuad_clauses`/`maud_clauses` via
  `observability.extraction_gt.catalog_expected_fields`) instead of raw Hub
  label JSON, which the suite scored as 0 (a perfect prediction scored 0.0).
- **Calibration scorers** — `calibration_*` scorer names had no `_score_case`
  branch (every calibration case scored empty → all-zero sweeps); aliased to
  their eval node scorers.
- **Performance totals** — `summarize_performance` reads the rows' nested
  `tokens`/`cost_usd` shape (flat-key reads always yielded 0); per-case cost
  derives the model from usage; run `model` = dominant by_agent model.

## [0.2.0] — 2026-09-12

Prompt lineage, essential-sink scoring, and the full post-hoc suite.

### Added

- **Per-agent performance attribution** — the pipeline usage accumulator
  (`pipeline.limits.record_usage`) now records the calling agent; every case
  row carries `agent_usage` (per-agent calls/tokens/models) and every run
  summary `performance.by_agent` with estimated cost (sorted by spend).
  `AGENT_CATALOG` (registry.py) maps every evaluated node to its agents
  (26 LLM agents + procedural nodes); the experiment log renders a
  per-agent performance table per run; the site snapshot catalogs agents
  (node, role, evaluated-by tasks, models seen) and the viewer renders
  per-agent tables on run detail + an agent catalog on the environment page.
- **Vercel viewer & dashboard** (`web/` + `vercel.json`) — zero-dependency
  static site deployed via the GitHub integration: run-result viewer
  (dashboard / runs / run detail with per-case tables and expected→predicted
  matrices) plus an environment dashboard (task catalog, corpus pin, prompt
  lineage, health checks). Data via the tracked, generated
  `web/data/snapshot.json` (`scripts/export_site_snapshot.py`, `--check`
  staleness mode); root `vercel.json` rewrites `/` to the viewer with
  board-grade security headers.
- **Viewer analytics views** — Trends (per-task metric history over time,
  SVG chart with best/worst/mean and mock/real split) and Compare (A/B two
  runs: metric deltas with better/worse verdicts, per-case disagreement
  tables); run-detail upgrades (failures-only filter, subclass confusion
  matrix); dashboard recent-activity feed; `scripts/viewer_smoke.js`
  headless regression check over every route.
- **Repo `.env` LLM provider loading** — `evals/__init__` loads the gitignored
  `.env` via python-dotenv (override=False — exported vars win). OpenRouter
  (`OPENROUTER_API_KEY`) stays the primary provider; the Vercel AI Gateway
  is a documented alternative (`DEFAULT_PROVIDER=generic` +
  `GENERIC_BASE_URL` + `GENERIC_API_KEY`, OpenAI-compatible, model IDs pass
  through verbatim).

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
  sections; AGENTS.md non-negotiables 8–10; prompt-lineage skill.

### Changed

- Test suite grown to 124 tests (prompt lineage, judging, analysis, site
  snapshot, invoke/pilot/registry, scoring essentials, CLI smoke,
  per-agent performance).
- `run_evals.py` validates `--mock`/`--real` exclusivity and unknown task ids
  (clean `parser.error` instead of a traceback).
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
