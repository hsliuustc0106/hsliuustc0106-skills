---
name: update-vllm-omni-recipes
description: Audit and update the in-tree vLLM-Omni deployment recipes for a final stable release. Use when a vLLM-Omni stable tag is published or when asked to refresh recipes, release compatibility claims, commands, local links, coverage, or recipes/README.md for a stable release. Preserve historical test evidence, distinguish static checks from hardware revalidation, and treat publication to vllm-project/recipes as a separate opt-in task.
---

# Update vLLM-Omni Recipes

Refresh `vllm-project/vllm-omni/recipes/` against one final release without
turning unverified assumptions into compatibility claims.

## Establish scope

1. Read every applicable `AGENTS.md` before acting.
2. Require an explicit final target tag such as `v0.26.0`. If the user did not
   name one, show the plausible final tags and ask which release to use. Do not
   select a release candidate, nightly, development version, branch, or moving
   commit as the stable target.
3. Default to the in-tree `recipes/` directory in `vllm-project/vllm-omni`.
   Treat these alternatives as different tasks and ask before including them:
   - publishing selected mirrors to `vllm-project/recipes` or
     `recipes.vllm.ai`;
   - updating a separate cookbook repository;
   - changing the release process or automation itself.
4. Identify the preceding final tag. Allow an explicit override for a patch or
   nonstandard release range, and state the selected range before editing. If
   the official release notes compare against a different baseline, present
   both interpretations: use the immediately preceding final tag for an
   incremental maintenance audit, and use the official baseline for the full
   feature summary.
5. Determine which validation resources are available: static inspection, CI
   results, maintainer evidence, and specific hardware. Never imply that static
   inspection substitutes for a hardware run.

## Choose read-only or editing mode

For an audit, explanation, or report-only request, keep the repository
unchanged. Do not create a branch or worktree, and do not fetch when the user
explicitly prohibited local writes. Use remote-ref inspection and existing
objects; if the published commit is unavailable locally, report that limit or
use an ephemeral clone only when the request permits it.

For a request to change recipes, prepare an isolated checkout as follows.

## Prepare an isolated checkout for edits

Follow the repository's branch and worktree policy. In the standard personal
workspace, fetch `origin/main`, inspect published tags, then create a fresh
`codex-` branch from the latest `origin/main` in an isolated worktree under
`/home/hsliu/tmp`. Do not disturb an existing dirty checkout and do not work on
`main`.

Compare the local target and baseline tag commits with `git ls-remote` before
using them. First verify that the selected remote points to
`vllm-project/vllm-omni`; pass `--remote upstream` when `origin` is a fork. A
final tag can be stale or moved locally. If the local and
published commits differ, stop and surface both SHAs; never force-move a tag or
silently audit the local ref. After confirming that the published refs are
authoritative, use an isolated ref, temporary clone, or the audit utility's
explicit `--use-remote-tags` mode.

Before editing, record:

- the target tag and commit;
- the preceding tag and commit;
- the current `origin/main` commit;
- whether the target is a published final release;
- any uncommitted files already present in the selected checkout.

Stop if the target tag, repository, or intended publication scope remains
ambiguous.

## Generate the audit

Run the bundled read-only audit from the skill directory:

```bash
python3 scripts/audit_release_recipes.py \
  --repo /path/to/vllm-omni \
  --target v0.26.0 \
  > /tmp/vllm-omni-recipe-audit-v0.26.0.md
```

Pass `--previous <tag>` only when the automatically selected preceding final
tag is not the intended baseline. By default the utility verifies both final
tags against `origin` and stops on a mismatch. Use `--use-remote-tags` only
after choosing the published remote SHAs and only when those objects already
exist locally. Use `--offline` only for a deliberately local snapshot, never
as evidence of a published release. Use `--strict` after editing to make
structural findings fail the command.

Treat the report as a triage aid, not proof that a recipe works. Inspect every
reported item in source context. Its version-evidence section deliberately
includes exact commits and development versions for classification; those are
not automatic replacement candidates.

## Build the release delta

Use the target range and repository history to identify:

- recipe files added, removed, renamed, or changed between the two final tags;
- recipe-linked examples or documentation changed in that range;
- models and hardware added, removed, or materially changed in release notes
  and the supported-model tables;
- public command, module path, CLI flag, API schema, model ID, dependency, or
  installation changes that invalidate existing instructions;
- pre-release versions, development versions, PR branches, raw commits, and
  floating `current checkout` language that require human review;
- broken local links, missing repository paths inside fenced commands, and
  disagreement between recipe files and the `recipes/README.md` inventory.

Map release changes to affected recipes by evidence. Do not assume every code
change affects every recipe, and do not limit the audit to files that happened
to change under `recipes/`.

## Classify before editing

Assign each candidate recipe one disposition:

| Disposition | Use when | Action |
|---|---|---|
| Update | Released paths, flags, dependencies, or instructions are provably stale | Edit and cite the source evidence in the work notes |
| Revalidate | A stable-release compatibility claim needs CI or hardware evidence | Queue the exact command and hardware; do not claim validation yet |
| Preserve | The entry is an exact historical test record and no replacement evidence exists | Keep it intact and explain why |
| Remove | The recipe is intentionally retired or replaced, with maintainer or release evidence | Remove it and repair every index and link |

Do not globally replace version strings. Fields such as `vLLM version`,
`vLLM-Omni version or commit`, driver versions, memory measurements, and
throughput numbers often describe a real historical run. Preserve them unless
the same configuration was rerun or an authoritative artifact proves the new
value.

## Edit recipes

- Keep one model-family recipe by default and keep hardware-specific sections
  aligned with `recipes/TEMPLATE.md`. Preserve intentional platform-specific
  companion files.
- Use released, public commands and paths. Verify renamed modules and flags at
  the target tag or in authoritative release documentation.
- Record an exact stable tag only for a configuration supported by evidence.
  Label static compatibility analysis as static analysis.
- Add new validation results instead of rewriting older measurements when both
  remain useful.
- Keep model IDs, hardware names, prerequisites, inputs, outputs, memory notes,
  key flags, and known limitations concrete.
- Update `recipes/README.md` whenever recipe inventory, task coverage, or
  hardware coverage changes. Keep all relative links resolvable.
- Change `recipes/TEMPLATE.md` only for a recurring requirement that should
  apply to future recipes, not to solve a one-off release issue.
- Avoid drive-by edits outside release-relevant recipes and their indexes.

## Validate in layers

1. Rerun the audit with `--strict`. Resolve structural findings or document an
   intentional inventory exception explicitly.
2. Run repository-provided Markdown, link, spelling, and documentation checks
   that cover the changed files.
3. Statically verify commands against the target tree: imports, example
   paths, CLI help, API fields, model IDs, and dependency names.
4. Use existing CI artifacts or run focused non-hardware checks when they are
   authoritative for the claim.
5. Run the documented recipe on its stated hardware when available. Capture
   the exact commit/tag, environment, command, expected output, and observed
   result.
6. Mark each recipe as `hardware verified`, `CI verified`, `static only`, or
   `needs revalidation`. Never collapse these labels into a generic “verified.”

Before handoff, review the final diff against both the target tag and current
`origin/main`. Ensure post-release fixes on `main` are not accidentally
described as available in the target release.

## Report and publish

Summarize the result with a compact matrix containing recipe, change,
evidence, and validation level. List remaining hardware work separately.
Include the target range and commands used for validation.

If asked to commit or open a PR, follow repository conventions and add the DCO
`Signed-off-by` trailer. Do not publish mirrored recipes externally unless the
user explicitly included that scope; inspect the external repository's own
instructions and use a separate branch or PR when they do.
