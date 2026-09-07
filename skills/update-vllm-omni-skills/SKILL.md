---
name: update-vllm-omni-skills
description: Refresh this repository's vLLM-Omni skills against a published upstream release, update stale guidance from pinned source evidence, validate affected skills, and prepare a PR-ready patch. Use when the user asks to update or maintain these skills for a new release, audit their release compatibility, or continue an incomplete release refresh. Ordinary vLLM-Omni development and PR review use their existing skills.
---

# Update vLLM-Omni Skills

Keep the project, review, cookbook, and deck skills useful as upstream releases
change. Produce source-backed edits and an honest coverage record.

## Inputs and defaults

- Use the requested vLLM-Omni release; otherwise discover the latest published
  stable release from the verified `vllm-project/vllm-omni` upstream.
- Locate the skills source checkout from task context and verified Git remotes.
  Do not treat an installed skill cache as its source repository. If it cannot
  be located, finish read-only release triage and ask for the source checkout.
- Read applicable repository instructions and the current
  [coverage record](references/release-status.md). Its recorded release is
  historical evidence, not a hard-coded target for future runs.
- Continue an explicitly identified maintenance branch. For new work, follow
  the user's branch/worktree policy and preserve existing changes.

## Refresh workflow

Read [release-maintenance.md](references/release-maintenance.md) for the impact
map, evidence rules, validation, and maintenance-record format, then:

1. Resolve the release and prior recorded baseline to upstream commits. Record
   release metadata and inspect the release notes and changed source paths.
2. Identify affected skill instructions, references, helpers, commands, and
   examples. Carry forward unresolved items from a partial previous audit.
3. Verify concrete assumptions against the release's code, tests, dependency
   files, and owning design documents. Inspect linked PRs only when needed to
   explain changed behavior or contracts.
4. Update the relevant skills and their source links. Keep stable writing and
   visual-design rules unless an actual change affects them. Remove obsolete
   requirements and mark historical guidance with its supported target.
5. Validate the changed skill frontmatter, links, packaging dependencies, and
   affected helpers. Separate source inspection from runtime validation. Do not
   start accelerator workloads just to refresh documentation; any requested
   device verification follows the applicable reservation and experiment rules.
6. Update the coverage record with the exact commit, checked areas, evidence,
   validation, and remaining work. Mark the refresh partial when relevant
   release-impact areas remain unverified; do not claim full model support.
7. Prepare a concise PR title/body describing the release comparison, changed
   behavior, tests, and limitations. If the user authorized a PR, commit with
   verified DCO identity, push, and create it. Otherwise deliver the local patch
   and PR text. Reuse existing authorization; do not ask again for covered work.

If the recorded target is already current and complete, verify that no relevant
inputs changed and report that no update is needed. Do not manufacture edits or
an empty PR. If it is current but partial, continue the recorded outstanding
scope instead of presenting it as a newly detected release.

## Handoff

Report the release/tag and SHA, affected skills, checks performed, unresolved
coverage, and the PR link or local patch location. Distinguish a completed
release-impact audit from a successful runtime test. This skill runs when
invoked; recurring release monitoring requires a separately requested schedule.
