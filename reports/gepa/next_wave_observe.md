# GEPA next wave — OBSERVE inputs (no spend)

Failure exports from the N=50 seed-42 Qwen 3.7 baselines for near-miss specialists. Use with `score_run.py --export-failures` pattern before drafting v5+ mutations.

| Specialist | Baseline run | Manifest (local export) | Notes |
|------------|--------------|-------------------------|--------|
| correspondence | `20260928T052606Z-eval-correspondence` | `data/manifests/gepa_observe_correspondence_v1_n50.jsonl` | v2 CI lo −0.0023 @ N=50; extraction F1 / entity_list dominate failures |
| corporate_records | `20260928T062251Z-eval-corporate_records` | `data/manifests/gepa_observe_corporate_v1_n50.jsonl` | v4 CI lo −0.0064; entity_name + signatories on resolutions |

Manifest paths are gitignored under `/data/manifests`; re-export on any machine with:

```bash
uv run python scripts/score_run.py --run-id 20260928T052606Z-eval-correspondence \
  --export-failures data/manifests/gepa_observe_correspondence_v1_n50.jsonl
uv run python scripts/score_run.py --run-id 20260928T062251Z-eval-corporate_records \
  --export-failures data/manifests/gepa_observe_corporate_v1_n50.jsonl
```

Accepted promotion to carry forward: **`contracts_specialist_v3`** (`20260928T054828Z` → `20260928T063713Z`).
