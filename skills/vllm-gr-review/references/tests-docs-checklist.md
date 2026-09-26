# Tests and Documentation Checklist

Use this reference when tests or public behavior change, or when risky runtime
code lacks obvious coverage.

## Build a coverage packet

For each semantic change, record internally:

```text
changed contract and failure risk
  -> existing unit/contract/integration/system coverage
  -> uncovered boundary
  -> smallest stable assertion that closes it
```

The test should fail if the changed behavior is reverted or broken. Check that
it reaches the production dispatcher rather than only a copied helper or mock.

## Route to likely tests

Search the frozen branch; names differ across `main` and development branches.
Common starting points are:

- **Config, CLI, defaults, and versions:** `tests/test_gr_config*.py`,
  `tests/test_attention_backend_*.py`, `tests/packaging/`, and
  `tests/test_runtime_versions.py`.
- **Runtime patches and upstream APIs:** `tests/test_patch_initialization.py`,
  `tests/test_upstream_api_contract.py`, `tests/contract/`, and GPU/NPU
  ModelRunner patch tests.
- **Candidate selection, stops, and logprobs:**
  `tests/test_beam_search_decision_utils.py`, beam CPU/reference/decision tests
  when present, and offline parity tests.
- **Catalog and canonical constraints:** `tests/test_catalog.py`,
  `tests/test_task_specific_catalog_program.py`, `tests/constraints/`, and
  constrained Top-K kernel tests when present.
- **Engine wire/session/DP lifecycle:** `tests/test_engine_core_codec.py`,
  `tests/test_beam_request_unit.py`, `tests/test_dp_beam_request_unit.py`, and
  `tests/test_serving_beam_lifecycle.py`.
- **KV, attention, runner, graph, and reorder:**
  `tests/test_beam_attention_*.py`, worker/runner and prefill graph tests, plus
  beam session/pool/reorder tests when present.
- **Offline/OpenAI end to end:** `tests/test_offline_beam_search.py`,
  `tests/test_serving_beam_search.py`, `tests/test_serving_catalog.py`, and
  system benchmark scripts.
- **Ordinary/Pangu passthrough:** `tests/test_pangu_llm_passthrough.py` and the
  Pangu system and accuracy tests.
- **Metrics and benchmarks:** Prometheus metric tests, `tests/tools/`,
  `tests/system/`, and the base branch's `.github/benchmark-gate.yaml`.

Do not rely only on filename mapping; search for the changed symbols and config
keys. A hardware skip is not a pass.

## Test quality

Verify that assertions pin the contract:

- exact recommendation token IDs/ordering/parents/scores where stable;
- legal-output validity and no illegal constraint fallback;
- correct request/session cleanup and resource release;
- production backend/dispatcher selection;
- ordinary and feature-off behavior for shared patches;
- deterministic seeds, ordering, synchronization, and numeric tolerances;
- invalid, boundary, failure, cancellation, and reuse cases introduced by the
  diff; and
- real device execution for device-specific claims.

Mocks must preserve relevant types, MRO, signatures, return tuples, shapes,
devices, async behavior, and lifecycle ownership. Flag only the one or two test
defects that materially weaken confidence; keep grades/matrices internal.

## CI and local gates

Read the base branch's current workflow and benchmark policy. The broad local
gate is `./tools/run_test.sh`, and the underlying test hook commonly runs the
full `tests/` tree with slow tests enabled. Execute it only when the trusted
environment and resource policy allow; otherwise run narrower static/CPU tests
and record the accelerator/model gap.

The full gate may wait for an accelerator and invokes pre-commit hooks that can
rewrite files. Run it only in an isolated task-owned snapshot, never in the
user's dirty review worktree.

Check CI changes for:

- actual triggering on the PR's target branch;
- fail-closed benchmark-policy resolution from the base branch;
- device/board-specific threshold selection;
- accidental skips, allowlists, or warning-only conversions;
- single-commit/DCO/package-version gates; and
- tests that report success without reaching their claimed backend.

## Documentation sync

Require user-facing docs when the diff changes:

- CLI/API/config keys, defaults, validation, or migration behavior;
- supported hardware, dtype, model, constraint, cache, or attention behavior;
- offline/online examples or response/logprob/metric semantics;
- install pins, extras, wheel selection, or environment requirements; or
- benchmark workloads, metrics, thresholds, or interpretation.

Verify commands, paths, identifiers, defaults, limitations, and output schemas
against live code. Update maintained contract docs when their production
behavior changes. Do not demand implementation of a document that labels
itself prospective; require its status/scope to stay truthful instead.

## Contributor evidence

For reported tests or benchmarks, require enough provenance to evaluate them:
frozen SHA, hardware, relevant software versions, model/data, exact command,
configuration, result, and approximate runtime. Apply
[perf-verification.md](perf-verification.md) to quantitative claims.
