# Task catalog

Every task registered in `src/evals/registry.py`. Ids are
`<family>:<name>`; the CLI accepts one id, `all` (eval family), or `--list`.

## Task modules (`src/evals/tasks/`)

Each eval node has a module that frames the measurement as a **request** the
agent/node must fulfill (system-prompt role, entity schema for specialists,
structured output keys). Modules expose `TASK: EvalTask` with
`build_cases` → `invoke` → `score`; the shared runner still executes runs.

Specialist framing (contracts / merger_agreement / corporate_records /
correspondence / insurance_claims):

> Using your activated system prompt, extract the registered live-schema
> entities from the sorter-handed document and return one complete JSON
> object. Unstated values are null or [].

OpenRouter API waves (specialists + sorter): read
[`docs/openrouter-braintrust-runbook.md`](openrouter-braintrust-runbook.md) —
especially **§5 one coverage call per document**. Correspondence and
insurance must never be source-chunked on pinned draws; high call counts on
those tasks are usually JSON retries, not merger-style chunking.

After every run the harness:

1. Forwards **essential** span metrics to the trace sink; on Braintrust, real
   runs also open an **Experiment** linked to a project **Dataset** mirroring
   the pinned HF corpus (`evals.braintrust_experiment`, `BRAINTRUST_EXPERIMENTS=auto`).
   Experiment `scores` are capped to ≤2 headline metrics per case
   (`scoring.sink_score_metrics`); the full suite stays in the experiment log.
2. Writes the **full** deterministic scoring suite to
   `data/experiments/<run_id>/scoring_suite.json`
3. Locks the exact case set to `subset_manifest.json` (+ `.jsonl`) for
   reproducibility
4. Runs **preflight** before any live API spend (`evals.preflight`)

```bash
# Preflight blocks --real without OPENROUTER_API_KEY (or gateway .env)
uv run python scripts/run_evals.py --task eval:contracts --real \
    --subset class:contract --sample 25 --seed 42 \
    --model ibm-granite/granite-4.2-8b \
    --decode-profile granite-4.2-8b \
    --prompt-version contracts_specialist_v1 \
    --trace-backend braintrust --require-trace-sink
```

## eval family — per-node performance analysis

| id | node observed (span name) | default subset | scorer | agent mode |
|---|---|---|---|---|
| `eval:intake` | `intake` (`intake-document`) | `full` | intake invariants + triage agreement | yes |
| `eval:classification` | `classify` (`classify-document`) | `full` | class + subclass accuracy | yes |
| `eval:contracts` | `extract` (`extract-fields`) | `class:contract` | suite field score + CUAD label P/R/F1 | yes |
| `eval:merger_agreement` | `extract` | `class:merger_agreement` | suite field score + MAUD label P/R/F1 | yes |
| `eval:corporate_records` | `extract` | `class:corporate_record` | suite field score | yes |
| `eval:correspondence` | `extract` | `class:correspondence` | suite field score | yes |
| `eval:insurance_claims` | `extract` | `class:insurance_claim` | suite field score (13 insurance GT fields) | yes |
| `eval:judge_arbiter` | `judge_verify` (`judge-verify`) | `fixtures` | verdict agreement vs `review_expected` | yes |
| `eval:arbiter` | `arbiter` (`arbitrate-verdict`) | `fixtures` | decision validity + `arbiter_outcome` agreement | yes |
| `eval:boss` | `boss_escalation` (`adjudicate-conflict`) | `fixtures` | decision validity | yes |
| `eval:archivist` | `archive` (`archive-document`) | `fixtures` | manifest/audit/sha256/stage conformance | yes (stub) |
| `eval:pipeline_chain` | full graph (`document-pipeline`) | `pilot` | stage conformance + end-to-end scores | **no** |

Procedural nodes (`compile_report`, `catalog_write`) are intentionally not
registered — no LLM, nothing to evaluate.

## pilot family — cheap validation

`pilot:<name>` exists for every eval task. A pilot replaces the subset with a
**stratified micro-slice**: one document per class × subclass stratum from
`docclass-pilot`, plus a three-fixture pinch for the decision nodes
(judge, arbiter, boss, archivist). Same scoring, tracing, and logging path as
the full eval — the point is validating the chain, not measuring it.

```bash
uv run python scripts/run_evals.py --task pilot:classification --mock    # CI gate
uv run python scripts/run_evals.py --task pilot:pipeline_chain --real    # pre-sweep gate
```

## calibration family — edge-test + thresholds

| id | node | probes | analyzer |
|---|---|---|---|
| `calibration:classify` | classify | 2×2 grid + confidence kinds | reliability, ECE, review-gate threshold |
| `calibration:judge` | judge_verify | incomplete + `review_expected` | completeness-threshold sweep |
| `calibration:arbiter` | arbiter | `arbiter_outcome` cells | decision confusion |
| `calibration:retry` | extract | `retry_expected` + `failure_stage` | retry-trigger threshold |
| `calibration:boss` | boss_escalation | `conflicting` fixtures | review-routing rate |
| `calibration:intake` | intake | messy/ambiguous + bundles + streams | no-truncation, triage CI |
| `calibration:archivist` | archive | `failure_stage=archival` | conformance rates |

See [calibration.md](calibration.md) for the methodology and report shape.

For the OpenRouter-provider + Braintrust-sink path specifically — model
roster, decode profiles, concurrency reliability, the full-corpus Dataset
sync, and exact per-task commands — see
[openrouter-braintrust-runbook.md](openrouter-braintrust-runbook.md).

## CLI reference

```bash
uv run python scripts/run_evals.py --task <id|all> \
    --invoke node|agent \
    --subset <spec> \
    --sample N --seed S --n N \
    --mock | --real \
    --trace-backend auto|braintrust|phoenix|none \
    --model <slug> --prompt-version <tag> \
    --concurrency N \
    --dry-run \
    --resume <run_id> \
    --export csv|parquet \
    --json
```

| flag | meaning |
|---|---|
| `--invoke` | `node` (raw graph node fn + `DocumentState`) or `agent` (agent class) |
| `--subset` | grammar: `full/train/test/class:/subclass:/fixtures/bundles/streams/pilot/cuad/enron/claims` |
| `--sample/--seed` | stratified sample by `expected`, deterministic |
| `--mock` | deterministic fake LLM; forces tracing to `none` unless a backend is explicit |
| `--real` | live LLM via the pipeline's provider registry (`OPENROUTER_API_KEY`) |
| `--model` | OpenRouter slug from `config/openrouter_models.yaml` (uniform agent override + cost pricing) |
| `--list-models` | print the registered OpenRouter roster and exit |
| `--prompt-version` | A/B tag — rides trace metadata + the experiment log |
| `--resume` | skip cases already recorded in `<run_id>`, append to its dir (subset manifest is read, never truncated) |
| `--require-trace-sink` | preflight-fails a real run that would resolve to trace backend `none` |
| `--skip-preflight` | bypass preflight checks (warns when combined with `--real`; not recommended) |
| `--export` | write the run's case rows as `cases.csv` / `cases.parquet` |
| `--dry-run` | load + invoke exactly one case |
