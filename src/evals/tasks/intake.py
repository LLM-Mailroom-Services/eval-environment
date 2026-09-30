"""Intake eval — triage / clean / prepare invariants."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="intake",
    node_name="intake-document",
    default_subset="full",
    scorer="intake",
    description="Intake node: triage/clean/prepare invariants + triage agreement",
    request=(
        "You are the intake agent. Given a raw inbound document (filename + text), "
        "triage, clean, and prepare it for the sorter: emit cleaned text, triage "
        "labels, and intake stats without truncating content. Do not classify or "
        "extract fields — only prepare the document for downstream nodes."
    ),
    agent_roles=("intake", "image_extractor", "pdf_transcriber"),
    prompt_role="intake",
    output_keys=("doc_text", "cleaned", "triage", "intake_stats"),
    tags=("intake",),
)
