# vLLM-GR Review Architecture

This is a review map, not a substitute for the frozen branch's code and docs.
vLLM-GR evolves on more than one target branch, so verify every listed path and
contract before applying it.

## Product boundary

vLLM-GR is an inference extension around pinned vLLM APIs for generative
recommendation. Its main behavior is OneRec beam search with optional catalog
or table constraints. It also retains ordinary LLM/Pangu passthrough behavior
and CUDA/NPU adaptations.

The highest-risk boundary is not a single model class. It is the cross-process
chain from public request and GR configuration through patched vLLM internals,
beam/KV state, accelerator execution, and terminal response cleanup.

## Configuration and initialization

Public configuration enters through CLI, offline, or OpenAI surfaces and is
serialized into vLLM configuration for reconstruction in the API server,
EngineCore, and workers.

Review invariants:

- validation rejects invalid combinations before device work begins;
- explicit false/null/user values are not replaced by platform defaults;
- canonical and legacy keys do not produce ambiguous mixed state;
- every process reconstructs the same effective GR configuration; and
- disabled GR features leave ordinary vLLM behavior unchanged.

The plugin and patch layer runs in multiple process roles. Registration,
environment checks, platform activation, compatibility patches, and neutral GR
patches must occur in the intended order. Patch installation should be lazy,
idempotent, observable, and fail-closed when required hooks are missing.

## Beam decision and catalog semantics

Candidate geometry is a core correctness contract. Token IDs, cumulative
scores, logprobs, ranks, decoded tokens, parent indices, request-row offsets,
and candidate caches must remain aligned through masking, stop completion,
selection, materialization, transport, and output reconstruction.

Review invariants:

- the explicit candidate-to-parent mapping is authoritative; do not infer it
  from a fixed block width unless the producer contract guarantees that width;
- catalog filtering masks invalid scores without rewriting token IDs or
  changing candidate order;
- stop/EOS completion happens before active-beam selection when required and
  mutates a score copy rather than corrupting shared input;
- tie/order behavior changes only with an explicit compatibility decision;
- active children preserve the correct prompt, LoRA request, logprob lineage,
  and parent/token fork mapping; and
- terminal, dead-end, max-token, and catalog-fill behavior cannot return an
  illegal or over-budget recommendation.

Offline and OpenAI entrypoints intentionally differ in some stop-token,
output-inclusion, LoRA, metrics, and asynchronous lifecycle details. Require
parity only where the documented contract is shared.

## Constraints

Some branches contain both legacy Trie/catalog filtering and a canonical
constraint artifact/table path. Resolve which live dispatcher is used before
reviewing semantics.

For canonical tables, check:

- schema/version, tokenizer identity, artifact digest, immutable ownership,
  shapes, dtypes, ranges, byte limits, and deterministic loading;
- sorted/monotone lookup structures and the exact prefix-depth/state-machine
  contract;
- explicit validity masks/counts rather than padding or finite-score guesses;
- global versus sliced vocabulary token-ID conversion;
- mathematically correct normalization over legal candidates before Top-K;
- identical resource identity and acknowledgement across TP/DP workers; and
- no silent fallback from an invalid table to a Trie or unconstrained decode.

Direct CUDA/NPU tests must reach the intended backend. A CPU or generic Torch
fallback is useful parity evidence but does not prove device-kernel execution.

## Engine protocol and lifecycle

Grouped beam execution crosses public frontend, EngineCore client, wire codec,
EngineCore process, scheduler metadata, worker, and output processing.

Review invariants:

- wire enum values and array-like field order do not collide or drift;
- request, external request, session, parent, and child identities remain
  correlated across retries and process boundaries;
- DP rank/engine affinity is stable for the whole beam session;
- scheduler metadata reaches the exact request rows it describes;
- a fork applies parent state before the next child write and pruned state is
  released once;
- success, early completion, dead end, abort, cancellation, and exception all
  converge on cleanup; and
- a prospective batch contract is not mistaken for a production protocol
  until ingress, scheduler, worker, and response consumers are actually wired.

## Worker, KV, attention, and graph execution

Beam decoding combines shared prompt KV with divergent suffix state. Review
the ownership of each region rather than assuming an ordinary per-request block
table represents both.

Review invariants:

- GPU and NPU wrappers preserve their distinct pinned upstream signatures and
  return contracts;
- prefill, chunked prefill, decode, speculative decode, mixed ordinary/beam,
  and feature-off paths dispatch deliberately;
- beam width, result width, decode step, request-local offsets, physical rows,
  and logical parents are never conflated;
- reorder happens at the correct step and at most once;
- cache reads stay within initialized valid ranges after lazy reset/reuse;
- attention metadata agrees with KV layout, context lengths, block tables,
  beam bounds, devices, and dtypes;
- graph-captured buffers keep fixed addresses and capacity, while runtime
  scalars are refreshed without allocation or pointer changes; and
- unsupported shape/width/platform combinations take a correct eager fallback
  or fail explicitly.

Kernel validation must cover boundary widths and steps, zero/fewer/more than K
legal candidates, invalid prefixes, temperature edge cases, sliced/global
vocabulary, ties, duplicate/unsorted/shrinking/fan-out parents, and fixed-output
graph variants where those behaviors are supported.

## Upstream and optional integrations

The supported vLLM and vLLM-Ascend versions are part of the runtime contract.
Read them from the frozen branch's package metadata and patch inventory rather
than hard-coding a remembered version.

For every changed monkey patch:

- verify the exact upstream target, descriptor/signature, private fields, and
  return shape at the pinned revision;
- preserve installer ordering, process roles, idempotence, validation, and
  force/reapply behavior;
- update `docs/runtime_patch_inventory.md` and
  `docs/patch_inventory.yaml` together; and
- require a focused upstream-contract or patch-initialization test.

LMCache and accelerator providers are optional boundaries. They must load
lazily, activate only under explicit configuration, use exact canonical device
types, and never silently fall back to CUDA or alter non-integrated requests.

## Observability and passthrough

Metrics are user-visible contracts. Check names, units, labels, denominators,
counter/histogram semantics, request correlation, and whether skipped/failed
requests are counted consistently.

Global GR changes must retain Pangu and ordinary LLM behavior. A passing beam
test is not evidence for passthrough; inspect and run the dedicated path when
patch, scheduler, worker, logits, attention, cache, or packaging behavior is
shared.
