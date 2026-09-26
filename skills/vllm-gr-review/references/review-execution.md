# Review Execution

Use this reference for every vLLM-GR review.

## Freeze a pull request

Resolve the repository explicitly and capture the actual base/head identities:

```bash
vllm_gr_pr=123  # Replace with the target PR number.
gh api "repos/JiusiServe/vllm-gr/pulls/${vllm_gr_pr}" \
  --jq '{number, title, draft, mergeable, state,
    base_ref: .base.ref, base_sha: .base.sha,
    head_ref: .head.ref, head_sha: .head.sha,
    head_repo: .head.repo.full_name}'
gh pr checks "${vllm_gr_pr}" --repo JiusiServe/vllm-gr
gh pr diff "${vllm_gr_pr}" --repo JiusiServe/vllm-gr
```

Record at least the PR number, base branch/SHA, head SHA, draft state,
mergeability, and required-check status. A failed or pending check is evidence,
not a reason to skip static review. Inspect only the first relevant failure
when CI already proves an issue.

Re-read `.head.sha` from the pull-request API immediately before delivery. If
it changed, discard line-number and runtime evidence tied to the old head and
review the new snapshot. If the head repeatedly changes, report the churn
instead of mixing evidence from different commits.

## Materialize safely

Use an isolated detached worktree for a trusted PR head. Do not switch the
user's current checkout or reuse a dirty worktree. Resolve paths before
creating or removing a task-owned worktree.

A worktree freezes Git identity but is not a security sandbox. For an
untrusted fork, do not run imports, hooks, tests, builds, benchmark scripts, or
repository-configured tools on the reviewer host. Use static inspection or an
approved disposable sandbox with no secrets and restricted filesystem,
network, devices, and process access.

Do not expose tokens in command output. Prefer `gh`'s existing authentication
and avoid commands that print environment variables or credential files.

## Freeze a local review

First establish the intended base; do not assume `main` when the branch may
target `decode_graph` or `develop`. Capture:

```text
base merge-base and HEAD SHA
committed diff
staged diff
unstaged diff
in-scope untracked paths and bytes
```

Use NUL-safe file discovery for untracked paths. Do not include ignored caches,
models, generated data, virtual environments, or unrelated user files merely
because they are present. Record a content fingerprint or recreate a pristine
snapshot before validation and delivery so local edits cannot silently stale
the review.

Never reset, clean, stash, or overwrite the user's local changes as part of a
review.

## Build the diff census

Classify every changed path:

- runtime/production code;
- tests and test resources;
- public docs and examples;
- configuration, packaging, and dependencies;
- CI and benchmark policy; or
- generated/binary artifacts.

Map each production change to its test and each test to the behavior it claims
to protect. Compare the PR body with the actual diff. Use linked issues only
when they define the expected contract, reproduction, or accepted design.

## Inspect with bounded searches

Read the changed hunk, its containing function/class, direct callers, direct
consumers, and the closest sibling implementation. Expand only to resolve a
specific uncertainty. Useful searches include changed symbol names, config
keys, patch targets, request fields, metric names, and test references.

For monkey patches and upstream private APIs, inspect both the GR wrapper and
the exact pinned upstream implementation. Use the branch's dependency metadata
and `docs/runtime_patch_inventory.md`; do not compare against an arbitrary
installed or latest upstream version.

## Validate without widening scope

On trusted code, start with low-cost static checks and the narrowest relevant
test. Verify the installed/imported package actually resolves to the frozen
checkout before treating a result as evidence. Record skipped tests and their
reason.

Do not install large dependencies, download gated models/datasets, acquire
accelerators, stop shared servers, or start remote jobs merely because a test
might benefit. Follow the host and repository resource policy. Use
[verification.md](verification.md) when execution is appropriate.

Treat CI status as supporting evidence. A green job can miss a path; a red job
may be infrastructure or pre-existing. Classify the first relevant failure
before turning it into a finding.

## Deliver against the same snapshot

Before delivery:

1. recheck the PR head or local content fingerprint;
2. confirm each finding is introduced or exposed by the review diff;
3. confirm its line is in the changed file and remains current;
4. deduplicate findings with the same root cause; and
5. separate verified defects from validation gaps.

Return findings first. Keep comments human-sized; do not paste an internal
checklist. A finding should state trigger, current behavior, impact, and the
smallest fix. Zero findings is valid.

Review is read-only by default. Viewing metadata, diffs, checks, and existing
threads does not authorize posting. Do not submit inline comments, review
events, labels, reviewer requests, code changes, commits, or pushes without
explicit user authorization for that action.
