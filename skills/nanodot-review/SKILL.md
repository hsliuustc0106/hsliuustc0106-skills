---
name: nanodot-review
description: Review pull requests or local branches in ThinkFlowLab/nanodot, grounding findings in the exact source snapshot, deterministic watch behavior, permission boundaries, persistence, and tests. Use for nanodot code review or explicitly requested batch review selection, not general implementation or reviews of other repositories.
---

# nanodot Review

Review `ThinkFlowLab/nanodot` with the evidence-first structure of the bundled
vLLM-Omni review skill, adapted to nanodot's actual contracts. Keep findings short,
actionable, and high-confidence. Zero findings is a valid result.

## Start from the right snapshot

- For a PR, pin base and head SHAs, state, changed paths, complete diff, and current
  discussions/checks. For a local branch, identify the named base and merge base.
- With no PR/branch or explicit batch-selection request, ask for the target.
- Read repository instructions at the target SHA. Never treat a design proposal,
  open integration branch, future port, or green CI as proof of main behavior.
- The [source map](references/architecture.md) separates the verified main scaffold
  from the unmerged MVP. Refresh those pins before relying on current-state claims.
- API errors, incomplete pages, hidden required checks, and missing test execution
  remain **unknown**, not clean, empty, absent, or successful.

## Review workflow

1. Skim the diff, then load only matching [review routes](references/review-routing.md).
   Inspect callers and tests before alleging a defect. For broad diffs, independent
   read-only reviewers may investigate separate areas; verify their findings.
2. Apply [blocker patterns](references/blocker-patterns.md) to touched contracts:
   deterministic outcome, scope/permission enforcement, state/delivery ordering,
   interruption/replay, and untrusted data. Do not invent missing runtime code on main.
3. Run affected tests using the target's configuration and the
   [test-quality checklist](references/test-quality-evaluation.md). Report what ran,
   failed, skipped, or was not tested. Static inspection is not runtime validation.
4. Ground every finding in an exact head, changed path/line, reachable trigger,
   wrong observable outcome, and smallest correction or concrete missing test.
   Check existing discussions for duplicates; suppress already-fixed/stale findings.
5. Use [execution and severity guidance](references/review-execution.md) to deliver
   only substantiated defects. A missing test or speculative edge case alone is not
   automatically blocking. Keep coverage gaps separate from findings.

## Batch selection (only when requested)

Use [selection policy and helper](references/selection-policy.md). Its label rule is
repository-catalog based: if `ready` exists, require `high priority` **and** `ready`;
otherwise require `high priority`. Inspect every page. Review only a new head since
its prior completed review; at most 10 completed review jobs per repository per
Asia/Shanghai day. Deduplicate `(repo, PR, head, policy)`.

There is no PR-creation-age cutoff and no permanent "ever reviewed" exclusion.
Selection is read-only and does not mark a head reviewed. Reserve work atomically
when multiple workers share a ledger; this helper does not provide distributed locks.

## Delivery and authorization

Return a concise local review first: findings by severity, exact source anchors,
validation, and untested scope. Do not approve, request changes, comment, merge,
close, mutate upstream code, or install tools merely because this skill is loaded.
External actions need the user's authorization for that action and target.

Immediately before an authorized post, refetch head/state, required-check evidence,
and discussions. If the head changed, stop posting, discard old coordinates, and
review the new diff; do not transfer old findings by line number alone. The helper's
`--revalidate` mode checks the selected head and open state. Rerun selection for
current labels and ledger capacity; neither replaces code, CI, or duplicate-comment
verification.

## Skill validation

The [evaluation contract](references/evaluation.md) describes the small pinned
regression corpus and its limits. Run network-free helper, packaging, routing,
and grounding tests from the skills repository:

```bash
python3 -m unittest discover -s tests -v
```

This skill does not require GPU/model execution, live notifications, credentials,
or provider API calls. Test those only when relevant and separately authorized.
