"""Classification (sorter) eval — doc class + subclass accuracy."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="classification",
    node_name="classify-document",
    default_subset="full",
    scorer="classification",
    description="Classify node (sorter): doc class + subclass accuracy",
    request=(
        "You are the sorter. Given prepared document text from intake, classify "
        "the document into one of the live Hub classes (contract, merger_agreement, "
        "corporate_record, correspondence, insurance_claim) and emit the matching "
        "subclass / contract_subtype when applicable, plus a confidence score. "
        "Output structured classification fields only — do not extract entities."
    ),
    agent_roles=("sorter", "sorter_reviewer"),
    prompt_role="sorter",
    output_keys=("doc_type", "contract_subtype", "doc_subclass", "confidence"),
    tags=("sorter", "classification"),
)
