# ModernBERT (mailroom-ml) — training & held-out test reports

Canonical home for ModernBERT classifier reports. The sandbox repo
(`local-mailroom-sandbox`) only **feeds** weights via `MAILROOM_ML_SRC` /
`MODERNBERT_MODEL_PATH`; it does not own these write-ups.

| Section | Contents |
| --- | --- |
| [training/](./training/) | Run 1–3 training legs (Modal / resume lineage) |
| [held-out-test/](./held-out-test/) | 323-document test split eval (canonical: Modal `eval_full_test_20260927.json`) |
| [comparisons/](./comparisons/) | Cost vs LLM sorter (API legs from this repo’s experiment log) |

**Live SSH training (2026-09-27):** do not launch competing GPU jobs on the
training host. Refresh held-out + comparison reports when the new checkpoint
and `mailroom-ml/training/eval_modernbert.py --json` export land.

**Sorter cost basis:** measured OpenRouter API runs under
`reports/api-comparisons/qwen3-8b/classification/` (not sandbox fixtures).
