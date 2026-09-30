"""Per-node evaluation tasks.

Each module frames the node's eval as a concrete request (system prompt role,
entity schema for specialists, structured output) and exposes an
:class:`~evals.tasks.base.EvalTask` with ``build_cases`` → ``invoke`` →
``score``. Execution still goes through the shared runner
(``evals.runner.run_task``); the registry (``evals.registry``) is the
executable source of truth for CLI task ids.

Trace sinks for these tasks: **Braintrust** or **Arize Phoenix** (never
Langfuse in this repo). Swap prompt versions via ``--prompt-version`` /
``--prompt-source`` and OpenRouter models via ``--model``. Subsets are locked
into ``subset_manifest.json`` per run for reproducibility. Real runs must
pass :mod:`evals.preflight` before any live API spend.
"""

from __future__ import annotations

from . import (
    arbiter,
    archivist,
    boss,
    classification,
    contracts,
    corporate_records,
    correspondence,
    insurance_claims,
    intake,
    judge_arbiter,
    merger_agreement,
    pipeline_chain,
)
from .base import EvalTask

# Ordered to match registry.EVAL_TASKS.
ALL_EVAL_TASKS: tuple[EvalTask, ...] = (
    intake.TASK,
    classification.TASK,
    contracts.TASK,
    merger_agreement.TASK,
    corporate_records.TASK,
    correspondence.TASK,
    insurance_claims.TASK,
    judge_arbiter.TASK,
    arbiter.TASK,
    boss.TASK,
    archivist.TASK,
    pipeline_chain.TASK,
)

TASKS_BY_NAME: dict[str, EvalTask] = {t.name: t for t in ALL_EVAL_TASKS}
TASKS_BY_ID: dict[str, EvalTask] = {t.task_id: t for t in ALL_EVAL_TASKS}


def get_eval_task(task_id_or_name: str) -> EvalTask:
    """Resolve an eval task module by ``eval:<name>`` or bare ``name``."""
    key = task_id_or_name.strip()
    if key in TASKS_BY_ID:
        return TASKS_BY_ID[key]
    if key.startswith("eval:") and key[5:] in TASKS_BY_NAME:
        return TASKS_BY_NAME[key[5:]]
    if key in TASKS_BY_NAME:
        return TASKS_BY_NAME[key]
    # Pilot / calibration ids map onto the eval module of the same name.
    if ":" in key:
        _family, name = key.split(":", 1)
        if name in TASKS_BY_NAME:
            return TASKS_BY_NAME[name]
        # calibration:classify → classification
        aliases = {"classify": "classification", "judge": "judge_arbiter", "retry": "contracts"}
        if name in aliases:
            return TASKS_BY_NAME[aliases[name]]
    known = ", ".join(sorted(TASKS_BY_ID))
    raise KeyError(f"unknown eval task {task_id_or_name!r}; known: {known}") from None


def list_eval_tasks() -> list[EvalTask]:
    return list(ALL_EVAL_TASKS)
