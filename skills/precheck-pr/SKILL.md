---
name: precheck-pr
description: Obtain traceable human intent before implementing or submitting a contribution, then continue repository-owned self-review checks. Not an independent-review queue policy.
---

# Contributor pre-PR check

Read the target repository's contribution instructions and applicable agent rules.
For this skills repository, start with [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Before implementation: human intent

Before implementing a contribution intended for a PR, obtain these answers from
the human contributor:

1. What outcome do you really want?
2. What is the highest-leverage variable that determines it?
3. Will this work move that variable, or just keep you busy?
4. Who is the customer, and what do they really want?

Reuse explicit answers already supplied by the human in the task or a linked
issue; keep their provenance and do not ask the same questions again. Do not infer
or invent missing answers, silently choose priorities, or answer on the human's
behalf. Ask only the missing material questions together and wait before
implementation or PR submission. Read-only investigation to clarify the questions
may continue.

Then ask whether the outcome needs a PR at all. Record the human's decision; a
configuration change, existing capability, documentation answer, or no change may
be sufficient. For a bug fix, link evidence of an actual failure: an observed
trace, a minimal reproducer with its observed result, or an executed failing
regression test. An unexecuted reproducer or hypothetical diagnosis is not proof
of a failure that already happened.

## Before submission

- Make the human-provided intent and PR-necessity decision traceable in the issue
  or PR. Do not copy private conversations, customer data, or restricted evidence
  into a broader audience; obtain an authorized summary or scoped reference.
- Recheck the answers when the proposed scope materially changes, and ask the
  human about gaps rather than rewriting their goal.
- Continue the repository's existing self-review, tests, evidence, and approval
  requirements. This gate does not authorize implementation, publication, or merge
  outside the user's request.
- This contributor gate is not a prerequisite for independent read-only reviews
  or issue triage. It does not change review queue labels, draft eligibility,
  head-SHA deduplication, or publication policy.
