# Using this repo with Cursor

This repository includes Cursor project rules under [`.cursor/rules`](.cursor/rules). Open the folder in Cursor and the rules will be available from Cursor's project rules UI.

## In this repository

- [`.cursor/rules/agentic-coding-guidelines.mdc`](.cursor/rules/agentic-coding-guidelines.mdc) applies the shared behavior rules.
- Project-specific rules are available for `vllm`, `vllm-omni`, `afd-plugin`, `vllm-omni-cookbook`, `nanodot`, `router`, `sciencediscovery`, and `system1-omni`.
- The legacy `.cursorrules` format is intentionally not used.

## Use in another project

Use the sync script so the selected rules and their loader dependencies are
installed together:

```bash
~/.agentic-coding-rules/scripts/sync-project.sh --project vllm-omni --tools cursor --target /path/to/project
```

For Codex or Claude Code, select `--tools codex` or `--tools claude`. Existing
conflicting files are preserved unless explicitly replaced with `--force`.
Project review entrypoints load their canonical repository source through an
authorized checkout or the connected GitHub API; review policy is not copied
into this personal repository.

## Keep files in sync

When the shared rules change, update:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/agentic-coding-guidelines.mdc`
- `skills/agentic-coding-guidelines/SKILL.md`
