"""Boss escalation eval — conflict adjudication."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="boss",
    node_name="adjudicate-conflict",
    default_subset="fixtures",
    scorer="boss",
    description="Boss escalation decisions on conflicting fixtures",
    request=(
        "You are the boss escalation agent. Given a conflict-flagged manifest "
        "(doc id, type, extracted data, escalation reason), adjudicate the "
        "conflict and emit an approved/review decision for human-routing."
    ),
    agent_roles=("boss",),
    prompt_role="boss",
    output_keys=("decision",),
    tags=("boss",),
)
