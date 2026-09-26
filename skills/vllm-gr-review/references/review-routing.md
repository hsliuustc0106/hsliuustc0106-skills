# Review Routing

Route from changed behavior, not only filenames or title prefixes. Select the
smallest applicable set of checks, then read the live producer and consumer.

## Primary areas

### Configuration and entrypoints

Paths: `vllm_gr/config/`, `vllm_gr/engine/arg_utils_gr.py`, and
`vllm_gr/entrypoints/`.

Check that CLI/API/offline inputs validate once, preserve explicit defaults,
and round-trip through `additional_config` to every process. Keep offline and
OpenAI behavior aligned only where their contracts match.

### Beam decisions and catalog

Paths: `vllm_gr/beam_search_decision_utils.py`,
`vllm_gr/utils/catalog.py`, `vllm_gr/sampling_params.py`, and
`vllm_gr/logprobs*`.

Check token IDs, scores, ranks, decoded tokens, parents, and deferred logprob
lineage. Preserve stop, catalog-terminal, pruning, fill, and LoRA semantics.

### Canonical constraints

Paths when present: `vllm_gr/constraints/` and
`vllm_gr/v1/worker/constraint_hook.py`.

Check artifact/table schemas, digests, tokenizer identity, dtypes, ranges,
validity, worker injection, and CPU/CUDA/NPU semantics. Fail closed.

### Beam sessions and worker decisions

Path when present: `vllm_gr/v1/beam/`.

Check session state, result widths, parent mappings, reorder timing, divergent
suffix KV, fixed-capacity buffers, and worker-decision fallbacks. Treat passive
or prospective batch contracts as non-production until a live dispatcher
consumes them.

### Engine protocol and lifecycle

Path: `vllm_gr/v1/engine/`.

Check wire values and field order, request/session identities, output queues,
DP affinity, scheduler metadata, aborts, and terminal cleanup across processes.

### ModelRunner integration

Path: `vllm_gr/v1/worker/`.

Check exact upstream GPU/NPU signatures, return shapes, request-row mappings,
ordinary requests, speculative/chunked paths, and sampling/logprob geometry.

### Attention, operations, and platforms

Paths: `vllm_gr/v1/attention/`, `vllm_gr/ops/`, and
`vllm_gr/platforms/`.

Check shapes, layouts, devices, dtypes, beam bounds, block tables, graph
buffers, capability checks, and eager fallbacks on the real backend.

### Plugin, patches, and integrations

Paths: `vllm_gr/plugin.py`, `vllm_gr/patch.py`, `vllm_gr/_env_check.py`,
`vllm_gr/v1/ascend_compat.py`, and `vllm_gr/lmcache_patch.py`.

Check ordered process-local initialization, lazy imports, idempotence,
fail-closed validation, pinned upstream compatibility, and both patch
inventories.

### Metrics and benchmarks

Paths: `vllm_gr/v1/metrics/`, `benchmarks/`, and
`.github/benchmark-gate.yaml`.

Check units, labels, denominators, timing scopes, quality gates, and
branch-aware base/head comparisons.

### Packaging and CI

Paths: `setup.py`, `pyproject.toml`, `requirements/`, and CI workflows.

Check device selection, pinned versions, wheel metadata, Python support,
dependency extras, and clean-install behavior.

## Required overlays

Apply these in addition to the primary area when relevant:

- **Ordinary-path overlay:** any global patch, scheduler, worker, sampling,
  logits, attention, cache, or config change must preserve GR-disabled and
  Pangu passthrough behavior.
- **Cross-platform overlay:** shared code must be checked against both CUDA and
  NPU contracts; platform-specific code needs an explicit unsupported or eager
  fallback rather than accidental import-time selection.
- **Constraint overlay:** distinguish legacy Trie/catalog filtering from the
  canonical artifact/table backend present on some branches. Do not assume one
  silently falls back to the other.
- **Lifecycle overlay:** any request/session/beam state change must cover
  success, early terminal/dead end, abort, cancellation, exception, and server
  shutdown where applicable.
- **Performance/accuracy overlay:** load
  [perf-verification.md](perf-verification.md) for quantitative or optimization
  claims.
- **Public-contract overlay:** load
  [tests-docs-checklist.md](tests-docs-checklist.md) for CLI/API/config/default,
  supported-platform, example, or benchmark-policy changes.

## Branch-local contract resolution

Use documentation from the frozen base/head, especially when present:

- `docs/runtime_patch_inventory.md` and `docs/patch_inventory.yaml`;
- `docs/platform_backend_contract.md`;
- `docs/beam_search_decision_helper_contract.md`;
- `docs/beam_search_metrics.md`; and
- `docs/beam_batch_execution_contract.md`.

Read each document's status and scope. In particular, do not require current
runtime code to implement a document that explicitly describes a prospective
or passive contract. Conversely, when a production contract changes, require
its maintained docs and machine-readable inventory to change with it.
