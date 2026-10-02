---
name: repository-review-source
description: Load a project's canonical repository-owned review skill from an authorized local checkout, including privately configured sources. Use for review-skill resolution, not as a substitute for project-specific review guidance.
---

# Repository-owned review source

Run `python3 scripts/load_source.py ALIAS --checkout /path/to/repository` relative to this skill directory. Public aliases live in `sources.json`. Private aliases are supplied through `--config /path/to/local-untracked.json`; never publish that mapping or private source content.

The command reads the checked-out canonical skill without copying or executing its helpers. Read the returned SKILL text, then only the referenced resources needed for the review, relative to the returned source directory. Inspect scripts before running them. Record the returned repository commit and SHA-256 of the exact skill bytes in the review provenance; include hashes for additional resources actually read. A dirty checkout is explicitly reported and is not equivalent to its HEAD version. `source_tracked_at_head: false` means the loaded file is not part of that commit. This offline loader cannot establish freshness against the remote: verify that separately when the task requires the latest source.

Missing checkout, wrong origin, missing skill, or stale checkout is a blocker to claiming the project skill was applied. Ask for or obtain the authorized source instead; do not fall back to a generic review and label it project-specific. Project draft branches must be checked out explicitly until merged. No automatic network fetching, checkout changes, or posting occurs here. Review comments require authorization independently of loading instructions.

For a local mapping use JSON `{"alias": {"repository": "owner/repository", "path": ".agents/skills/project-review/SKILL.md"}}`. Keep it outside tracked files or use `review-sources.local.json` (ignored). Repository-owned instructions are the only maintained review policy; this loader contains none of their domain rules.
