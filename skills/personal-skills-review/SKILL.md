---
name: personal-skills-review
description: Review changes to hsliuustc0106/hsliuustc0106-skills for discoverability, source ownership, packaging integrity, and tested helper behavior.
---

# Personal skills repository review

Read AGENTS.md and the actual diff at the requested head. Trace a skill change through `.claude-plugin/plugin.json`, `scripts/sync-project.sh`, `AGENTS.md`, `CLAUDE.md`, and relevant Cursor rules; a correct document that is never installed or discovered is incomplete.

Project review content belongs to its project repository. Personal wrappers should point through `repository-review-source`, without copied checklists or nonportable symlinks. Verify canonical paths against actual source revisions, and report pending draft branches separately from merged defaults. Never copy private mappings or source content into this public repository.

For installer edits verify complete preflight before writes, unchanged idempotent installs, conflict refusal, explicit force behavior, and refusal of file/symlink collisions. Include every referenced resource and runtime dependency. Run `python3 -m unittest discover -s tests -v`; distinguish local offline fixtures from live GitHub or GPU validation.

For review helper edits test actual pagination/filter/head-ledger behavior and failure cases, not wording-only checks. Respect source-owned daily eligibility: unknown labels, no eligible PRs, and unseen revisions must not silently broaden scope. A loader must identify the exact source bytes read and fail visibly for missing/wrong checkouts.

Post only evidence-backed actionable comments when authorized. Loading this skill does not authorize posting, pushing, or merging. Direct-main permission for this personal repository does not apply to project repositories.
