#!/usr/bin/env bash
# Granite sorter (eval:classification) N=100 — mirrors API-leg run
# 20260927T070900Z-eval-classification (N=20, concurrency 8, frozen sorter_v1).
# Draw: --subset full --sample 100 --seed 42 → stratified_sample on
# expected_doc_class (even round-robin across the five doc classes, shuffled
# within each class — same harness as specialist subset draws).
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
  --model ibm-granite/granite-4.2-8b \
  --decode-profile granite-4.2-8b \
  --require-trace-sink \
  --prompt-source frozen \
  --trace-backend braintrust \
  --concurrency 8 \
  "$@"
