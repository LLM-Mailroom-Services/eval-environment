---
name: mailroom-corpus
description: Schema, configs, and subset selection for Lucius-Morningstar/mailroom-corpus and its family corpora. Use whenever loading eval cases, choosing subsets/splits, interpreting ground-truth columns, or debugging corpus loads in mailroom-evals.
---

# mailroom-corpus (schema v8)

The ONE loading path is `evals.cases` → `pipeline.hf_corpus_loader`
(`Digital-Mailroom/packages/llm-mailroom/src/pipeline/hf_corpus_loader.py`).
It joins the `ground_truth` config (labels) to `default` (blind text) on
`filename`, pinned to revision `eafe1ab4c0d330d8f9c7a5fb254155e75d290828`,
with `content_sha256` verification. Never zip rows positionally — always join.

## Configs (verified against the Dataset Viewer 2026-09-11)

| config | train | test | contents |
| --- | --- | --- | --- |
| `default` | 1792 | 208 | blind: `filename`, `doc_text`, `prompt`, `metadata` |
| `ground_truth` | 1792 | 208 | labels + provenance (~60 cols) |
| `fixtures` | 26 | 6 | calibration cells (see [calibration](../calibration/SKILL.md)) |
| `bundles` | 46 | 4 | duplicate/bundle families (`bundle_family`, `duplicate_type`) |
| `streams` | 58 | 4 | thread/stream scenarios (`thread_position`, `thread_size`) |

Train + test = 2000 docs = the "full" dataset. Family corpora (via
`hf_corpora.py` registry): `docclass-pilot` (138 stratified class×subclass),
`mailroom-cuad-contracts-full` (510), `enron-correspondence-dedup` (247k),
`cms-desynpuf-insurance-claims` (400).

## Ground-truth columns that drive evals

- `expected` — doc class: `contract | merger_agreement | corporate_record | correspondence | insurance_claim`
- `expected_subclass` — subclass (e.g. `powers_of_attorney`, MAUD consideration)
- `expected_specialist` — `contracts_specialist | corporate_records_specialist | correspondence_specialist | insurance_claims_specialist | …`
- `expected_stage` — terminal stage (`archived`, `review`, …)
- `review_expected` / `retry_expected` — gating labels for judge/arbiter/retry calibration
- `expected_post_retry_state`, `expected_correction`, `expected_post_correction_state` — post-retry conformance
- Insurance GT fields: `claim_number`, `policy_number`, `insurer`, `insured_party`, `claim_type`, `date_of_loss`, `date_filed`, `claimed_amount`, `adjuster`, `damages_description`, `coverage_determination`, `denial_reasons`, `supporting_documents`
- Contracts/merger: `cuad_clause_labels`, `maud_clause_labels`
- Provenance: `document_id`, `source_corpus`, `content_sha256`, `annotation_*`, `matter_id`, `group_id`, `thread_*`, `relationships`

## Subset spec grammar (`--subset`)

`full` | `train` | `test` | `class:<name>` | `subclass:<class>:<subclass>` |
`fixtures` | `bundles` | `streams` | `pilot` | `cuad` | `enron` | `claims`

Combine with `--sample N --seed S` (stratified by `expected`) and `--n N` caps.

## Environment

`HF_TOKEN` optional (public, ungated reads); `MAILROOM_HF_CACHE_DIR`
overrides the parquet cache (default `<base>/hf_cache/corpus`). The loader is
stdlib + httpx + pandas with a `datasets`-library preference when installed.
