# vLLM-GR Blocker Patterns

Use these as proof prompts, not automatic findings. Report a pattern only when
the frozen diff introduces or exposes a reachable trigger, impact, and fix.

## Candidate geometry drift

High-risk signals:

- parent indices reconstructed from `candidate_index // K` after pruning or
  variable-width candidate generation;
- token, score, rank, decoded-token, or cache arrays sliced/deduplicated with
  different indices;
- global prefix sums consumed as request-local row offsets;
- `result_width`, beam width, candidate width, or decode step reused as if
  interchangeable; or
- sampled-token dedup applied to a constrained block with a different producer
  contract.

Prove the smallest variable-width, pruned, duplicated, or multi-request input
that selects the wrong parent/token/score or indexes the wrong row.

## Catalog or constraint semantic broadening

Block when invalid state silently becomes less restrictive or more restrictive:

- invalid catalog/artifact/tokenizer/digest data falls back to unconstrained
  decoding;
- masking rewrites IDs/order instead of only validity/scores;
- padding sentinels or large negative values are treated as validity;
- normalization happens over illegal candidates before masking;
- sliced-vocabulary local IDs leak into global output IDs, or vice versa;
- a fixed-depth table is applied to a Trie contract of arbitrary depth; or
- a truncated generated table is accepted as complete.

Require invalid-input tests plus a legal-output parity case. For device code,
confirm the intended kernel ran rather than a CPU fallback.

## Session, transport, and cleanup leaks

Look for:

- wire enum collisions, field-order drift, or decoder acceptance of malformed
  widths/IDs/arrays;
- a session registered before all later failure paths acquire cleanup;
- DP routing recomputed mid-session;
- parent/child state forked after a write that should have used reordered
  state;
- pruned requests, output queues, BeamAttention state, or KV resources retained
  after success, dead end, abort, cancellation, or exception; or
- self-advance/worker-decision results both applied locally and resent through
  a legacy frontend update.

Trace one complete success and one failure/cancellation path across all owning
processes. A `finally` in the frontend is insufficient if EngineCore or worker
state has a separate owner.

## KV, reorder, and graph state corruption

High-risk signals:

- reuse/reset leaves readable stale suffix or decision-buffer values;
- reorder is skipped, repeated, or valid only for sorted full-width parents but
  is used for shrinking, unsorted, duplicate, or fan-out mappings;
- captured tensors resize, allocate, or change `data_ptr()` during replay;
- runtime scalar/device metadata is frozen at capture time;
- eager fallback uses different row geometry or output ordering; or
- mixed ordinary/beam or speculative paths enter a beam-only graph/kernel.

These are usually P1 because they can return plausible but wrong
recommendations. Require a deterministic CPU/reference comparison and real
accelerator evidence when the defect depends on a device implementation.

## Upstream patch drift

Block when a required patch can partially install or target the wrong upstream
contract:

- descriptor/signature/return tuple changed at the pinned upstream revision;
- validation checks presence but not identity or required companion hooks;
- repeated initialization double-wraps a method or mutates global state twice;
- import-time hardware selection loads both CUDA and NPU stacks;
- unknown backend or missing optional integration silently falls back to CUDA;
- patch order differs across main, EngineCore, and worker processes; or
- code changes a private dependency without updating both patch inventories
  and a contract test.

Do not compare only with the reviewer's installed package. Resolve the exact
version/revision supported by the frozen branch.

## Feature-off and passthrough regression

Global changes require an explicit ordinary path. Flag:

- GR config defaults enabling beam/constraint/attention behavior unexpectedly;
- a scheduler/runner wrapper assuming every request has beam metadata;
- sampling/logits reshaping applied to ordinary requests;
- Pangu or standard LLM requests routed through CUSTOM attention; or
- optional LMCache/platform code imported or activated with no opt-in.

Prove the issue with the smallest GR-disabled request or dedicated Pangu path,
not by requesting broad unrelated model coverage.

## CUDA/NPU divergence hidden by tests

A mock or CPU fallback can preserve shapes while missing the real ABI. Treat as
a finding when changed code claims device support but:

- imports or calls `torch.cuda` directly in shared code despite repository
  platform guards;
- CUDA and NPU runner tuple shapes or hook locations are assumed identical;
- unsupported dtype/layout/width silently selects a wrong kernel;
- NPU/CUDA-specific tests skip before reaching the changed symbol; or
- a test monkeypatches away the production dispatcher, resource injection,
  synchronization, or cleanup being claimed.

Missing hardware is a validation gap unless static code proves an invalid
dispatch or ABI.

## Error, async, and security contracts

Look for broad exception swallowing, blocking work in async serving, unsafely
shared mutable request state, unbounded retries/timeouts, user-controlled paths
or shell commands, insecure deserialization, secret logging, and error
responses that expose internals.

For expected invalid requests, require early actionable errors without leaving
partial session/device state. For unexpected runtime faults, preserve causal
context and terminal cleanup; do not turn corruption into a warning and
continue.

## Test and documentation evidence

A missing test is actionable when it leaves changed high-risk behavior
unprotected. Prefer:

- a regression test that fails on the frozen base for a bug fix;
- a contract test for wire/config/patch/schema changes;
- a reference/parity test for beam decisions and kernels; and
- a production-dispatch test for lifecycle or backend routing.

Do not accept `no crash`, non-null output, or a mocked helper call as proof of
correct recommendation IDs, ordering, scores, cleanup, or device execution.
