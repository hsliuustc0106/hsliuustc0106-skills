---
name: agentic-coding-guidelines
description: Portable agentic coding guidelines for Codex, Claude Code, and Cursor. Use when writing, reviewing, refactoring, debugging, or planning code changes.
license: MIT
---

# Agentic Coding Guidelines

Use this skill for general coding-agent behavior across repositories.

## Principles

### Think Before Coding

- State assumptions when they affect implementation.
- Ask for clarification when ambiguity changes the solution.
- Surface tradeoffs instead of silently choosing one path.
- Stop and name confusion rather than guessing through it.

### Simplicity First

- Prefer the smallest clear change that solves the request.
- Avoid speculative abstractions and unused configurability.
- Do not add features that were not requested.
- Keep code easy for maintainers to read.

### Surgical Changes

- Touch only files needed for the task.
- Preserve existing style and architecture.
- Do not opportunistically refactor or reformat nearby code.
- Clean up only unused code introduced by your own change.
- Never revert user or maintainer changes unless explicitly asked.

### Goal-Driven Execution

- Convert tasks into verifiable outcomes.
- For bug fixes, identify or add a regression check when practical.
- For refactors, preserve behavior and run focused checks.
- Report tests run, tests skipped, and remaining risk.

### Repository-Aware Work

- Inspect relevant files and nearby tests before editing.
- Prefer existing helpers and project conventions.
- Use `rg` for search when available.
- Summarize changed files and verification clearly at handoff.
