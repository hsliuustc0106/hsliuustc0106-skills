# Evidence, Provenance, and Status

Use this reference for every analysis. The report must make it possible for a reader to distinguish what exists, what was measured, what was calculated, and what is only proposed.

## Contents

- [Evidence ledger](#evidence-ledger)
- [Evidence classes](#evidence-classes)
- [Source precedence](#source-precedence)
- [Support status vocabulary](#support-status-vocabulary)
- [Orthogonal runtime state](#orthogonal-implementation-and-validation-state)
- [Conflicts and confidence](#resolving-conflicts)

## Evidence ledger

Assign stable IDs (`E1`, `E2`, ...) while researching. Record:

| Field | Required content |
|---|---|
| ID | Stable evidence ID used beside claims |
| Claim/use | The narrow fact the source supports |
| Source | Pinned code permalink, test, recipe, release, paper, model card, issue, or local path |
| Revision/date | Commit, tag, version, publication date, or access date |
| Class | One of the evidence classes below |
| Confidence | `High`, `Medium`, or `Low`, with a reason when not high |
| Notes | Scope, workload, hardware, conflict, or limitation |

Do not make one evidence row support a broader claim than the source does. Cite `[E#]` beside important statements and table cells, then expand each ID in the Evidence Index.

Cite multiple sources as individual IDs such as `[E1] [E2]`; do not use an ID range such as `[E1-E3]` because it obscures which ledger rows support the claim.

## Evidence classes

- `Observed`: directly inspected code, configuration, checkpoint metadata, test definition, or another static artifact; it does not claim an execution result.
- `Measured`: an executed smoke, benchmark, profiler trace, accuracy result, or end-to-end run with a recorded environment and workload.
- `Reported`: a primary maintainer/vendor source reports the result, but it was not reproduced in this analysis.
- `Community-reported`: a third party reports the result; record missing environment or workload details and normally use medium or low confidence.
- `Derived`: transparent calculation from cited inputs. Show the formula and assumptions.
- `Estimated`: capacity or performance projection that has not been validated on the target configuration.
- `Proposed`: future implementation or optimization direction.

Do not label an issue checklist `Observed`; it is `Reported` planning state until current code or tests corroborate it.

For mutable runtime features, also record `effective_on_revision`, plus `superseded_by` or `reverted_by` when applicable. A merged change is not necessarily active on the target revision.

## Source precedence

Use the most specific current evidence, not simply the newest prose. A practical order is:

1. Reproduced run on the exact revision, hardware, and workload.
2. Current code plus an automated correctness, accuracy, or performance test.
3. Current code plus an official, hardware-specific recipe or release artifact.
4. Current registry, support table, or official documentation.
5. Merged pull request or release note when the target revision contains it.
6. Open pull request, roadmap issue, maintainer comment, or vendor claim.
7. Community report or architectural inference.

Lower-ranked evidence can add detail but cannot override stronger contradictory evidence without explanation.

Current negative evidence—such as a reproducible crash, accuracy regression, reverted path, or explicit task exclusion—can narrow or downgrade an older positive claim when revision and scope match. Preserve both entries and explain which is effective on the target revision.

## Support status vocabulary

Use exactly these labels in support matrices:

- `Supported`: the scoped capability is present at the pinned revision and has direct evidence appropriate to the claim.
- `Partial`: some tasks, modes, shapes, precisions, or platforms work, but the scoped capability is incomplete or constrained.
- `Unsupported`: current code or authoritative documentation explicitly excludes the capability, or a reproducible blocker prevents it.
- `Unverified`: evidence is absent, stale, contradictory, or too weak to decide.
- `N/A`: the capability does not apply to this architecture or scope.

Never use an empty cell to mean unsupported. Empty cells hide uncertainty.

## Orthogonal implementation and validation state

For vLLM-Omni and other evolving runtimes, do not compress lifecycle state into support status.

Use one implementation state:

- `Unknown` — implementation evidence was unavailable or not inspected.
- `Absent`
- `Proposed`
- `PR open`
- `Merged/present`
- `Superseded`
- `Reverted`

Record validation evidence as an unordered set of scoped gates rather than a single maturity level. In the support matrix, join multiple gates with semicolons and use the canonical labels below:

- `Unknown`
- `No evidence found`
- `Unit`
- `Contract`
- `Smoke`
- `Recipe-validated`
- `Accuracy/quality`
- `Benchmark`
- `Recurring CI`
- `Production exercise`

Then assign support status for the exact task/API/platform scope. For example, a path can be `Merged/present`, `Smoke; Accuracy/quality`, and `Partial` on one backend. Record each gate's task and platform; recurring unit CI does not supersede a one-off accuracy result. Record the effective revision and link later changes that supersede or revert the original implementation.

Use `Absent` only when current primary evidence establishes absence. Use `Unknown — <reason>` when the relevant repository, test, or history could not be inspected; do not turn missing access into `Absent` or `No evidence found`.

Never aggregate materially different device families into one support cell. If Ascend A2 and A3, or NVIDIA consumer and datacenter architectures, have different evidence, create separate rows and then state any broader conclusion as `Unverified` or appropriately narrowed.

## Resolving conflicts

When sources disagree:

1. Confirm they refer to the same revision, task, API, precision, and hardware.
2. Prefer direct, scoped evidence over a broad table.
3. Add a conflict note with both evidence IDs.
4. Narrow the conclusion to what is jointly defensible.
5. Mark the broader conclusion `Unverified` until the discrepancy is resolved.

Example: a hardware recipe with a measured run and a support table with an empty cell do not justify silently choosing either “supported” or “unsupported.” Report the recipe-validated task, the documentation inconsistency, and the missing CI or support-table alignment.

## Confidence

- `High`: current primary evidence directly matches the claim's revision and scope.
- `Medium`: primary evidence is indirect, reported rather than reproduced, or misses one material dimension.
- `Low`: inference, community evidence, unresolved conflict, or an unvalidated estimate.

Confidence describes evidence strength, not implementation quality.
