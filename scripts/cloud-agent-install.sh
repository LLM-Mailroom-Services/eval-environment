#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for mailroom-evals.
# Installs uv, checks out the pipeline path source declared in pyproject.toml,
# and syncs the locked environment. Safe to re-run.
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
fi
export PATH="/usr/local/bin:${PATH}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

eval "$(python3 - <<'PY'
import tomllib
from pathlib import Path

root = Path.cwd()
with (root / "pyproject.toml").open("rb") as handle:
    spec = tomllib.load(handle)
rel = Path(spec["tool"]["uv"]["sources"]["mailroom"]["path"])

# Two layouts are in tree history:
# - this branch: Digital-Mailroom/packages/llm-mailroom (workspace member)
# - main: ../llm-mailroom (standalone Exios66/llm-mailroom clone)
if "Digital-Mailroom" in rel.parts:
    dest = root / "Digital-Mailroom"
    url = "https://github.com/LLM-Mailroom-Services/Digital-Mailroom.git"
    # main @ 2026-09-24, mailroom 0.7.1 + workspace llm-dojo-scoring 0.15.0
    pin = "e5eeac603edf27f9fe4f306cf086aa9c31965d9a"
else:
    dest = (root / rel).resolve()
    url = "https://github.com/Exios66/llm-mailroom.git"
    # main @ 2026-09-24, mailroom 0.7.1 with dojo git pin v0.15.0
    pin = "28cb4be816fbb60e56cd3bb2ab72f8d9be1ab636"

print(f"DEST={dest}")
print(f"URL={url}")
print(f"PIN={pin}")
PY
)"

if [[ ! -d "${DEST}/.git" ]]; then
  mkdir -p "$(dirname "${DEST}")"
  git clone --depth 1 "${URL}" "${DEST}"
fi

head="$(git -C "${DEST}" rev-parse HEAD)"
if [[ "${head}" != "${PIN}" ]]; then
  git -C "${DEST}" fetch --depth 1 origin "${PIN}"
  git -C "${DEST}" checkout --detach "${PIN}"
fi

echo "pipeline checkout: $(git -C "${DEST}" rev-parse HEAD) at ${DEST}"
uv sync --extra dev --frozen
uv run python -c 'import evals, pipeline; print("imports ok", pipeline.__file__)'
