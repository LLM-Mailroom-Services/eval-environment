# Ingest-Node ML Assistant — Model Proposal & Implementation Plan

**Status:** Proposal (research-backed, implementable) · **Date:** 2026-09-17
**Scope:** llm-mailroom ingest node (`intake_node` → `classify_node`) · mailroom-evals harness
**Author:** Ponytail Hermes Chan 🦉 (orchestrator-governor protocol, research + design)

---

## 1. Executive summary

Deploy a **fine-tuned ModernBERT-base hierarchical classifier** as a deterministic
fast-path inside the ingest node, gated by the pipeline's existing confidence
bands, with the current LLM sorter retained as the calibrated fallback for the
hard tail (messy, ambiguous, over-budget documents).

- **Model:** `answerdotai/ModernBERT-base` (149M params, 22 layers, 8,192-token
  native context, Apache-2.0) — the current SOTA small encoder, fine-tuned on
  the pinned mailroom-dataset (2,979 train rows).
- **Task split:** hierarchical heads — 5-way `doc_type` head + per-class
  `subclass` heads (25 CUAD families, MAUD consideration, corporate-record,
  correspondence, insurance-claim subclasses) — mirroring the pipeline's
  existing `contract_subtype`-only-when-contract structure.
- **Long documents:** title + head + the pipeline's own `sliding_windows`
  machinery, merged by plurality vote — the exact merge the sorter already uses,
  so nothing new is invented.
