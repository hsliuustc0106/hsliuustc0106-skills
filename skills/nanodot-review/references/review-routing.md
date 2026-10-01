# Review routes

Route by changed code and call graph, not title prefix alone. At the pinned main,
only the package scaffold, empty core/native/ports package initializers, tests,
and design documents exist.
Resolve each listed path against the target before loading integration guidance.

| Changed area | Trace and test |
| --- | --- |
| `src/nanodot/ports/`, contract docs | Structural protocols, immutable evidence, exception semantics, compatibility with both native and alternate adapters |
| `src/nanodot/core/github_eval.py`, `statemachine.py` | Required-check knowledge versus observed failure; current head; latest attempts; event precedence; fail closed on incomplete evidence |
| `src/nanodot/core/runner.py`, `tasks.py`, `native/daemon.py`, `native/runner_control.py`, `cli.py` | Validate/reload scope, cancellation while fetching, no next task after stop, backoff, terminal state, crash/replay |
| `src/nanodot/core/permissions.py`, `egress.py`, `native/github_client.py`, `native/http.py`, `native/secrets_file.py` | Exact grant/action/resource, redirection, pagination, token leakage, revocation and expiry at execution boundary |
| `src/nanodot/core/activity.py`, `native/notifier.py`, `paths.py`, task persistence | Atomic writes, activity replay, stable notification identity, delivery-before-terminal ordering |
| `src/nanodot/core/memory.py`, `redaction.py`, `native/inference_api.py` | Secret filtering, expiry, provenance, bounded optional summaries, inference cannot determine watcher truth |
| `tests/`, `.github/workflows/`, `pyproject.toml`, demos | Assertions, offline/online separation, clean environment, packaging, real first-use paths |
| `docs/`, README, config only | Claims against current code/accepted contract; executable commands; migration impact, not speculative runtime faults |

For mixed diffs, union the relevant routes and inspect their seams. Do not require
all references for a small documentation fix. Detailed nanodot review does not
activate Omni, GPU, diffusion, model-addition, or unrelated deployment guidance.

A test-only change still needs a correctness review of setup, assertions and
failure sensitivity. A design-only main change can break a port contract, but
must not be reported as a production-runtime regression without implementation.

Unmapped source paths require context inspection; never silently drop them merely
because they share the `src/nanodot/` prefix with a known area.
