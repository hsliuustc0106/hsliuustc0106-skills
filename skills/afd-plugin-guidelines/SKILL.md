---
name: afd-plugin-guidelines
description: Project guidance for working in plugin-style repositories with host framework integration boundaries.
license: MIT
---

# AFD Plugin Guidelines

Use this skill when working in `afd-plugin`.

## Rules

- Preserve plugin boundaries and avoid leaking project-specific logic into generic utilities.
- Be conservative with public APIs, config names, integration behavior, and compatibility assumptions.
- Check host framework expectations before changing lifecycle, registration, loading, or config behavior.
- Prefer focused tests that exercise plugin integration points.
- Keep examples and docs aligned with actual install and runtime behavior.

