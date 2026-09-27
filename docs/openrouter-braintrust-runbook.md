# OpenRouter + Braintrust runbook — specialists & sorter

Step-by-step instructions for running the five extraction specialists
(`eval:contracts`, `eval:merger_agreement`, `eval:corporate_records`,
`eval:correspondence`, `eval:insurance_claims`) and the sorter/classification
node (`eval:classification`) against a live OpenRouter model, traced to
Braintrust. Written from the SAND-027 Leg B N=20 waves so a following agent
can replicate the same experiments without rediscovering the pitfalls.

Read [`docs/tasks.md`](tasks.md) first for the general task/CLI reference —
this doc only covers the OpenRouter-provider + Braintrust-sink path and the
concurrency-reliability findings specific to it.

## 1. Prerequisites

```bash
uv sync --extra dev
uv run python scripts/draw_subsets.py --check   # canonical N=20/50 draws, expect all OK
```

Environment (repo-root `.env`, gitignored, or exported in-shell):

| variable | required for | note |
|---|---|---|
| `OPENROUTER_API_KEY` | `--real` | primary provider; preflight hard-fails without it (or the gateway alternative below) |
| `DEFAULT_PROVIDER=generic` + `GENERIC_BASE_URL` + `GENERIC_API_KEY` | `--real` (alternative) | Vercel AI Gateway, OpenAI-compatible; loaded by `evals/__init__`, real env always wins |
| `BRAINTRUST_API_KEY` | Braintrust tracing | resolves the sink to `braintrust` automatically when set |
| `BRAINTRUST_PROJECT` | Braintrust tracing | defaults to `mailroom`; SAND-027 waves used `Mailroom-Evals` |

Never export `OBSERVABILITY_PROVIDER` or `MAILROOM_BASE_DIR` yourself — the
runner sets both per run.

## 2. OpenRouter as the provider

`--model <slug>` applies one model uniformly to every non-procedural agent
for the run (`evals.openrouter_roster.apply_model_override`): it monkey-patches
`pipeline.config.load_config` for the duration of the run so every agent's
`provider`/`model` become `openrouter`/`<slug>`, and merges the slug's
per-token pricing into `cost_models` for accurate cost estimates.

Slugs come from the allow-list `config/openrouter_models.yaml` — unknown
slugs fail preflight before any spend:

```bash
uv run python scripts/run_evals.py --list-models
```

To add a model: append an entry with `label`, `modality`, `context_tokens`,
`input_per_million`, `output_per_million` (USD per 1M tokens, from the
OpenRouter model page). Roster prices can expire — re-verify before a wave
if the comment on an existing entry says so (e.g. `qwen/qwen3-8b` was
verified 2026-09-26, expires 2026-10-09).

Agents that always keep taxonomy defaults regardless of `--model`:
`gmail_triage`, `relations`, `reporter` (free-lane / optional-LLM / procedural
— see `_SKIP_MODEL_OVERRIDE` in `openrouter_roster.py`). The sorter (`sorter`,
`sorter_reviewer`) and all five specialists ARE overridden by `--model`.

### Decode profiles (specialists only)

`--decode-profile {qwen3-8b,granite-4.2-8b}` lifts each specialist's
completion budget for thinking-ON decodes and raises the per-call timeout to
600s (`src/evals/decode_budget.py`, `CLASS_BUDGETS` keyed by specialist agent
name). **This profile map has no entry for `sorter`** — passing
`--decode-profile` on `eval:classification` is harmless but does nothing
useful; omit it for sorter runs. Passing `--decode-profile` is also what
triggers the auto-written Modal-comparable report
(`reports/api-comparisons/<model>/<task>/RUN-<wave>-<CLASS>-<MODEL>-REPORT.md`
— always separated by specialist/task, never flat across a model dir) —
without it, no comparison report is emitted for that run.

## 3. Braintrust as the trace sink

```bash
--trace-backend braintrust --require-trace-sink
```

`--require-trace-sink` preflight-fails a `--real` run that would otherwise
resolve to backend `none` (e.g. missing `BRAINTRUST_API_KEY`) — always pass
it for any run whose results matter.

Two independent Braintrust surfaces exist; do not conflate them:

- **Experiment** (one per run, `evals.braintrust_experiment.begin_eval_run`):
  every specialist/node invocation is its own row (20 docs → 20 rows), scored
  with the ≤2 headline metrics in `scoring.ESSENTIAL_SCORES` — the full
  scoring suite stays local (`data/experiments/<run_id>/scoring_suite.json`).
  Corpus documents are **not** inserted as Experiment rows; `input` is a
  curated case reference (never raw document text — see
  `evals.tracing.public_case_ref` / `doc_text_sha256`).
