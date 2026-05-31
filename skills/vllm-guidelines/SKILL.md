---
name: vllm-guidelines
description: Project guidance for working in vLLM-style inference engine repositories.
license: MIT
---

# vLLM Guidelines

Use this skill when working in `vllm`.

## Rules

- Be careful around scheduler, executor, distributed execution, attention backends, quantization, and model loading paths.
- Inspect nearby tests and existing architecture before changing behavior.
- Consider tensor parallelism, pipeline parallelism, speculative decoding, batching, streaming, and prefix caching where relevant.
- For CUDA, Triton, or low-level tensor changes, identify dtype, shape, device, layout, and memory ownership assumptions.
- Prefer focused regression tests near the changed subsystem.
- Avoid broad refactors unless the requested change truly requires them.

