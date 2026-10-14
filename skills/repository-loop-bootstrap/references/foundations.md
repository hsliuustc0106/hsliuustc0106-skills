# Foundation guidance

Use only the sections needed for identified gaps. Suggested field names and locations are examples, not a mandatory filesystem layout. Prefer existing repository tooling over introducing another system.

## Navigation and architecture

For a full bootstrap, create or update root AGENTS.md as the default agent entrypoint and CONTRIBUTING.md as the human entrypoint; if an established equivalent exists, link to it rather than duplicate it. Both must lead to canonical architecture/contracts, setup/testing and validation matrix, review/merge rules, and lessons. Keep the entrypoints short, with explicit instructions to read the relevant canonical guidance before changing code and consult lessons for the affected area.

Inspect applicable nested AGENTS.md, existing CLAUDE.md, repository skills, and other configured tool instructions. Wire existing applicable consumers to the same canonical guidance without overwriting their scope or adding tool files for tools the project does not use. Verify the load chain from each actual entrypoint and record any tool-specific discovery limitation. A link makes guidance traversable, not necessarily automatically loaded: claim automatic consumption only if that tool's applicable behavior/configuration was verified. A repository skill's mere existence does not prove agents invoke it. Respect nested instruction precedence; surface contradictory rules. A navigation map should connect common changes to implementation and validation locations.

Before marking architecture, system contracts, or code regulations current, pin the inspected revision and read their bodies, not only their links. Declare risk-based coverage: prioritize public behavior, defaults, required invariants, validation commands, ownership/approval rules, and claims affected by recent changes. Compare each reviewed claim with concrete code, configuration, and tests; record unreviewed sections and conflicting evidence rather than implying exhaustive alignment. Classify described capabilities as implemented, default-enabled, optional/disabled, or planned, preserving relevant qualifiers. Source inspection supports alignment claims, not proof of executed runtime behavior.

Record whether each reviewed document/section is unchanged-and-verified, refreshed, or unresolved, with revision and evidence paths. Preserve explicitly dated historical audits as historical records; add a dated current clarification or follow-up where appropriate rather than silently updating their date or rewriting the past. A completed link/load-chain check, a substantive content audit, and executed runtime validation are three different results.

Describe component boundaries, inputs/outputs, invariants, compatibility constraints, and external contracts. Cite concrete implementation and tests separately from design proposals. Label discrepancies and unresolved questions; do not turn a proposal into an implemented guarantee. A behavior or contract change should update affected canonical architecture, API, and user documentation in the same PR. If deferred, record the explicit gap, tracked follow-up, and owner; do not auto-generate unverified documentation.

## Validation and ownership

Use a compact matrix in an existing contributor/testing document, for example:

| Change category / paths | Fast local check | Additional check, if applicable; requirement status | Platform / environment | Evidence | Owner / unresolved handoff |
| --- | --- | --- | --- | --- | --- |

Choose checks from this repository’s objectives, change risks, available infrastructure, cost, and responsible owners. Label each as existing-required, available-optional, or proposed-new, with supporting evidence; keep unknown requirements explicit. Missing infrastructure is a limitation, not an automatic new requirement. Verify what commands execute and where; job names alone do not establish hardware or runtime coverage. Populate commands from repository evidence. Include relevant negative, compatibility, performance, or cross-platform checks when justified by the change, not as universal requirements. Separate cheap presubmit checks from expensive or privileged runs. Record prerequisites, expected duration when measured, and the path for untestable platforms. Do not copy project-specific quotas or arbitrary test budgets into another repository.

Author evidence does not change validation ownership or approval authority established by this repository. Preserve its actual division of responsibility without introducing another project’s test tiers or gates. CODEOWNERS identifies ownership; it alone does not prove who can approve or merge. Unavailable branch-protection or permission state stays unknown. Passing CI is necessary only where the repository says so and is never a substitute for required human approval.

## Lessons and independent recurrence

For a full bootstrap, create or wire a discoverable lessons.md by default. If an existing canonical lessons store uses another path/name, link it from the requested entrypoint rather than copying lessons; an explicit user-requested filename should still have a small pointer when useful. Set the active limit to 200 lines by default, configurable by the user; preserve stricter existing limits. Wire lessons from agent and human entrypoints and tell contributors when to consult and update it.

With no verified incidents, create an honest empty structure: purpose, active limit, consultation/update rule, entry fields, and archive location/convention, followed by “No verified lessons recorded yet.” Do not manufacture incidents to fill a template or count a hypothetical fixture scenario as a real event. Each actual lesson needs a concise rule, scope, supporting incident link/key, preventive check, and owner/status. Consolidate duplicates. Archive resolved or superseded detail with a short reference from the active file; preserve incident history.

Count independent failures, not observations: reruns, retries, duplicate issue reports, and multiple alerts from one incident count once. Record a stable incident key, provenance, suspected failure mechanism, and confidence; investigate uncertain identity before incrementing recurrence. Use an existing repository escalation policy if one is established; otherwise leave the trigger for human policy selection rather than inventing a numeric default. When the selected policy applies, propose a proportionate regression test, invariant, tooling check, or design repair with an owner. Label an unapproved escalation policy as proposed; do not adopt it as binding merely because it appears in this skill. Preserve existing human approval for resulting policy or consequential changes. Do not automatically change permissions, policies, or infrastructure. Keep an unresolved incident visible if archival would hide ongoing risk.

Prefer the narrowest prevention supported by the failure: a focused regression check or local clarification before a shared rule, and a shared rule before new infrastructure when those remedies fit. A confirmed first incident can justify a local fix; broader escalation needs evidence of its scope or consequence, not an invented recurrence threshold. Retire or consolidate guidance that no longer prevents a demonstrated failure.

## Reliable execution and measurements

Prefer the repository's established scripts and CI. Capture revision, command, relevant tool versions/platform, start/end time, result, and artifact links. Checkpoint durable task state before handoff. Resume by reconciling current external state, not replaying prior writes.

Retry only transient, safe operations within a configured time/attempt budget. A retry cannot expand authorization. Diagnose deterministic failures; stop on access denial, exhausted budget, material scope changes, or required user decisions. Record blockers and the next safe action. Avoid parallel jobs that share mutable worktrees or conflicting resources.

Select metrics that answer a real improvement question: time to first useful feedback, cycle time, repeated independent incidents, flaky checks, or escaped regressions. Define event timestamps, denominators, observation window, and data source before reporting. Report unknowns and sample sizes. A merged PR is an outcome, not proof that a specific workflow caused improvement; observational comparisons do not establish causality.

## Read efficiency without stale decisions

Prefer a single metadata traversal and reuse its results within the run. Cache immutable sources by full commit SHA and diffs by both base and head SHA. Refresh mutable CI, reviews, and discussions independently of head changes or item updated_at timestamps; neither guarantees those sources are unchanged. Force a final refresh of the relevant gates before a consequential action. Honor rate-limit Retry-After/reset guidance and stop or wait within the task budget; never rotate identities to evade limits. Measure actual fetches, cache hits, and source coverage. An offline fixture can verify cache/reconciliation logic, but cannot substantiate remote latency or performance improvements.
