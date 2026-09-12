#!/usr/bin/env python3
"""Prompt Engineer — DRAFT-phase mutations for the mailroom-evals lineage.

The DRAFT step of the GEPA iteration loop (arXiv 2507.19457): given a
failed-eval manifest (``score_run.py --export-failures``), decompose the
misses into clusters, then have an LLM propose ONE surgical ``.replace()``
mutation per invocation under strict mechanical validation:

    OBSERVE (failure manifest) -> DECOMPOSE (clusters + evidence)
    -> DRAFT (LLM proposal as JSON) -> VALIDATE (the four gates)
    -> APPLY (persist to prompts/mutations.json + registry)

Validation gates (a proposal failing any gate is rejected, never applied):
    1. ANCHOR  — anchor substring occurs EXACTLY ONCE in the parent prompt
    2. KEY     — new key unused + lineage naming (<role>_v<parent.version+1>)
    3. ADDITIVE— parent text preserved outside the anchor span
    4. METADATA— parent + change note recorded

The tool never runs the A/B itself; it prints the exact runner command
(one rule per iteration → one A/B per mutation):

    uv run python scripts/run_evals.py --task eval:classification --real \
        --subset class:contract --sample 50 --seed 42 --prompt-version sorter_v2

Usage:
    uv run python scripts/prompt_engineer.py --manifest <failures.jsonl> --dry-run
    uv run python scripts/prompt_engineer.py --manifest <failures.jsonl> \
        --parent sorter_v1 --focus insurance_claim --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.env import load_env

load_env()

from evals.prompts import mutations
from evals.prompts.lineage import resolve

META_SYSTEM = """You are the Prompt Engineer for a legal-document classification \
prompt program. You follow a strict iteration doctrine:

- ONE rule per mutation. Never bundle unrelated fixes.
- Mutations are surgical .replace() edits on the parent prompt: you return an \
ANCHOR (a verbatim substring of the parent, occurring exactly once) and its \
REPLACEMENT (anchor preserved plus your insertion/edit).
- Every rule carries: the concrete failure evidence it addresses (filename, \
GT vs prediction), the mechanism, a scope guard against over-firing, and \
where possible a worked example.
- Prefer corpus-convention rules ("the ground truth follows the folder") over \
legal reasoning when the misses follow a labeling convention.
- Known GT artifacts are NOT prompt-fixable: say so and skip.
- Counterfactual discipline: name what your rule could break on OTHER corpora \
and add the carve-out preemptively.

Return ONE JSON object: {"anchor": "...", "replacement": "...", "note": "why + mechanism + scope guard", "skipped": null | "reason the failure is not prompt-fixable"}"""


def load_manifest(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def decompose(rows: list[dict], *, focus: str | None = None) -> dict:
    """Cluster the failures: by expected class, by miss type, by frequency."""
    if focus:
        rows = [r for r in rows if r.get("expected_doc_class") == focus]
    by_class = Counter(str(r.get("expected_doc_class") or "?") for r in rows)
    by_error = Counter(
        "runtime_error" if r.get("error") else
        "low_score" if isinstance((r.get("scores") or {}).get("overall_score"), (int, float))
        else "decision_miss"
        for r in rows
    )
    examples = defaultdict(list)
    for row in rows[:200]:
        key = str(row.get("expected_doc_class") or "?")
        if len(examples[key]) < 5:
            examples[key].append({
                "filename": row.get("filename"),
                "expected": row.get("expected_doc_class"),
                "predicted": (row.get("prediction") or {}).get("doc_type"),
                "scores": row.get("scores"),
            })
    return {"n_failures": len(rows), "by_class": dict(by_class), "by_type": dict(by_error), "examples": dict(examples)}


def draft_proposal(clusters: dict, parent_key: str) -> dict | None:
    """One LLM mutation proposal (real mode). Mock mode returns None (the
    caller prints the clusters + the manual proposal shape)."""
    try:
        from llm.client import get_llm

        client, model = get_llm("judge")
        parent = resolve(parent_key)
        user = json.dumps({
            "parent_key": parent_key,
            "parent_tail": parent.text[-3000:],
            "failure_clusters": clusters,
        }, default=str)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": META_SYSTEM}, {"role": "user", "content": user}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        return json.loads(response.choices[0].message.content or "{}")
    except Exception as exc:
        print(f"  draft proposal failed ({type(exc).__name__}: {exc}) — clusters only")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", required=True, help="failure manifest (score_run.py --export-failures)")
    parser.add_argument("--parent", default="sorter_v1", help="parent version key to mutate")
    parser.add_argument("--focus", default=None, help="restrict clustering to one expected class")
    parser.add_argument("--apply", action="store_true", help="validate + persist the proposal (default: dry-run)")
    args = parser.parse_args()

    rows = load_manifest(Path(args.manifest))
    clusters = decompose(rows, focus=args.focus)
    print(f"failures: {clusters['n_failures']} | by class: {clusters['by_class']} | by type: {clusters['by_type']}")

    proposal = draft_proposal(clusters, args.parent)
    if proposal is None:
        print("\n(no LLM proposal — feed the clusters above to the prompt-engineer subagent,")
        print(" or re-run with OPENROUTER_API_KEY set for the real DRAFT call)")
        return 0
    if proposal.get("skipped"):
        print(f"skipped (not prompt-fixable): {proposal['skipped']}")
        return 0

    parent = resolve(args.parent)
    new_key = f"{args.parent.rsplit('_v', 1)[0]}_v{parent.version + 1}"
    print(f"\nproposal: {args.parent} → {new_key}")
    print(f"  note: {proposal.get('note')}")
    try:
        if args.apply:
            meta = mutations.apply_mutation(
                parent_key=args.parent, new_key=new_key,
                anchor=proposal["anchor"], replacement=proposal["replacement"],
                note=proposal.get("note", ""),
            )
            mutations.render_prompts_mirror()
            print(f"  APPLIED → {meta['sha256'][:12]} (prompts/{new_key}.md)")
        else:
            mutations.validate_mutation(
                parent_key=args.parent, new_key=new_key,
                anchor=proposal["anchor"], replacement=proposal["replacement"],
                note=proposal.get("note", ""),
            )
            print("  gates PASS (dry-run — add --apply to persist)")
    except mutations.MutationError as exc:
        print(f"  REJECTED: {exc}")
        return 1

    print(f"\nnext A/B (one rule per iteration):\n"
          f"  uv run python scripts/run_evals.py --task eval:<task> --real \\\n"
          f"      --prompt-version {new_key} --subset <same-as-baseline> --seed <same>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
