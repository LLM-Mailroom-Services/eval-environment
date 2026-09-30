# SAND-027 Leg B (OpenRouter API) — Handoff to the spend agent

**Date:** 2026-09-26 · **Repo:** `LLM-Mailroom-Services/eval-environment` (mailroom-evals) · **Branch:** `main`
**Mission:** everything short of spend is done; you run the N=20 probe waves, verify pairing with the Modal legs, and stage the N=50 gate.

---

## 0. Read order (30 minutes)

1. This file, end to end.
2. `reports/api-comparisons/README.md` — report naming schema + pairing rule.
3. Issue #18 (run program + decode controls), #20 (same-subset guarantee) — closed-loop notes below.
4. Sandbox reference for Leg A semantics: `local-mailroom-sandbox/reports/RUN-20-CORRESPONDENCE-AWQ-REPORT.md` (plus its `-C8-` concurrency variant) and `local-mailroom-sandbox/reports/RUN-COST-DERIVATION.md` (caps arithmetic).

---

## 1. State at handoff (all committed to `main`)

| Commit | What |
|---|---|
| `431fd6e` | PR #25: eval-tasks landing (preflight, resume-safe subset manifests, schema v3, 195→204 tests) |
| `7ec9e59` | PR #31 (parallel session): Braintrust experiment wrapper — **merged while this work was in flight; a stash-pop conflict in `runner.py` was resolved as a union** (their BT wrapper + our decode-profile controls). Verify no marker regressions with `grep -rn '<<<<<<<' src/` (clean at handoff). |
| `1635f90` | Decode profiles (`src/evals/decode_budget.py`), Modal-comparable reports (`src/evals/comparison_report.py`), runner wiring + CLI `--decode-profile`, 13 tests |
| `11f6cc1` | Report fixes: applied decode map re-bound post-run; timeout row from params |
| `4883b9b` | Canonical subset draws (#20) + tracked report tree + snapshot refresh |

**Suite:** 217 passed (`uv run pytest tests/ -q`). **Log:** 39 records, schema v3 valid. **Snapshot:** `web/data/snapshot.json` current (`export_site_snapshot.py --check` exits 0).

### What exists now

- **Decode profiles** (`--decode-profile {qwen3-8b,granite-4.2-8b}`): per-class completion budgets (correspondence 4096, insurance_claims 6144, contract/merger/corporate 8192), IBM-mandated sampling for Granite (T=1.0, top_p=0.95, seed=42) injected at both call families, 600 s per-call timeout (vendored default is 120 — Granite thinking-ON blows past it), client-side `<thinking>/<response>` strip + `recover_prediction()` re-scoring before metrics. Without the flag nothing changes.
- **Comparison reports** auto-emitted on every `--decode-profile` run → `reports/api-comparisons/<model>/RUN-<wave>-<CLASS>-<MODEL>-REPORT.md`, tracked in git, carrying the Modal-comparable surface (wall, concurrency, cost + cost/doc, latency e2e/p50/p95/max, tokens, cost-cap status, per-agent usage, per-doc table, decode posture, provenance; cold-boot/gpu-seconds as explicit N/A rows).
- **Canonical draws** (#20): `data/manifests/subset-draws/<class>-n{20,50}-seed42/` — 10 manifests, filenames + `doc_text_sha256`, re-verified by `scripts/draw_subsets.py --check` (10/10 OK at handoff).
- **Cost cap guard**: each profile carries `cost_cap_usd: 1.50`; the run summary gets `cost_cap.status` (`under_cap`/`over_cap`) and the report prints it. `over_cap` on a 50-doc wave is EXPECTED until the board re-caps.

---

## 2. Decisions locked (do not relitigate)

| Decision | Value | Why |
|---|---|---|
| Qwen comparator | `qwen/qwen3-8b` (roster price 0.117/0.455 per 1M, verified 2026-09-26) | HF id `Qwen/Qwen3-8B` byte-equal to Modal leg; **roster listing expires 2026-10-09 — re-verify before any later wave** |
| Qwen decode posture | pipeline defaults (T=0.1 call sites), only budgets+timeout lifted | match what the Modal Qwen leg actually ran |
| Granite comparator | `ibm-granite/granite-4.2-8b` (0.06/0.25) | mandated T=1.0/top_p=0.95/seed=42 on BOTH legs eventually (Modal leg must adopt it for pairing — note in #18) |
| Waves | 20 → 50 (seed 42) | issue #18 (20/50/100). **Nesting verified on the committed manifests: 20 ⊂ 50 for all 5 classes.** Issue #38 doctrine wants every size sliced from ONE locked 100-draw — 100-slice equality could not be network-verified at handoff (HF datasets-server 500 on the pinned revision); it is a **pre-N=50 gate** below. N=20 pairing needs only the 20-draw itself (deterministic loader + committed manifest) and is unblocked. 50 is **board-gated**, not pre-authorized |
| Wave caps | $1.50 hard cap per 20-doc profile wave; ≈$0.80 expected (Granite leg) | derived from Leg A costs in sandbox `RUN-COST-DERIVATION.md` |
| Keys | in `.env` (gitignored): `OPENROUTER_API_KEY`, `BRAINTRUST_API_KEY`, `BRAINTRUST_PROJECT=mailroom-sandbox` | **rotate both keys when the program closes** |
| Trace sink | Braintrust auto-when-keyed; `--require-trace-sink` for real runs | issue #21 coverage |

---

## 3. YOUR runbook — the N=20 probe (the only pre-authorized spend)

Environment: `export PATH="$HOME/.local/bin:$PATH"`; `uv sync --extra dev` already done. From repo root:

```bash
# 0) gates: clean tree, suite green, draws verified
git status --short && uv run pytest tests/ -q
uv run python scripts/draw_subsets.py --check          # expect 10/10 OK

# 1) Qwen twin leg — 5 waves × 20 docs (≈ $0.80 total, cap $1.50/wave)
run_wave () {  # $1=class  $2=task-id  $3=model  $4=profile
  uv run python scripts/run_evals.py \
    --task "$2" --real --subset "class:$1" --sample 20 --seed 42 \
    --model "$3" --decode-profile "$4" --require-trace-sink
}
for spec in \
  "correspondence eval:correspondence" \
  "insurance_claim eval:insurance_claims" \
  "contract eval:contracts" \
  "merger_agreement eval:merger_agreement" \
  "corporate_record eval:corporate_records"; do
  set -- $spec
  run_wave "$1" "$2" qwen/qwen3-8b qwen3-8b
done

# 2) Granite leg — same 5 waves, mandated sampling
for spec in \
  "correspondence eval:correspondence" \
  "insurance_claim eval:insurance_claims" \
  "contract eval:contracts" \
  "merger_agreement eval:merger_agreement" \
  "corporate_record eval:corporate_records"; do
  set -- $spec
  run_wave "$1" "$2" ibm-granite/granite-4.2-8b granite-4.2-8b
done
```

Task ids are the registry's (`--list`): `eval:correspondence`,
`eval:insurance_claims`, `eval:contracts`, `eval:merger_agreement`,
`eval:corporate_records`. Real-mode preflight hard-fails before spend on
missing keys/model/sink — do **not** pass `--skip-preflight`.

After each wave: the report lands at
`reports/api-comparisons/<model>/RUN-20-<CLASS>-<MODEL>-REPORT.md`; check
`cost_cap.status == under_cap`, then **verify the draw**:

```bash
uv run python scripts/draw_subsets.py --check
# diff the run's manifest against canonical (filenames + doc_text_sha256):
diff <(jq -S '.filenames' data/experiments/<run_id>/subset_manifest.json) \
     <(jq -S '.filenames' data/manifests/subset-draws/<cls>-n20-seed42/subset_manifest.json)
```

Wrap-up duties after all 10 waves: `uv run python scripts/export_site_snapshot.py` (commit snapshot with the reports), `uv run pytest tests/ -q`, commit `DMR`-style message naming run_ids, push.

### Escalation rules (issue #18)

- Per-class cost > 3× its N=20 measured cost at the next wave → stop, raise a `needs_attention` note.
- Any `over_cap` at N=20 → stop that leg, report, wait.
- N=50 wave requires board sign-off (the report will read `over_cap` under the current $1.50 profile cap — that is the intended tripwire, not a bug) **and** the #38 slice gate: once `datasets-server.huggingface.co` recovers, draw each class at n=100 seed 42 and confirm `s100[:50] == n50-manifest.filenames` and `s100[:20] == n20-manifest.filenames` for all 5 classes (same snippet shape as the draw check; HF was 500 at handoff). If any class mismatches, redraw ALL sizes for that class from the locked 100-draw slices, recommit, and note the break in #20 before proceeding.

### Pairing with the Modal legs

Modal reports live in `local-mailroom-sandbox/reports/` (`RUN-20-CORRESPONDENCE-AWQ-REPORT.md`, `-C8-` concurrency variant). Same stem = same wave+class. For the paired table: API `cost_usd_est_total` vs Modal `estimated GPU cost` (their $0.114231 for 20 correspondence docs is the reference point), latency p50/p95/max, docs-ok/total, overall score. **Note honestly in every report**: Modal figures used the pre-SAND-027 scoring posture where noted, and the Modal Qwen leg ran T=0.1 (matches the Qwen profile by design).

---

## 4. Known gaps / next steps (in priority order)

1. **#19 prompt-stem alignment map** — the draw manifests pin `doc_text_sha256`; still owed: the prompt-stem sha256 map + drift check tying each specialist prompt to its Leg A counterpart. Owner: next session; not spend-blocking for N=20 (same repo, same frozen lineage — `scripts/freeze_prompts.py --check` is 15/15).
2. **Modal-leg Granite posture** — pairing the Granite API leg requires the Modal Granite leg to adopt T=1.0/top_p=0.95/seed=42. Surface to the sandbox agent; flag in #18.
3. **`compare_runs.py --cost`** — A/B cost verdict mode ("leg B cheaper at equal score") is not built; the per-report cost/doc columns make it low-effort. Post-N=20.
4. **Roster price expiry** — `qwen/qwen3-8b` listing expires 2026-10-09; re-verify live prices before any later wave (`scripts/verify_roster.py` if present, else the OpenRouter models endpoint).
5. **Key rotation** — both keys in `.env` rotate after the program closes.

---

## 5. Environment gotchas

- **A parallel session is active in this checkout** (GitHub Desktop + local commits — it landed `d918cda`, `7ec9e59` mid-flight and stash-popped over working edits once). Before ANY edit: `git branch --show-current`, `git status --short`, commit early, never trust a dirty tree you didn't dirty. If you find conflict markers: resolve as union of both sides, never `checkout --theirs`.
- `../llm-mailroom` (pipeline clone) carries local commit `776ccfa` (drops workspace source for llm-dojo-scoring) — **never push it upstream**.
- Mock smokes must use `EVALS_TRACE_BACKEND=none` (or conftest equivalents); mock never touches the network.
- Every run (including failures) writes an experiment-log record — never edit old records; follow-ups are new records. Schema changes bump `schema_version` + `schemas/` + the experiment-log skill in the same commit.
- Sandbox board: SAND-027 track (SAND-027-2 = this repo's Leg B prep) — after the N=20 waves land, check the card off with report paths + run_ids as Evidence.
