# Agentic Coding Skills

Portable coding-agent rules for Codex, Claude Code, and Cursor.

This repo is based on the compact skills layout popularized by the Karpathy-inspired agent guidelines, but adapted for reusable day-to-day work across inference, multimodal, plugin, and cookbook repositories.

## What This Provides

- `AGENTS.md`: shared source of truth for Codex and other agents that read root instruction files.
- `CLAUDE.md`: thin Claude Code wrapper that imports `AGENTS.md`.
- `.cursor/rules/*.mdc`: Cursor project rules for shared and project-specific guidance.
- `skills/*/SKILL.md`: reusable skills for general coding and specific repositories.
- [skills/repository-maintenance/](skills/repository-maintenance/SKILL.md): a
  shared maintenance SOP for one or more repositories, with project-specific
  instructions applied where they exist.
- [skills/repository-loop-bootstrap/](skills/repository-loop-bootstrap/SKILL.md): initialize or audit a repository's evidence-backed development loop while preserving existing conventions.
- `skills/ncu-report-skill/`: Nsight Compute profiling, report analysis, and
  evidence-backed CUDA optimization plans, with B200/sm_100 references and helpers.
- `skills/product-deep-dive/`: research a product and create two editable,
  source-backed PowerPoint slides covering its business and technical views.
- [skills/formal-slides/](skills/formal-slides/SKILL.md): create editable presentations
  using ten bundled layouts, adapting or adding matching templates when needed.
- `skills/setup-server-project/`: prepare `repos/`, `models/`, `llm_wiki/`, and
  `envs/` in an existing server account, clone repositories, install dependencies, and verify
  the setup without expanding into account or machine administration.
- `skills/vllm-omni-deck/`: an editable vLLM-Omni PowerPoint skill with
  a seven-layout example template, an eight-page blank template with a branded
  white canvas, intact source-figure reuse, and typed generators.
- [Project review overlays](skills/repository-maintenance/references/project-reviews.md):
  repository-specific context and daily-queue rules used by the shared SOP.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and its
[contributor pre-PR check](skills/precheck-pr/SKILL.md) before implementation.
The skill is discoverable through the existing plugin's `./skills/` directory;
this change does not add it to project-rule sync installations.

## Core Principles

1. Think before coding.
2. Prefer simple, local, surgical changes.
3. Preserve existing project style and maintainer changes.
4. Turn tasks into verifiable goals.
5. Inspect the repository before editing and verify before handoff.

## Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── CURSOR.md
├── .cursor/
│   └── rules/
│       ├── agentic-coding-guidelines.mdc
│       ├── vllm.mdc
│       ├── vllm-omni.mdc
│       ├── afd-plugin.mdc
│       └── vllm-omni-cookbook.mdc
├── skills/
│   ├── agentic-coding-guidelines/
│   ├── repository-maintenance/
│   ├── repository-review-source/
│   ├── ncu-report-skill/
│   └── vllm-omni-deck/
├── external/
│   ├── ncu-report-skill.md
│   └── vllm-omni-review.md
└── scripts/
    └── sync-project.sh
```

## Install

Clone this repository somewhere stable:

```bash
git clone <this-repo-url> ~/.agentic-coding-rules
```

Sync the shared skills into any project:

```bash
cd /path/to/project
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools codex,claude,cursor
```

The `generic` profile installs the shared coding and maintenance skills, their
project review overlays and daily selectors, and the canonical review-source
loader. The project-specific resources are not separate discoverable skills.
The existing plugin also discovers the maintenance skill through `./skills/`;
if the plugin is already available, invoke it without syncing each repository.

For a single user-wide Codex installation, copy the shared skills to the Codex
home instead of installing them in every project:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools skills --target ~/.codex
```

Use your configured Codex home in place of `~/.codex` if different. This installs
real skill directories for discovery; rerun with `--force` to replace the
installed shared files when you intentionally update them. Existing local
`review-sources.local.json` mappings are never copied or overwritten. The generic
profile includes the configured project-specific daily-brief resources.

Named project profiles remain available for their existing project-specific
rules and review workflows:

- `vllm`
- `vllm-omni`
- `afd-plugin`
- `vllm-omni-cookbook`
- `nanodot`
- `router`
- `sciencediscovery`
- `system1-omni`

Supported tools (each also installs the skills referenced by the project rules):

