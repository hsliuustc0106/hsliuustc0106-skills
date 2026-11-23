# Repository health-check guide

Use these four priorities for a general health check. For targeted work, use
only the relevant sections. Discover the repository's own conventions and
record the scope and evidence; do not infer a shared CI taxonomy, label policy,
review requirement, or merge authority across projects.

## Documentation system

- Find the human and agent entrypoints and the canonical setup, architecture,
  API, testing, and contribution guidance relevant to the work. Check whether
  the intended audience can reach it; check representative links and verify
  commands when practical.
- Compare a risk-based sample of important claims with implementation, tests,
  and configuration at the inspected revision. Distinguish current behavior,
  optional features, plans, and historical records; name unreviewed areas.
- When behavior changes, update the affected canonical docs or identify a
  concrete follow-up. Preserve existing documentation structure and owners.

## CI and validation levels

- Identify the project's actual levels or suites, their triggers and scope,
  relevant platforms and prerequisites, and which changes they cover. These may
  include static, unit, integration, end-to-end, nightly, or hardware checks;
  use the project's own names and requirements rather than inventing tiers.
- Separate workflow configuration, required checks or branch protection when
  observable, and actual run results. For a PR, identify the tested commit or
  merge ref and its relationship to the current head and base; report failed,
  pending, skipped, unavailable, and untriggered checks accurately. Distinguish
  mocked checks from live or hardware evidence.
- Identify gaps or unreliable checks with evidence and a practical next step.
  If access, execution, or requirements are unknown, say so instead of assuming
  success or failure.

## Contribution and review-to-merge loop

- Trace the established path from issue or proposal through implementation,
  author validation and self-review, PR preparation, reviewer feedback,
  approvals, CI, merge, and follow-up. Locate its canonical instructions and
  distinguish contributor, reviewer, and maintainer responsibilities.
- For the requested PRs, inspect the current head and relevant open feedback,
  review state, checks, and merge conditions. An old approval, a configured job,
  or CODEOWNERS alone does not prove that the current head meets the actual
  requirements. Treat unavailable branch protection or permissions as unknown.
- Report blockers and the next responsible action. Follow existing issue closure
  and post-merge conventions; do not infer that a merged PR completes an issue
  when its acceptance criteria or remaining work say otherwise.

## Issue and PR label system

- Inspect the complete available label catalog and applicable triage guidance.
  Determine exact spelling, meaning, ownership, and any effects on routing or
  automation; common categories may include priority, type, area, and state,
  but their names and meanings are repository-specific.
- Compare relevant open issues and PRs with those conventions. Surface missing,
  ambiguous, contradictory, stale, or ineffective labels only when supported by
  the repository's actual policy and current state. Distinguish issue/PR labels
  from Git release tags.
- Respect configured queue filters and personal overrides. Directly requested
  reviews are not constrained by a daily queue's selection filter. Do not
  create, remove, or apply labels without authorization.

## Report coverage

For each repository and each applicable priority, state the inspected scope,
revision or observation time, evidence paths or links, actionable findings or no
findings within that scope, and the next action. Mark inaccessible, incomplete,
and uninspected areas explicitly; a missing page or unavailable permission is
not a clean result. Separate actual changes and executed checks from proposals.
