# Active Verification

Use this reference only for trusted code and an environment authorized for the
affected path. Static analysis and CI evidence remain useful when execution is
not safe or available.

## Define the run first

For accelerator, performance, accuracy, serving, or benchmark work, write down:

- the hypothesis;
- one isolated variable;
- fixed controls;
- success criterion; and
- stop condition.

Freeze and record the repository SHA. Keep hardware, NUMA affinity, model,
arguments, readiness definition, cache state, and software environment fixed
across comparisons.

## Choose the narrowest level

- **Static/CPU only:** diff hygiene, import/version preflight,
  config/codec/schema resolution, and focused CPU/reference tests.
- **Matching accelerator:** one focused unit or kernel test after a CPU/static
  feasibility probe.
- **Accelerator plus model/data:** a focused test, then one bounded
  production-path request with output/validity inspection.
- **Quantitative claim:** base/head or reference/head A/B under
  [perf-verification.md](perf-verification.md).
- **Missing dependency, hardware, or asset:** state the exact gap and audit
  contributor/CI evidence.

Use the shortest path: GPU-free probe, one feasibility run, then only the
repetitions required for a claimed A/B result. Do not expand a review into a
long benchmark campaign without a claim and success criterion.

## Environment preflight

Before trusting a result:

1. confirm the process imports `vllm_gr` from the frozen checkout;
2. record Python, vLLM, vLLM-Ascend if applicable, vLLM-GR, driver/runtime,
   device, model, and relevant optional-integration versions;
3. confirm the base branch's supported-version contract;
4. confirm the selected test reaches the changed dispatcher/backend; and
5. separate environment preparation, downloads, copies, and warmup from
   process-to-readiness and measured request time.

## Shared accelerator safety

Obey the host's accelerator policy. When local instructions require `gpu run`,
all CUDA work must use it with exact device reservation. Otherwise use the
repository's documented allocator without disturbing existing workloads. The
repository's NPU helper is discovery-only on current branches: its `lock_npu`
function is a stub and does not reserve a device. Run NPU validation only when
exclusive allocation is guaranteed by an external scheduler or owner.

Do not kill processes, claim shared ports, drop shared caches, weaken health
checks, download large/gated assets, or install into a shared environment
without authorization. Reuse a task-owned prepared environment and one server
per configuration for recurring runs.

Clean up task-owned servers, child processes, ports, temporary files, and device
memory at the end. Preserve commands and raw results before cleanup.

## Production-path checks

For beam or constraint behavior, inspect actual outputs rather than process
survival:

- returned recommendation IDs are legal and ordered as claimed;
- parent/score/logprob geometry is coherent;
- stop/max-token/catalog-terminal behavior is correct;
- session/KV/beam resources are released after completion and failure;
- the expected CUDA/NPU kernel or eager fallback executed; and
- a representative ordinary/Pangu request still works when shared code changed.

For serving changes, validate readiness separately, issue one bounded first
request, inspect response/error/metrics, and stop the task-owned server.

## Report evidence

Bind every command and result to the frozen SHA and environment. Classify a
failure as change-induced, pre-existing, test defect, environment,
infrastructure, or flaky before reporting it as a code finding. One passing
rerun does not erase a flakiness signal.

Never claim device evidence from a mock, CPU fallback, or unverified CI label.
Missing hardware lowers confidence and is reported as a validation gap, not a
fabricated pass or automatic defect.
