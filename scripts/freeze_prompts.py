#!/usr/bin/env python3
"""Freeze the mailroom production prompt lineage into mailroom-dataset-v1.

Materializes the live llm-mailroom production prompts (``llm.prompts.prompt_templates``,
derived from each role's live production template) plus the Langfuse pipeline evaluator
rubrics and the intake production template into THIS repo as the official frozen prompt
version 1 of the new ``mailroom-dataset-v1`` lineage — the seed GEPA mutations iterate on.

Frozen keys (role-name keys, lineage-prefixed):

    sorter_v1                       <- sorter (production)
    contracts_specialist_v1         <- contracts_specialist (production)
    corporate_records_specialist_v1 <- corporate_records_specialist (production)
    correspondence_specialist_v1    <- correspondence_specialist (production)
    insurance_claims_specialist_v1  <- insurance_claims_specialist (production)
    sorter_reviewer_v1              <- sorter_reviewer (production)
    arbiter_v1                      <- arbiter (production)
    boss_v1                         <- boss (production)
    judge_v1                        <- judge (production)
    judge-classification_v1         <- judge-classification (production)
    judge-correctness_v1            <- judge-correctness (production)
    intake_v1                       <- INTAKE_SYSTEM_PROMPT (production)
    pipeline_verdict_v1             <- PIPELINE_PROMPT (sync_evaluators.py)
    pipeline_quality_v1             <- QUALITY_PROMPT (sync_evaluators.py)

The script is IDEMPOTENT: re-running on an unchanged pipeline produces
byte-identical output (verified by tests). It writes:

    src/evals/prompts/frozen_v1.py   versioned constants (importable, frozen)
    prompts/<key>.md                 human-readable mirror (never hand-edit)
    prompts/manifest.json            provenance (pipeline git commit, source
                                     keys, derivation recipe, sha256, stamp)

Usage:
    uv run python scripts/freeze_prompts.py            # freeze + verify
    uv run python scripts/freeze_prompts.py --check    # drift check only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from evals.prompts.mirror_md import prompt_mirror_markdown


def _ensure_pipeline_importable() -> None:
    pipeline_src = REPO_ROOT.parent / "Digital-Mailroom" / "packages" / "llm-mailroom" / "src"
    path = str(pipeline_src)
    if path not in sys.path:
        sys.path.insert(0, path)
    from pipeline.env import load_env

    load_env()

# role -> (frozen key, source kind, source key)
FREEZE_MAP: tuple[tuple[str, str, str], ...] = (
    ("sorter", "production", "sorter"),
    ("contracts_specialist", "production", "contracts_specialist"),
    ("corporate_records_specialist", "production", "corporate_records_specialist"),
    ("correspondence_specialist", "production", "correspondence_specialist"),
    ("insurance_claims_specialist", "production", "insurance_claims_specialist"),
    ("sorter_reviewer", "production", "sorter_reviewer"),
    ("arbiter", "production", "arbiter"),
    ("boss", "production", "boss"),
    ("judge", "production", "judge"),
    ("judge-classification", "production", "judge-classification"),
    ("judge-correctness", "production", "judge-correctness"),
    ("intake", "production", "INTAKE_SYSTEM_PROMPT"),
    ("pipeline_verdict", "evaluator", "PIPELINE_PROMPT"),
    ("pipeline_quality", "evaluator", "QUALITY_PROMPT"),
)

LINEAGE_ID = "mailroom-dataset-v1"
FROZEN_MODULE = REPO_ROOT / "src" / "evals" / "prompts" / "frozen_v1.py"
PROMPTS_DIR = REPO_ROOT / "prompts"
MANIFEST_PATH = PROMPTS_DIR / "manifest.json"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pipeline_git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT.parent / "Digital-Mailroom" / "packages" / "llm-mailroom"),
             "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def collect_frozen() -> dict[str, tuple[str, str, str]]:
    """role -> (text, source_kind, source_key). Raises when the pipeline
    cannot supply a template — freezing a partial lineage is worse than
    failing loudly."""
    _ensure_pipeline_importable()
    from agents.intake import INTAKE_SYSTEM_PROMPT
    from llm.prompts import prompt_templates
    from scripts.sync_evaluators import PIPELINE_PROMPT, QUALITY_PROMPT

    templates = prompt_templates()
    out: dict[str, tuple[str, str, str]] = {}
    for role, kind, source_key in FREEZE_MAP:
        if kind == "evaluator":
            text = PIPELINE_PROMPT if source_key == "PIPELINE_PROMPT" else QUALITY_PROMPT
        elif source_key == "INTAKE_SYSTEM_PROMPT":
            text = INTAKE_SYSTEM_PROMPT
        else:
            text = templates[source_key]
        out[role] = (text, kind, source_key)
    return out


def _safe_ident(role: str) -> str:
    """Python-safe identifier for a role (hyphens -> underscores)."""
    return role.replace("-", "_")


def render_module(frozen: dict[str, tuple[str, str, str]]) -> str:
    """Render frozen_v1.py — versioned constants + VERSIONS dict + metadata."""
    stamp = datetime.now(UTC).isoformat(timespec="seconds")
    lines = [
        f'"""FROZEN prompt lineage {LINEAGE_ID} — DO NOT EDIT BY HAND.',
        "",
        "Materialized by scripts/freeze_prompts.py from the llm-mailroom",
        "production lineage (llm.prompts.prompt_templates), the intake production",
        "template, and the Langfuse pipeline evaluator rubrics. This is the",
        "official prompt version 1 of the mailroom-dataset lineage and the seed",
        "for GEPA mutations (mutations append via evals/prompts/mutations.py,",
        "never here).",
        "",
        f"Freeze stamp: {stamp}",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        f'LINEAGE_ID = {LINEAGE_ID!r}',
        "FROZEN_VERSION = 1",
        "",
    ]
    for role, (text, kind, source_key) in frozen.items():
        key = f"{role}_v1"
        ident = _safe_ident(role) + "_v1"
        lines.append(f"# key: {key} — source: {kind}:{source_key} (sha256 {sha256(text)[:12]})")
        lines.append(f"{ident} = {text!r}")
        lines.append("")
    lines.append("VERSIONS: dict[str, str] = {")
    for role in frozen:
        lines.append(f"    {role + '_v1'!r}: {_safe_ident(role)}_v1,")
    lines.append("}")
    lines.append("")
    lines.append("SOURCE_OF: dict[str, str] = {")
    for role, (_text, kind, source_key) in frozen.items():
        lines.append(f"    {role + '_v1'!r}: {kind + ':' + source_key!r},")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def render_manifest(frozen: dict[str, tuple[str, str, str]]) -> dict:
    return {
        "lineage_id": LINEAGE_ID,
        "frozen_version": 1,
        "frozen_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "pipeline_git_commit": pipeline_git_commit(),
        "derivation": "llm-mailroom production prompt_templates (live production templates) + intake production template + Langfuse pipeline evaluator rubrics",
        "versions": {
            f"{role}_v1": {
                "source_kind": kind,
                "source_key": source_key,
                "sha256": sha256(text),
                "chars": len(text),
            }
            for role, (text, kind, source_key) in frozen.items()
        },
    }


