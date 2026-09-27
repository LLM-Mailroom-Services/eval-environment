## 20260926T232547Z-eval-pipeline_chain

| Key | Value |
|---|---|
| family / task | eval / pipeline_chain |
| invoke / mode | node / mock |
| model / prompt | qwen/qwen3.7-flash / None |
| trace backend | none |
| git | commit: 7ec9e59 · dirty: False |
| started / finished | 2026-09-26T23:25:47+00:00 → 2026-09-26T23:25:49+00:00 |
| duration_s | 1.7 |
| error | — |

### Dataset

| Key | Value |
|---|---|
| case_ids | corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… |
| config | Lucius-Morningstar/docclass-pilot |
| filenames | 0001062993-15-000198_s1011515_ex3z2.htm, 0001469709-14-0000… |
| n_selected | 2 |
| n_total | 138 |
| repo | Lucius-Morningstar/docclass-pilot |
| revision | — |
| sample | — |
| seed | 42 |
| split | train+test |
| subset | pilot |
| subset_manifest_jsonl | data/experiments/20260926T232547Z-eval-pipeline_chain/subse… |
| subset_manifest_path | data/experiments/20260926T232547Z-eval-pipeline_chain/subse… |
| subset_spec | kind: corpus · value: pilot |

### Metrics

| Metric | Value |
|---|---|
| class_accuracy | 0.0 |
| errors | 0 |
| n | 2 |
| overall_score | 0.0 |
| scorer_errors | 0 |

### Performance

| Metric | Value |
|---|---|
| cost_usd_est_total | — |
| latency_ms_mean | 193.55 |
| latency_ms_p95 | 225.3 |
| tokens_completion_total | 420 |
| tokens_prompt_total | 780 |

### Per-agent performance

| agent | calls | prompt_tokens | completion_tokens | total_tokens | cost_usd_est | models |
|---|---|---|---|---|---|---|
| sorter | 6 | 720 | 360 | 1080 | 0.0001 | qwen/qwen3.7-flash |
| intake | 4 | 40 | 40 | 80 | — | mock-model |
| sorter_reviewer | 2 | 20 | 20 | 40 | — | mock-model |

### Cases

| case_id | scores | latency_ms | error |
|---|---|---|---|
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001062… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 225.3 | — |
| corpus:Lucius-Morningstar/docclass-pilot:train+test:0001469… | final_stage: review · overall_score: 0.0 · needs_judge_revi… | 161.8 | — |
