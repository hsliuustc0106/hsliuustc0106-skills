---
name: router-review
description: Review vllm-project/router pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# router review

The [canonical source](https://github.com/vllm-project/router/blob/main/.agents/skills/review-pr/SKILL.md) lives in `vllm-project/router` at `.agents/skills/review-pr/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py router --checkout /path/to/router`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Initial source migration: [project PR](https://github.com/vllm-project/router/pull/336). Check its current state; use its source branch only while unmerged, then the maintained default branch.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). Its offline adapter enforces exact labels, new-head evidence, the daily cap, and delivery deduplication; it does not replace the canonical review checklist. Directly requested PR reviews do not use this daily filter.
