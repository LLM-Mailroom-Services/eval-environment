---
name: mailroom-corpus
description: Schema, configs, and subset selection for Lucius-Morningstar/mailroom-dataset (schema v9, successor of the frozen v8 mailroom-corpus) and its family corpora. Use whenever loading eval cases, choosing subsets/splits, interpreting ground-truth columns (incl. the nested gt_fields payload), or debugging corpus loads in mailroom-evals.
---

# mailroom-corpus (schema v9 — `mailroom-dataset`)

The ONE loading path is `evals.cases` → `pipeline.hf_corpus_loader`
(`Digital-Mailroom/packages/llm-mailroom/src/pipeline/hf_corpus_loader.py`).
It joins the `ground_truth` config (labels) to `default` (blind text) on
`filename`, pinned to revision `46a4d3c240a36671cde0182fff4960f6b8b73aca`,
with `content_sha256` verification. Never zip rows positionally — always join.

**Lineage**: `mailroom-dataset` v1 (= schema v9 of the corpus family, 3,302
rows) is the standalone successor of `Lucius-Morningstar/mailroom-corpus`
(frozen v8 baseline, 2,000 rows @ `eafe1ab4c0d330d8f9c7a5fb254155e75d290828`,
kept for lineage reference — never destroyed). The v8 base + 1,302 expansion
draws: contract +91, corporate_record +411, correspondence +650,
insurance_claim +150.

## Configs (verified against the Dataset Viewer 2026-09-13, GT-closure revision `46a4d3c2`)

| config | train | test | contents |
| --- | --- | --- | --- |
| `default` | 2979 | 323 | blind: `filename`, `doc_text`, `prompt`, `metadata` — zero labels by construction |
| `ground_truth` | 2979 | 323 | labels + provenance (36 cols; per-field GT nested in `gt_fields`) |
| `fixtures` | 26 | 6 | calibration cells (see [calibration](../calibration/SKILL.md)) |
| `bundles` | 47 | 3 | duplicate/bundle families (`bundle_family`, `duplicate_type`) |
| `streams` | 59 | 3 | thread/stream scenarios (`thread_position`, `thread_size`) |

Train + test = 3302 docs = the "full" dataset. Class mix: contract 600,
corporate_record 450, correspondence 1000, insurance_claim 1100,
merger_agreement 152 (train per class: insurance 986 · correspondence 915 ·
contract 540 · corporate_record 403 · merger 135). Family corpora (via
`hf_corpora.py` registry, floating on Hub tip — only the main corpus is
sha-pinned): `docclass-pilot` (138 stratified class×subclass),
`mailroom-cuad-contracts-full` (510; viewer parquet export currently failed),
`enron-correspondence-dedup` (247k; viewer conversion pending),
`cms-desynpuf-insurance-claims` (400).

## Ground-truth columns that drive evals

- `expected` — doc class: `contract | merger_agreement | corporate_record | correspondence | insurance_claim`
- `expected_subclass` — subclass (e.g. MAUD consideration, record type)
- `expected_specialist` — `contracts_specialist | corporate_records_specialist | correspondence_specialist | insurance_claims_specialist | …`
- `expected_stage` — terminal stage (`archived`, `review`, …)
- `review_expected` / `retry_expected` — gating labels for judge/arbiter/retry
  calibration (v9 serializes them as `'true'`/`'false'` strings)
- `expected_post_retry_state` — post-retry conformance
- **`gt_fields`** — nested JSON-string payload hoisted to flat keys by
  `evals.cases._expand_gt_fields` before scoring. It carries:
  - the 13 insurance GT fields: `claim_number`, `policy_number`, `insurer`,
    `insured_party`, `claim_type`, `date_of_loss`, `date_filed`,
    `claimed_amount`, `adjuster`, `damages_description`,
    `coverage_determination`, `denial_reasons`, `supporting_documents`
  - `cuad_clause_labels`, `maud_clause_labels` — JSON **object** strings
    (clause → annotation spans); empty = the literal 2-char string `'{}'`
    (never null/`''`). `adjuster` is legitimately empty on 950 rows
    (CMS DE-SynPUF / GNOTHEIA / INSURBIAS have no adjuster in source).
- Provenance: `document_id`, `source_document_id`, `source_revision`,
  `content_sha256`, `annotation_*`, `matter_id`, `group_id`, `thread_*`,
  `relationships`, `related_document_ids`.

## Subset spec grammar (`--subset`)

`full` | `train` | `test` | `class:<name>` | `subclass:<class>:<subclass>` |
`fixtures` | `bundles` | `streams` | `pilot` | `cuad` | `enron` | `claims`

Combine with `--sample N --seed S` (stratified by `expected`) and `--n N` caps.
Caveat: `cuad`/`enron` currently fail Hub-side parquet conversion —
`load_cases` raises loudly rather than returning 0 cases.

## Environment

`HF_TOKEN` optional (public, ungated reads); `MAILROOM_HF_CACHE_DIR`
overrides the parquet cache (default `<base>/hf_cache/corpus`). The loader is
stdlib + httpx + pandas with a `datasets`-library preference when installed.
