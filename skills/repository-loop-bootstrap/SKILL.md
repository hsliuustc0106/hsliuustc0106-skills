---
name: repository-loop-bootstrap
description: Initialize or audit a repository's fast, evidence-backed development loop, adapting existing contributor guidance, validation, review rules, lessons, and PR tracking. Use for repository workflow bootstrapping, not ordinary feature implementation.
---

# Repository loop bootstrap

Create a complete, minimally duplicated initialization that lets a contributor find the right code, choose meaningful validation, and hand off a change with trustworthy evidence. Support both empty and mature repositories. Preserve the repository's conventions and canonical documents.

## Choose the requested outcome

- **Audit/plan:** inspect and propose; do not imply missing foundations were implemented.
- **Full bootstrap (default for “initialize”, “bootstrap”, or “apply this skill”):** implement all applicable foundations in the authorized workspace, including root AGENTS.md and a discoverable lessons.md by default. Reuse equivalent canonical content through these entrypoints. A narrow fix is not a completed full bootstrap.
- **Targeted update:** limit edits to the explicitly requested subset and label that scope.

Initialization establishes the repository's guidance and evidence contracts; continuous operation uses them for actual changes. When asked to initialize or audit that operational process, read [operating-cycle guidance](references/operations.md). This does not activate a coding runner, watcher, or recurring review; deployment and subsequent actions need their own authorized scope.

## Scope and discovery

Default to a plan and local files in the authorized workspace. Reading a repository or drafting a workflow does not authorize pushing, opening PRs, posting comments, merging, changing protections or permissions, installing hooks, scheduling jobs, or starting paid/external runs. Obtain target-specific authorization before deployment. Do not invent owner identities or approval authority.

1. Read applicable AGENTS.md instructions, contributor docs, architecture/API contracts, manifests, tests, CI definitions, ownership files, and existing review/tracking conventions. Inspect code to distinguish intended design from current implementation. On an empty repository, mark stack/platform/owner choices unresolved instead of inventing them.
2. Inventory all seven foundations below as present, partial, absent, or unknown before edits. Record canonical paths, how contributors or agents reach/consume them, and evidence. A file existing somewhere is not evidence that the workflow uses it. Pin the inspected repository revision (or file digests without Git), read canonical architecture, system contracts, and code regulations in full within the declared review scope, and compare their substantive claims against implementation/configuration/tests using the foundation guidance. Navigation repair alone is not content alignment. Local workflow YAML establishes configured checks, not observed success or remote branch-protection settings.
3. Resolve paths, commands, supported platforms, owners, scope, and writable state location from evidence. Ask only for decisions that block a useful safe plan. Existing rules outrank suggested defaults. Read [foundation guidance](references/foundations.md) when filling gaps, and [tracking semantics](references/tracking.md) when proposing PR/issue state.
4. Propose a short all-foundation gap plan, reusing canonical files with links. If authorized to edit local files, implement the applicable gaps with minimal additive changes and explain conflicts rather than silently replacing rules. Do not create seven documents just because there are seven foundations; do not shrink a full bootstrap to its easiest document fix. Mark authority-dependent runtime work blocked or deferred instead of installing it implicitly.

## Seven foundations

- Contributor navigation: a concise entrypoint pointing to canonical setup, code, tests, contracts, and operational guidance.
- Architecture and contracts: boundaries, invariants, public behavior, implementation locations, and explicit known gaps.
- Change-to-validation matrix: change category → checks, relevant platform, evidence needed, and accountable owner.
- Review and merge rules: contribution evidence, repository-established review and merge requirements, validation ownership, and actual authority to merge.
- Bounded lessons: actionable prevention linked to incidents, with independent recurrence escalation and archives.
- Persistent PR/issue state: exact-head evidence, freshness, dependencies, next action, and deduplication across restarts.
- Reliable execution and metrics: bounded retries, checkpointing, reproducible commands, and measurements with honest limitations.

## Completion acceptance

Produce a coverage record for every foundation: status, inspected revision, canonical evidence paths, entrypoint/consumer, declared content-review coverage, what was implemented or exercised, remaining gap, and owner/next action when needed. Distinguish wiring, content alignment, and executed runtime validation. For reviewed content, record unchanged-and-verified, refreshed, or unresolved with supporting evidence; untouched or unchecked text cannot be called verified. Allowed final statuses:

- **Present and wired:** existing content/mechanism is reachable and its substantive claims are current within the declared review coverage, with evidence; actual consumption is verified or its limit stated.
- **Newly implemented:** the missing content/mechanism was created, wired, and validated at its stated level.
- **Not applicable:** give a repository-specific reason; missing permission, tooling, or time is not “not applicable.”
- **Blocked/deferred:** state what is missing, why, and the decision/authorization needed. Required blocked/deferred foundations prevent a full-completion claim.

For a full bootstrap, verify root AGENTS.md and lessons.md (or an explicitly agreed equivalent) exist and are wired; provide the human CONTRIBUTING entrypoint and applicable existing tool instructions with links to canonical architecture/contracts, testing, review, and lessons. Read [foundation guidance](references/foundations.md) for the load-chain check. Do not equate a schema, dry run, or manual checklist with an installed operational runner. Report “documentation initialization complete; operational tracking deferred,” for example, when that is the actual result rather than declaring the entire loop complete.

## Validate the initialization

- Verify local links including anchors, and commands against the repository; check syntax using already available tools. Reconcile historical review guides with current source and CI, surfacing contradictions rather than copying stale instructions. Never label a command tested if it was only found in source.
- Exercise one representative change through the matrix. Show which checks apply, who owns unresolved validation, and which established merge requirements remain unmet, if any. If execution is unavailable or costly, report the missing evidence rather than fabricating a pass.
- If state tracking is included, exercise a head change, a same-head CI change, and a repeated observation. The first invalidates head-bound evidence; the second refreshes CI without hiding the change; the third must not duplicate an action.
- If operational guidance is included, replay a real available change through its evidence, action authority, and linked-issue completion decisions. Supplement missing cases with clearly labeled isolated fixtures; never present simulated results as observed repository behavior.
- Run only authorized, proportionate checks. Report exact commands, environment/platform, exit status, and untested limits. Check that generated content introduces no conflicting authority, duplicated canonical guidance, credentials, or deployment side effects.
- Start from root AGENTS.md and the human contributor entrypoint and traverse the required links, including lessons; verify applicable existing agent/tool instructions do not bypass or contradict them. A missing required entrypoint or unreachable lessons fails full-bootstrap acceptance.
- Re-read the result as a new contributor: can they locate the implementation, select checks, distinguish evidence from obligations, and resume the next action?

Deliver a concise inventory, changed-file list, actual validation evidence, unresolved decisions, and the next authorized step. Installation or rollout is a separate action unless explicitly requested for the identified target.
