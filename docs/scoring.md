# Extraction scoring (eval harness)

Deterministic extraction scores flow through `evals.scoring.score_extraction`,
which delegates to the pipeline's `observability.suite_scoring.score_with_suite`
(same rubric as production, wired via `evals.dojo_wiring`).

## Class-scoped ground truth (issue #9)

Hub `ground_truth` / nested `gt_fields` often carries a **union** of specialist
columns. For a correspondence document, insurance-claim placeholders
(`claim_number`, `denial_reasons: []`, …) are not applicable extraction events
and must **not** reduce `overall_score`. The symmetric rule applies for any
other-class key on the wrong `expected` class.

Before the suite runs, `evals.extraction_scope` filters each
`(doc_class, predicted, expected)` pair:

1. Drop empty GT placeholders (`[]`, `{}`, `""`, `null`) — the dojo skips
   `None`/`""` but not empty lists.
2. Drop keys outside the live schema for `doc_class` (five Hub classes).
3. Drop trace-only keys (`reasoning`, `confidence`).
4. Alias Hub union names (`claimed_amount` → `demand_amount` on correspondence).

Case loading (`cases._expected_fields`) applies the same expected-field filter
so experiment-log rows match what the scorer uses. Clause-label F1
(`score_label_lists`) still reads label columns from the case row; empty
`{}` / `[]` payloads skip per the v9 convention.

Reference implementation: [local-mailroom-sandbox PR #33](https://github.com/Exios66/local-mailroom-sandbox/pull/33)
(`extraction_scope.py` @ `97c0f940`).
