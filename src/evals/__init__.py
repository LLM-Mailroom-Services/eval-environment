"""mailroom-evals — evaluation tasks, pilot scenarios, and calibration suites
for the llm-mailroom langgraph pipeline.

Task families (``evals.registry``):
- ``eval:<node>``        per-node performance analysis over mailroom-corpus subsets
- ``pilot:<node|chain>`` cheap stratified validation runs before full sweeps
- ``calibration:<node>`` edge-fixture suites that calibrate node decision boundaries

Trace sinks: Braintrust (when BRAINTRUST_API_KEY is set) else local Arize
Phoenix; ``none`` disables. Every run appends to the centralized experiment
log (``evals.experiment_log``).
"""

from pathlib import Path

from dotenv import load_dotenv

# Repo-local .env (gitignored): LLM provider config (e.g. the Vercel AI
# Gateway), sink keys. override=False so real environment variables always
# win; must NOT set OBSERVABILITY_PROVIDER / MAILROOM_BASE_DIR (runner-owned).
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False)

__version__ = "0.3.0"
