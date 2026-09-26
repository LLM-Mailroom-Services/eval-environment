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

# Frozen v1 extraction specialists — concise sandbox stems @ DEFAULT_SANDBOX_SHA
# (local-mailroom-sandbox PR #33 lineage; eval-environment #4).
CONCISE_SPECIALIST_STEMS: dict[str, str] = {
    "contracts_specialist": "contracts_specialist_v33_simplified",
    "corporate_records_specialist": "corporate_records_specialist_simplified",
    "correspondence_specialist": "correspondence_specialist_simplified",
    "insurance_claims_specialist": "insurance_claims_specialist_simplified",
}


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


def upgrade_frozen_specialists(
    *,
    sandbox_sha: str = DEFAULT_SANDBOX_SHA,
) -> dict[str, dict]:
    """Replace frozen v1 extraction specialist prompts with sandbox concise text."""
    from scripts.freeze_prompts import write_frozen

    frozen: dict[str, tuple[str, str, str]] = {}
    for key, text in frozen_v1.VERSIONS.items():
        role = key.rsplit("_v1", 1)[0]
        prov = frozen_v1.SOURCE_OF[key]
        kind, source_key = prov.split(":", 1)
        frozen[role] = (text, kind, source_key)

    updated: dict[str, dict] = {}
    for role, stem in CONCISE_SPECIALIST_STEMS.items():
        if role not in frozen:
            raise SystemExit(f"frozen role missing: {role!r}")
        new_text = fetch_sandbox_prompt(sandbox_sha, stem)
        label = f"{stem}@{sandbox_sha[:12]}"
        frozen[role] = (new_text, "sandbox", label)
        updated[role] = {"key": f"{role}_v1", "sha256": sha256(new_text), "chars": len(new_text)}

    write_frozen(frozen)
    return updated


def promote_freeze_new(
    *,
    role: str,
    sandbox_sha: str,
    sandbox_stem: str,
    source_label: str,
) -> dict:
    from scripts.freeze_prompts import write_frozen

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
    write_frozen(frozen)
    key = f"{role}_v1"
    mirror = REPO_ROOT / "prompts" / f"{key}.md"
    mirror.write_text(prompt_mirror_markdown(key, new_text), encoding="utf-8")
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

    upg = sub.add_parser(
        "upgrade-frozen-specialists",
        help="replace all frozen v1 extraction specialists with sandbox concise prompts",
    )
    upg.add_argument("--sandbox-sha", default=DEFAULT_SANDBOX_SHA)

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
    if args.cmd == "upgrade-frozen-specialists":
        meta = upgrade_frozen_specialists(sandbox_sha=args.sandbox_sha)
        print(json.dumps({"updated": meta, "sandbox_sha": args.sandbox_sha}, indent=2))
        return 0
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
