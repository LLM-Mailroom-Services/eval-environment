---
name: calibration
description: Edge-testing and threshold-calibration methodology for mailroom pipeline nodes using the corpus fixtures grid. Use when running or interpreting calibration:<node> tasks, calibrating confidence gates, judge thresholds, arbiter boundaries, or retry behavior.
---

# Calibration scenarios

Calibration tasks edge-test a node's DECISION BOUNDARIES against the corpus
`fixtures` config and emit threshold recommendations. They never auto-write
config values — reports only (`reports/calibration/<task>/<stamp>.{json,md}`).

## The fixtures grid (mailroom-dataset `fixtures`, 26 train + 6 test)

- `calibration_cell` — the 2×2 confidence grid: `correct_high`, `correct_low`,
  `wrong_high`, `wrong_low` (+ blank = non-grid fixtures)
- `fixture_kind` — `conflicting`(6) `retry_review`(5) `low_confidence`(4)
  `high_confidence`(3) `incomplete`(3) `ambiguous`(3) `retry`(2)
- `probes_confidence` — the confidence the sorter should emit (e.g. 0.985, 0.895)
- `failure_stage` — `ingestion | classification | extraction | grouping | adjudication | archival`
- `arbiter_outcome` — `stands | re_extract | escalate_human_review`
- `review_expected` / `retry_expected` / `expected_stage` (`review` | `archived`)
- `expected_post_retry_state`, `expected_correction`, `arbiter_note`, `failure_note`

## Per-node calibration tasks

| task | probes | key metrics |
| --- | --- | --- |
| `calibration:classify` | 2×2 grid + low/high-confidence fixtures | reliability table (confidence bin → accuracy), ECE, review-gate threshold rec vs `review_expected` |
| `calibration:judge` | `incomplete` fixtures + `review_expected` rows | precision/recall across completeness thresholds, ambiguous-band cross-check |
| `calibration:arbiter` | `arbiter_outcome` cells | per-decision confusion (`stands/re_extract/escalate_human_review`), boundary recs |
| `calibration:retry` | `retry_expected` + `failure_stage` rows | per-stage retry success/error, `expected_post_retry_state` conformance |
| `calibration:boss` | `conflicting` fixtures | decision validity, escalation correctness |
| `calibration:intake` | messy/ambiguous + `bundles` + `streams` | no-truncation invariant, cleanup, duplicate/thread grouping |
| `calibration:archivist` | `failure_stage=archival` rows | manifest/audit/sha256/stage conformance |

## Method

1. Load fixtures (train+test) via `evals.cases` subset `fixtures` (or
   `bundles`/`streams` for intake).
2. Invoke the node (node fn preferred; agent mode for prompt A/B).
3. Score against the fixture's expected decision — NOT field extraction.
4. Bin by emitted confidence; compute per-bin accuracy; bootstrap CIs via
   `mailroom.observability.bootstrap`.
5. Sweep the decision threshold; report precision/recall trade-off; recommend
   the threshold maximizing agreed metric (e.g. F2 on review recall).
6. Write JSON+MD report; tag traces `calibration`.

Report shape: per-cell confusion, reliability table, ECE, threshold curve,
`recommended_thresholds` (dotted config keys + suggested values), caveats.