- `codex`: installs `AGENTS.md`
- `claude`: installs `CLAUDE.md` and `AGENTS.md`
- `cursor`: installs `.cursor/rules/*.mdc`
- `skills`: installs the selected profile's skills without project rules

The installer checks all destination files before copying. Identical files are
left alone; conflicting files cause it to stop. Merge existing project rules
manually, or pass `--force` only when you intend to replace them. Symlink and
directory destinations are never replaced. Previously synced skills are not
automatically deleted; remove obsolete copies only after checking for local edits.
Existing commands or automations that invoke a retired project review skill or
its old selector path need to use `$repository-maintenance` and the matching
`references/projects/<alias>/scripts/select_daily.py` resource in the installed
skill. This migration does not change or schedule any automation.

## Shared maintenance SOP

Ask the agent to use `$repository-maintenance` for a repository or a named set
of repositories, for example: “Use `$repository-maintenance` to triage open PRs
and CI for these repositories and report the next actions.” The SOP establishes
scope, reads each project's instructions, inspects relevant evidence, performs
requested work, and reports findings and verification separately per project.
It does not assume every project uses the same labels or review rules.
General health checks cover the documentation system, CI levels, the
contribution and review-to-merge loop, and issue/PR labels; targeted requests
inspect only the relevant areas. See the [health-check guide](skills/repository-maintenance/references/health-check.md).
When a demonstrated failure can recur, prefer a proportionate executable guard
and verify both failing and passing cases. Choose runtime evidence appropriate to
the change, and distinguish observed results from configured checks.

Shared development guidance, project review overlays, and opt-in queue contracts
live under the maintenance skill. Project-specific development and review skill
entrypoints have been consolidated; the overlays preserve source, evidence, and
policy differences. For a new repository, start with the generic SOP and add an
overlay only for a real project-specific need.

Mapped repositories use their repository-owned review skills. The matching
overlay supplies explicitly configured personal daily-brief rules. If required
review instructions are unavailable, the SOP reports the blocker instead of
silently substituting a generic review.

## Tool-Specific Installation

Use the sync script so the instruction files and their skill dependencies stay
together. Use `generic` for the shared SOP or a named project profile when its
additional project-specific rules are needed.

For Codex:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools codex
```

For Claude Code:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools claude
```

For Cursor:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project generic --tools cursor
```

## Repository-owned review skills

Project repositories own the maintained review instructions. The shared SOP
loads those sources and only the matching [personal overlay](skills/repository-maintenance/references/project-reviews.md),
without copying project review checklists. Supported public review projects are
vLLM Omni, AFD Plugin, Router, ScienceDiscovery, System1 Omni, and nanodot.

See [repository-review-source](skills/repository-review-source/SKILL.md).
The connected GitHub API can load the canonical skill and needed references at
a resolved immutable commit without a local checkout; record the commit and
Git blob identifiers of the actual files read. See the connector workflow in
the loader skill. Alternatively, given an authorized local checkout:

```bash
python3 skills/repository-review-source/scripts/load_source.py nanodot --checkout /path/to/nanodot
```

The read-only loader verifies the checkout origin, returns the canonical skill,
and reports the exact HEAD and skill content hash. It does not fetch or switch
branches. Until a project skill PR merges, explicitly check out that draft
branch; missing main-branch instructions are reported as missing, not replaced
with generic guidance. A changed checkout is labeled dirty.

Private sources use the same generic loader with a local JSON mapping through
`--config`; keep that mapping outside the repository or in ignored
`review-sources.local.json`. No private project identity or content is bundled.

For this repository itself use its
[personal review overlay](skills/repository-maintenance/references/projects/personal-skills/review.md).

## Nsight Compute Profiling

Use [skills/ncu-report-skill/SKILL.md](skills/ncu-report-skill/SKILL.md) for CUDA
kernel profiling and `.ncu-rep` analysis. The complete upstream skill, helpers,
references, and MIT license are bundled; see
[source and runtime notes](external/ncu-report-skill.md) for the pinned version.
The existing plugin discovers it through `./skills/`; the project-rule sync
script continues to copy only the skills referenced by those project rules.

Profiling requires CUDA/Nsight Compute and an appropriate GPU; report analysis
requires Nsight Compute's `ncu_report` Python module. Adding the skill does not
install these tools or change GPU performance-counter permissions.

## Helper Regression Tests

Run the network-free installation, canonical-source loader, personal queue,
review-evidence, and bundled NCU packaging tests with Python 3.8+ and Bash:

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
