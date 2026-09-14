# Calibration methodology

Calibration tasks edge-test a node's **decision boundaries** and emit
threshold recommendations. They are **report-only** — recommendations land in
`reports/calibration/<task>/<stamp>.{json,md}` and are never auto-applied to
pipeline configs.

## The fixtures grid

`Lucius-Morningstar/mailroom-dataset` config `fixtures` (26 train + 6 test,
schema v9; the frozen v8 parent `mailroom-corpus` carried the identical grid)
is a purpose-built calibration matrix:

- **`calibration_cell`** — the 2×2 confidence grid: `correct_high`,
  `correct_low`, `wrong_high`, `wrong_low` (+ blank for non-grid fixtures).
  A calibrated node scores `correct_*` confidently right and `wrong_*`
  confidently wrong; `wrong_high` (confidently wrong) is the dangerous cell.
- **`fixture_kind`** — `conflicting`(6), `retry_review`(5),
  `low_confidence`(4), `high_confidence`(3), `incomplete`(3), `ambiguous`(3),
  `retry`(2).
- **`probes_confidence`** — the confidence the sorter should emit
  (e.g. `0.985`, `0.895`).
- **`failure_stage`** — `ingestion`, `classification`, `extraction`,
  `grouping`, `adjudication`, `archival`.
- **`arbiter_outcome`** — `stands`, `re_extract`, `escalate_human_review`.
- **`review_expected` / `retry_expected` / `expected_stage`** — gating labels.

`bundles` (47+3, duplicate families) and `streams` (59+3, thread scenarios)
extend intake calibration. `ground_truth` rows flagged `review_expected=true`
/ `retry_expected=true` add at-scale signal.

## Per-node tasks

| task | probes | reads |
|---|---|---|
| `calibration:classify` | 2×2 grid + low/high-confidence fixtures | `fixture_cell`, `probes_confidence`, `review_expected` |
| `calibration:judge` | `incomplete` + `review_expected` rows | `review_expected`, judge completeness score |
| `calibration:arbiter` | `arbiter_outcome` cells | `arbiter_outcome` → decision map |
| `calibration:retry` | `retry_expected` + `failure_stage` rows | `retry_expected`, extraction confidence |
| `calibration:boss` | `conflicting` fixtures | decision validity + review routing |
| `calibration:intake` | messy/ambiguous + `bundles` + `streams` | no-truncation invariant, triage agreement |
| `calibration:archivist` | `failure_stage=archival` rows | conformance rates in the isolated base dir |

## Method (base.py)

1. Load fixtures via the subset grammar (`fixtures`, or `bundles`/`streams`).
2. Invoke the node (node fn preferred; agent mode for prompt A/Bs).
3. Score the **decision**, not field extraction.
4. Bin by emitted confidence → reliability table (n + accuracy per bin) →
   **ECE** (|accuracy − bin center| weighted by n; >0.05 = miscalibrated).
5. Sweep the decision threshold → precision/recall/F2 curve → recommend the
   operating point (F2 weights recall — the fail-safe direction for review
   gating).
6. Bootstrap CIs (`n_boot=1000`, seed 42); a recommendation whose CI spans
   >0.1 becomes an "insufficient evidence" caveat instead.
7. Write JSON+MD; tag traces `calibration`.

## Report shape

```json
{
  "reliability_table":  [{"bin": "0.95-1.00", "n": 3, "accuracy": 1.0}],
  "ece": 0.02,
  "cell_confusion":     {"wrong_high": {"n": 5, "agreed": 4, "agreement": 0.8}},
  "threshold_curve":    [{"threshold": 0.85, "tp": 4, "fp": 1, "fn": 0, "precision": 0.8, "recall": 1.0, "f2": 0.95}],
  "recommended_thresholds": {"review_gate_min_confidence": {"threshold": 0.85, "metric": "f2", "value": 0.95, "config_hint": "..."}},
  "caveats": ["small fixture sample (n=26) — CIs are wide; extend fixtures before trusting thresholds"]
}
```

## Reading the reports

- **Inverted cells** (`correct_high` scoring wrong, or `wrong_low` passing)
  are the loudest failure signal — fix before touching thresholds.
- **ECE > 0.05** means the confidence numbers themselves cannot gate anything
  yet; recalibrate before tuning downstream thresholds.
- **Sample size**: the fixtures grid is 32 rows total; every recommendation
  ships with its n. Extend fixtures (corpus-curator subagent) before pinning
  production thresholds on thin cells.
