---
name: gen-model-architecture-analysis
description: Produce comprehensive, evidence-backed architecture, hardware, and inference-performance reports for generative models, with an optional vLLM-Omni support and optimization profile. Use for end-to-end assessments spanning model components, data flow, tensor shapes, serving readiness, NVIDIA GPU or Ascend NPU requirements, detailed compute/memory/communication analysis, local tests or profiling, and—when vLLM-Omni is in scope—runtime gaps and prioritized enablement or performance work. Applies to autoregressive, diffusion, speech, image, video, and multimodal models. Do not use for a narrow sizing question or pull-request review.
---

# Generative Model Architecture Analysis

## Purpose

Turn model code, configuration, documentation, tests, and measured runs into a decision-ready report. Keep observed facts, derived estimates, and proposed work visibly separate. Do not turn a roadmap issue, an open pull request, or a memory-capacity estimate into a support claim.

Include detailed inference-performance analysis in every report. Make local execution conditional on whether a bounded test or profile is safe, feasible, and able to change the conclusion; do not make the analysis itself conditional.

Default to a Markdown report. Match another requested format only after the analysis is complete.

## Route the Analysis

Read these references completely when their route applies:

- Always read [evidence-and-status.md](references/evidence-and-status.md), [architecture-analysis.md](references/architecture-analysis.md), [performance-analysis.md](references/performance-analysis.md), and [report-template.md](references/report-template.md).
- Read [hardware-requirements.md](references/hardware-requirements.md) when hardware, memory, deployment, NVIDIA, or Ascend is in scope.
- Read [vllm-omni-analysis.md](references/vllm-omni-analysis.md) when the user asks about vLLM-Omni support, enablement, serving, or optimization.

Do not force diffusion-specific concepts onto autoregressive or speech models. Do not add a vLLM-Omni section to a general architecture report unless it is requested or clearly relevant.

## Establish Scope

Record these before making claims:

1. Exact model identifier and revision, including task variants or checkpoint partitions.
2. Reference implementation repository and pinned revision.
3. vLLM-Omni revision when that profile applies.
4. Modalities, tasks, API/offline modes, and representative workloads.
5. Target platforms and topology. Treat NVIDIA GPU and Ascend NPU as separate targets.
6. Performance question and required evidence depth: static analysis, local test, or target-shape profiling.
7. Available local repositories, checkpoints, accelerators, environments, profiler tools, execution budget, and unavailable inputs.
8. Evidence cutoff date.

If a missing value does not block research, continue with an explicit assumption and mark the affected result `Unverified`. Ask only when different interpretations would materially change the analysis.

## Workflow

### 1. Build an evidence ledger

Search current primary sources because support and hardware status change quickly. Pin repository evidence to a commit or release when possible. Assign every important claim an evidence ID and class using [evidence-and-status.md](references/evidence-and-status.md).

Prefer current code and executed tests over summaries. When sources conflict, show the conflict and narrow the claim; do not silently select the most optimistic source.

### 2. Reconstruct the architecture

Start from entrypoints and configuration, then trace preprocessing, encoders, core network, scheduler or decode loop, and output decoders. Capture concrete tensor shapes and dtypes at major boundaries. Cover only mechanisms present in the inspected variant.

Include one Mermaid component/data-flow diagram for the representative path. Put major components in execution order, label each major data edge with symbolic and—when available—canonical concrete I/O shape and dtype, and keep at least one connected source-to-output route of two or more shape-labeled data edges. Show important modality branches and repeated generation loops, and cite the diagram inputs in visible prose within `Model Architecture`. Keep exact formulas and variant details in the component/shape tables; do not put evidence IDs inside the Mermaid code block.

Use the inspection map and calculation rules in [architecture-analysis.md](references/architecture-analysis.md). Never import or execute untrusted remote model code merely to discover its structure.

### 3. Choose performance evidence depth

Inventory the local environment before asking the user for information. Choose and record one of these evidence paths:

- static analysis when compatible execution inputs are unavailable;
- bounded local tests for shapes, operator paths, memory feasibility, or microbenchmarks;
- representative end-to-end profiling when a conclusion depends on bottleneck ordering, latency, throughput, peak memory, communication share, or an optimization A/B.

Start with the cheapest useful check and escalate only when it changes a decision. Use local tests or profiling when compatible code, model artifacts, hardware, and execution authority are available. Do not occupy shared accelerators blindly, download large checkpoints without need, or run untrusted model code. If a run is not performed, state why, retain estimates as `Derived` or `Estimated`, and give the exact command or experiment that would close the gap.

