# Inference Performance Analysis

Use this reference for every report. A useful analysis combines architecture-derived cost with the cheapest local evidence that can change a decision. Local execution remains conditional: an expensive end-to-end run is not required when the model, target hardware, execution budget, or performance question does not justify it.

## Contents

- [Evidence decision](#choose-an-evidence-path)
- [Local execution](#use-local-tests-and-profiling)
- [Workload contract](#freeze-the-workload-contract)
- [Cost model](#build-an-operation-level-cost-model)
- [Optimization dimensions](#cover-the-required-optimization-dimensions)
- [Measurement protocol](#measurement-protocol)
- [Reporting](#reporting-requirements)

## Choose an evidence path

Inspect local state before asking the user: repository revisions, checkpoint completeness, accelerator type/count/free memory, active workloads, installed environments, and available profiler or benchmark entrypoints. Then select the highest useful path that is safe and feasible:

| Path | Use when | Required output |
|---|---|---|
| Static analysis | No compatible runnable environment exists, or code/configuration answers the question | Exact formulas, cited inputs, assumptions, sensitivity, and the run needed to validate the result |
| Local test | Shapes, dispatch, correctness, memory feasibility, or one operator can be checked cheaply | Exact command, pass/fail or measured result, environment, and artifact/log |
| Local profile | Bottleneck ordering or an end-to-end performance conclusion affects the recommendation | Representative trace or stage profile, repeated latency/memory results, and a quality gate |
| Source measurement | A primary source reports the exact workload but it is not reproduced locally | Source environment and workload, reported result, transfer limits, and a separate local-run decision |
| Community measurement | A third party reports a useful result that is not reproduced locally | Exact available scope, missing environment/workload fields, lower confidence, transfer limits, and a separate local-run decision |

Use local tests or profiling when all required inputs are present and the result could change a hardware or optimization conclusion. Profiling is normally required before claiming that a path is compute-bound, communication-bound, launch-bound, or faster by a stated amount. Static analysis may identify a hypothesis, not achieved behavior.

If the local path is not run, record the concrete reason: missing checkpoint partition, incompatible accelerator, insufficient free memory, unavailable environment, unsafe shared-device contention, prohibitive run cost, or user-declared scope. Provide the exact bounded command or experiment that would promote the claim. Do not write only “not tested.”

Ask one focused question only when alternative workloads, hardware, or permission would materially change what must be executed. Do not ask the user for information discoverable from the workspace.

## Use local tests and profiling

Escalate in this order and stop when additional cost cannot change the decision:

1. **Preflight:** pin code/model revisions; verify artifact completeness; record device, topology, free memory, software versions, and other active processes.
2. **Static and shape checks:** inspect configs and code; run deterministic calculators or contract tests that do not load full weights.
3. **Smoke validation:** load the narrowest required component or run the smallest supported request; validate output shape, dtype, finiteness, and modality contract.
4. **Microbenchmark:** isolate the suspected operation with production shapes, dtype, backend, compilation mode, and parallel group.
5. **End-to-end profile:** capture the representative workload after warmup and attribute stages, repeated forwards, communication, host transfers, and memory.
6. **Optimization A/B:** change one mechanism at a time and retain identical inputs, seed, output contract, placement, and quality checks.

Prefer repository-provided tests, benchmarks, and profiling controls. Inspect their current help and documentation rather than copying an old command. Never import arbitrary remote code merely to make a profile run. Do not terminate another process or commandeer a busy accelerator. Use a free device or report the contention as the reason a run was not performed.

Keep generated traces and large outputs outside the skill package. Record stable paths or checksums in the evidence ledger. Treat a successful file write as a smoke result, not a quality or performance qualification.

## Freeze the workload contract

Performance numbers are meaningless without the executed workload. Record:

- task/variant, inputs, batch and concurrency;
- prompt or conditioning length, including actual tokenizer revision when it affects shapes;
- resolution, frames, duration, sample rate, latent/patch geometry, and reference inputs;
- configured scheduler points, actual loop transitions, model forward calls, and CFG or branch multiplier;
- logical/used sequence length separately from alignment padding and per-rank partitioning;
- precision, quantization, attention backend, compile mode, cache state, offload, and placement;
- device count, parallel dimensions, rank mapping, and interconnect.

Use one canonical workload for the main cost table and show sensitivity for the variables that dominate scaling. Do not mix shapes from one workload with latency or memory from another.

## Build an operation-level cost model

Trace the critical loop and calculate its major operations. State the counting convention. Common dense-transformer terms are:

```text
linear FLOPs = 2 * rows * input_width * output_width
dense attention FLOPs ~= 4 * heads * sequence_length^2 * head_dim
SwiGLU MLP FLOPs ~= 6 * rows * hidden_width * intermediate_width
generation FLOPs = FLOPs per forward * actual forward calls
```

Adjust these formulas for grouped-query attention, cross-attention, sparsity, convolution, MoE routing, classifier-free guidance, cached decode, padding behavior, and implementation-specific projections. Separate modules that run once, once per request, once per diffusion step, and once per output token. Cross-check arithmetic with a script or a second calculation.

For arithmetic intensity, state the bytes counted and reuse assumption. A GEMM weight-reuse upper bound such as `FLOPs / weight_bytes` is not an end-to-end roofline result. Compare per-operation intensity with a cited machine balance, then use a profiler to establish achieved utilization, memory traffic, launch gaps, and overlap before assigning a measured bottleneck.

For communication, inspect the actual collective and layout transition. Count every tensor carried, distinguish logical payload from network bytes that exclude self traffic, identify collective frequency, and state topology/bandwidth assumptions. Do not estimate Ulysses, TP, ring, or pipeline cost from one activation tensor while omitting Q/K/V, output, duplication, or overlap semantics.

## Cover the required optimization dimensions

Provide concrete analysis—not a technique list—for each applicable dimension:

1. **Compute and intensity:** per-module and per-forward FLOPs, generation multiplier, dominant operations, roofline hypothesis, and measured utilization when profiled.
2. **Parallelism and communication:** available TP/SP/PP/DP/VAE or stage parallelism, collective count/payload, topology, scaling limit, and platform-specific behavior.
3. **Precision and quantization:** actual dtype by component and critical FP32 paths, implemented quantization coverage, metadata/scale overhead, kernel availability, accuracy evidence, and incompatible features.
4. **Memory and residency:** stored weights, resident weights by stage/rank, persistent state, peak live activations, communication buffers, workspaces, allocator reserve, host memory, and transfer overlap. State whether each number is measured, derived, or reported.
5. **Attention and sparsity:** logical sequence layout, backend, explicit-score avoidance, dense/sparse complexity, backend constraints, and whether sparse behavior is present and quality-qualified.
6. **Step or decode reduction:** actual forward count, CFG branches, early-exit/speculation/cache/distillation availability, scheduler semantics, and quality-risk validation.
7. **Fusion and compile:** exact operator boundary and shapes, current eager/compiled islands, launch or bandwidth evidence, backend ownership, graph-break risk, and an A/B microbenchmark.
8. **Caching and redundant work:** prove that cached values are independent of timestep, noisy state, changing tokens, request options, and mutable model state. Define the cache boundary, key, invalidation, lifetime, memory cost, and quality test. Repeated text input alone does not make attention K/V reusable inside a joint multimodal block.

Mark a dimension `N/A — <reason>` only when the architecture makes it inapplicable. Mark unimplemented but plausible work `Proposed`, and unprofiled bottlenecks `Hypothesis`.

## Measurement protocol

For every benchmark or profile:

1. Save the exact command/configuration and pin code, model, dependencies, driver/runtime, device, topology, and environment variables.
2. Use a fixed representative input, seed, output contract, and placement.
3. Separate cold start, model load, compile, warm cache, steady-state, and queueing.
4. Exclude declared warmup from steady-state statistics. Record repetitions and report a central value plus spread; retain raw samples.
5. Capture end-to-end latency, stage latency, actual model-forward time/count, throughput/concurrency, peak allocated/reserved memory, device telemetry, host transfers, collectives, and top kernels as applicable.
6. Pair speed and memory results with task-appropriate correctness or perceptual/semantic quality gates.
7. For NVIDIA, use the runtime's current PyTorch-profiler or CUDA/Nsight control path when appropriate. For Ascend, use the current CANN/`torch_npu` profiling path. Do not translate CUDA kernel conclusions directly to Ascend.

If profiling overhead materially distorts the run, use a low-overhead stage baseline for the headline result and a separate detailed trace for attribution.

## Reporting requirements

The performance section must include:

- an evidence-mode table that records the local-test/profile decision;
- the canonical dimension matrix summarizing workload/counts, compute/intensity, communication, precision/memory, and attention/steps/cache/fusion with evidence classes;
- workload and actual execution-count derivation;
- operation-level compute and arithmetic-intensity analysis;
- parallelism and communication analysis;
- precision, quantization, and memory analysis;
- attention, step reduction, caching, fusion, and compile analysis;
- measured results with artifacts, or explicit static-only limits and a reproducible next experiment;
- a short list of conclusions that feed directly into the optimization roadmap.

Keep values in formulas at useful precision and avoid false accuracy. Cite each input and label the resulting calculation `Derived`; cite measurements separately as `Measured`.
