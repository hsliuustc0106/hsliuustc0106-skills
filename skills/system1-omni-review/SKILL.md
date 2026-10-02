---
name: system1-omni-review
description: Review ThinkFlowLab/system1-omni pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# system1-omni review

The [canonical source](https://github.com/ThinkFlowLab/system1-omni/blob/main/.agents/skills/system1-omni-review/SKILL.md) lives in `ThinkFlowLab/system1-omni` at `.agents/skills/system1-omni-review/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py system1-omni --checkout /path/to/system1-omni`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.