Follow [performance-analysis.md](references/performance-analysis.md). Record commands, revisions, environment, workload, warmup/repetitions, raw artifacts, results, and quality gates. Never label a roofline estimate or source-reported benchmark as a local measurement.

### 4. Assess vLLM-Omni support by capability when applicable

When vLLM-Omni is in scope, avoid a single supported/unsupported verdict. Build rows for the requested tasks, inputs, output contract, loading, execution modes, APIs, correctness tests, performance tests, and each hardware backend. Use only the status vocabulary defined in [evidence-and-status.md](references/evidence-and-status.md).

For vLLM-Omni, follow the repository inspection order and state model in [vllm-omni-analysis.md](references/vllm-omni-analysis.md). Record implementation state, validation evidence, support status, and effective revision independently. A registry entry, a hardware recipe, and recurring CI demonstrate different dimensions; do not treat them as a total ordering.

### 5. Derive the hardware envelope

Separate checkpoint storage, host RAM, accelerator memory, device count, interconnect, and software-stack requirements. Separate measured configurations from estimates and recommendations. Include the workload behind every number.

Use [hardware-requirements.md](references/hardware-requirements.md). Never infer Ascend compatibility from CUDA compatibility, or a lower-memory GPU recipe from arithmetic capacity alone.

### 6. Produce an optimization roadmap

For vLLM-Omni analysis, first produce the detailed inference-performance analysis required by [performance-analysis.md](references/performance-analysis.md). Start each recommendation from a demonstrated gap, measurement, or explicitly labeled hypothesis. Connect each proposal through:

`evidence -> bottleneck -> mechanism -> vLLM-Omni touchpoint -> platform impact -> validation`

Rank correctness and missing support before performance. Distinguish cross-platform work from NVIDIA- or Ascend-specific kernels. Include a measurement plan and quality guardrail for every optimization; avoid unsupported speedup percentages. Check cache eligibility against actual data dependencies and invalidation conditions rather than assuming repeated inputs imply reusable K/V. Omit the vLLM-Omni roadmap from a base report, but retain the core inference-performance analysis.

### 7. Synthesize and validate

Use [report-template.md](references/report-template.md), including when returning the report only in the response. Keep the executive summary concise, put details in matrices, and end with prioritized next actions, risks, unknowns, and the evidence index.

Resolve `SKILL_DIR` to the directory containing this `SKILL.md`, then validate a saved report. Repeat `--require-platform` only for platforms in the requested scope. For example:

Run the validator from an existing local environment that satisfies `scripts/requirements.txt` (`markdown-it-py` is used so code, raw HTML, quotations, links, headings, and tables are classified by rendered Markdown structure rather than regex alone). If the selected environment is missing it, use a task-local environment rather than altering an unrelated shared environment.

```bash
python3 "$SKILL_DIR/scripts/validate_report.py" REPORT.md
python3 "$SKILL_DIR/scripts/validate_report.py" REPORT.md \
  --require-platform nvidia \
  --require-platform ascend \
  --strict
python3 "$SKILL_DIR/scripts/validate_report.py" REPORT.md \
  --profile vllm-omni \
  --require-platform nvidia \
  --require-platform ascend \
  --strict
```

Pass `-` instead of `REPORT.md` to validate Markdown from standard input without creating a file.

Resolve errors before delivery. Review warnings rather than suppressing them mechanically.

## Non-Negotiable Quality Gates

- State the model, repository revisions, and evidence cutoff. State workload, precision, and topology for hardware or performance claims.
- Include a Mermaid component/data-flow diagram with shape-bearing labels on the major interfaces; keep its shapes consistent with the component table and canonical workload.
- State the selected performance evidence path and the local-test/profile decision. Do not silently omit measurement when an optimization conclusion depends on it.
- Cite architecture and support claims at the point of use with evidence IDs.
- Label calculations `Derived`, projections `Estimated`, and future work `Proposed`.
- Separate logical FLOPs/bytes from achieved throughput, allocator peaks from device telemetry, and configured diffusion steps from actual model forward calls.
- Use `Unknown` or `Unverified` when evidence is absent; do not fill gaps with plausible defaults.
- Keep task, API, backend, quantization, and production-readiness status separate.
- Report both success evidence and known limitations.
- Do not claim a hardware minimum from a single successful run.
- Do not claim an optimization is available because it is architecturally applicable.
- Preserve source language for identifiers and provide the narrative in the user's requested language.
