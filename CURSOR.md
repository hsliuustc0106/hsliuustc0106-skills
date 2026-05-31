# Using this repo with Cursor

This repository includes Cursor project rules under [`.cursor/rules`](.cursor/rules). Open the folder in Cursor and the rules will be available from Cursor's project rules UI.

## In this repository

- [`.cursor/rules/agentic-coding-guidelines.mdc`](.cursor/rules/agentic-coding-guidelines.mdc) applies the shared behavior rules.
- Project-specific rules are available for `vllm`, `vllm-omni`, `afd-plugin`, and `vllm-omni-cookbook`.
- The legacy `.cursorrules` format is intentionally not used.

## Use in another project

Copy the relevant `.mdc` files into that project's `.cursor/rules/` directory:

```bash
mkdir -p .cursor/rules
cp ~/.agentic-coding-rules/.cursor/rules/agentic-coding-guidelines.mdc .cursor/rules/
cp ~/.agentic-coding-rules/.cursor/rules/vllm-omni.mdc .cursor/rules/
```

For Codex and Claude Code, copy or symlink `AGENTS.md` and `CLAUDE.md` as needed.

## Keep files in sync

When the shared rules change, update:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/agentic-coding-guidelines.mdc`
- `skills/agentic-coding-guidelines/SKILL.md`
