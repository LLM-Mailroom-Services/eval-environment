#!/usr/bin/env bash
# DeepSeek v4.1-Flash sorter (eval:classification) N=100 — same draw as Granite/Qwen:
# subset full, sample 100, seed 42 (see 20260927T100340Z-eval-classification manifest).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
export BRAINTRUST_PROJECT="${BRAINTRUST_PROJECT:-Mailroom-Evals}"

exec uv run python -u scripts/run_evals.py \
  --task eval:classification \
  --real \
  --subset full \
  --sample 100 \
  --seed 42 \
  --model deepseek/deepseek-v4.1-flash \
  --require-trace-sink \
  --prompt-source frozen \
  --trace-backend braintrust \
  --concurrency 8 \
  "$@"