- **Integration:** the classifier's output rides the existing `intake_prep.triage`
  slot as the labeled prior; the LLM sorter fires only when classifier confidence
  < 0.88 (the pipeline's existing `low` band) or the deterministic clerk flags
  messy. Zero new graph nodes, zero new thresholds.
- **Cost:** ~2–3 orders of magnitude cheaper per document than any LLM call
  (µs–ms, ~$0.000001/doc on CPU vs $0.0002–0.0004/doc for deepseek-v4-flash),
  with the LLM budget reserved for the ~10–20% of documents that need it.

**Why this beats the alternatives:** fine-tuned small models beat zero-shot
LLM prompting for text classification at this data scale (arXiv 2406.08660);
ModernBERT is the strongest small encoder on GLUE (88.4 base — best among
similarly-sized encoders, large second only to DeBERTa-v3-large); and the
pipeline already has every integration seam (gate, prior slot, confidence
bands, windowing) the classifier needs. The 3,302-doc corpus is enough to
fine-tune a 149M encoder but not to train cleaning/section-mapping models —
so the LLM keeps those jobs.

---

## 2. Problem framing — what the ingest node actually does

From `graph/build_graph.py:intake_node` (HUB-038, the unified ingest+intake step):

| Step | Mechanism today | ML-assistable? |
|---|---|---|
| 1. Claim + transcribe file | `_read_file_text` (deterministic) | no (I/O) |
| 2. Deterministic intake clerk | `apply_intake` → `deterministic_normalize` + `looks_messy` (dojo, never skipped) | **yes — messy detection upgrade (Phase 2)** |
| 3. LLM-assisted intake (gated) | `IntakeAgent.intake_run`: TRIAGE (advisory class read), CLEAN (structural repair), PREPARE (section map) — only when messy or over sorter budget | **yes — TRIAGE is the classification fast-path** |
| 4. Manifest + catalog + audit | deterministic | no |
| 5. Sorter (`classify_node`) | `SorterAgent.classify_json`: 5-class + subclass, sliding windows, never truncates | **yes — this is the same classification surface** |

The ML-assistable core is **preliminary classification** (doc_type + subclass)
and **messy detection**. Cleaning (seq2seq repair) and section mapping
(sequence labeling) are NOT trainable from the current corpus — the GT has
doc-level labels only, no paired messy/clean text and no section-role
annotations. The proposal therefore targets classification first; cleaning and
section mapping stay with the LLM (and are noted as future annotation work).

### The classification surface (from `config/taxonomy.yaml` + `sorter_agent.py`)

- **5 doc classes:** `contract` (600), `corporate_record` (450),
  `correspondence` (1000), `insurance_claim` (1100), `merger_agreement` (152).
- **Subclasses:** 25 CUAD contract families + `other`; MAUD consideration
  (all_cash / all_stock / mixed_cash_stock / other); corporate-record types
  (bylaws, articles_of_incorporation, powers_of_attorney, …); correspondence
  types (email, letter, notice, memo, …); insurance-claim types (auto, carrier,
  property, inpatient, outpatient, pde, …).
- **Critical corpus property:** the ground truth follows **folder/title
  conventions** (the sorter prompt's "title-wins doctrine"). Titles and
  filenames are highly predictive — a classifier must see them.
- **Document lengths:** up to **482K chars** (p90 ≈ 317K, mean ≈ 78K on the
  DMR-067 sample). No encoder fits this in one pass; windowing is mandatory.

### Constraints that shape the design

1. **Small data:** 2,979 train rows, with heavy class imbalance (merger 152 vs
   insurance 1,100) and a long tail of subclasses with single-digit counts.
2. **Calibration matters:** the pipeline routes on confidence (high 0.97 /
   low 0.88 / judge band 0.95, retry_max 2). An uncalibrated classifier would
   silently mis-route documents — calibration is a first-class requirement.
3. **Cost is the point:** the caller wants deepseek-v4-flash vs local/Modal
   comparisons; a classifier that cuts LLM calls by 80–90% changes the
   economics of the whole pipeline.
4. **No new graph topology:** the pipeline already has the gate
   (`should_llm_intake`), the prior slot (`intake_prep.triage`), the windowing
   (`sliding_windows`), and the confidence bands. The classifier slots in.

---

## 3. Research foundation

### 3.1 Fine-tuned small models beat zero-shot LLMs for classification

**arXiv 2406.08660** ("Fine-Tuned 'Small' LLMs (Still) Significantly
Outperform Zero-Shot Generative AI Models in Text Classification"): for text
classification, fine-tuning a small model on task data is preferable to
zero-shot prompting a large generative model — the tailored approach wins on
accuracy and cost. This is the core argument for a trained classifier over
"just prompt deepseek-v4-flash for everything."

### 3.2 ModernBERT is the current small-encoder SOTA

From the model card (`answerdotai/ModernBERT-base`, Apache-2.0):

- 149M params / 22 layers (base), 395M / 28 layers (large).
- Pre-trained on 2T tokens (English + code); **native 8,192-token context**
  (RoPE + local-global alternating attention) — 16× BERT's 512-token limit.
- **GLUE 88.4 (base)** — best among similarly-sized encoders; large is second
  only to DeBERTa-v3-large.
- Unpadding + Flash Attention 2 for fast, memory-efficient inference; standard
  `AutoModelForSequenceClassification` fine-tuning recipe (transformers ≥ 4.48).
- No token-type IDs (simpler inputs than BERT).

Why ModernBERT over the alternatives:

| Encoder | Params | Context | Notes |
|---|---|---|---|
| **ModernBERT-base** | 149M | 8,192 | SOTA small encoder, Apache-2.0, fast inference, GLUE 88.4 |
| DeBERTa-v3-base | 86M | 512 | Strong but 512-token cap hurts long legal docs; needs windowing at 512 |
| Legal-BERT | 110M | 512 | Domain-pretrained on legal text, but 512 cap + older architecture |
| sentence-transformers + linear probe | 22–110M | 512 | Good baseline; weaker than fine-tuned encoder on subclass tail |

ModernBERT's 8,192-token context is the decisive advantage for legal documents:
at ~3.8 chars/token it reads ~31K chars per window vs ~2K for BERT-class
models — 15× fewer windows per document, and the head/title strategy covers
most classification signal anyway.

### 3.3 Long-document classification: windowing + aggregation

The literature standard for encoder-based long-doc classification is
**segment-then-aggregate**: split into windows, classify each, merge by vote
or attention pooling (hierarchical transformers; Longformer-style local-global
attention is the architectural cousin). The mailroom already implements the
merge: `SorterAgent` classifies overlapping `sliding_windows` and merges by
**plurality vote among non-unknown classes, ties on window confidence, mean
confidence of agreeing windows** (`agents/sorter.py`). The classifier reuses
this exact machinery — same windows, same merge — so behavior is consistent
between fast path and LLM fallback.

### 3.4 Small-data + imbalance: what actually works

- **Class-weighted loss + stratified sampling** — standard for the 152-vs-1100
  imbalance; the eval harness's `stratified_sample` already enforces even
  per-class draws for evaluation.
- **Augmentation** (SFRSA, arXiv 2406.08660-adjacent; Springer 2026 small-data
  survey): generate-then-select augmentation helps tail classes; the corpus's
  own LLM (deepseek-v4-flash) can synthesize subclass variants for the
  single-digit-count subclasses — cheap, and the GT-closure revision makes
  provenance auditable.
- **Hierarchical heads over flat multi-class** — the 5-way head sees 2,979
  rows; each subclass head sees only its class's rows (e.g. contract head sees
  540 rows across 26 labels). This is strictly better than one 40+-label flat
  head at this data size, and it matches the pipeline's existing
  `contract_subtype`-only-when-contract contract.
- **Calibration:** temperature scaling (Platt-style) on a held-out split,
  mapped onto the existing 0.88/0.97 bands. The eval harness already has
  `calibration:classify` (reliability tables, ECE, review-gate threshold) —
  the classifier is scored with the same tooling as the LLM sorter.

---

## 4. Proposed architecture — the cascade

```
document
  │
  ▼
[intake_node]
  ├─ 1. claim + transcribe (unchanged)
  ├─ 2. deterministic clerk: normalize + looks_messy (unchanged, never skipped)
  ├─ 3. NEW: ML fast-path classifier (ModernBERT-base, fine-tuned)
  │      ├─ input: title/filename + head (first ~8K tokens) + sliding windows
  │      │        (reusing agents.intake.sliding_windows) when over budget
  │      ├─ output: doc_type, subclass, calibrated confidence, per-window votes
  │      └─ rides state.intake_prep.triage (the existing labeled-prior slot)
  ├─ 4. gate (extended should_llm_intake):
  │      LLM intake + sorter fire ONLY when:
  │        • deterministic clerk says messy, OR
  │        • classifier confidence < 0.88 (pipeline low band), OR
  │        • document over sorter budget AND classifier windows disagree
  │        (plurality tie / low agreement)
  └─ 5. manifest + catalog + audit (unchanged)
```

**Key properties:**

- **No new graph nodes.** The classifier is a function inside `intake_node`
  (and optionally a pre-check inside `classify_node`), same as the clerk.
- **The LLM sorter remains the authority.** The classifier is advisory — the
  sorter already "re-classifies independently and never trusts [intake] over
  the document" (intake prompt doctrine). The classifier only *earns* the LLM
  skip when it is confident AND the clerk is clean.
- **Confidence bands are reused verbatim.** 0.88 low / 0.97 high / judge band
  0.95 — no new thresholds, no calibration drift between paths.
- **Traceable.** The classifier emits a span (same `observation` pattern as
  `intake-llm-prep`): input = filename + chars + windows, output = class +
  subclass + confidence + votes, metadata = model id + revision + calibration
  version. Braintrust/Phoenix pick it up automatically.

---

## 5. Model + training configuration (implementable spec)

### 5.1 Model

- **Base:** `answerdotai/ModernBERT-base` (149M, Apache-2.0, transformers ≥ 4.48).
- **Heads:** `AutoModelForSequenceClassification` × 6:
  - `doc_type` head: 6 labels (5 classes + `unknown`)
  - `contract_subclass` head: 26 labels (25 CUAD families + `other`)
  - `merger_subclass` head: 4 labels (all_cash, all_stock, mixed_cash_stock, other)
  - `corporate_record_subclass` head: ~9 labels
  - `correspondence_subclass` head: ~7 labels
  - `insurance_claim_subclass` head: ~6 labels
  - (subclass heads fire only when the doc_type head predicts their class —
    the pipeline's existing conditional structure)
- **Input construction (per window):** `title/filename + "\n\n" + window_text`,
  truncated to 8,192 tokens. Title first — the corpus's title-wins convention
  makes it the single most predictive feature.

### 5.2 Training data (from the pinned corpus — no new data needed)

- Source: `Lucius-Morningstar/mailroom-dataset` @ `46a4d3c2…` (GT-closure
  revision), `ground_truth` config, `train` split (2,979 rows) — the exact
  loader `evals.cases` uses (`pipeline.hf_corpus_loader`, sha-verified).
- Labels: `expected` → doc_type head; `expected_subclass` → subclass head
  (normalized via the same `_normalize_subclass` mapping the sandbox corpus
  uses, so `Service`/`service` and `Co_Branding`/`co_branding` unify).
- Split: 90/10 stratified train/validation (stratified by `expected`, seeded
  42 — same seed discipline as every eval run).
- **Test split (323 rows) is held out entirely** — it is the eval surface and
  must never touch training (the harness's `--subset test` runs stay honest).

### 5.3 Training recipe

| Hyperparameter | Value | Rationale |
|---|---|---|
| Optimizer | AdamW (bf16) | standard for ModernBERT fine-tune |
| LR | 2e-5, linear schedule, warmup 6% | GLUE recipe |
| Epochs | 5–8 with early stopping on val loss | small data → watch overfit |
| Batch | 16 (grad-accum to 32) | 8,192-token windows are memory-heavy |
| Loss | class-weighted cross-entropy (weights ∝ 1/freq per head) | merger 152 vs insurance 1,100 |
| Augmentation | LLM-synthesized tail-class variants (deepseek-v4-flash, ≤ 3× per tail subclass, provenance-logged) | SFRSA-style generate-then-select |
| Calibration | temperature scaling on val split, per head | maps to 0.88/0.97 bands |
| Eval | per-head accuracy, macro-F1, ECE, reliability table | same shape as `calibration:classify` |

### 5.4 Long-document strategy

- ≤ 8,192 tokens: single window (title + head).
- Over budget: `agents.intake.sliding_windows(text, budget, overlap)` — the
  pipeline's own paragraph-aware windower — with the sorter's merge:
  plurality vote among non-unknown classes, ties on mean window confidence,
  mean confidence of agreeing windows, first non-null subclass.
- The 8,192-token context means most documents need 1–3 windows (vs 10–40 for
  a 512-token encoder).

### 5.5 Messy detection (Phase 2, optional)

Fine-tune a tiny binary head (messy/clean) on the deterministic clerk's
`looks_messy` output as weak labels + LLM-verified subset. Deferred: the
heuristic + LLM gate already works; the classifier's *confidence* is itself a
messy signal (garbled text → low confidence → LLM path).

---

## 6. Deployment + cost model

### 6.1 Serving

| Option | Where | Latency/doc | Cost/doc | Verdict |
|---|---|---|---|---|
| **ONNX Runtime, CPU** (host or Modal CPU container) | local | ~5–20 ms | ~$0.000001 | **primary** — 149M params is CPU-trivial |
| Modal GPU (L4, shared with vLLM) | Modal | ~1–5 ms | amortized | fallback if CPU latency matters at scale |
| OpenRouter (no — it's an encoder, not an API model) | — | — | — | n/a |

The classifier is small enough that the existing Modal `sandbox-vllm` L4
endpoint could serve it, but CPU/ONNX is the honest recommendation: no GPU
burn, no cold-start, no per-call cost. Export via `optimum`/`onnxruntime`,
quantize to int8 (149M params ≈ 60 MB int8 — loads in ms).

### 6.2 Cost comparison (per document, from `taxonomy.yaml` cost_models)

| Path | Cost/doc (est.) | Latency | Notes |
|---|---|---|---|
| deepseek-v4-flash sorter (12K-char doc ≈ 3.5K in + 0.2K out tokens) | ~$0.0002–0.0004 | 1–3 s | current API path |
| qwen3.7-flash sorter | ~$0.0001–0.0003 | 1–3 s | current API path |
| gemma-4-E4B-it via Modal L4 (run-50-gemma4-e4b) | ~$0.0005–0.001 (GPU-hour amortized) | 2–10 s | local path, cold-start risk |
| **ModernBERT-base classifier (CPU/ONNX)** | **~$0.000001** | **5–20 ms** | **this proposal** |

At the pipeline's steady state (say 1,000 docs/day), the classifier path cuts
LLM spend by 80–90%: only the ~10–20% of documents that are messy, ambiguous,
or over-budget pay LLM prices. The LLM budget is preserved for exactly the
documents where it earns it.

### 6.3 What the LLM keeps

- Cleaning (structural repair) — no paired training data exists.
- Section maps (PREPARE) — no section-role annotations exist.
- The hard classification tail: subclasses with < 5 training rows, adversarial
  hybrids (the sorter prompt's 30 rules encode corpus conventions the encoder
  cannot learn from 3K docs), and any document the classifier is unsure about.

---

## 7. Evaluation plan (mailroom-evals, no new harness)

The classifier is scored with the **same harness, same subsets, same seeds**
as the LLM sorter — that is the entire point of the caller's request
(comparable metrics vs local models + Modal costs):

1. **`eval:classification`** on the DMR-067 stratified 50 (`--subset test
   --sample 50 --seed 42`, subclass-stratified buckets per the sandbox spec) —
   class_accuracy, subclass_accuracy, per-stratum confusion. Run for:
   - ModernBERT-base classifier (fast path)
   - deepseek-v4-flash sorter (the requested comparison)
   - gemma-4-E4B-it sorter (the existing run-50-gemma4-e4b reference)
   - qwen3.7-flash sorter (existing runs)
2. **`calibration:classify`** — reliability tables + ECE for the classifier's
   confidence vs the LLM's, verifying the 0.88/0.97 band mapping holds.
3. **`compare_runs.py --a <classifier> --b <deepseek run>`** — A/B + CIs on
   the same 50.
4. **Cost ledger:** `performance.by_agent` (calls/tokens/models + estimated
   cost) already lands in every run summary — the classifier run logs its
   CPU cost as a constant, the LLM runs log API/GPU cost. Comparable by
   construction.
5. **Braintrust:** every run traces (root span per case, metadata.run_id +
   model + prompt_version). The classifier emits its own span type
   (`intake-ml-triage`) so fast-path vs LLM-path decisions are auditable
   per document.

**Success criteria (go/no-go for deployment):**

| Metric | Threshold to deploy |
|---|---|
| doc_type accuracy on the stratified 50 | ≥ 0.95 (LLM sorter reference: 0.90–0.96) |
| subclass accuracy | ≥ 0.75 (LLM reference: 0.40–0.76) |
| ECE (calibration) | ≤ 0.05 across the 0.88–0.97 band |
| LLM-call reduction at steady state | ≥ 80% of documents skip the LLM |
| Cost/doc | ≤ 1/100th of the deepseek-v4-flash path |

---

## 8. Risks + mitigations

| Risk | Mitigation |
|---|---|
| Subclass tail too thin (single-digit rows) | hierarchical heads + LLM augmentation + `other` fallback; LLM keeps the tail |
| Title-wins doctrine overfits filenames | train with title + head + body; eval on `--subset test` (held out); monitor per-stratum confusion |
| Calibration drift after retraining | temperature scaling is per-head, re-fit on val each training run; `calibration:classify` gates every release |
| Encoder can't learn corpus conventions (SEC joint filings → joint_venture, etc.) | those rules stay in the LLM prompt; the classifier defers via low confidence — the cascade is the safety net |
| Garbled/OCR-messy docs poison the classifier | clerk's messy flag routes them to the LLM before the classifier is trusted; Phase 2 messy head |
| Cost of training (GPU hours) | 149M-param fine-tune is ~1–2 L4-hours; one-time, amortized instantly |

---

## 9. Implementation roadmap

| Phase | Work | Verification gate |
|---|---|---|
| **P0 — Baseline** | Train ModernBERT-base doc_type head only; report accuracy on held-out test | ≥ 0.95 class accuracy or stop |
| **P1 — Full heads** | Add 5 subclass heads + windowing + vote merge | subclass ≥ 0.75 on stratified 50 |
| **P2 — Calibration** | Temperature scaling per head; `calibration:classify` report | ECE ≤ 0.05 |
| **P3 — Integration** | Wire into `intake_node` (triage slot + extended gate); span emission | `pilot:pipeline_chain --real` green |
| **P4 — A/B vs LLMs** | deepseek-v4-flash + gemma-4-E4B-it + qwen3.7-flash on the same 50; `compare_runs.py` | cost/doc ≤ 1/100th LLM; accuracy parity |
| **P5 — Deploy** | ONNX int8 export, CPU serving, Braintrust-traced shadow run | 1 week shadow, zero mis-route regressions |

Every phase logs to `reports/experiment_log.jsonl` (append-only, one summary
line per run — including the classifier runs, which are registered as a new
`eval:classifier` task per the eval-engineering skill, not a one-off script).

---

## 10. Bottom line

The best deployable ML model for the ingest node is a **fine-tuned
ModernBERT-base hierarchical classifier** — not because encoders are trendy,
but because: (1) the task is textbook encoder territory (fixed taxonomy,
doc-level labels, 3K docs), (2) the research says fine-tuned small models beat
zero-shot LLMs for exactly this, (3) ModernBERT's 8,192-token context and
Apache-2.0 license make it the strongest practical choice, and (4) the
pipeline already has every seam — gate, prior slot, windowing, confidence
bands, eval harness, Braintrust tracing — so the classifier is a ~200-line
addition, not a new system. The LLM sorter stays as the calibrated authority
for the hard tail, which is where its cost is justified. The result is a
pipeline that classifies 80–90% of documents at 1/100th the cost with the
same accuracy, and the eval harness measures it head-to-head against
deepseek-v4-flash, gemma-4-E4B-it, and qwen3.7-flash on the same stratified
50 — exactly the comparison the caller asked for.