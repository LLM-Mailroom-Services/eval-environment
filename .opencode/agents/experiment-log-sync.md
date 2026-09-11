---
description: Validates, repairs, and renders the centralized experiment log for mailroom-evals — schema conformance, JSONL integrity, markdown rebuilds, and cross-run comparisons. Use when the log looks inconsistent, after schema changes, or when producing comparison reports.
mode: subagent
---

# Experiment log sync

You guard the centralized experiment log (see the `experiment-log` skill at
`.opencode/skills/experiment-log/SKILL.md`).

## Tasks

- **Validate**: every `reports/experiment_log.jsonl` line parses as JSON and
  conforms to `schemas/experiment_record.v1.json` (`schema_version`,
  `record_kind`, required keys); case files referenced by `cases_ref` exist
  and their rows carry `run_id`.
- **Render**: rebuild `reports/experiment_log.md` via
  `uv run python scripts/render_experiment_log.py` (idempotent, tables only).
- **Compare**: produce run-vs-run tables filtered by task / prompt_version /
  model / subset (metrics + performance deltas) when asked for A/B reads.
- **Repair**: a torn last line (crashed append) gets truncated with a note;
  history is never rewritten otherwise.

## Tools

```bash
uv run python scripts/render_experiment_log.py --validate
uv run python scripts/render_experiment_log.py
uv run python -c "from evals.experiment_log import load_runs; print(len(load_runs()))"
```

Return: validation verdict (n runs, n invalid), render status, and any
schema-drift findings with the exact offending lines.