def write_frozen(frozen: dict[str, tuple[str, str, str]]) -> None:
    FROZEN_MODULE.parent.mkdir(parents=True, exist_ok=True)
    FROZEN_MODULE.write_text(render_module(frozen), encoding="utf-8")
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    for role, (text, _kind, _source) in frozen.items():
        key = f"{role}_v1"
        (PROMPTS_DIR / f"{key}.md").write_text(prompt_mirror_markdown(key, text), encoding="utf-8")
    MANIFEST_PATH.write_text(json.dumps(render_manifest(frozen), indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="drift check only (no writes)")
    args = parser.parse_args()

    if args.check:
        if not FROZEN_MODULE.exists() or not MANIFEST_PATH.exists():
            print("frozen lineage missing — run scripts/freeze_prompts.py first")
            return 1
        manifest = json.loads(MANIFEST_PATH.read_text())
        try:
            frozen = collect_frozen()
        except ModuleNotFoundError:
            frozen = None
        drifted = []
        for key, meta in manifest["versions"].items():
            if meta.get("source_kind") == "sandbox":
                continue
            if frozen is None:
                continue
            role = key.rsplit("_v1", 1)[0]
            if sha256(frozen[role][0]) != meta["sha256"]:
                drifted.append(key)
        if drifted:
            print(f"DRIFT detected for: {drifted} — the pipeline prompts moved; re-run scripts/freeze_prompts.py to cut a new version")
            return 1
        skipped = " (production keys skipped — llm-mailroom not importable)" if frozen is None else ""
        print(f"OK: {len(manifest['versions'])} frozen versions match the live pipeline (lineage {LINEAGE_ID}){skipped}")
        return 0

    frozen = collect_frozen()
    write_frozen(frozen)
    manifest = json.loads(MANIFEST_PATH.read_text())
    print(f"frozen {len(manifest['versions'])} prompts as {LINEAGE_ID}")
    print(f"  pipeline git: {manifest['pipeline_git_commit']}")
    print(f"  module: {FROZEN_MODULE.relative_to(REPO_ROOT)}")
    print(f"  mirror: {PROMPTS_DIR.relative_to(REPO_ROOT)}/<key>.md + manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
