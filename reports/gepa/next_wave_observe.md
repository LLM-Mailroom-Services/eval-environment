# GEPA next wave — OBSERVE inputs (no spend)

Failure exports from the N=50 seed-42 Qwen 3.7 baselines for near-miss specialists. Use with `score_run.py --export-failures` pattern before drafting v5+ mutations.

| Specialist | Baseline run | Manifest (local export) | Notes |
|------------|--------------|-------------------------|--------|
| correspondence | `20260928T052606Z-eval-correspondence` | `data/manifests/gepa_observe_correspondence_v1_n50.jsonl` | v2 CI lo **−0.0023** @ N=50; 8 vs 7 case wins, 35 ties |
| contracts (v2 cand.) | `20260928T055822Z-eval-contracts` | `data/manifests/gepa_observe_20260928T055822Z-eval-contracts.jsonl` | v2 CI lo **−0.0036** @ N=50; 30 vs 8 case wins — v3 promoted instead |
| corporate_records | `20260928T062251Z-eval-corporate_records` | `data/manifests/gepa_observe_corporate_v1_n50.jsonl` | v4 CI lo −0.0064; entity_name + signatories on resolutions |
| merger (v2 cand.) | `20260928T061548Z-eval-merger_agreement` | `data/manifests/gepa_observe_20260928T061548Z-eval-merger_agreement.jsonl` | v2 negative @ N=50 |

Manifest paths are gitignored under `/data/manifests`; re-export on any machine with:

```bash
uv run python scripts/score_run.py --run-id 20260928T052606Z-eval-correspondence \
  --export-failures data/manifests/gepa_observe_correspondence_v1_n50.jsonl
uv run python scripts/score_run.py --run-id 20260928T062251Z-eval-corporate_records \
  --export-failures data/manifests/gepa_observe_corporate_v1_n50.jsonl
```

Accepted promotion to carry forward: **`contracts_specialist_v3`** (`20260928T054828Z` → `20260928T063713Z`).
