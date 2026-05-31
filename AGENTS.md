# Agentic Coding Rules

Portable coding-agent guidelines for Codex, Claude Code, Cursor, and project-specific workflows.

These instructions define the default behavior expected from coding agents in this workspace. Merge them with local project instructions when a repository already has its own rules.

## Core Principles

### 1. Think Before Coding

Do not assume silently. Surface uncertainty, conflicting interpretations, and tradeoffs before making consequential changes.

- State assumptions explicitly when they affect implementation.
- Ask for clarification when ambiguity would change the solution.
- Push back when a simpler or safer approach is available.
- Stop and name confusion instead of guessing through it.

### 2. Simplicity First

Use the smallest clear change that solves the problem.

- Do not add features beyond the request.
- Do not introduce abstractions for single-use logic.
- Do not add configurability, indirection, or broad error handling without a real need.
- Prefer code that a maintainer can understand quickly.

### 3. Surgical Changes

Touch only what the task requires.

- Preserve existing style and architecture.
- Do not refactor adjacent code opportunistically.
- Do not reformat files just because they are nearby.
- Clean up only unused code, imports, or variables created by your own changes.
- Never revert user or maintainer changes unless explicitly asked.

### 4. Goal-Driven Execution

Turn tasks into verifiable outcomes.

- For bug fixes, try to identify or add a regression check.
- For refactors, verify behavior before and after when practical.
- For new behavior, define what success means before implementing.
- Run focused tests or explain clearly why they were not run.

### 5. Repository-Aware Work

Let the repository teach you how to move.

- Inspect relevant files and nearby tests before editing.
- Prefer existing helpers, patterns, and local conventions.
- Use `rg` for search when available.
- Keep implementation notes concise and tied to decisions that matter.
- Summarize changed files and verification at handoff.

## Tool Notes

- Codex: this file is the primary instruction entrypoint.
- Claude Code: `CLAUDE.md` imports this file and may add Claude-specific notes.
- Cursor: `.cursor/rules/*.mdc` adapts these rules for Cursor project rules.

## Project Skills

Use the matching skill when working in these repositories:

- `vllm`: `skills/vllm-guidelines/SKILL.md`
- `vllm-omni`: `skills/vllm-omni-guidelines/SKILL.md`
- `afd-plugin`: `skills/afd-plugin-guidelines/SKILL.md`
- `vllm-omni-cookbook`: `skills/vllm-omni-cookbook-guidelines/SKILL.md`

For vLLM Omni review workflows, use the external `vllm-omni-review` skill repository as the source of truth. Keep its concrete URL in local setup docs or personal configuration rather than hard-coding an account name here.

