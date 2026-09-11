---
name: pipeline-internals
description: How to invoke llm-mailroom graph nodes and agents in isolation from mailroom-evals — node functions, DocumentState construction, agent classes, judge gating, and isolation rules. Use when implementing or debugging evals.invoke, node-level tasks, or the chained pipeline eval.
---

# Pipeline internals (for eval invocation)

Canonical code: `Digital-Mailroom/packages/llm-mailroom/src/` (installed
editable as top-level modules: `agents`, `graph`, `pipeline`, `observability`,
`llm`, `schemas`).

## Graph nodes (build_graph.py:2487-2503)

`intake, classify, retry_classify, review_classify, extract, retry_extract,
judge_verify, arbiter, human_review, boss_escalation, compile_report,
catalog_write, archive`. Node contract: `def node(state: DocumentState) ->
dict[str, Any]` — returns ONLY changed fields; LangGraph merges. Procedural
nodes (`compile_report`, `catalog_write`) are skipped by eval tasks.

## Node-level invocation (evals.invoke)

Build a `DocumentState` from a corpus row: `doc_id`, `matter_id`,
`original_filename`, `file_path` (write doc_text to a temp .txt under the
isolated base dir), `doc_text`, `stage`, `doc_type` (from GT `expected` for
extract dispatch), `classification_attempts=0`, `extraction_attempts=0`,
`messages=[]`, transient counters 0. Call the raw node fn
(`graph.build_graph.classify_node` etc.). Judge gating: `judge_gate(state)`
(`graph/routing.py:313`) fires only in the ambiguous band
(0.70 ≤ extraction_confidence < 0.85) unless `MAILROOM_JUDGE_VERIFY=off` —
judge/arbiter evals set `extraction_confidence` explicitly to control the gate.

## Agent-level invocation

Direct agent classes: `SorterAgent().classify_json(text)`,
specialists `.<specialist>() .extract(text)`,
`CompletenessJudge().judge_completeness(doc_type, extracted, doc_text)`,
`ArbiterAgent().arbitrate(doc_type, extracted, judge_verdict, judge_findings,
judge_score)`, `BossAgent().adjudicate(manifest, matter_context=...)`,
`IntakeAgent().intake_run(text, filename)`,
`archive_document(manifest, file_path, prev_audit_hash)`.

## Isolation rules (MANDATORY)

- Set `MAILROOM_BASE_DIR` to a per-run temp dir BEFORE importing pipeline
  modules — intake/archive/catalog write real bins, manifests, SQLite
  catalogs, and audit chains under it.
- Mock mode monkeypatches `agents.base.BaseAgent.__init__` + `llm.client.OpenAI`
  with the FakeLangChainLLM pattern (see `run_agent_eval.py:_install_mocks`);
  never hit the network in mock.
- Real mode needs `OPENROUTER_API_KEY`; the runner sets
  `OBSERVABILITY_PROVIDER` from the resolved trace backend so LLM calls
  auto-trace.
- Full-chain eval uses `graph.build_graph.run_pipeline(file_path, matter_id)`
  (fresh `build_graph()` per test; `reset_compiled_graph()` between runs).
