# Snapshot-aware architecture

Verified 2026-10-02 Asia/Shanghai. This is a source map, not a claim that every
listed behavior has been executed or shipped. Refresh exact refs on each review.

## Main and integration are different

- [Main 82eb79a](https://github.com/ThinkFlowLab/nanodot/commit/82eb79a241a024005416ee8053099e6a0ddab5cb)
  contains the scaffold from PR #15 and adapter-seam design from PR #16. Source
  consists of CLI, paths, package version, and empty core/native/ports initializers.
  It does **not** contain implemented watcher protocol types or the MVP loop.
- [PR #28](https://github.com/ThinkFlowLab/nanodot/pull/28) was open and unmerged at
  [661f4bae](https://github.com/ThinkFlowLab/nanodot/commit/661f4bae106e9f9718137812a803020b8954acc8).
  PRs #17–27 merged into stacked feature-branch bases, not main. Their merged flag
  does not establish release/main availability.
- The public releases collection was empty. Do not infer tag absence or a release
  version. The PR body and historical safety-validation notes contain older test
  counts; only exact-head runs support current verification claims.

Main declares Python >=3.11, setuptools, pytest>=8, and `nanodot.cli:main`.
[CI](https://github.com/ThinkFlowLab/nanodot/blob/82eb79a241a024005416ee8053099e6a0ddab5cb/.github/workflows/ci.yml)
uses Python 3.12, editable dev installation, then pytest. Its
[five scaffold tests](https://github.com/ThinkFlowLab/nanodot/blob/82eb79a241a024005416ee8053099e6a0ddab5cb/tests/test_scaffold.py)
cover import boundary, version/module CLI and isolated data-home behavior. The AST
boundary disallows native/third-party imports in core but allows other `nanodot.*`;
it is not a stronger proof that core imports only ports.

The [adapter-seam design](https://github.com/ThinkFlowLab/nanodot/blob/82eb79a241a024005416ee8053099e6a0ddab5cb/docs/design/adapter-seam.md)
is intended architecture. Verify implementation rather than treating it as shipped.

## Integration-only map (661f4bae)

All paths below resolve under the pinned
[integration tree](https://github.com/ThinkFlowLab/nanodot/tree/661f4bae106e9f9718137812a803020b8954acc8).

| Boundary | Actual implementation |
| --- | --- |
| Composition | `cli.py` wires stores/ports and validates fixed scope; `_run_runner` holds a lifetime RunnerLease before wiring |
| Snapshot | `ports/github.py` defines CheckRun, RequiredCheck, Snapshot and typed errors; `native/github_client.py` performs GET-only paginated head-pinned reads |
| Deterministic decision | `core/github_eval.py` evaluates required success separately from observed failure; `core/statemachine.py` generates transitions/events with persisted occurrence sequence |
| Durable task loop | `core/tasks.py` owns SQLite task scope/lifecycle; `core/runner.py` reloads scope/state before delivery, handles blockers/backoff, notifies before checkpoint and persists terminal state before optional memory |
| Scheduler control | `native/daemon.py` isolates task failures and checks stop before each task; `native/runner_control.py` uses flock and token-specific stop/readiness ownership, not PID alone |
| Delivery | `native/notifier.py` owns SQLite inbox/event-key dedup and best-effort OS popup; persistence is actually here despite broader design wording |
| Safety and optional inference | core permissions/egress/config/redaction/memory plus native secrets/http/inference adapters; anonymous mode must not read/send saved credentials; summary failure cannot determine watcher truth |

## Locate tests by symbols

- Evaluator/transitions: `tests/test_github.py`, `test_statemachine.py`
- Store/scope: `test_tasks.py`, `test_scope_lifecycle_safety.py`
- Loop/retry/stop: `test_runner.py`, `test_daemon_resilience.py`, `test_runner_control.py`
- Inbox/replay: `test_notifier.py`, `test_first_use_demo.py`
- Real CLI: `test_cli.py`, `test_public_mode.py`; eight fake-HTTP/real-CLI scenarios
  live in `examples/first_pr_watch.py`
- Safety: `test_secrets.py`, `test_http_transport.py`, `test_inference.py`,
  `test_production_safety.py`, `test_permissions.py`, `test_memory.py`
- Whole flow and boundaries: `test_e2e.py`, `test_offline.py`, `test_scaffold.py`

Use an isolated home, installed declared dependencies and the target's offline
fixture configuration. Integration `tests/conftest.py` blocks in-process sockets
and DNS; dead proxies propagate to subprocesses. This is a tripwire, not an OS
network sandbox. Do not put dead proxies on dependency-install/checkout steps.
