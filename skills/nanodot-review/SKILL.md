---
name: nanodot-review
description: Review ThinkFlowLab/nanodot pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# nanodot review

The [canonical source](https://github.com/ThinkFlowLab/nanodot/blob/main/.agents/skills/nanodot-review/SKILL.md) lives in `ThinkFlowLab/nanodot` at `.agents/skills/nanodot-review/SKILL.md`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md). With a local checkout, run its `scripts/load_source.py nanodot --checkout /path/to/nanodot`; without one, follow its Connected GitHub path to read the canonical skill and needed references at one resolved commit. Read the returned canonical skill and its relevant references before reviewing. Record the actual commit and content hash loaded, and honor its selection, evidence, and posting boundaries. If the canonical skill is still on a draft PR branch, use that branch explicitly; do not claim it exists on main. Missing source must be reported, never silently replaced with generic guidance.

Source migration [PR29](https://github.com/ThinkFlowLab/nanodot/pull/29) merged on 2026-10-03. Resolve the maintained default branch at review time; the bounded audit pin is not a freshness guarantee.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). Its offline adapter enforces the exact labels, verified new commits, distinct-PR daily cap, and delivery deduplication. It does not replace the canonical review checklist. Directly requested PR reviews bypass this daily filter.
