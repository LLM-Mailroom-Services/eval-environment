"""Completeness-judge eval — verdict agreement vs review_expected."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="judge_arbiter",
    node_name="judge-verify",
    default_subset="fixtures",
    scorer="judge",
    description="Completeness judge verdicts vs review_expected",
    request=(
        "You are the completeness judge. Given a document type, the specialist's "
        "extracted JSON, and the source document text, judge whether the extraction "
        "is complete and grounded. Emit a verdict (complete / incomplete / …), a "
        "completeness score, and findings. Score against fixture `review_expected`."
    ),
    agent_roles=("judge",),
    prompt_role="judge",
    output_keys=("judge_verdict", "completeness_label", "completeness", "judge_findings"),
    tags=("judge",),
)
