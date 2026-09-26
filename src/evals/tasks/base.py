"""Shared eval-task contract — frames each node/agent as a concrete request.

Task modules under ``evals.tasks`` expose an :class:`EvalTask` that documents
what the agent is asked to do (system prompt role, entity schema, structured
output), then delegates execution to the shared runner path
(``build_cases`` → ``invoke`` → ``score``). The registry
(``evals.registry``) remains the executable catalog of ``TaskSpec`` ids.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from evals import invoke as invoke_mod
from evals import scoring
from evals.cases import load_cases
from evals.extraction_scope import LIVE_SCHEMA_FIELDS
from evals.registry import TaskSpec, get_task


@dataclass(frozen=True)
class EvalTask:
    """Discoverable per-node eval contract.

    ``request`` is the human-readable framing of what the agent/node is asked
    to perform — specialists receive their system prompt + entity schema and
    must extract structured fields from the sorter-handed document.
    """

    name: str
    node_name: str
    default_subset: str
    scorer: str
    description: str
    request: str
    agent_roles: tuple[str, ...] = ()
    prompt_role: str | None = None
    doc_class: str | None = None
    entity_fields: tuple[str, ...] = ()
    output_keys: tuple[str, ...] = ()
    supports_agent_mode: bool = True
    family: str = "eval"
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def task_id(self) -> str:
        return f"{self.family}:{self.name}"

    def to_spec(self) -> TaskSpec:
        return TaskSpec(
            name=self.name,
            family=self.family,
            node_name=self.node_name,
            default_subset=self.default_subset,
            scorer=self.scorer,
            description=self.description,
            supports_agent_mode=self.supports_agent_mode,
            tags=self.tags,
        )

    def registry_spec(self) -> TaskSpec:
        """The registered TaskSpec (source of truth for CLI ids)."""
        return get_task(self.task_id)

    def build_cases(
        self,
        subset: str | None = None,
        *,
        sample: int | None = None,
        seed: int = 42,
        n: int | None = None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return load_cases(
            subset or self.default_subset,
            sample=sample,
            seed=seed,
            n=n,
        )

    def invoke(self, case: dict[str, Any], *, mode: str = "node") -> dict[str, Any]:
        return invoke_mod.invoke(self.name, case, mode=mode)

    def score(self, case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
        from evals.runner import _score_case

        return _score_case(self.name, self.scorer, case, prediction)

    def framing(self) -> dict[str, Any]:
        """Serializable contract block for preflight / run provenance."""
        return {
            "task_id": self.task_id,
            "request": self.request,
            "node_name": self.node_name,
            "agent_roles": list(self.agent_roles),
            "prompt_role": self.prompt_role,
            "doc_class": self.doc_class,
            "entity_fields": list(self.entity_fields),
            "output_keys": list(self.output_keys),
            "scorer": self.scorer,
            "default_subset": self.default_subset,
            "supports_agent_mode": self.supports_agent_mode,
        }


def specialist_entity_fields(doc_class: str) -> tuple[str, ...]:
    """Live extraction keys for a Hub document class (sorted for stability)."""
    return tuple(sorted(LIVE_SCHEMA_FIELDS.get(doc_class, ())))


def specialist_task(
    *,
    name: str,
    doc_class: str,
    agent_role: str,
    description: str,
    default_subset: str,
) -> EvalTask:
    """Build the standard extraction-specialist eval framing."""
    fields = specialist_entity_fields(doc_class)
    field_list = ", ".join(fields) if fields else "(live schema)"
    request = (
        f"You are the {agent_role}. The sorter has classified this document as "
        f"`{doc_class}` (subclass may be present as sorter handoff context). "
        f"Using your activated system prompt (prompt role `{agent_role}`), "
        f"extract the registered entities from the document text and return "
        f"one complete JSON object with every live schema field "
        f"({field_list}). Unstated values must be null or []. Never invent "
        f"facts from letterhead, filename, or general knowledge."
    )
    return EvalTask(
        name=name,
        node_name="extract-fields",
        default_subset=default_subset,
        scorer="extraction",
        description=description,
        request=request,
        agent_roles=(agent_role,),
        prompt_role=agent_role,
        doc_class=doc_class,
        entity_fields=fields,
        output_keys=("extracted_data", "extraction_confidence", "doc_type"),
        tags=("specialist", "extraction", doc_class),
    )


def write_subset_manifest(
    cases: list[dict[str, Any]],
    *,
    run_dir: Path,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist the exact case set for reproducibility (filenames + sha256).

    Writes ``subset_manifest.jsonl`` (one row per case) and
    ``subset_manifest.json`` (summary + ordered ids) under ``run_dir``.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.append(
            {
                "case_id": case.get("id"),
                "filename": case.get("filename"),
                "expected_doc_class": case.get("expected_doc_class"),
                "expected_subclass": case.get("expected_subclass"),
                "doc_text_sha256": scoring.sha256_text(str(case.get("text") or "")),
                "source": case.get("source"),
                "config": case.get("config"),
                "split": case.get("split"),
            }
        )
    jsonl_path = run_dir / "subset_manifest.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, default=str) + "\n")
    summary = {
        "n": len(rows),
        "case_ids": [r["case_id"] for r in rows],
        "filenames": [r["filename"] for r in rows],
        "doc_text_sha256": [r["doc_text_sha256"] for r in rows],
        "provenance": provenance or {},
        "manifest_jsonl": str(jsonl_path),
    }
    summary_path = run_dir / "subset_manifest.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    summary["manifest_json"] = str(summary_path)
    return summary


def write_scoring_suite(
    case_rows: list[dict[str, Any]],
    *,
    run_dir: Path,
    scorer: str,
    essential_on_sink: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Full post-run score rollup (all deterministic keys, not sink essentials).

    The designated trace sink already carries ``ESSENTIAL_SCORES`` per case;
    this artifact is the complete quantification surface for interpretation.
    LLM-as-judge dimensions remain opt-in via ``scripts/score_run.py --judge``.
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    metrics = scoring.summarize_scores(case_rows)
    performance = scoring.summarize_performance(case_rows)
    essential = scoring.essential_rollup(scorer, case_rows)
    suite = {
        "scorer": scorer,
        "metrics_full": metrics,
        "metrics_essential": essential,
        "essential_forwarded_to_sink": essential_on_sink or essential,
        "performance": performance,
        "n_cases": len(case_rows),
        "n_errors": sum(1 for r in case_rows if r.get("error")),
        "post_hoc": {
            "recompute": "uv run python scripts/score_run.py --run-id <run_id> --recompute",
            "judges": "uv run python scripts/score_run.py --run-id <run_id> --judge verdict,quality",
            "compare": "uv run python scripts/compare_runs.py --a <run_a> --b <run_b>",
        },
    }
    path = run_dir / "scoring_suite.json"
    path.write_text(json.dumps(suite, indent=2, default=str), encoding="utf-8")
    suite["path"] = str(path)
    return suite
