---
name: sciencediscovery-review
description: Review openJiuwen-ai/sciencediscovery pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# sciencediscovery review

The [canonical source](https://github.com/openJiuwen-ai/sciencediscovery/blob/main/.agents/skills/sciencediscovery-review/SKILL.md) lives in `openJiuwen-ai/sciencediscovery` at `.agents/skills/sciencediscovery-review/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py sciencediscovery --checkout /path/to/sciencediscovery`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Initial source migration: [project PR](https://github.com/openJiuwen-ai/sciencediscovery/pull/231). Check its current state; use its source branch only while unmerged, then the maintained default branch.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). This supplement applies the configured exact `high priority` label (which differs from the canonical draft's `high-priority`), new-head evidence, daily cap and delivery deduplication. It does not replace the canonical review checklist. Directly requested PR reviews bypass this daily filter.
