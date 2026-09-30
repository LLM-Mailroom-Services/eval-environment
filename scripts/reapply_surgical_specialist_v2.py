#!/usr/bin/env python3
"""Replace bloated auto-drafted specialist v2 mutations with length-budget edits."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

from pipeline.env import load_env

load_env()

from evals.prompts import mutations
from evals.prompts.lineage import resolve

MUTATIONS_PATH = REPO / "prompts" / "mutations.json"
DROP = {
    "correspondence_specialist_v2",
    "insurance_claims_specialist_v2",
    "contracts_specialist_v2",
}

SPECS = [
    {
        "parent": "correspondence_specialist_v1",
        "new_key": "correspondence_specialist_v2",
        "note": "GEPA: Enron inbox/meeting_request sparse headers — floor confidence when intent/subject clear (N=20 observe).",
        "anchor": (
            "- confidence (number): 0.0–1.0 from evidence in THIS communication "
            "(share of fields found, lowered by uncertainty or truncation). Never default to 0.90 / 0.95."
        ),
        "replacement": (
            "- confidence (number): 0.0–1.0 from evidence in THIS communication "
            "(share of fields found, lowered by uncertainty or truncation). Never default to 0.90 / 0.95. "
            "Enron inbox/meeting_request: if intent and subject_matter are clear, floor 0.60 — sparse nulls are corpus-normal."
        ),
    },
    {
        "parent": "insurance_claims_specialist_v1",
        "new_key": "insurance_claims_specialist_v2",
        "note": "GEPA: CMS DE-SynPUF table rows — read headers/cells, not narrative letter mode (N=20 observe).",
        "anchor": (
            "- Numeric zero (0, 0.0, $0, $0.00) on claimed_amount is a stated amount. "
            "Do not compute totals or convert currencies."
        ),
        "replacement": (
            "- Numeric zero (0, 0.0, $0, $0.00) on claimed_amount is a stated amount. "
            "Do not compute totals or convert currencies. "
            "CMS DE-SynPUF (pde/carrier/inpatient/outpatient): extract from table headers and row values."
        ),
    },
    {
        "parent": "contracts_specialist_v1",
        "new_key": "contracts_specialist_v2",
        "note": "GEPA: cuad_clauses empty on full CUAD bodies — require Parties/date lines when cuad_family set (N=20 observe).",
        "anchor": (
            "- cuad_clauses (string[]): present CUAD categories only, as '<Category>: <short verbatim evidence span>' "
            "using the exact Atticus names below. Omit absent categories. Do not dump open-ended obligation lists. "
            "None present → []."
        ),
        "replacement": (
            "- cuad_clauses (string[]): present CUAD categories only, as '<Category>: <short verbatim evidence span>' "
            "using the exact Atticus names below. Omit absent categories. Do not dump open-ended obligation lists. "
            "When cuad_family is set, include Parties and any stated Agreement/Effective Date lines; [] only for signature-page stubs."
        ),
    },
]


def main() -> int:
    data = json.loads(MUTATIONS_PATH.read_text(encoding="utf-8"))
    kept = [row for row in data.get("mutations", []) if row["key"] not in DROP]
    if len(kept) != len(data.get("mutations", [])) - len(DROP):
        missing = DROP - {r["key"] for r in data.get("mutations", []) if r["key"] in DROP}
        if missing:
            print(f"warning: expected to drop {DROP}, missing keys {missing}")
    data["mutations"] = kept
    MUTATIONS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    for key in DROP:
        path = REPO / "prompts" / f"{key}.md"
        if path.exists():
            path.unlink()

    for spec in SPECS:
        parent = resolve(spec["parent"])
        assert parent.text.count(spec["anchor"]) == 1, spec["parent"]
        meta = mutations.apply_mutation(
            parent_key=spec["parent"],
            new_key=spec["new_key"],
            anchor=spec["anchor"],
            replacement=spec["replacement"],
            note=spec["note"],
        )
        print(f"{spec['new_key']}: net_chars={meta['net_chars']:+d}")

    mutations.render_prompts_mirror()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
