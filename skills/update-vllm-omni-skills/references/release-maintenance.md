# Maintaining vLLM-Omni Skills Across Releases

Use this reference when refreshing the vLLM-Omni skills for a published release,
or when version-sensitive guidance disagrees with the task's target checkout.
The current maintenance record is [release-status.md](release-status.md).

## During ordinary work

Identify the target vLLM-Omni tag or commit, its paired vLLM dependency, and the
relevant platform before applying concrete paths, flags, test commands, or
architecture rules from these skills. For a PR review, preserve the requested
base/head snapshot. Do not replace it with the latest release or main.

Use code, tests, dependency files, and applicable design documents from that
snapshot. A skill is navigation and review guidance, not independent proof of
the project's current contract. A draft design is not normative merely because
an older skill describes it as mandatory. Separate implemented behavior,
accepted contracts, proposals, and historical examples.

If the maintenance record does not cover the target or subsystem, verify the
specific assumption needed for the task and disclose remaining uncertainty.
Do not block ordinary work just because a full skill refresh is incomplete.

## Release update procedure

1. **Discover the release.** Check the official
   [published releases](https://github.com/vllm-project/vllm-omni/releases).
   Record the tag, release URL, publication time, and resolved commit SHA.
   Exclude drafts and prereleases unless they are the requested target. Do not
   infer release order from a lexicographic tag sort or a local checkout date.
2. **Freeze the comparison.** Resolve the previous recorded release and the new
   tag to commits from the verified upstream repository. Compare their release
   notes and changed files. If no previously reviewed baseline exists, record
   a first audit with explicit coverage; do not invent a previous validation.
   Carry unresolved areas from a partial audit forward even when the new diff
   does not touch them. Keep main-only behavior separate from released behavior.
3. **Map changes to guidance.** Inspect the owning code, tests, docs, and linked
   merged PRs at the release SHA. Release notes locate changes; confirm concrete
   commands and contracts in source. Follow the impact table below. Avoid
   copying the complete changelog or maintaining a second supported-model list.
4. **Make focused updates.** Correct removed paths/options, changed APIs,
   dependency constraints, test selection, and obsolete review assumptions.
   Preserve historical guidance only when a supported older target needs it,
   clearly labeling its version range and source. Replace duplicated volatile
   explanations with discovery instructions and pinned primary-source links.
5. **Validate proportionally.** Check skill frontmatter, relative links, bundled
   dependencies, and helper tests when scripts change. For changed commands,
   use source inspection first, then a non-accelerator probe where safe. Report
   static checks separately from runtime evidence. Test collection can import
   hardware code; inspect fixtures before running it. Accelerator verification
   follows the host's reservation and experiment rules and is not implied by a
   documentation refresh.
6. **Record coverage.** Update the maintenance record with the release SHA,
   date, affected skills, source links, checks performed, and unresolved areas.
   Use `partial` while relevant areas remain unchecked; `complete` means the
   declared release-impact scope has been covered, not that every model works.
7. **Distribute deliberately.** Keep changes on a task branch. When publication
   is authorized, include the release comparison and validation in the PR,
   update plugin versions for consumers, and retain DCO sign-off. Refresh
   installed copies only after the source change is accepted and installation
   is authorized. Never edit an installed cache as the source of truth.

## Impact map

| Upstream change | Skills/references to inspect | Evidence at the target SHA |
| --- | --- | --- |
| vLLM rebase, Python or backend requirements | Project guidelines; review verification/performance setup; cookbook environments | `pyproject.toml`, `setup.py`, platform requirements, installation docs |
| Configuration, orchestration, output, connector, or scheduler contracts | Review architecture and blocker references; relevant model checklists | Owning `docs/design/module/` documents, implementation, contract tests |
| CLI, serving endpoints, flags, or examples | Review API/verification guidance; cookbook commands | CLI registration, entrypoints, configuration docs, online/offline examples |
| Test layout, markers, fixtures, or CI gates | Review test-quality, verification, and execution references | Pytest configuration/plugins, hardware marker helpers, active CI definitions |
| Models, modalities, acceleration, or platform coverage | Review routing and relevant model/diffusion checklists; cookbook | Registries, model adapters, supported-feature docs, integration tests |
| Technical claims used in presentations | Deck source-and-claim guidance and affected example content | Versioned sources, original figures, benchmark conditions |

Deck typography, layout, and figure-preservation rules do not require changes
merely because a runtime release shipped. Generic skills such as technical
writing or interactive slide planning need an update only if their own workflow
or an embedded vLLM-Omni assumption changes.

## Maintenance record fields

Record the upstream repository, tag, commit, release publication time, review
date, comparison baseline (or explicitly absent), status, affected areas,
source-backed changes, validation, and unresolved work. Keep the previous
release's evidence reachable through Git history or a version-specific note.
Do not advance a `complete` baseline solely because a release was detected.

Published releases are the default maintenance trigger. A failed task caused by
stale guidance can receive an immediate, explicitly version-scoped correction;
it does not establish coverage of unreleased main.
