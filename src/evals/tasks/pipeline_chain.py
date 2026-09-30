"""Full chained pipeline eval — 13-node graph end-to-end."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="pipeline_chain",
    node_name="document-pipeline",
    default_subset="pilot",
    scorer="pipeline",
    description="Full chained pipeline (13-node graph) end-to-end",
    request=(
        "Run one document through the full 13-node LangGraph mailroom pipeline "
        "(intake → classify → extract → judge/arbiter → report → catalog → "
        "archive). Score stage conformance and end-to-end class agreement. "
        "Node-mode only — agent-mode is not supported for the chain."
    ),
    agent_roles=(
        "intake",
        "image_extractor",
        "pdf_transcriber",
        "sorter",
        "sorter_reviewer",
        "contracts_specialist",
        "merger_agreement_specialist",
        "corporate_records_specialist",
        "correspondence_specialist",
        "insurance_claims_specialist",
        "judge",
        "arbiter",
        "boss",
    ),
    prompt_role=None,
    output_keys=(
        "stage",
        "doc_type",
        "extracted_data",
        "classification_confidence",
        "extraction_confidence",
        "review_decision",
        "error_message",
    ),
    supports_agent_mode=False,
    tags=("pipeline", "chain"),
)
