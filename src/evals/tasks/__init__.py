"""Per-node evaluation tasks.

Each module documents its task's contract (what the node decides, which
corpus subset drives it, which scorer family applies). Execution goes through
the shared runner (``evals.runner.run_task``) — these modules exist to keep
task-specific knowledge discoverable and to host any future task-specific
case shaping. The registry (``evals.registry``) is the executable source of
truth.
"""
