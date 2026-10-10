---
name: repository-review-source
description: Load a project's canonical repository-owned review skill from an authorized local checkout, including privately configured sources. Use for review-skill resolution, not as a substitute for project-specific review guidance.
---

# Repository-owned review source

Use either an authorized local checkout or the connected GitHub read API. No local checkout is required for connector-only reviews.

## Local checkout

Run `python3 scripts/load_source.py ALIAS --checkout /path/to/repository` relative to this skill directory. Public aliases live in `sources.json`. Private aliases are supplied through `--config /path/to/local-untracked.json`; never publish that mapping or private source content.

The command reads the checked-out canonical skill without copying or executing its helpers. Read the returned SKILL text, then only the referenced resources needed for the review, relative to the returned source directory. Inspect scripts before running them. Record the returned repository commit and SHA-256 of the exact skill bytes in the review provenance; include hashes for additional resources actually read. A dirty checkout is explicitly reported and is not equivalent to its HEAD version. `source_tracked_at_head: false` means the loaded file is not part of that commit. This offline loader cannot establish freshness against the remote: verify that separately when the task requires the latest source.

Missing checkout, wrong origin, missing skill, or stale checkout is a blocker to claiming the project skill was applied. Ask for or obtain the authorized source instead; do not fall back to a generic review and label it project-specific. Project draft branches must be checked out explicitly until merged. No automatic network fetching, checkout changes, or posting occurs here. Review comments require authorization independently of loading instructions.

For a local mapping use JSON `{"alias": {"repository": "owner/repository", "path": ".agents/skills/project-review/SKILL.md"}}`. Keep it outside tracked files or use `review-sources.local.json` (ignored). Repository-owned instructions are the only maintained review policy; this loader contains none of their domain rules.

The project installer excludes `review-sources.local.json` at every depth and leaves existing destination mappings untouched, including with `--force`. Keep differently named private mappings outside the skills repository. The loader's output also contains source text, repository identity, paths, and provenance: retain private-source results only in the authorized private review context, never public logs, fixtures, or artifacts.

## Connected GitHub (no checkout required)

1. Read the alias entry from `sources.json` for the repository and canonical path. For a private source, use the privately supplied mapping, never copy it into a public file or comment. Repository access is required; stop on denied or unavailable reads.
2. Resolve the source revision through the authorized GitHub connector/API. For the maintained default branch, read the repository's `default_branch`, then that branch's commit SHA. If the skill exists only in a draft PR, read the linked `proposed_source` PR, verify its repository, state, head repository, and head SHA, and explicitly identify this as draft-source use. A URL alone is not proof of current state. Do not guess that main contains an unmerged skill or automatically substitute an unrelated branch.
3. Fetch `GET /repos/{source-owner}/{source-repo}/contents/{canonical-path}?ref={resolved-full-commit-sha}` (or equivalent connector file read). Decode the returned content if needed. Read the full canonical `SKILL.md` before applying it. Resolve only needed relative references inside that skill directory; fetch each from the same source repository and immutable commit. Never combine main instructions with draft references. If the canonical skill intentionally routes to other repository-owned skills, resolve those at the same repository commit and record them separately.
4. Record the actual source repository, full commit SHA, canonical path, and the returned Git blob SHA for every instruction/reference file actually read. If bytes are materialized locally, additionally compute SHA-256. Record discovered-but-unread paths separately; discovery does not count as applying a skill. Some connectors return decoded file text without blob metadata. In that case read the commit's Git tree (checking for truncation) to obtain the exact path's blob ID, or record a computed content SHA-256 and explicitly say blob metadata was unavailable. GitHub blob IDs and SHA-256 are different identifiers and must be labeled accurately.
5. Review the target PR at its separately resolved current head. Keep review-target revision distinct from skill-source revision. Follow the loaded project instructions, including daily eligibility and evidence limits. Scripts require a supported execution environment; reading a script is not running its tests. Report unavailable execution honestly, without silently weakening required checks.

API reads do not copy canonical policy into this personal repository. Missing skill or reference, access errors, and unresolved draft provenance block claiming the project skill was applied. Do not substitute older bundled content or a generic checklist. Recheck relevant source/target heads before posting when the canonical workflow requires it; posting still needs its own authorization.
