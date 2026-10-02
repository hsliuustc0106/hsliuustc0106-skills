# vLLM Omni Review Skill

The canonical review skill lives in `vllm-project/vllm-omni` at
`.claude/skills/review-pr/SKILL.md`. The personal
[entrypoint](../skills/vllm-omni-review/SKILL.md) loads that repository source
through [repository-review-source](../skills/repository-review-source/SKILL.md).
The project sync script installs the loader, not a second maintained review
checklist. Inspect the source checkout and record the actual version read.
