---
name: sciencediscovery-review
description: Review openJiuwen-ai/sciencediscovery pull requests using its canonical repository-owned review skill. Use for this project's review, evidence checks, and PR triage.
---

# sciencediscovery review

The configured repository-owned entrypoint is `.agents/skills/sciencediscovery-review/SKILL.md` in `openJiuwen-ai/sciencediscovery`. Do not maintain a second review checklist here.

Load [repository-review-source](../repository-review-source/SKILL.md) and resolve the entrypoint at the current authorized revision. With a local checkout, run its `scripts/load_source.py sciencediscovery --checkout /path/to/sciencediscovery`; without one, follow its Connected GitHub path. Read the canonical skill and needed references at one immutable revision. Record the revision and content hash. **If main has no entrypoint and no maintained replacement can be verified, report the project-specific review as blocked. A closed, unmerged source PR is historical, not a fallback.** Do not apply a sibling development or CI skill as a substitute.

## Source and evidence checkpoint (2026-11-19 Asia/Shanghai)

- The initial [source migration #231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231) closed without merge on Nov 16, and its head ref was deleted. The configured file and root `AGENTS.md` are absent at [audited main `d57fc26`](https://github.com/openJiuwen-ai/sciencediscovery/commit/d57fc2693e0972b5c1040d47a4b74370eb011c3f). This replaces the November 12 draft-source routing in the maintenance history. Re-resolve on the next pass rather than treating this dated absence as permanent.
- The complete catalog had 57 labels, including exact `ready` and neither `high priority` nor `high-priority`; the 41 open PRs included none with exact `ready` or `high priority`. The personal queue has no eligible candidates under the unchanged conjunction; this does not make canonical instructions available. Both catalogs were enumerated through the empty second page.
- Distinguish [stable v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0), [v0.4.0-rc1](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.4.0-rc1) (built from `5cac2ce590f09f97164f4528c034170dbc5d1c63`), and Nightly. Main and the RC have diverged (99 main-only and 5 RC-only commits at this pin). For Windows, [#1194](https://github.com/openJiuwen-ai/sciencediscovery/pull/1194) separates test and typecheck status and disables implicit installer publishing. The [Nov 18 Nightly job](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/44199315530) verifies package build/upload and desktop checks, not installed chat recovery or prevention of duplicate tool execution. Read the exact build and job steps instead of inferring runtime acceptance from a green Nightly.
- Bounded audit: 173 commits and 430 changed paths since the previous audited main. Inspected loader provenance, release/tag ancestry, current contribution guidance, and the Windows packaging evidence above, not every changed product path. All 13 open PRs in the skills repository were checked for path overlap; none touched this skill.

For the explicitly configured personal daily brief, also read [selection and maintenance evidence](references/maintenance.md). This supplement applies the configured exact `high priority` label (which differs from the canonical draft's `high-priority`), new-head evidence, daily cap and delivery deduplication. It does not replace the canonical review checklist. Directly requested PR reviews bypass this daily filter.
