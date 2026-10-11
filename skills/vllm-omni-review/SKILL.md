---
name: vllm-omni-review
description: Review vllm-project/vllm-omni pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# vllm-omni review

The [canonical source](https://github.com/vllm-project/vllm-omni/blob/main/.claude/skills/review-pr/SKILL.md) lives in `vllm-project/vllm-omni` at `.claude/skills/review-pr/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py vllm-omni --checkout /path/to/vllm-omni`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

The canonical skill already exists on the maintained default branch. The
[proposed helper/backend extension](https://github.com/vllm-project/vllm-omni/pull/8410)
is separate: an open proposal does not make its older head the default source.
Use that branch only when explicitly reviewing or evaluating the proposal, and
record its draft provenance separately. See the dated maintenance audit below.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). Its offline adapter enforces the exact labels, new-head evidence, daily cap, and delivery deduplication; it does not replace the canonical review checklist. Directly requested PR reviews do not use this daily filter.
