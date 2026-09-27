# Pipeline checkout (mailroom path source)

`pyproject.toml` resolves the pipeline under test as an editable sibling:

```toml
mailroom = { path = "../llm-mailroom", editable = true }
```

## Default (local dev + GitHub Actions)

From the repo root:

```bash
bash scripts/ci_bootstrap_pipeline.sh
uv sync --extra dev
```

The bootstrap script clones `Exios66/llm-mailroom` at the pinned SHA into `../llm-mailroom`.

## Cloud agents (repo parent not writable)

When `../llm-mailroom` cannot be created (read-only parent), use an in-repo monorepo slice:

```bash
git clone --depth 1 https://github.com/LLM-Mailroom-Services/Digital-Mailroom.git Digital-Mailroom
```

Temporarily point `[tool.uv.sources].mailroom` at `Digital-Mailroom/packages/llm-mailroom` for `uv sync` on that machine only. Do not commit that path override — `Digital-Mailroom/` is gitignored.

## OpenRouter + Braintrust preflight (handoff)

- Eval task modules + preflight: merged on `main` (see `src/evals/tasks/`, `src/evals/preflight.py`).
- Braintrust LangChain spans: `input.messages` with `{role, content}` and trace truncation (`src/evals/tracing.py`).

Await the handoff plan before full `--real` sweeps.