- **Dataset** (`mailroom-hf-<revision[:8]>`, one per corpus pin, populated by
  `sync_full_corpus_dataset` / `scripts/sync_braintrust_dataset.py`): the
  *complete* pinned corpus (3,302 rows, both `train` and `test` splits),
  independent of any single run's N-sample subset. Run once per corpus
  re-pin:

  ```bash
  uv run python scripts/sync_braintrust_dataset.py
  ```

  Idempotent — rows are keyed by the stable corpus case id
  (`corpus:<config>:<split>:<filename>`), so re-running updates in place. If
  `list(braintrust.init_dataset(...))` shows extra rows keyed by 64-char
  sha256-looking ids that this sync path doesn't use, they predate this sync
  function (an earlier, now-dead insertion scheme) — do not assume they are
  safe to delete without checking first; flag and leave them if unsure.

## 4. Concurrency & reliability (read before spending on `--concurrency 8`)

**Only ever run one `--concurrency 8` real job at a time.** Running two
concurrent qwen3-8b jobs simultaneously does not parallelize cleanly on the
OpenRouter side and wastes spend on results that then have to be redone.
Use a single tmux session and confirm the previous job's pane is idle
(`bash`/shell prompt, not `uv`/`python`) before launching the next.

### The failure mode this fixes

`qwen/qwen3-8b` under `--concurrency 8` returned coherent-looking but
non-JSON placeholder text (e.g. `// JSON output here (as per the
instructions) //`) on roughly half of raw completions — confirmed via direct
in-process repro: 0/20 parse errors at concurrency=1 vs. 18/20 at
concurrency=8 on identical docs/prompts, even with no other job running.
Two independent, compounding root causes, both fixed in `src/evals/specialist_llm.py`:

1. **No retry on "successful" garbled responses.** The old retry path only
   fired on network exceptions, not on a 200 response that failed to parse
   as JSON. `_complete_json` now retries once on either condition (with a
   plain-JSON-only system-prompt nudge on the retry attempt).
2. **Shared per-document retry budget.** `llm_call_budget(needed)` used to
   grant one shared spare call per document (`ceil(needed * 1.15)`); a
   multi-chunk document with 2+ chunks needing a retry only had one spare
   slot, so later chunks got `_budget_exhausted` with no retry. It now grants
   **one retry slot per coverage chunk** (`needed * 2`).

Both fixes are covered by `tests/test_specialist_llm.py`. Verified at full
N=20 scale post-fix: correspondence 0/20 parse errors (score 0.318 → 0.513
vs. the contaminated concurrency=8 baseline), insurance_claims 0/20 parse
errors (score 0.202 → 0.7488, close to the concurrency=1 reference of
0.8056).

If you see `specialist_llm_retry_blocked_by_budget` warnings in logs at any
non-trivial rate, that is a signal the model/load combination needs a larger
budget multiplier than `needed * 2` — do not silently raise it without
re-verifying the retry-rescue rate first (see §6, in-process diagnostic).

## 5. The specialist runbook (N=20, concurrency=8, single job at a time)

Task ids, model, and profile are the only per-class variables:

```bash
cd /workspace
set -a && source .env && set +a
export PYTHONUNBUFFERED=1 BRAINTRUST_PROJECT=Mailroom-Evals

run_specialist () {  # $1=task-id  $2=class  $3=model  $4=decode-profile
  uv run python -u scripts/run_evals.py \
    --task "$1" --real --subset "class:$2" --sample 20 --seed 42 \
    --model "$3" --decode-profile "$4" \
    --require-trace-sink --prompt-source frozen \
    --trace-backend braintrust --concurrency 8 \
    2>&1 | tee -a /tmp/run.log
}

run_specialist eval:correspondence     correspondence     qwen/qwen3-8b qwen3-8b
run_specialist eval:insurance_claims   insurance_claim    qwen/qwen3-8b qwen3-8b
run_specialist eval:contracts          contract           qwen/qwen3-8b qwen3-8b
run_specialist eval:corporate_records  corporate_record   qwen/qwen3-8b qwen3-8b
run_specialist eval:merger_agreement   merger_agreement   qwen/qwen3-8b qwen3-8b
```

Run each of the five sequentially (one at a time — §4), never in parallel.
For Granite comparisons, swap `qwen/qwen3-8b qwen3-8b` for
`ibm-granite/granite-4.2-8b granite-4.2-8b` (mandated sampling `T=1.0,
top_p=0.95, seed=42` is applied automatically by the profile).

