---
name: vllm-omni-guidelines
description: Project guidance for working in vLLM Omni, especially multimodal model behavior and review workflows.
license: MIT
---

# vLLM Omni Guidelines

Use this skill when working in `vllm-omni`.

## Rules

- Treat multimodal behavior as first-class: text, image, audio, video, processors, modality routing, and model-specific input paths may interact.
- Preserve compatibility with upstream vLLM conventions where possible.
- When touching model loading, processing, or input plumbing, inspect both text-only and multimodal paths.
- Be careful around processor config, prompt formatting, batching, caching, streaming, and examples.
- Add focused tests or examples that cover the relevant modality.

## Review Workflow

For vLLM Omni code review, use the bundled
[vllm-omni-review skill](../vllm-omni-review/SKILL.md) as the source of truth.
