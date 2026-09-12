---
name: eval-tool-router
description: Choose the correct mailroom-evals skill for corpus loading, trace sinks, experiment logging, calibration, or pipeline internals. Read this FIRST at the start of any eval, pilot, calibration, dataset, Braintrust, Phoenix, or langgraph task in this repo so only the most appropriate skill is used.
---

# Eval tool router

Read this skill **first** when the task touches datasets, tracing, scoring,
calibration, or the llm-mailroom pipeline. Then open exactly one specialty
skill below. Do not invent a second trace sink or a parallel corpus loader —
this repo has exactly one of each.

## Decision table

| Job | Use | Skill | Do **not** |
| --- | --- | --- | --- |
| Load corpus rows / pick subsets | `evals.cases` (wraps `pipeline.hf_corpus_loader`) | [mailroom-corpus](../mailroom-corpus/SKILL.md) | Ad-hoc `datasets.load_dataset` or raw `/rows` fetches |
| Trace an eval run | `evals.tracing` (Braintrust → Phoenix → none) | [braintrust](../braintrust/SKILL.md) or [apache-phoenix](../apache-phoenix/SKILL.md) | Adding Langfuse as a sink here (out of scope by design) |
| Log run results | `evals.experiment_log` (append-only JSONL + MD) | [experiment-log](../experiment-log/SKILL.md) | Free-form JSON dumps or per-run one-off formats |
| Edge-test / calibrate a node | `evals.calibration.*` | [calibration](../calibration/SKILL.md) | Guessing thresholds without the fixtures grid |
| Invoke a pipeline node or agent | `evals.invoke` (node fn or agent class) | [pipeline-internals](../pipeline-internals/SKILL.md) | Reimplementing agent prompts or node logic |
| Prompt versions / lineage / GEPA | `evals.prompts.*` + freeze script | [prompt-lineage](../prompt-lineage/SKILL.md) | Editing frozen prompts or forking prompt text |
| Design a new eval task | `evals.registry` + `evals.runner` | [eval-engineering](../eval-engineering/SKILL.md) | One-off scripts outside the task registry |

## Non-negotiables

- Every run appends ONE run-summary line to `reports/experiment_log.jsonl`
  and carries Braintrust/Phoenix trace ids — no exceptions, including mock.
- Corpus loads pin revision `eafe1ab4c0d330d8f9c7a5fb254155e75d290828`
  (never float on Hub tip).
- Mock mode (`--mock`) must never hit the network; real mode needs
  `OPENROUTER_API_KEY`.
- Archive/intake evals run inside an isolated temp `MAILROOM_BASE_DIR`.
