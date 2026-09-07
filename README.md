# Agentic Coding Skills

Portable coding-agent rules for Codex, Claude Code, and Cursor.

This repo is based on the compact skills layout popularized by the Karpathy-inspired agent guidelines, but adapted for reusable day-to-day work across inference, multimodal, plugin, and cookbook repositories.

## What This Provides

- `AGENTS.md`: shared source of truth for Codex and other agents that read root instruction files.
- `CLAUDE.md`: thin Claude Code wrapper that imports `AGENTS.md`.
- `.cursor/rules/*.mdc`: Cursor project rules for shared and project-specific guidance.
- `skills/*/SKILL.md`: reusable skills for general coding and specific repositories.
- `skills/vllm-omni-deck/`: an editable vLLM-Omni PowerPoint skill with
  a seven-layout example template, an eight-page blank template with a branded
  white canvas, intact source-figure reuse, and typed generators.
- `skills/vllm-omni-review/`: bundled vLLM Omni review workflow and helpers.

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
│   ├── vllm-omni-deck/
│   ├── vllm-guidelines/
│   ├── vllm-omni-guidelines/
│   ├── afd-plugin-guidelines/
│   └── vllm-omni-cookbook-guidelines/
├── external/
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

## vLLM Omni Review

For vLLM Omni code review, use
[skills/vllm-omni-review/SKILL.md](skills/vllm-omni-review/SKILL.md) as the source
of truth. Review helpers require Bash, `gh`, `jq`, and Python 3.8 or newer.

## Helper Regression Tests

Run the network-free installation and review-helper tests with Python 3.8+,
Bash, and `jq` available (the tests provide a fake `gh`):

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
