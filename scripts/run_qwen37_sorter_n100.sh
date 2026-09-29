#!/usr/bin/env bash
# Qwen 3.7-Flash sorter (eval:classification) N=100 — same seed-42 full draw as Granite
# (manifest: 20260927T100340Z-eval-classification). Pair with run_deepseek41_sorter_n100.sh.
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
  --model qwen/qwen3.7-flash \
  --require-trace-sink \
  --prompt-source frozen \
  --trace-backend braintrust \
  --concurrency 8 \
  "$@"
