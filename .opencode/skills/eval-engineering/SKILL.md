---
name: eval-engineering
description: Methodology for designing, adding, and auditing evaluation tasks in mailroom-evals. Use when creating a new eval/pilot/calibration task, extending the registry, or auditing task quality — not for one-off ad-hoc scripts.
---

# Eval engineering (mailroom-evals)

New tasks are REGISTERED, never hand-rolled scripts. Workflow:
map the node → pick data + scorers → register the task → mock smoke →
real pilot → full run → audit.

## Task contract

Every task module in `src/evals/tasks/` (or `src/evals/calibration/`)
exposes `TASK` metadata (name, family, node, corpus defaults) and implements
the runner interface from `evals.runner`: `build_cases(subset, ...)` →
`invoke(case, mode)` → `score(case, prediction)` → metrics summary. The
shared runner supplies CLI, sampling, resume, tracing, experiment log.

## Design rules

1. **Score what the node decides**, not what downstream nodes decide
   (classify → class/subclass accuracy; judge → verdict agreement; arbiter →
   decision validity).
2. **Deterministic scorers only** for pass/fail metrics (reuse
   `mailroom.observability.classification_scoring` / `suite_scoring` /
   `field_scoring`); LLM-as-judge is out of scope for v1.
3. **Every case records performance**: latency_ms, token usage, cost, retry
   counts — per-node performance analysis is a first-class output.
4. **Subsets over full runs by default**: pilot first, then class slices,
   then `full` (2000 docs × real LLM is expensive; resume manifest protects
   long runs).
5. **Mock smoke is the CI gate**: every task must pass `--mock --n 3` with
   zero network and deterministic scores.
6. **Trace + log everything**: one span per case, one run-summary line per
   run (see [experiment-log](../experiment-log/SKILL.md)).
7. **Prompt iterations**: pass `--prompt-version`; it rides trace metadata,
   the experiment log, and report filenames — A/B comparisons come from
   filtering the log by prompt_version.

## Audit loop

After each real run: fetch traces fresh from the sink, confirm span
shape/metadata, spot-check 3 scored cases against raw output, verify the
experiment-log line round-trips (`load_runs`), then record caveats in the
run's MD report.
