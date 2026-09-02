# Performance and Accuracy Verification

Apply this reference when a PR claims or intentionally changes latency,
throughput, memory, scaling, recommendation accuracy, or output quality.

## Coupled evidence contract

A faster recommendation path is not a valid improvement if legal-output or
accuracy behavior regresses. Require both:

- **performance evidence:** the metric named by the claim, such as end-to-end
  latency, TTFT/TPOT, throughput, process-to-readiness, or peak device memory;
  and
- **correctness/accuracy evidence:** repository accuracy metrics, exact
  constrained-output validity, or a justified fixed-input parity comparison.

Use the frozen base branch's `.github/benchmark-gate.yaml` for declared
thresholds and failure modes. Do not invent universal percentage gates.

## Comparable A/B design

For an existing path, compare frozen base and head. For a new path absent from
base, compare head with a pinned canonical/reference implementation. Keep fixed:

- exact hardware, driver/runtime, NUMA affinity, and software versions;
- model/checkpoint, tokenizer, catalog/constraint artifact, and dataset;
- request inputs, seed, precision, beam width, output count, batch/concurrency,
  topology, cache state, and feature flags;
- warmup, repetitions, synchronization, timing boundaries, readiness
  definition, and memory collection; and
- correctness/accuracy metric and tolerance.

State the hypothesis, isolated variable, success criterion, and stop condition
before running. Follow the shortest-run policy in
[verification.md](verification.md): one feasibility run, then two repetitions
per side only when claiming an A/B result unless a stricter repository policy
or statistical question requires more.

## Evidence to request

Ask for:

```text
base/head (or reference/head) SHAs
hardware and software fingerprint
exact commands and environment/configuration
preparation and warmup procedure
raw per-run results plus aggregate/variability
accuracy or validity result for the same runs
timing and memory boundaries
artifacts or logs needed to reproduce the claim
```

Separate downloads, copies, compilation, and cache preparation from
process-to-readiness. Do not hide warmup or use dummy/lazy health checks to
improve startup numbers.

## GR-specific measurements

Choose metrics that match the change:

- OneRec accuracy and recall/pass metrics from the base-branch benchmark gate;
- offline and online elapsed time under equivalent inputs;
- TTFT/TPOT and request throughput for serving changes;
- peak allocated/reserved device memory and OOM boundary for memory work;
- prefill/decode/sort or kernel timing only when boundaries and overlap are
  defined; and
- legal-candidate count/output validity for pruning or constrained Top-K work.

Check ordinary/Pangu accuracy and behavior when shared vLLM paths change.

## Reviewer verification ladder

1. Audit the methodology and commands statically.
2. Run a CPU/static feasibility probe where possible.
3. Run one bounded head feasibility case on suitable authorized hardware.
4. Run controlled base/head repetitions only for a claim worth independently
   verifying.
5. Validate one first production request for the winning configuration.

If hardware or assets are unavailable, name the exact unverified claim and
evaluate contributor/CI evidence. Do not simulate accelerator evidence.

Classify discrepancies as implementation regression, benchmark bug,
environmental drift, noise, or unsupported claim. Report claimed and measured
values together, with uncertainty and raw artifact locations.
