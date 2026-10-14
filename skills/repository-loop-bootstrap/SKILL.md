---
name: repository-loop-bootstrap
description: Initialize or audit a repository's fast, evidence-backed development loop, adapting existing contributor guidance, validation, review rules, lessons, and PR tracking. Use for repository workflow bootstrapping, not ordinary feature implementation.
---

# Repository loop bootstrap

Create the smallest maintainable initialization that lets a contributor find the right code, choose meaningful validation, and hand off a change with trustworthy evidence. Support both empty and mature repositories. Preserve the repository's conventions and canonical documents.

## Scope and discovery

Default to a plan and local files in the authorized workspace. Reading a repository or drafting a workflow does not authorize pushing, opening PRs, posting comments, merging, changing protections or permissions, installing hooks, scheduling jobs, or starting paid/external runs. Obtain target-specific authorization before deployment. Do not invent owner identities or approval authority.

1. Read applicable AGENTS.md instructions, contributor docs, architecture/API contracts, manifests, tests, CI definitions, ownership files, and existing review/tracking conventions. Inspect code to distinguish intended design from current implementation. On an empty repository, mark stack/platform/owner choices unresolved instead of inventing them.
2. Inventory the seven foundations below as present, partial, absent, or unknown. Record canonical paths and evidence. Local workflow YAML establishes configured checks, not observed success or remote branch-protection settings.
3. Resolve paths, commands, supported platforms, owners, scope, and writable state location from evidence. Ask only for decisions that block a useful safe plan. Existing rules outrank suggested defaults. Read [foundation guidance](references/foundations.md) when filling gaps, and [tracking semantics](references/tracking.md) when proposing PR/issue state.
4. Propose a short gap plan, reusing canonical files with links. If authorized to edit local files, make minimal additive changes and explain conflicts rather than silently replacing rules. Do not create seven documents just because there are seven foundations.

## Seven foundations

- Contributor navigation: a concise entrypoint pointing to canonical setup, code, tests, contracts, and operational guidance.
- Architecture and contracts: boundaries, invariants, public behavior, implementation locations, and explicit known gaps.
- Change-to-validation matrix: change category → checks, relevant platform, evidence needed, and accountable owner.
- Review and merge rules: contribution evidence, required independent review, maintainer ownership, and actual authority to merge.
- Bounded lessons: actionable prevention linked to incidents, with independent recurrence escalation and archives.
- Persistent PR/issue state: exact-head evidence, freshness, dependencies, next action, and deduplication across restarts.
- Reliable execution and metrics: bounded retries, checkpointing, reproducible commands, and measurements with honest limitations.

## Validate the initialization

- Verify local links including anchors, and commands against the repository; check syntax using already available tools. Reconcile historical review guides with current source and CI, surfacing contradictions rather than copying stale instructions. Never label a command tested if it was only found in source.
- Exercise one representative change through the matrix. Show which checks apply, who owns unresolved validation, and what prevents merge. If execution is unavailable or costly, report the missing evidence rather than fabricating a pass.
- If state tracking is included, exercise a head change, a same-head CI change, and a repeated observation. The first invalidates head-bound evidence; the second refreshes CI without hiding the change; the third must not duplicate an action.
- Run only authorized, proportionate checks. Report exact commands, environment/platform, exit status, and untested limits. Check that generated content introduces no conflicting authority, duplicated canonical guidance, credentials, or deployment side effects.
- Re-read the result as a new contributor: can they locate the implementation, select checks, distinguish evidence from obligations, and resume the next action?

Deliver a concise inventory, changed-file list, actual validation evidence, unresolved decisions, and the next authorized step. Installation or rollout is a separate action unless explicitly requested for the identified target.
