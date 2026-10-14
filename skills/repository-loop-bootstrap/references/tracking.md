# Persistent tracking semantics

Use this when PR/issue monitoring or resumable review is needed. Reuse an existing tracker and storage format if it preserves these invariants. For a bootstrap without remote access, propose the record shape and test it locally; do not create watchers or webhooks automatically.

## State implementation and completion

Record the actual level: design/schema only; manual durable records with tested read/write/restart behavior; or an installed runner with observed reconciliation and delivery behavior. These levels are not interchangeable. A schema or documented scenario does not implement persistent monitoring. A manual workflow can satisfy a deliberately manual scope, but cannot satisfy a requested automated runner. For a full bootstrap, explicitly report a missing required runner as blocked/deferred with its authorization and deployment prerequisites; never hide the gap behind a successful documentation test. Do not install hooks, webhooks, schedules, permissions, or external runners without their required target-specific authorization.

## Minimal adaptable record

A plain local JSON file is sufficient for a small workflow; an established database may be better for concurrent writers. A record should retain:

- Stable repository identity and PR or issue identifier, canonical URL when known.
- Observation time and source; current open/closed/merged state, base and head SHA for PRs.
- Check identities, run/attempt IDs, status/conclusion, checked SHA, timestamps, platform, and evidence links. Store review decisions with their actual scope and revision where available.
- Requirements and owners separately from author evidence; missing or blocked checks and unresolved authority.
- Linked issues/PRs, dependencies, next action, and last reconciled state.
- For issue-resolution work, acceptance conditions and their individual evidence/status, including residual scope, owner, and follow-up. Keep source issue claims separate from verified behavior.
- Reusable evidence references: artifact identity, source revision, relevant base/merge revision, command/check and inputs, environment, result, and applicability limits. Several consumers may cite one artifact; citations are not independent executions.
- An action ledger: stable dedup key, target, purpose, evidence version, status (planned/in-flight/confirmed/uncertain), external result ID if available, and timestamps.

Issues have no inherent head SHA. Link them to PRs and the relevant revisions without manufacturing an issue head. A closed issue or merged PR is not evidence that all linked tasks are complete.

Reuse evidence only while its relevant inputs and scope still match. Preserve old artifacts as history; invalidate affected applicability when code, base/merge context, check inputs, or environment changes. Immutable test evidence does not replace refreshing mutable approval, CI, or permission state. Do not create a second ledger solely to connect implementation, review, and issue triage.

## Reconciliation rules

1. Read current state before deciding. Use stable repository + item IDs rather than titles. Mark unavailable observations stale; retain the last known result and its age without presenting it as current.
2. On a head change, keep old evidence as history but invalidate its applicability to the new head. Recompute validation needs; respect the repository's review-dismissal policy rather than assuming reviews survive or vanish.
3. On the same head, still reconcile checks, rerun attempts, reviews, base changes, requirements, and mergeability. A completion, failure, or cancellation can arrive without a commit. Base/merge-result changes may require additional validation even if the head is unchanged.
4. Bind actions to a meaningful state transition and target. A possible key is repository/item + action type + relevant evidence version, where evidence version includes check run/attempt and conclusion or review changes, not only head SHA. Repeated observations of the same transition must not repeat comments, retries, or notifications.
5. Persist intent before a permitted external write and reconcile its returned identifier afterward. If the result is uncertain, inspect the destination before retrying; deduplication is not proof of exactly-once delivery. Serialize updates or use atomic replacement/locking appropriate to the chosen store. Do not store secrets or unnecessary personal data.
6. Recheck head and relevant gates immediately before any separately authorized merge or other consequential action. A record is evidence, not authorization.

## Tiny local acceptance scenario

Use an isolated fixture and simulated observations; no service account or live PR is necessary.

- Observe PR 7 at head A with CI run 10 pending. Persist it, restart/read the state, and retain its next action.
- Observe head A with run 10 failed. Update the evidence and make a new proposed action eligible even though the SHA did not change.
- Observe the same failure again. The existing action key prevents a duplicate action.
- Observe head A with rerun 11 successful. Store its own evidence and supersede the old CI status; required review and platform ownership remain separate.
- Observe head B. Evidence for A cannot satisfy B. Preserve A's history.
- Observe two retries of one incident and a distinct later incident. The recurrence count is two, not four.

If no tracker implementation was requested, a documented dry-run of these transitions is sufficient. Do not claim that it validates an absent automation or guarantees remote delivery.
