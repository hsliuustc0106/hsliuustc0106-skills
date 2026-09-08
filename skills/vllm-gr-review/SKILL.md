---
name: vllm-gr-review
description: Review pull requests and local branches for JiusiServe/vllm-gr with frozen inputs, GR-domain routing, targeted validation, and concise evidence-backed findings. Use for reviews involving OneRec or Pangu inference, beam search, catalog or table constraints, EngineCore protocols, runtime patches, CUDA or NPU workers and kernels, tests, benchmarks, accuracy, or compatibility with upstream vLLM.
---

# vLLM-GR PR Review

## Overview

Review vLLM-GR like a maintainer: direct, selective, and focused on defects
that automation does not prove away. Prefer a few high-confidence findings to
an exhaustive checklist. Zero findings is a valid result.

This skill is a review router for `JiusiServe/vllm-gr`. It supports pull
requests, committed local branches, and local worktrees with staged, unstaged,
or untracked changes. It is not an author pre-submit checklist.

## Quality contract

Every finding must be:

- **Correct**: prove a reachable failure or contract violation.
- **Prioritized**: lead with wrong results, crashes, hangs, state corruption,
  and compatibility breaks.
- **Actionable**: identify the smallest safe fix direction.
- **Evidence-based**: cite changed code plus its caller, consumer, contract,
  test, CI result, or measurement.
- **Concise**: avoid checklist dumps and repeated summaries.
- **Calibrated**: distinguish a defect from an unverified claim or optional
  improvement.

Do not report unrelated backlog, formatting already enforced by pre-commit,
or a missing test that would not protect changed behavior.

## Select the input and depth

Use the PR's actual base branch. vLLM-GR changes may target `main`,
`decode_graph`, `develop`, or a development branch; never silently substitute
`main`.

| Input | Review surface |
| --- | --- |
| PR number or URL | Frozen metadata, base/head SHAs, diff, and checks. |
| Local branch/worktree | Merge base plus committed and local changes. |
| Pre-filled context | Reuse supplied facts; fetch only missing data and diff. |

If no target is supplied, ask for a PR number/URL or a local branch and base.
Default to maintainer brevity. A detailed or audit request expands coverage but
keeps the same evidence and severity bar.

## Reference guide

Read references lazily. Do not load every file for every review.

| Situation | Read |
| --- | --- |
| Every review | [review-execution.md](references/review-execution.md) |
| After the diff census | [review-routing.md](references/review-routing.md) |
| Production behavior changes | [architecture.md](references/architecture.md) |
| Blocker scan for production or high-risk test changes | [blocker-patterns.md](references/blocker-patterns.md) |
| Tests, docs, CI, public behavior, or risky code changes | [tests-docs-checklist.md](references/tests-docs-checklist.md) |
| A safe runnable path or accelerator is available | [verification.md](references/verification.md) |
| Latency, throughput, memory, scaling, or accuracy is claimed | [perf-verification.md](references/perf-verification.md) |

Branch-local code and documentation are authoritative. A document marked
prospective, proposed, or reference-only is a design input, not proof that its
protocol is wired into production.

## Workflow

### 1. Freeze the review snapshot

Pin and report the actual base and head before drawing conclusions. For local
reviews, include the index, worktree, and in-scope untracked files in the
snapshot. Recheck the snapshot before delivery.

Treat fork code as untrusted unless the user and environment establish
otherwise. Do not import, test, build, or execute an untrusted head on a host
with secrets or shared resources. Use static SHA-addressed inspection or a
disposable, secret-free sandbox instead.

Follow [review-execution.md](references/review-execution.md) for commands,
trust gates, local-state coverage, and staleness handling.

### 2. Build a diff census

Group changes into production code, tests, docs, configuration, packaging/CI,
benchmarks, and generated artifacts. Reconcile the PR title and body with the
actual files. Mark unrelated scope and unexplained generated data.

Do not infer behavior from the description alone. Trace changed symbols to
their live callers and consumers with bounded searches.

### 3. Route and trace the GR path

Use [review-routing.md](references/review-routing.md) to choose the smallest
set of domain checks. For changed beam behavior, trace the applicable path:

```text
offline / CLI / OpenAI ingress
  -> config validation and cross-process transport
  -> catalog or constraint construction
  -> candidate generation, stop handling, and beam selection
  -> EngineCore wire, session, scheduler, and DP routing
  -> ModelRunner, KV state, attention, and accelerator operations
  -> logprobs, response assembly, metrics, and terminal cleanup
```

Check the ordinary non-beam/Pangu path and feature-off defaults whenever a
global patch, config, scheduler, worker, attention, or sampling path changes.

### 4. Run the blocker scan

Apply [blocker-patterns.md](references/blocker-patterns.md). In particular,
look for:

- candidate, parent, score, logprob, and row-geometry misalignment;
- catalog or constraint paths that silently broaden or narrow legal outputs;
- request/session cleanup gaps on success, error, abort, or cancellation;
- wire, scheduler, ModelRunner, or patch drift from pinned upstream APIs;
- KV-cache, beam-suffix, reorder, or graph-replay state corruption;
- CUDA/NPU behavior divergence hidden by a CPU fallback or mock; and
- regressions in ordinary vLLM/Pangu behavior when GR is disabled.

A suspicious pattern is not yet a finding. Prove its reachable trigger and
impact against the frozen diff.

### 5. Evaluate evidence and verify proportionately

Map each semantic change to a test that would fail if the behavior regressed.
Use [tests-docs-checklist.md](references/tests-docs-checklist.md) for coverage,
CI selection, and documentation. Use [verification.md](references/verification.md)
only when execution is trusted and the environment supports the affected path.

Performance and accuracy are coupled for recommendation inference. Apply
[perf-verification.md](references/perf-verification.md) to every quantitative
claim. Do not turn missing accelerator access into simulated evidence; name
the exact validation gap.

### 6. Consolidate and deliver

Verify each finding against the final snapshot, deduplicate by root cause, and
return findings first in severity order.

Each finding must include:

- `[P0]`, `[P1]`, or `[P2]` plus a concise title;
- the smallest changed `path:line` range;
- the trigger or caller-to-consumer path;
- current behavior and user/runtime impact; and
- the smallest safe fix direction.

Severity guide:

- **P0**: security exposure, broad or irrecoverable data/state corruption, or
  broad project unusability.
- **P1**: reachable wrong recommendation output, crash, hang, resource leak,
  compatibility break, or unsafe lifecycle in the changed path.
- **P2**: a real, bounded defect with a concrete failure mode that is not an
  immediate blocker.

If there are no findings, say so briefly and name material validation gaps.
Keep the review read-only unless the user explicitly authorizes posting,
requesting reviewers, editing code, or submitting a GitHub review event.
