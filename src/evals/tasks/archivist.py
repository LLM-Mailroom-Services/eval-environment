"""Archivist eval — archive conformance (manifest / audit / sha256 / stage)."""

from __future__ import annotations

from evals.tasks.base import EvalTask

TASK = EvalTask(
    name="archivist",
    node_name="archive-document",
    default_subset="fixtures",
    scorer="archivist",
    description="Archive conformance (manifest/audit/sha256/stage)",
    request=(
        "You are the archivist (procedural node). Given a report-compiled "
        "document state, archive the file under the isolated base dir, write "
        "the manifest sidecar, and advance stage to archived. Conformance is "
        "scored on archive path presence, audit/manifest write, content "
        "sha256 integrity, and final stage."
    ),
    agent_roles=(),
    prompt_role=None,
    output_keys=("stage", "archive_path", "audit_entry", "sha256_ok"),
    supports_agent_mode=True,  # stub agent path exists
    tags=("archivist", "procedural"),
)
