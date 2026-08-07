# vLLM-Omni Support and Optimization Profile

Use this profile only when vLLM-Omni is in scope. Pin the repository revision because model, platform, and performance support changes rapidly.

## Contents

- [Implementation inspection](#inspect-the-implementation-surface)
- [Support matrix](#build-a-multi-axis-support-matrix)
- [Roadmap evidence](#use-roadmap-issues-correctly)
- [Local performance evidence](#use-the-runtime-profiling-surface)
- [Optimization funnel](#optimization-funnel)
- [Prioritization and records](#prioritization)
- [Completion gates](#completion-gates-for-new-model-support)

## Inspect the implementation surface

Locate current paths with `rg`; names can move. Inspect the applicable routes:

1. Supported-model documentation and model-specific recipes.
2. Autoregressive model registry under `vllm_omni/model_executor/models/`, diffusion registry under `vllm_omni/diffusion/`, or multistage pipeline registry under `vllm_omni/config/`.
3. Model metadata, pipeline/stage configuration, task dispatch, weight loading, and feature-compatibility documentation.
4. Input processors, request schema, online API, offline examples, and output postprocessing.
5. Platform implementations under `vllm_omni/platforms/` and backend/operator selection.
6. Unit, contract, end-to-end, accuracy, performance, and hardware-marked CI tests.
7. Merged changes, releases, open work, and roadmap issues.

Use current code and tests to verify roadmap statements. A model name in a registry demonstrates discovery, not task correctness or hardware qualification.

## Build a multi-axis support matrix

Create separate rows for:

- model discovery, configuration, weight loading, and checkpoint variants;
- each advertised modality/task and input combination;
- offline inference and each public serving API;
- output contract, streaming where applicable, and request validation;
- single-device and distributed execution modes;
- each requested hardware backend, with separate rows for materially different NVIDIA or Ascend device families;
- attention backends, compilation, quantization, CPU/layerwise offload, and caching;
- unit/contract tests, end-to-end smoke, accuracy CI, and performance CI;
- continuous batching, concurrency, cancellation/abort, observability, and recovery.

For every row provide implementation state, validation evidence, support status, effective revision, scope/limitation, and evidence IDs. Add `superseded_by` or `reverted_by` when a later change alters the effective path. Do not let a checkmark for one task imply support for all tasks or platforms.

## Use roadmap issues correctly

[MiniMax-H3 issue #5700](https://github.com/vllm-project/vllm-omni/issues/5700) is a useful structure exemplar: it separates feature completeness, usability, performance, production serving, CI, hardware recipes, and task-specific limitations. Re-read the live issue when analyzing MiniMax-H3; do not copy its checkboxes as timeless facts.

Roadmap evidence should answer:

- What gap is claimed?
- Is the referenced PR merged into the pinned revision?
- Which task, API, precision, hardware, and shape does it cover?
- Is there code, a recipe, or recurring CI that independently corroborates it?
- What remains after the narrow item is complete?

## Use the runtime profiling surface

Apply [performance-analysis.md](performance-analysis.md), then inspect the pinned runtime's current profiling documentation, model recipe, benchmark entrypoints, and profiler tests. In current layouts these may include `docs/contributing/profiling.md`, diffusion serving benchmarks, `profiler_config`, `start_profile()` / `stop_profile()`, online `/start_profile` and `/stop_profile` controls, PyTorch trace export, stage timers, and CUDA/Nsight capture. Locate them with `rg`; do not assume paths or flags are stable.

For a vLLM-Omni performance profile:

1. Run a model-specific contract or smoke test before a full-weight profile when one exists.
2. Capture one warm representative request for attribution and separate repeated unprofiled requests for headline latency/variability.
3. Record stage timings, actual denoiser/decode forward counts, rank-local peak allocation/reservation, host transfer/offload, collective activity, and the top kernels or graph breaks.
4. Save trace paths and exact commands in the evidence ledger; profiling artifacts alone do not establish output quality.
5. Repeat the baseline after changing attention backend, compile, quantization, offload, cache, or parallel dimensions, with only one mechanism changed at a time.

On NVIDIA, select the runtime's supported torch-profiler or CUDA/Nsight path. On Ascend, inspect platform hooks and use the compatible CANN/`torch_npu` profiler; a CUDA trace cannot establish NPU bottlenecks. If the target runtime or hardware is unavailable, retain the analysis as static/source-reported and supply the exact target qualification run.

## Optimization funnel

Do not begin with a generic technique list. Use this sequence:

1. Establish reference parity and a representative end-to-end baseline, or state why it could not be run locally.
2. Attribute time and memory by stage and repeated operation using local profile evidence when available.
3. Identify the architecture-specific bottleneck and scaling limit.
4. Check whether vLLM-Omni already exposes the needed abstraction or backend.
5. Separate cross-platform logic from platform-specific kernels.
6. Propose the smallest change and a quality/performance verification plan.
7. Rank it against missing correctness, support, and production gaps.

## Optimization families

Consider a family only when architecture and profiling evidence make it relevant:

| Family | Evidence that motivates it | Typical vLLM-Omni direction | Platform split |
|---|---|---|---|
| Attention and kernels | Long dense/packed sequences dominate | Backend selection, variable-length support, sparse/local attention, fused QKV/RoPE/norm | CUDA and Ascend kernels require separate qualification |
| Quantization | Resident weights or GEMMs dominate memory/time | Online/offline quant config, loader integration, quality tests | FP8/FP4/INT8 support differs by device and operator stack |
| Memory/offload | Weights or stage overlap exceed device memory | CPU offload, layerwise/distributed offload, resident-window tuning, component lifecycle | Transfer engines and pinned memory are platform/topology sensitive |
| Redundant computation/cache | Invariants repeat across steps or requests | Hoist conditioning/masks/embeddings, reference or cross-step cache | Core eligibility can be shared; kernels/storage may differ |
| Operator fusion/compile | Small ops or launch overhead dominate | Regional compile and architecture-specific fusion points | Keep hardware-specific implementations under platform boundaries |
| Parallelism/communication | Per-rank compute falls but collectives dominate | TP, Ulysses/SP, ring, VAE parallelism, fused/packed collectives | Validate topology and backend collective semantics independently |
| Stage separation | Encoder/DiT/VAE or talker/vocoder have different residency/scaling | Stage placement, disaggregation, resource-specific workers | May assign different accelerator types or counts by stage |
| Serving/scheduling | Queueing, single-request batches, or cancellation gaps dominate | Continuous batching, async scheduling, abort propagation, admission control | Mostly runtime-wide, with backend memory/recovery hooks |
| CI/observability | Support exists but regressions are invisible | Accuracy/perf baselines, profiler spans, hardware matrices | Each claimed platform needs recurring coverage or explicit limits |

Architecture-specific examples are hypotheses until profiled. A repeated diffusion loop makes invariant hoisting plausible; a long packed video/audio sequence makes attention and sequence-parallel work plausible; a multi-component pipeline makes lifecycle/offload or stage separation plausible. Verify the exact dependency before proposing a cache: conditioning may be invariant before a joint block while its in-block K/V remains coupled to changing media state. None of these examples proves an optimization is implemented or beneficial.

## Prioritization

Use these default tiers:

- `P0 — correctness/blocker`: reference parity, load failure, wrong output, crash, or missing required task.
- `P1 — support/qualification`: platform recipe, API completeness, accuracy gate, lifecycle behavior, or a severe memory blocker.
- `P2 — measured performance`: a locally profiler-backed optimization with an A/B plan.
- `P3 — exploration`: plausible research direction without target-run evidence.

Score impact and effort only after assigning a tier. Do not allow speculative speedup to outrank a correctness gap.

## Recommendation record

Every optimization row must contain:

| Field | Content |
|---|---|
| Priority/status | P0-P3 and the current implementation state |
| Current gap | Narrow task/platform/workload limitation with evidence |
| Bottleneck | Prefix with `Observed`, `Measured`, `Reported`, `Community-reported`, `Derived`, `Estimated`, or `Hypothesis`, and cite its evidence |
| Change | Mechanism and likely vLLM-Omni component/touchpoint |
| NVIDIA impact | Applicable backend, dependency, and validation |
| Ascend impact | Applicable backend, dependency, and validation |
| Expected result | Directional goal unless measured; no invented percentage |
| Risks/dependencies | Correctness, quality, memory, topology, upstream, or kernel constraints |
| Verification | Use `Workload: baseline=... vs candidate=...; metrics: performance=..., resource=...; repetitions: warmups=N, measured=N; quality gate: pass if ...`. For cold/deterministic checks, replace `warmups=N` with `mode=cold` or `mode=deterministic`. Arm descriptions must differ, and repetitions must follow that exact count grammar. The quality gate must name an output/tensor-to-baseline tolerance, a named quality metric plus threshold, or a concrete media-output contract; generic “succeeds,” “valid,” or performance-only gates are insufficient. |

For every requested platform, include at least one substantive optimization or qualification direction. Use `N/A — <specific reason>` only for an individually inapplicable row; bare `N/A` is insufficient, and an all-`N/A` platform column does not satisfy platform coverage.

## Completion gates for new model support

A decision-ready enablement plan covers:

- registry and checkpoint loading;
- input conversion and task/API contract;
- core model/pipeline implementation;
- single-device reference parity;
- representative end-to-end outputs;
- distributed and hardware-specific validation;
- accuracy and performance baselines;
- recipe and supported-model documentation;
- known limitations and production-readiness gaps.

If the request is a PR review rather than a model analysis, route to the repository's vLLM-Omni review skill instead of treating this profile as a review checklist.
