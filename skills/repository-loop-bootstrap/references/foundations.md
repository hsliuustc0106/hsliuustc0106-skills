# Foundation guidance

Use only the sections needed for identified gaps. Suggested field names and locations are examples, not a mandatory filesystem layout. Prefer existing repository tooling over introducing another system.

## Navigation and architecture

Keep AGENTS.md or the existing contributor entrypoint short. Link to the source of truth rather than copying setup commands or architecture prose. Respect nested instructions. A navigation map should connect common changes to implementation and validation locations.

Describe component boundaries, inputs/outputs, invariants, compatibility constraints, and external contracts. Cite concrete implementation and tests separately from design proposals. Label discrepancies and unresolved questions; do not turn a proposal into an implemented guarantee. A behavior or contract change should update affected canonical architecture, API, and user documentation in the same PR. If deferred, record the explicit gap, tracked follow-up, and owner; do not auto-generate unverified documentation.

## Validation and ownership

Use a compact matrix in an existing contributor/testing document, for example:

| Change category / paths | Fast local check | Required broader check | Platform / environment | Evidence | Owner / unresolved handoff |
| --- | --- | --- | --- | --- | --- |

Populate commands from repository evidence. Include relevant negative, compatibility, performance, or cross-platform checks when justified by the change, not as universal requirements. Separate cheap presubmit checks from expensive or privileged runs. Record prerequisites, expected duration when measured, and the path for untestable platforms. Do not copy project-specific quotas or arbitrary test budgets into another repository.

An author can supply reproducible evidence. That does not transfer maintainer-owned L2 or equivalent integration/platform validation to the author, satisfy independent-review requirements, or confer merge authority. If the repository does not use L2, use its own terminology. CODEOWNERS identifies ownership; it alone does not prove who can approve or merge. Unavailable branch-protection or permission state stays unknown. Passing CI is necessary only where the repository says so and is never a substitute for required human approval.

## Lessons and independent recurrence

Use an existing lessons file or create one only if useful. A configurable default active limit is 200 lines; preserve stricter existing limits. Each lesson needs a concise rule, scope, supporting incident link, preventive check, and owner/status. Consolidate duplicates. Archive resolved or superseded detail with a short reference from the active file; preserve incident history.

Count independent failures, not observations: reruns, retries, duplicate issue reports, and multiple alerts from one incident count once. Record a stable incident key, provenance, suspected failure mechanism, and confidence; investigate uncertain identity before incrementing recurrence. Configure the escalation threshold for the repository (a proposed starting point is two independent incidents). When reached, propose a stronger regression test, invariant, tooling check, or design repair with an owner. Do not automatically change permissions, policies, or infrastructure. Keep an unresolved incident visible if archival would hide ongoing risk.

## Reliable execution and measurements

Prefer the repository's established scripts and CI. Capture revision, command, relevant tool versions/platform, start/end time, result, and artifact links. Checkpoint durable task state before handoff. Resume by reconciling current external state, not replaying prior writes.

Retry only transient, safe operations within a configured time/attempt budget. A retry cannot expand authorization. Diagnose deterministic failures; stop on access denial, exhausted budget, material scope changes, or required user decisions. Record blockers and the next safe action. Avoid parallel jobs that share mutable worktrees or conflicting resources.

Select metrics that answer a real improvement question: time to first useful feedback, cycle time, repeated independent incidents, flaky checks, or escaped regressions. Define event timestamps, denominators, observation window, and data source before reporting. Report unknowns and sample sizes. A merged PR is an outcome, not proof that a specific workflow caused improvement; observational comparisons do not establish causality.

## Read efficiency without stale decisions

Prefer a single metadata traversal and reuse its results within the run. Cache immutable sources by full commit SHA and diffs by both base and head SHA. Refresh mutable CI, reviews, and discussions independently of head changes or item updated_at timestamps; neither guarantees those sources are unchanged. Force a final refresh of the relevant gates before a consequential action. Honor rate-limit Retry-After/reset guidance and stop or wait within the task budget; never rotate identities to evade limits. Measure actual fetches, cache hits, and source coverage. An offline fixture can verify cache/reconciliation logic, but cannot substantiate remote latency or performance improvements.
