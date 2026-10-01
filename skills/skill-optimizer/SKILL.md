---
name: skill-optimizer
description: Review, validate, and propose focused improvements to Codex skills while preserving an explicit human approval gate. Use when a user asks to optimize, audit, validate, compare, or synchronize skills; when files under a skill directory have changed; or when performing a periodic review of discussion feedback and skill changes. Present evidence and selectable options before editing, and never modify, install, commit, push, or publish a skill until the user approves the exact action.
---

# Skill Optimizer

Turn skill changes and user feedback into small, evidence-backed proposals. Keep
analysis read-only until the user approves a specific proposal.

## Review Scope

1. Identify the source skill directories, installed copies, repository
   instructions, and review period.
2. Inspect available discussion context or supplied transcripts. Do not claim
   access to conversations that are not present.
3. Inspect skill diffs, manifests, bundled resources, related skills, and
   installation state.
4. Preserve unrelated user changes and existing repository conventions.

For a periodic review, use only evidence available for the requested period.
Treat isolated preferences as weak signals; prioritize repeated feedback,
observed failures, conflicting instructions, and missing validation.

## Optimization Options

Offer only options supported by the evidence:

1. **Validate only** — check naming, frontmatter, links, referenced files, and
   bundled scripts without changing files.
2. **Improve triggers** — make the frontmatter description identify the skill's
   purpose and invocation contexts more reliably.
3. **Clarify instructions** — remove ambiguity, duplication, contradictions, or
   unnecessary context.
4. **Update examples or resources** — add or revise reusable examples,
   references, or deterministic scripts when repeated usage justifies them.
5. **Reconcile conflicts** — align the skill with repository instructions and
   related skills without weakening higher-priority requirements.
6. **Synchronize installation** — copy an approved source version to the
   selected user skill directory and verify it byte-for-byte.
7. **Skip** — retain the current version.

Do not add speculative features or optimize wording merely for stylistic
preference.

## Proposal Gate

Before any write, present a compact proposal containing:

- evidence and the observed problem;
- affected skills and exact files;
- numbered optimization options;
- intended changes and expected effect;
- validation to run;
- whether installation, version-control actions, or publication are included;
- excluded or uncertain suggestions.

Ask the user to select options and explicitly approve them. Approval applies
only to the displayed files and actions. If the scope or proposed behavior
changes, present the revised proposal and request approval again.

Treat approval to edit source files, synchronize installed copies, commit, push,
and open a pull request as separate actions unless the user's approval
explicitly includes them. A scheduled or periodic invocation may prepare a
proposal but may not bypass this gate.

## Apply an Approved Proposal

After approval:

1. Recheck repository status and confirm the approved files have not changed.
2. Make the smallest approved edits.
3. Validate each affected skill with the available skill validator. Run focused
   checks for modified scripts or assets.
4. Review the final diff for scope, broken references, and instruction
   conflicts.
5. Synchronize an installed copy only when that action was approved, then
   compare source and destination.
6. Perform commit, push, or pull-request actions only when they were approved.

Report changed files, validation results, installation status, and any remaining
risks. State that updated installed skills become available on a subsequent
turn.
