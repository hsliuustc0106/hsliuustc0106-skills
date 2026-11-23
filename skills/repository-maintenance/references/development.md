# Shared development guidance

Read only the sections relevant to the change. Project instructions and
repository-owned contracts determine the actual supported behavior.

## Plugin and host integration

- Preserve plugin boundaries and avoid leaking project-specific logic into
  generic utilities. Check host expectations for lifecycle, registration,
  loading, and configuration changes.
- Consider public API, config, and integration compatibility. Exercise the
  affected integration points and keep install and runtime examples accurate.

## Inference engines and kernels

- Trace the affected scheduler, executor, distributed execution, attention,
  quantization, or model-loading path before changing its behavior.
- Consider tensor and pipeline parallelism, speculative decoding, batching,
  streaming, and prefix caching where relevant. For CUDA, Triton, or tensor
  changes, identify dtype, shape, device, layout, and memory ownership assumptions.

## Multimodal paths

- Consider interactions among text, image, audio, video, processors, modality
  routing, and model-specific inputs. When changing loading or input plumbing,
  inspect the affected text-only and multimodal paths.
- For downstream integrations, preserve compatibility with upstream engine
  contracts and conventions where practical.
- Check relevant processor configuration, prompt formatting, batching, caching,
  streaming, and examples; exercise the modalities affected by the change.

## Tutorials and examples

- Favor clear, complete, runnable examples. Include useful environment and model
  assumptions, expected inputs, and outputs, without unnecessary complexity.
- Test commands and examples when practical; identify unverified assumptions.
