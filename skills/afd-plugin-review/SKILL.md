---
name: afd-plugin-review
description: Review vllm-project/afd-plugin pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# afd-plugin review

The [canonical source](https://github.com/vllm-project/afd-plugin/blob/main/.agents/skills/review-pr/SKILL.md) lives in `vllm-project/afd-plugin` at `.agents/skills/review-pr/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py afd-plugin --checkout /path/to/afd-plugin`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Initial source migration: [project PR](https://github.com/vllm-project/afd-plugin/pull/420). PR #420 is closed without merge as of the 2026-10-27 Asia/Shanghai audit. The canonical source is available on the maintained default branch. Do not select a closed migration branch merely because it is unmerged; any draft-source exception requires a currently open source PR and explicit applicable authorization.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). Its offline adapter enforces exact labels, new-head evidence, the daily cap, and delivery deduplication; it does not replace the canonical review checklist. Directly requested PR reviews do not use this daily filter.
