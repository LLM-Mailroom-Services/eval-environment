#!/usr/bin/env python3
"""Promote sandbox simplified specialist prompts into the eval catalog.

Uses the official lineage paths only:
  - ``evals.prompts.mutations.apply_mutation`` for v2+ (full-text replace via
    parent-span anchor when the sandbox text is not a surgical GEPA edit).
  - ``scripts/freeze_prompts.write_frozen`` for a new frozen v1 role key.

Provenance: pass sandbox git SHA + stem; never hand-edit frozen v1 bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from evals.prompts import frozen_v1, mutations
from evals.prompts.mirror_md import prompt_mirror_markdown

SANDBOX_REPO = "Exios66/local-mailroom-sandbox"
DEFAULT_SANDBOX_SHA = "97c0f940194f030504db0b49443caf90ce749d79"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_sandbox_prompt(sha: str, stem: str) -> str:
    url = (
        f"https://raw.githubusercontent.com/{SANDBOX_REPO}/{sha}"
        f"/config/prompts/{stem}.txt"
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf-8")


def promote_mutation(
    *,
    parent_key: str,
    new_key: str,
    sandbox_sha: str,
    sandbox_stem: str,
    note: str,
) -> dict:
    from evals.prompts.lineage import resolve

    new_text = fetch_sandbox_prompt(sandbox_sha, sandbox_stem)
    parent = resolve(parent_key)
    meta = mutations.apply_mutation(
        parent_key=parent_key,
        new_key=new_key,
        anchor=parent.text,
        replacement=new_text,
        note=note,
        persist=True,
    )
    mutations.render_prompts_mirror()
    return meta


def _safe_ident(role: str) -> str:
    return role.replace("-", "_")


def _write_frozen_catalog(frozen: dict[str, tuple[str, str, str]]) -> None:
    """Rewrite frozen_v1 + mirrors + manifest without importing the pipeline."""
    from datetime import UTC, datetime

    manifest_path = REPO_ROOT / "prompts" / "manifest.json"
    prior = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    stamp = datetime.now(UTC).isoformat(timespec="seconds")
    module_path = REPO_ROOT / "src" / "evals" / "prompts" / "frozen_v1.py"
    lines = [
        '"""FROZEN prompt lineage mailroom-dataset-v1 — DO NOT EDIT BY HAND.',
        "",
        "Materialized by scripts/freeze_prompts.py / promote_sandbox_specialist.py.",
        "",
        f"Freeze stamp: {stamp}",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "LINEAGE_ID = 'mailroom-dataset-v1'",
        "FROZEN_VERSION = 1",
        "",
    ]
    for r, (text, kind, source_key) in frozen.items():
        key = f"{r}_v1"
        ident = _safe_ident(r) + "_v1"
        lines.append(f"# key: {key} — source: {kind}:{source_key} (sha256 {sha256(text)[:12]})")
        lines.append(f"{ident} = {text!r}")
        lines.append("")
    lines.append("VERSIONS: dict[str, str] = {")
    for r in frozen:
        lines.append(f"    {r + '_v1'!r}: {_safe_ident(r)}_v1,")
    lines.append("}")
    lines.append("")
    lines.append("SOURCE_OF: dict[str, str] = {")
    for r, (_text, kind, source_key) in frozen.items():
        lines.append(f"    {r + '_v1'!r}: {kind + ':' + source_key!r},")
    lines.append("}")
    lines.append("")
    module_path.write_text("\n".join(lines), encoding="utf-8")
    prompts_dir = REPO_ROOT / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    for r, (text, _kind, _source) in frozen.items():
        key = f"{r}_v1"
        (prompts_dir / f"{key}.md").write_text(prompt_mirror_markdown(key, text), encoding="utf-8")
    manifest = {
        "lineage_id": prior.get("lineage_id", "mailroom-dataset-v1"),
        "frozen_version": prior.get("frozen_version", 1),
        "frozen_at": stamp,
        "pipeline_git_commit": prior.get("pipeline_git_commit"),
        "derivation": prior.get(
            "derivation",
            "llm-mailroom production prompt_templates + intake + evaluator rubrics",
        ),
        "versions": {
            f"{r}_v1": {
                "source_kind": kind,
                "source_key": source_key,
                "sha256": sha256(text),
                "chars": len(text),
            }
            for r, (text, kind, source_key) in frozen.items()
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def promote_freeze_new(
    *,
    role: str,
    sandbox_sha: str,
    sandbox_stem: str,
    source_label: str,
) -> dict:
    new_text = fetch_sandbox_prompt(sandbox_sha, sandbox_stem)
    frozen: dict[str, tuple[str, str, str]] = {}
    for key, text in frozen_v1.VERSIONS.items():
        r = key.rsplit("_v1", 1)[0]
        prov = frozen_v1.SOURCE_OF[key]
        kind, source_key = prov.split(":", 1)
        frozen[r] = (text, kind, source_key)
    if role in frozen:
        raise SystemExit(f"role {role!r} already frozen")
    frozen[role] = (new_text, "sandbox", source_label)
    _write_frozen_catalog(frozen)
    key = f"{role}_v1"
    manifest = json.loads((REPO_ROOT / "prompts" / "manifest.json").read_text())
    return {
        "key": key,
        "sha256": sha256(new_text),
        "chars": len(new_text),
        "sandbox_sha": sandbox_sha,
        "sandbox_stem": sandbox_stem,
        "manifest_versions": len(manifest.get("versions") or {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    mut = sub.add_parser("mutation", help="append a v<N+1> mutation from sandbox text")
    mut.add_argument("--parent", required=True)
    mut.add_argument("--new-key", required=True)
    mut.add_argument("--sandbox-stem", required=True)
    mut.add_argument("--sandbox-sha", default=DEFAULT_SANDBOX_SHA)
    mut.add_argument("--note", required=True)

    frz = sub.add_parser("freeze-new", help="add a new frozen v1 role key from sandbox")
    frz.add_argument("--role", required=True)
    frz.add_argument("--sandbox-stem", required=True)
    frz.add_argument("--sandbox-sha", default=DEFAULT_SANDBOX_SHA)
    frz.add_argument(
        "--source-label",
        default=None,
        help="manifest source_key (default: sandbox stem @ sha)",
    )

    args = parser.parse_args()
    if args.cmd == "mutation":
        meta = promote_mutation(
            parent_key=args.parent,
            new_key=args.new_key,
            sandbox_sha=args.sandbox_sha,
            sandbox_stem=args.sandbox_stem,
            note=args.note,
        )
        print(json.dumps({"key": meta["key"], "sha256": meta["sha256"], "parent": meta["parent"]}, indent=2))
        return 0
    source = args.source_label or f"{args.sandbox_stem}@{args.sandbox_sha[:12]}"
    meta = promote_freeze_new(
        role=args.role,
        sandbox_sha=args.sandbox_sha,
        sandbox_stem=args.sandbox_stem,
        source_label=source,
    )
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
