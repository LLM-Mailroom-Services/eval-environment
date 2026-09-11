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

__version__ = "0.1.0"
