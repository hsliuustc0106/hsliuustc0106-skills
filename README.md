# Agentic Coding Skills

Portable coding-agent rules for Codex, Claude Code, and Cursor.

This repo is based on the compact skills layout popularized by the Karpathy-inspired agent guidelines, but adapted for reusable day-to-day work across inference, multimodal, plugin, and cookbook repositories.

## What This Provides

- `AGENTS.md`: shared source of truth for Codex and other agents that read root instruction files.
- `CLAUDE.md`: thin Claude Code wrapper that imports `AGENTS.md`.
- `.cursor/rules/*.mdc`: Cursor project rules for shared and project-specific guidance.
- `skills/*/SKILL.md`: reusable skills for general coding and specific repositories.
- `skills/ncu-report-skill/`: Nsight Compute profiling, report analysis, and
  evidence-backed CUDA optimization plans, with B200/sm_100 references and helpers.
- `skills/product-deep-dive/`: research a product and create two editable,
  source-backed PowerPoint slides covering its business and technical views.
- `skills/setup-server-project/`: prepare `repos/`, `models/`, `llm_wiki/`, and
  `envs/` in an existing server account, clone repositories, install dependencies, and verify
  the setup without expanding into account or machine administration.
- `skills/vllm-omni-deck/`: an editable vLLM-Omni PowerPoint skill with
  a seven-layout example template, an eight-page blank template with a branded
  white canvas, intact source-figure reuse, and typed generators.
- `skills/nanodot-review/`: thin loader for the canonical nanodot repository review skill.
- `skills/vllm-omni-review/`: thin loader for the canonical vLLM Omni repository review skill.

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
│   ├── ncu-report-skill/
│   ├── vllm-omni-deck/
│   ├── vllm-guidelines/
│   ├── vllm-omni-guidelines/
│   ├── afd-plugin-guidelines/
│   └── vllm-omni-cookbook-guidelines/
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

Sync into a project:

```bash
cd /path/to/project
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools codex,claude,cursor
```

Supported projects:

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

The installer checks all destination files before copying. Identical files are
left alone; conflicting files cause it to stop. Merge existing project rules
manually, or pass `--force` only when you intend to replace them. Symlink and
directory destinations are never replaced.

## Tool-Specific Installation

Use the sync script so the instruction files and their skill dependencies stay
together. Replace `vllm-omni` with the appropriate supported project.

For Codex:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools codex
```

For Claude Code:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools claude
```

For Cursor:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools cursor
```

## Repository-owned review skills

Project repositories own the maintained review instructions. Personal skill
entrypoints remain discoverable through the existing plugin and load those
sources without copying their checklists. Supported public review projects are
vLLM Omni, AFD Plugin, Router, ScienceDiscovery, System1 Omni, and nanodot.

See [repository-review-source](skills/repository-review-source/SKILL.md).
Given an authorized checkout containing its canonical skill:

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

For this repository itself use
[personal-skills-review](skills/personal-skills-review/SKILL.md).

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

Run the network-free installation, canonical-source loader, and bundled NCU
packaging tests with Python 3.8+ and Bash. Project review-helper and corpus tests
now live alongside their canonical project skills:

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
