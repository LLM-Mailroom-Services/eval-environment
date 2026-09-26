# Prompt lineage & GEPA

mailroom-evals owns a **frozen, versioned prompt lineage** — the official
prompt version 1 (`mailroom-dataset-v1`) that GEPA mutations iterate on — while
staying wired to the mailroom pipeline's live lineage for cross-source A/Bs.

## The four resolution layers

| layer | lineage id | source | when used |
|---|---|---|---|
| **frozen** | `mailroom-dataset-v1` | `src/evals/prompts/frozen_v1.py` (generated) | **default for every eval run** — concise specialists + production freeze for other roles |
| **archived** | same lineage, v0 | `src/evals/prompts/archived_production.py` | `--prompt-source archived` or `--prompt-version <role>_v0` — the pre-concise production specialists (not the development baseline) |
| **mutation** | same lineage, v2+ | `prompts/mutations.json` (GEPA output) | A/B candidates; recorded with parent + change note |
| **production** | pipeline | `llm.prompts.prompt_templates` | `--prompt-source production` — the pipeline's own templates |

Resolution: `evals.prompts.lineage.resolve(key)` — frozen wins ties; unknown
keys raise (fail loud, never silently substitute).

## The frozen v1 snapshot

Materialized by `scripts/freeze_prompts.py` (idempotent; re-run on an
unchanged pipeline is byte-identical) from the live llm-mailroom production
prompts (`llm.prompts.prompt_templates`), the intake production template,
and the Langfuse pipeline evaluator rubrics:

| frozen key | source |
|---|---|
| `sorter_v1` | `sorter` (production) |
| `contracts_specialist_v1` … `insurance_claims_specialist_v1`, `merger_agreement_specialist_v1` | sandbox concise prompts (`Exios66/local-mailroom-sandbox` @ `303e7f0bb05d`; promoted via `scripts/promote_sandbox_specialist.py upgrade-frozen-specialists`) |
| `sorter_reviewer_v1` / `arbiter_v1` / `boss_v1` | `sorter_reviewer` / `arbiter` / `boss` (production) |
| `judge_v1` / `judge-classification_v1` / `judge-correctness_v1` | `judge*` (production) |
| `intake_v1` | production `INTAKE_SYSTEM_PROMPT` |
| `pipeline_verdict_v1` / `pipeline_quality_v1` | `PIPELINE_PROMPT` / `QUALITY_PROMPT` (CORRECT/PARTIAL/MISS + 0–1.0 rubrics) |

The pipeline taxonomy has five canonical document classes: contract,
corporate_record, correspondence, insurance_claim, merger_agreement.
merger_agreement is the MAUD class (agreement and plan of merger); contract
is the CUAD commercial-contract class — each has its own frozen specialist
(`merger_agreement_specialist_v1` vs `contracts_specialist_v1`).

Artifacts: `prompts/<key>.md` (human-readable mirror — never hand-edit),
`prompts/manifest.json` (pipeline git commit, source keys, sha256 per
version, freeze stamp).

**Drift check**: `uv run python scripts/freeze_prompts.py --check` — compares
every frozen sha256 against the live pipeline. Keys with `source_kind: sandbox`
in `prompts/manifest.json` are pinned to the sandbox promotion and skipped.
Drift on production-sourced keys means the pipeline prompts moved: re-freeze
those keys (never silently mutate v1).

## Runtime injection

`evals.prompts.registry.activate(source, overrides)` makes the chosen lineage
the LIVE prompt surface of the pipeline for the run, at the two verified
choke points:

1. `llm.prompts.get_managed_prompt` — BaseAgent prompts
   (`agents.base.system_prompt` → `llm.prompts.get_managed_prompt`).
2. `langchain_agents.prompts.PROMPT_VERSIONS` — the vendored LangChain
   versioned path (e.g. the sorter chain's `sorter_v14` key).

Injection is process-local and restored in the runner's `finally` block. It
works for real runs too: with Braintrust/Phoenix as `OBSERVABILITY_PROVIDER`,
`get_managed_prompt` resolves the local fallback path — exactly the patched
surface.

## Provenance (every run)

- Run summary: `prompt_lineage`, `prompt_source`, `prompt_version`,
  `prompt_versions` (per-agent key/lineage/sha256), `pipeline_git` (the
  llm-mailroom commit the prompts came from).
- Run dir: `prompts_snapshot.json` — the exact rendered prompt text per role.
  Any run is fully reproducible without a prompt-management service.

## GEPA mutation loop (scaffolded; loop driver = phase 2)

Ports the proven iteration-OS from llm-entity-extraction
(`scripts/prompt_engineer.py`, mechanics pinned to gepa-ai/gepa @ `b265bf9`,
arXiv 2507.19457):

```
OBSERVE (score_run.py --export-failures → data/manifests/<run>.failures.jsonl)
  → DECOMPOSE (clusters + evidence) → SELECT PARENT (Pareto frontier from the log)
  → DRAFT (ONE surgical .replace() per iteration)
  → VALIDATE (4 gates) → APPLY (prompts/mutations.json + prompts/<key>.md)
  → EVALUATE (same subset/seed A/B) → ACCEPT (paired delta CI lo > 0)
```

**The four gates** (`evals.prompts.mutations.validate_mutation`): anchor
occurs exactly once · new key unused + lineage naming (`<role>_v<N+1>`) ·
additive-only (parent preserved outside the anchor span) · metadata recorded.
A failing proposal is rejected, never applied.

**Tools**: `scripts/prompt_engineer.py` (DRAFT, `--dry-run`/`--apply`),
`scripts/compare_runs.py` (paired bootstrap CIs), the
[prompt-engineer](../.opencode/agents/prompt-engineer.md) subagent
(+ `PROMPT_ENGINEER_GEPA_PROVENANCE.md`).

**Discipline**: one rule per mutation, one A/B per mutation, same
subset/seed both sides; negative results recorded in the experiment log;
frozen v1 is never edited — mutations append.