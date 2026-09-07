---
name: vllm-omni-cookbook-guidelines
description: Project guidance for examples, tutorials, and reproducible cookbook workflows.
license: MIT
---

# vLLM Omni Cookbook Guidelines

Use this skill when working in `vllm-omni-cookbook`.

## Rules

- Optimize examples for clarity, reproducibility, and user success.
- Prefer complete runnable examples over abstract snippets.
- Include environment assumptions, model names, expected inputs, and expected outputs when useful.
- Keep tutorial code simple unless complexity teaches something important.
- Test commands and examples when practical, or clearly mark unverified assumptions.
- Record the vLLM-Omni tag/commit, paired vLLM version, and backend for runnable
  examples. Resolve flags and deploy formats from that target's docs and code;
  label older recipes with their supported release instead of silently mixing
  current commands with historical environments.
- For release updates, use the shared
  [maintenance workflow](../update-vllm-omni-skills/references/release-maintenance.md)
  and record which recipes were actually checked.
