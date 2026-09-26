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
import subprocess
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from evals.prompts import frozen_v1, mutations
from evals.prompts.mirror_md import prompt_mirror_markdown

SANDBOX_REPO = "Exios66/local-mailroom-sandbox"
DEFAULT_SANDBOX_SHA = "97c0f940194f030504db0b49443caf90ce749d79"
DEFAULT_ARCHIVE_REF = "origin/main"
ARCHIVED_MODULE = REPO_ROOT / "src" / "evals" / "prompts" / "archived_production.py"
ARCHIVE_DIR = REPO_ROOT / "prompts" / "archive"
ARCHIVE_MANIFEST = ARCHIVE_DIR / "manifest.json"

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


def _safe_ident(role: str) -> str:
    return role.replace("-", "_")


def _git_show(ref: str, path: str) -> str:
    out = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if out.returncode != 0:
        raise SystemExit(f"git show {ref}:{path} failed: {out.stderr.strip() or out.stdout.strip()}")
    return out.stdout


def load_frozen_from_git(ref: str) -> dict:
    """Exec a historical frozen_v1.py from ``ref``; returns the module namespace."""
    raw = _git_show(ref, "src/evals/prompts/frozen_v1.py")
    ns: dict = {"__name__": "_historical_frozen_v1"}
    exec(compile(raw, f"{ref}:src/evals/prompts/frozen_v1.py", "exec"), ns)
    return ns


def render_archived_module(
    archived: dict[str, tuple[str, str, str]],
    *,
    from_ref: str,
) -> str:
    stamp = datetime.now(UTC).isoformat(timespec="seconds")
    lines = [
        '"""ARCHIVED production specialist prompts — DO NOT EDIT BY HAND.',
        "",
        "Predecessor of the concise frozen v1 specialists. Keys are <role>_v0 so",
        "--prompt-version contracts_specialist_v0 (or --prompt-source archived)",
        "injects the verbose production freeze. Default evals stay on frozen v1",
        "(concise sandbox) for API token budget and modal/vLLM deployment.",
        "",
        f"Archived from git ref {from_ref} by scripts/promote_sandbox_specialist.py.",
        f"Archive stamp: {stamp}",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        f"LINEAGE_ID = {frozen_v1.LINEAGE_ID!r}",
        "ARCHIVED_VERSION = 0",
        "",
    ]
    for role, (text, kind, source_key) in archived.items():
        key = f"{role}_v0"
        ident = _safe_ident(role) + "_v0"
        lines.append(f"# key: {key} — source: {kind}:{source_key} (sha256 {sha256(text)[:12]})")
        lines.append(f"{ident} = {text!r}")
        lines.append("")
    lines.append("VERSIONS: dict[str, str] = {")
    for role in archived:
        lines.append(f"    {role + '_v0'!r}: {_safe_ident(role)}_v0,")
    lines.append("}")
    lines.append("")
    lines.append("SOURCE_OF: dict[str, str] = {")
    for role, (_text, kind, source_key) in archived.items():
        lines.append(f"    {role + '_v0'!r}: {kind + ':' + source_key!r},")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def write_archived_production(
    archived: dict[str, tuple[str, str, str]],
    *,
    from_ref: str,
) -> None:
    ARCHIVED_MODULE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVED_MODULE.write_text(render_archived_module(archived, from_ref=from_ref), encoding="utf-8")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for role, (text, _kind, _source) in archived.items():
        key = f"{role}_v0"
        (ARCHIVE_DIR / f"{key}.md").write_text(prompt_mirror_markdown(key, text), encoding="utf-8")
    manifest = {
        "lineage_id": frozen_v1.LINEAGE_ID,
        "archived_version": 0,
        "archived_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "from_ref": from_ref,
        "note": (
            "Verbose production freeze superseded by concise sandbox frozen v1. "
            "Not the default; use --prompt-source archived or --prompt-version <role>_v0."
        ),
        "versions": {
            f"{role}_v0": {
                "source_kind": kind,
                "source_key": source_key,
                "sha256": sha256(text),
                "chars": len(text),
            }
            for role, (text, kind, source_key) in archived.items()
        },
    }
    ARCHIVE_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def archive_production_specialists(
    *,
    from_ref: str = DEFAULT_ARCHIVE_REF,
    skip_if_exists: bool = True,
) -> dict[str, dict]:
    """Snapshot the pre-concise production specialists as resolvable <role>_v0 keys."""
    if skip_if_exists and ARCHIVED_MODULE.exists() and ARCHIVE_MANIFEST.exists():
        existing = json.loads(ARCHIVE_MANIFEST.read_text())
        return {"skipped": True, "from_ref": existing.get("from_ref"), "versions": existing.get("versions")}

    ns = load_frozen_from_git(from_ref)
    versions: dict[str, str] = ns.get("VERSIONS") or {}
    source_of: dict[str, str] = ns.get("SOURCE_OF") or {}
    archived: dict[str, tuple[str, str, str]] = {}
    for role in CONCISE_SPECIALIST_STEMS:
        key = f"{role}_v1"
        if key not in versions:
            raise SystemExit(f"{from_ref} frozen lineage missing {key!r}")
        prov = source_of.get(key, "production:" + role)
        kind, source_key = prov.split(":", 1) if ":" in prov else ("production", role)
        if kind == "sandbox":
            raise SystemExit(
                f"{from_ref} {key} is already sandbox-sourced ({prov}); "
                "refusing to archive concise text as the production predecessor"
            )
        archived[role] = (versions[key], kind, source_key)
    write_archived_production(archived, from_ref=from_ref)
    return {
        "skipped": False,
        "from_ref": from_ref,
        "versions": {
            f"{role}_v0": {"sha256": sha256(text), "chars": len(text)}
            for role, (text, _kind, _src) in archived.items()
        },
    }


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
    archive_from_ref: str = DEFAULT_ARCHIVE_REF,
    skip_archive_if_exists: bool = True,
) -> dict[str, dict]:
    """Archive production specialists as v0, then freeze concise sandbox text as v1."""
    from scripts.freeze_prompts import write_frozen

    archived_meta = archive_production_specialists(
        from_ref=archive_from_ref,
        skip_if_exists=skip_archive_if_exists,
    )

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
    return {"updated": updated, "archived": archived_meta}


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
        help="archive production specialists as v0, then freeze concise sandbox text as v1",
    )
    upg.add_argument("--sandbox-sha", default=DEFAULT_SANDBOX_SHA)
    upg.add_argument("--archive-from-ref", default=DEFAULT_ARCHIVE_REF)
    upg.add_argument(
        "--rearchive",
        action="store_true",
        help="overwrite an existing archive snapshot (default: leave v0 in place)",
    )

    arc = sub.add_parser(
        "archive-production-specialists",
        help="snapshot pre-concise production specialists as <role>_v0 without changing frozen v1",
    )
    arc.add_argument("--from-ref", default=DEFAULT_ARCHIVE_REF)
    arc.add_argument("--rearchive", action="store_true")

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
    if args.cmd == "archive-production-specialists":
        meta = archive_production_specialists(
            from_ref=args.from_ref,
            skip_if_exists=not args.rearchive,
        )
        print(json.dumps(meta, indent=2))
        return 0
    if args.cmd == "upgrade-frozen-specialists":
        meta = upgrade_frozen_specialists(
            sandbox_sha=args.sandbox_sha,
            archive_from_ref=args.archive_from_ref,
            skip_archive_if_exists=not args.rearchive,
        )
        print(json.dumps({**meta, "sandbox_sha": args.sandbox_sha}, indent=2))
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