## 6. The sorter runbook (`eval:classification`)

Sorter has no decode-profile budget map (§2) and no per-class subset — its
default subset is `full`. Same OpenRouter + Braintrust wiring, no
`--decode-profile`:

```bash
uv run python -u scripts/run_evals.py \
  --task eval:classification --real --subset full --sample 20 --seed 42 \
  --model qwen/qwen3-8b \
  --require-trace-sink --prompt-source frozen \
  --trace-backend braintrust --concurrency 8 \
  2>&1 | tee -a /tmp/run.log
```

`--sample 20` draws a stratified sample across all five doc classes (not a
single-class N=20 like the specialist waves); use `--subset class:<name>`
instead of `full` if a single-class classification slice is wanted.

Pipe raw `tee` output to a scratch path outside the repo (e.g. `/tmp/run.log`
as above), not under `reports/`. `reports/` is git-tracked and reserved for
polished, self-contained deliverables (the experiment-log index/detail files
and `reports/api-comparisons/**`); a raw structured-log capture of a whole
session's job output is exactly the kind of unbounded, hard-to-read artifact
that does not belong there — see the `.gitignore` comment above
`data/experiments/` for the same reasoning applied to raw run dirs.

## 7. Verifying a run before trusting the number

Never trust a "run complete" claim (yours or anyone else's) without
checking directly — a long-running job (correspondence at concurrency=8 took
~20.5 minutes for 20 docs) can look stalled from the outside.

```bash
RUN_ID=<run_id>   # printed at the end of the run, e.g. 20260927T035135Z-eval-insurance_claims
ps aux | grep run_evals | grep -v grep          # confirm no process still running
wc -l data/experiments/$RUN_ID/cases.jsonl       # should equal --sample

python3 -c "
import json
n = err = 0
for line in open('data/experiments/$RUN_ID/cases.jsonl'):
    d = json.loads(line); n += 1
    out = d.get('output', {})
    if out.get('_parse_error') or out.get('extraction', {}).get('_parse_error'):
        err += 1
print('total', n, 'parse_errors', err)
"

tail -1 reports/experiment_log.jsonl | python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
print(d['run_id'], d.get('status'), d.get('metrics', {}).get('overall_score'))
"
```

`errors=0` in the run's own summary line only reflects *invocation* errors
(exceptions), not parse-quality — always check `_parse_error` per case
directly for a concurrency=8 run.

### In-process diagnostic (repro before you change retry/budget logic again)

If you suspect a fresh reliability regression, reproduce it directly instead
of guessing from aggregate scores — this was how both root causes in §4 were
found and verified fixed:

```python
from concurrent.futures import ThreadPoolExecutor
from evals.cases import load_cases
from evals.openrouter_roster import apply_model_override
from mailroom.agents.specialists import extract_entities  # or the relevant node fn

cases, _ = load_cases("class:contract", sample=8, seed=42)
with apply_model_override("qwen/qwen3-8b"):   # REQUIRED — extract_entities alone
    with ThreadPoolExecutor(max_workers=8) as ex:  # uses the taxonomy default model,
        results = list(ex.map(extract_entities, cases))  # not your --model override
```

Forgetting `apply_model_override` is the most common mistake here: a
standalone script calling a specialist/agent function directly resolves the
model via the taxonomy default, not whatever `--model` you intended — always
wrap the call.

## 8. Wrap-up after a wave

```bash
uv run python scripts/export_site_snapshot.py --check || uv run python scripts/export_site_snapshot.py
uv run pytest tests/ -q
git add data/experiments/<run_id>/ reports/
git commit -m "..."
git push -u origin <branch>
```

Update the PR (targeting `main` if the previous base has already merged —
check `git log --oneline -1 origin/main` before assuming the configured
default base is current).

## 9. Known open items

- 81 unexpected rows in the `mailroom-hf-<rev>` Braintrust Dataset, keyed by
  64-char sha256-looking ids inconsistent with the `corpus:<config>:<split>:
  <filename>` scheme `sync_full_corpus_dataset` uses. Not created by any
  current code path (`_record_id_by_sha` in `braintrust_experiment.py` is
  populated nowhere — vestigial). Left untouched; needs investigation before
  any cleanup.
- Roster price expiry: re-verify `qwen/qwen3-8b` pricing in
  `config/openrouter_models.yaml` against the live OpenRouter models
  endpoint before any wave after 2026-10-09.
- If a budget multiplier other than `needed * 2` is ever needed, re-run the
  §7 in-process diagnostic first to measure the actual retry-rescue rate
  under the new load before changing `llm_call_budget`.
