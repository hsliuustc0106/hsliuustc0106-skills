# Report Template

Use this structure for the final Markdown report. Remove instruction text and inapplicable optional rows. Write `Unknown — <reason>` when evidence is unavailable; do not leave cells blank.

## Contents

- [Core report](#core-report)
- [Presentation rules](#presentation-rules)

## Core report

```markdown
# <Model> Architecture Analysis

## Executive Summary

<Architecture identity plus only the support, hardware, blocker, and optimization conclusions requested in scope.>

## Scope and Revisions

| Item | Value |
|---|---|
| Model/checkpoint | <identifier and revision> |
| Reference implementation | <repository and commit/tag> |
| Runtime under analysis | <repository and commit/tag; remove this row when no runtime is in scope> |
| Evidence cutoff | <YYYY-MM-DD> |
| Tasks and APIs | <in-scope tasks/modes> |
| Representative workload | <batch/concurrency, tokens or resolution/frames/duration/steps> |
| Target hardware | <NVIDIA and/or Ascend devices/topology, or N/A> |
| Assumptions | <explicit assumptions> |

### Evidence Method

<Source precedence, whether runs were reproduced, and material source conflicts.>

## Model Architecture

### Architecture Identity and Data Flow

<Narrative and, only if useful, one architecture diagram.>

### Components

| Stage/component | Implementation | Input -> output shape/dtype | Parameters/config | Residency/frequency | Evidence |
|---|---|---|---|---|---|
| <stage> | <class/path> | <symbolic and concrete> | <facts> | <once/per-step/etc.> | [E1] |

### Critical Path and Implications

<Dominant loops/stages, memory/compute/communication drivers, variant differences, and unknowns.>

## Inference Performance Analysis

<!-- Required core section. Local execution is conditional; the analysis and local-test/profile decision are not. -->

### Evidence Level and Profiling Decision

| Evidence mode | Scope/workload | Environment | Method/artifact | Result | Limitation/reason | Evidence |
|---|---|---|---|---|---|---|
| Static analysis / Local test / Local profile / Source measurement / Community measurement / Not run | <narrow scope> | <code/model/device/software revisions> | <exact command and artifact, or bounded next command in inline code> | <result; label measured versus derived> | <scope limit or concrete reason the local run was skipped> | [E2] |

#### Required Dimension Matrix

| Dimension | Workload/shape | Analysis/result | Evidence class | Limitation/next validation | Evidence |
|---|---|---|---|---|---|
| Workload/execution count | <canonical workload and actual call multiplier> | <derived or measured result> | Derived | <sensitivity or next run> | [E3] |
| Compute/arithmetic intensity | <dominant production shapes and precision> | <per-operation/forward/generation cost and roofline status> | Derived | <profile needed to promote a bottleneck hypothesis> | [E4] |
| Parallelism/communication | <parallel dimensions, ranks, topology> | <collectives, calls, payload/network bytes, overlap> | Derived | <scaling or topology gap> | [E5] |
| Precision/quantization/memory | <component dtypes, placement, workload> | <quantization coverage and stored/resident/peak-memory result> | Observed | <quality or peak-memory gap> | [E6] |
| Attention/steps/caching/fusion | <sequence, backend, actual forward count> | <current mechanisms and semantic eligibility> | Observed | <A/B and quality validation> | [E7] |

### Workload and Execution Count

<Derive representative shapes, used versus padded rows, configured steps/tokens, actual loop transitions and forward-call multiplier, variants, and sensitivity.>

### Compute Cost and Arithmetic Intensity

<Show per-operation formulas and values, per-forward and per-generation totals, byte assumptions, dominant terms, and static roofline hypothesis. Add achieved utilization only when measured.>

### Parallelism and Communication

<For each applicable strategy, show collective/layout, calls, payload or network bytes, topology, overlap assumption, and scaling conclusion.>

### Precision, Quantization, and Memory

<Map dtypes and quantization coverage by component. Separate stored/resident weights, persistent state, live activations, buffers/workspaces, allocator reserve, host memory, and measured peaks.>

### Attention, Steps, Caching, and Fusion

<Analyze attention backend/sparsity, actual step reduction or distillation, semantic cache eligibility/invalidation, fusion/compile boundaries, platform split, and quality risks.>

## vLLM-Omni Support Status

<!-- Include this section only for the vLLM-Omni profile. -->

Status vocabulary: `Supported`, `Partial`, `Unsupported`, `Unverified`, `N/A`.

| Capability | Task/API/platform scope | Implementation | Validation | Support | Effective revision | Evidence | Gap or limitation |
|---|---|---|---|---|---|---|---|
| <loading/task/backend/test/production capability> | <narrow scope> | <implementation state> | <one or more semicolon-separated validation gates> | <status> | <commit/tag; superseded/reverted link if needed> | [E8] | <limit> |

### Source Conflicts

<Describe any mismatch among code, support tables, recipes, releases, CI, or issues.>

## Hardware Requirements

<!-- Include this section when hardware, deployment, memory sizing, or target-platform performance is in scope. -->

### Resource Envelope

| Resource | Observed or reported | Derived/estimated | Recommendation | Assumptions/evidence |
|---|---|---|---|---|
| Checkpoint storage | <value> | <calculation> | <headroom> | [E9] |
| Host RAM | <value> | <calculation> | <headroom> | [E10] |
| Device memory | <value> | <calculation> | <headroom> | [E11] |

### Platform Matrix

| Platform | Device/topology | Software stack | Workload | Precision/placement | Device memory | Host RAM/storage | Configuration class | Support status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NVIDIA | <device/count/interconnect> | <driver/CUDA/framework/runtime> | <shape> | <dtype/parallel/offload/backend> | <measured or estimate> | <host/storage> | <class> | <status> | [E12] |
| Ascend | <device/count/interconnect> | <driver/CANN/torch_npu/runtime/operators> | <shape> | <dtype/parallel/offload/backend> | <measured or estimate> | <host/storage> | <class> | <status> | [E13] |

### Qualification Gaps

<What has not been tested, and the exact run needed to qualify it.>

## vLLM-Omni Optimization Direction

<!-- Include this section only for the vLLM-Omni profile. -->

| Priority/status | Current gap and evidence | Bottleneck | Proposed change/touchpoint | NVIDIA direction | Ascend direction | Expected result | Risks/dependencies | Verification |
|---|---|---|---|---|---|---|---|---|
| P0/P1/P2/P3 — <implementation state> | <gap> [E14] | Measured/Reported/Community-reported/Derived/Estimated/Hypothesis — <bottleneck> [E15] | <mechanism/path> | <substantive effect, or N/A — reason> | <substantive effect, or N/A — reason> | <directional goal> | <risks> | Workload: baseline=<control workload> vs candidate=<changed workload>; metrics: performance=<latency/throughput/time>, resource=<memory/bytes/utilization>; repetitions: warmups=<nonnegative count>, measured=<positive count per arm>; quality gate: pass if <output-to-baseline tolerance, named quality-metric threshold, or concrete media contract> |

## Recommended Next Actions

1. <Highest-value in-scope action and owner/evidence needed.>
2. <Optional hardware qualification action; remove if out of scope.>
3. <Optional profiler-backed optimization experiment; remove if out of scope.>

## Risks and Unknowns

| Risk/unknown | Why it matters | Current evidence | Resolution path |
|---|---|---|---|
| <item> | <impact> | <what is known> | <test/source needed> |

## Evidence Index

| ID | Claim/use | Source | Revision/date | Class | Confidence | Notes |
|---|---|---|---|---|---|---|
| E1 | <narrow claim> | <pinned permalink or local path> | <commit/version/date> | Observed/Measured/Reported/Community-reported/Derived/Estimated/Proposed | High/Medium/Low | <scope/limitation> |
```

## Presentation rules

- Put evidence IDs beside claims, not only in the final index.
- Keep current support separate from proposed optimization work.
- Record a local-test/profile decision even when only source measurements or static estimates are available.
- Prefer tables for repeated comparisons and prose for reasoning.
- Use at most one architecture diagram unless additional diagrams materially clarify different execution paths.
- A Mermaid diagram is optional. Validate its syntax if one is included.
- Link directly to primary sources and pin code links to a commit where possible.
- Do not seed the report with hypothetical speedup numbers or universal hardware minima.
- For a base report, retain the inference-performance section and omit only the two vLLM-Omni sections.
