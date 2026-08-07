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

## vLLM-Omni Support Status

<!-- Include this section only for the vLLM-Omni profile. -->

Status vocabulary: `Supported`, `Partial`, `Unsupported`, `Unverified`, `N/A`.

| Capability | Task/API/platform scope | Implementation | Validation | Support | Effective revision | Evidence | Gap or limitation |
|---|---|---|---|---|---|---|---|
| <loading/task/backend/test/production capability> | <narrow scope> | <implementation state> | <one or more semicolon-separated validation gates> | <status> | <commit/tag; superseded/reverted link if needed> | [E2] | <limit> |

### Source Conflicts

<Describe any mismatch among code, support tables, recipes, releases, CI, or issues.>

## Hardware Requirements

<!-- Include this section when hardware, deployment, memory, or performance is in scope. -->

### Resource Envelope

| Resource | Observed or reported | Derived/estimated | Recommendation | Assumptions/evidence |
|---|---|---|---|---|
| Checkpoint storage | <value> | <calculation> | <headroom> | [E3] |
| Host RAM | <value> | <calculation> | <headroom> | [E4] |
| Device memory | <value> | <calculation> | <headroom> | [E5] |

### Platform Matrix

| Platform | Device/topology | Software stack | Workload | Precision/placement | Device memory | Host RAM/storage | Configuration class | Support status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NVIDIA | <device/count/interconnect> | <driver/CUDA/framework/runtime> | <shape> | <dtype/parallel/offload/backend> | <measured or estimate> | <host/storage> | <class> | <status> | [E6] |
| Ascend | <device/count/interconnect> | <driver/CANN/torch_npu/runtime/operators> | <shape> | <dtype/parallel/offload/backend> | <measured or estimate> | <host/storage> | <class> | <status> | [E7] |

### Qualification Gaps

<What has not been tested, and the exact run needed to qualify it.>

## vLLM-Omni Optimization Direction

<!-- Include this section only for the vLLM-Omni profile. -->

| Priority/status | Current gap and evidence | Bottleneck | Proposed change/touchpoint | NVIDIA direction | Ascend direction | Expected result | Risks/dependencies | Verification |
|---|---|---|---|---|---|---|---|---|
| P0/P1/P2/P3 — <implementation state> | <gap> [E8] | <measured or hypothesis> | <mechanism/path> | <effect or N/A> | <effect or N/A> | <directional goal> | <risks> | <A/B and quality gate> |

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
- Prefer tables for repeated comparisons and prose for reasoning.
- Use at most one architecture diagram unless additional diagrams materially clarify different execution paths.
- A Mermaid diagram is optional. Validate its syntax if one is included.
- Link directly to primary sources and pin code links to a commit where possible.
- Do not seed the report with hypothetical speedup numbers or universal hardware minima.
- If only a base architecture analysis is requested, omit both vLLM-Omni sections and validate with the base profile.
