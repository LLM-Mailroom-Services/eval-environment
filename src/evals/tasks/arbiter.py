"""Arbiter eval — decision validity vs arbiter_outcome."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="arbiter",
    node_name="arbitrate-verdict",
    default_subset="fixtures",
    scorer="arbiter",
    description="Arbiter decisions vs arbiter_outcome",
    request=(
        "You are the arbiter. Given the document type, extracted fields, the "
        "judge's verdict/findings/score, decide the pipeline disposition "
        "(approved / review / …). Emit a structured arbitration decision that "
        "agrees with fixture `arbiter_outcome` when present."
    ),
    agent_roles=("arbiter",),
    prompt_role="arbiter",
    output_keys=("decision",),
    tags=("arbiter",),
)
