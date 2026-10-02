---
name: nanodot-review
description: Review ThinkFlowLab/nanodot pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# nanodot review

The [canonical source](https://github.com/ThinkFlowLab/nanodot/blob/main/.agents/skills/nanodot-review/SKILL.md) lives in `ThinkFlowLab/nanodot` at `.agents/skills/nanodot-review/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md), then run its `scripts/load_source.py nanodot --checkout /path/to/nanodot`. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Initial source migration: [project PR](https://github.com/ThinkFlowLab/nanodot/pull/29). Check its current state; use its source branch only while unmerged, then the maintained default branch.
