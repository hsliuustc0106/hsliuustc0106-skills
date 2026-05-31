# Agentic Coding Skills

Portable coding-agent rules for Codex, Claude Code, and Cursor.

This repo is based on the compact skills layout popularized by the Karpathy-inspired agent guidelines, but adapted for reusable day-to-day work across inference, multimodal, plugin, and cookbook repositories.

## What This Provides

- `AGENTS.md`: shared source of truth for Codex and other agents that read root instruction files.
- `CLAUDE.md`: thin Claude Code wrapper that imports `AGENTS.md`.
- `.cursor/rules/*.mdc`: Cursor project rules for shared and project-specific guidance.
- `skills/*/SKILL.md`: reusable skills for general coding and specific repositories.
- `external/vllm-omni-review.md`: pointer to the external vLLM Omni review skill without hard-coding a personal account.

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

Supported tools:

- `codex`: installs `AGENTS.md`
- `claude`: installs `CLAUDE.md` and `AGENTS.md`
- `cursor`: installs `.cursor/rules/*.mdc`

## Direct Use

For Codex:

```bash
cp ~/.agentic-coding-rules/AGENTS.md ./AGENTS.md
```

For Claude Code:

```bash
cp ~/.agentic-coding-rules/AGENTS.md ./AGENTS.md
cp ~/.agentic-coding-rules/CLAUDE.md ./CLAUDE.md
```

For Cursor:

```bash
mkdir -p .cursor/rules
cp ~/.agentic-coding-rules/.cursor/rules/agentic-coding-guidelines.mdc .cursor/rules/
```

## vLLM Omni Review

For vLLM Omni code review, use the external `vllm-omni-review` skill repository as the source of truth. This repo intentionally keeps that URL configurable instead of hard-coding a personal GitHub account.

## License

MIT
