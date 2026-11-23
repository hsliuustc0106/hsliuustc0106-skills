---
name: repository-maintenance
description: Maintain and review software repositories with a consistent SOP for documentation, CI, contribution workflows, issue and PR labels, and requested fixes.
---

# Repository maintenance

Use this SOP for ongoing repository maintenance and cross-repository health
checks. Apply the user's requested scope and each repository's own instructions;
this skill does not replace project-specific guidance or establish a queue policy.

## 1. Establish scope and context

- Identify the requested repositories and actions. Work within the authorized
  workspace or connected repositories; do not treat the existence of other repos
  as a request to maintain them. Distinguish an inspection from a request to fix,
  review, or perform an external action.
- For each repository, read applicable agent and contributor instructions,
  discover relevant project-owned review or maintenance skills, and inspect
  enough code, tests, and CI configuration to understand the work. Identify
  the repository by its full remote identity when possible, not just the
  checkout directory name. Record the relevant revision and existing local
  changes before editing.
- Reuse project-specific skills and established triage rules. Resolve conflicts
  with the user's instructions and applicable project rules rather than
  imposing a shared label, priority, merge, or release policy.
- For changes to plugin integrations, inference engines, multimodal paths, or
  tutorials, read the relevant section of [shared development guidance](references/development.md).

## 2. Inspect and prioritize

For a general repository health check, cover documentation, CI and its levels,
the contribution/review-to-merge loop, and issue/PR labels. Use the
[health-check guide](references/health-check.md) for evidence and scope; include
other areas when requested or identified by the project as priorities. For a
targeted request, inspect only the relevant areas. Use the actual issue, PR
head, test result, or other evidence; a CI configuration is not an observed
successful run. Check pagination and freshness when the source requires it, and
report inaccessible or incomplete information instead of treating it as empty.

Prioritize actionable problems according to the user's goals and project rules.
For issues, distinguish a reproduced failure from a report or hypothesis. For
PRs, separate the current head and its evidence from older reviews or runs.
For repeat checks, compare with an available prior report or project tracker:
surface changed state and new heads, and avoid repeating completed actions.
Identify blockers and the next useful action rather than silently broadening the
requested work.

## 3. Perform requested work

- For fixes, follow the repository's development workflow, make the smallest
  useful change, and preserve unrelated work. Choose checks that exercise the
  affected behavior: static checks for structural rules, focused tests or
  reproductions for functional changes, and a representative runtime or user
  flow when appropriate and feasible. Capture screenshots, recordings, or other
  artifacts when they help verify the result. Report checks that could not run;
  configuration, mocks, or a single screenshot do not establish broader runtime
  correctness.
- When an observed failure could recur, consider preventing its class with a
  simpler API, type, focused regression test, or existing lint rule before
  adding another prose warning. Scope the guard to the demonstrated invariant,
  exercise a failing and a passing case, and wire it into an existing check
  when practical. Keep project-specific constraints project-specific.
- For reviews, inspect the diff, surrounding behavior, callers, and relevant
  tests; report evidence-backed, actionable defects with precise locations.
  Follow the review-source routing below before applying a general review.
- External comments, issue updates, PR creation, merging, releases, and scheduled
  jobs require the user's authorization for those actions. A health check or
  review alone does not authorize them.

## Review-source routing

Honor any project-owned review instructions and any more specific skill required
by applicable rules. For repositories listed in
[repository-review-source/sources.json](../repository-review-source/sources.json),
match the full repository identity, including configured rename aliases. For a
bundled public alias, read the matching [review overlay](references/project-reviews.md)
for its specific context and policies. Verify the identity, including any
documented rename, before using that alias. Then use
[repository-review-source](../repository-review-source/SKILL.md) to load the
canonical skill and needed references, recording their actual revisions and
hashes. Private mappings are considered only when supplied or configured for
the authorized context.

For reviews or skill/package changes in this skills repository, use its
[review overlay](references/projects/personal-skills/review.md) alongside this
SOP; its local review rules are not a mapped external canonical source.

If a required canonical source is missing or inaccessible, report that the
project-specific review is blocked; do not silently substitute a generic review
or a closed, unmerged source. If a required project overlay is missing, report
the gap instead of claiming its project-specific rules were applied. For an
explicitly configured personal daily brief, the matching overlay and its
selection policy are also required; if they are unavailable, report the brief
as blocked. Directly requested reviews do not inherit a daily queue's selection
filter.

Some explicitly configured personal briefs share a
[label/new-head selection contract](references/daily-label-queue.md). Apply it
only when the project's selection guidance links to it; the System1 override
and private queue have different contracts.

For an unmapped repository with no required project-specific review skill, use
the general review steps above and report any unavailable context. Do not apply
a different project's checklist merely because its repository name is similar.

## 4. Hand off consistently

Summarize each repository separately: the scope and revision or observation
time, findings in priority order, actions taken, verification and its limits,
and the next action or blocker. For general health checks, distinguish findings,
no findings within the inspected scope, unknowns, and areas not inspected for
each of the four priorities. Do not describe unavailable information as a clean
result or a planned action as completed.
