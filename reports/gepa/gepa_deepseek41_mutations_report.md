# DeepSeek v4.1 Flash × GEPA best mutations (N=20, seed 42)

**Model:** `deepseek/deepseek-v4.1-flash` (OpenRouter)  
**Baselines:** frozen v1 specialist prompts (2026-09-27 Leg B runs, same seed-42 draw)  
**Accept rule:** paired `overall_score`, bootstrap **CI lo > 0**

## Results

| Specialist | Mutation | Δ mean | CI lo | CI hi | Accepted |
|------------|----------|--------|-------|-------|----------|
| corporate_records | `corporate_records_specialist_v2` | +0.0209 | **+0.0006** | +0.0402 | **Yes** |
| merger_agreement | `merger_agreement_specialist_v2` | +0.1861 | −0.0525 | +0.4216 | No (wide CI @ N=20) |
| contracts | `contracts_specialist_v3` | +0.1082 | −0.0354 | +0.2551 | No (wide CI @ N=20) |
| correspondence | `correspondence_specialist_v2` | −0.0172 | −0.0453 | +0.0034 | No |
| insurance_claims | `insurance_claims_specialist_v2` | −0.0062 | −0.0166 | +0.0026 | No |

## Takeaways

- **Corporate v2** (signatories `[]` not null) **accepts on DeepSeek** where Qwen N=50 stayed negative — model–mutation interaction matters.
- **Merger v2** and **contracts v3** show **large positive means** on DeepSeek (+0.19 / +0.11) but **N=20 CIs still cross zero**; N=50 would be the natural follow-up if budget allows.
- **Correspondence v2** confidence-floor guidance **does not transfer** to DeepSeek on this draw (slight regression).

Compare artifacts: [reports/gepa-comparisons/deepseek-v4.1-flash/](../gepa-comparisons/deepseek-v4.1-flash/README.md)
