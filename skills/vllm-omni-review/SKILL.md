---
name: vllm-omni-review
description: Review vllm-project/vllm-omni pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# vllm-omni review

The [canonical source](https://github.com/vllm-project/vllm-omni/blob/main/.claude/skills/review-pr/SKILL.md) lives in `vllm-project/vllm-omni` at `.claude/skills/review-pr/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py vllm-omni --checkout /path/to/vllm-omni`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Initial source migration: [project PR](https://github.com/vllm-project/vllm-omni/pull/8410). Check its current state; use its source branch only while unmerged, then the maintained default branch.
