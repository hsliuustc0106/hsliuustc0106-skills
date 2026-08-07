# Hardware Requirements

Hardware analysis answers two different questions: what has been demonstrated, and what may fit. Keep those answers separate.

## Contents

- [Required dimensions](#required-resource-dimensions)
- [Configuration classes](#configuration-classes)
- [Resource calculations](#resource-calculations)
- [NVIDIA GPU](#nvidia-gpu-analysis)
- [Ascend NPU](#ascend-npu-analysis)
- [Qualification protocol](#benchmark-and-qualification-protocol)

## Required resource dimensions

Report all relevant dimensions:

- checkpoint/download storage and temporary conversion space;
- available host RAM, pinned-memory behavior, and NUMA considerations;
- accelerator count and memory per device;
- topology and interconnect used by TP/SP/PP/DP or offload;
- precision, quantization, compile mode, attention backend, and offload mode;
- driver, runtime, framework, and operator-library versions;
- workload: batch/concurrency, sequence length or resolution, frames/duration, steps, input references, and output count.

A GPU-memory number without its workload and placement policy is not a hardware requirement.

## Configuration classes

Label each row as one of:

- `Measured configuration`: recorded end-to-end or benchmark result on the exact devices.
- `Official validated configuration`: primary recipe/report with a complete environment, not reproduced here.
- `Capacity proxy`: exact topology exercised on different devices only to study allocation or correctness.
- `Derived capacity estimate`: calculated from parameters/configuration with explicit assumptions.
- `Recommended configuration`: operational headroom added to evidence; explain the margin.
- `Not validated`: no suitable target-platform evidence.

Never rename a capacity proxy as a minimum or supported configuration.

## Resource calculations

Use cited inputs and show arithmetic. At minimum consider:

```text
raw_weight_bytes = sum(parameter_count_i * stored_bytes_i)
peak_device_memory ~= resident_weights + persistent_state + activations
                     + caches + communication_buffers + kernel_workspace
                     + allocator/runtime_reserve
host_memory ~= offloaded_weights + pinned_staging + preprocessing
              + request_media + runtime_overhead + filesystem_cache
```

Account for quantization scales/metadata, multiple task partitions, shared components, tensor-parallel shards, duplicated buffers, and whether offloaded resident layers retain CPU master copies. Checkpoint file size is not peak device memory. Aggregate accelerator memory is not interchangeable with per-device capacity.

Use an explicit headroom policy for a recommendation. Do not present the result as a measured minimum.

## NVIDIA GPU analysis

Record:

- exact GPU model, count, memory per GPU, PCIe/NVLink/NVSwitch topology;
- compute capability or architecture when it controls kernel availability;
- NVIDIA driver, CUDA, PyTorch, the selected runtime, and optional kernel versions; record vLLM/vLLM-Omni only when used;
- supported parameter/activation dtypes and quantization path;
- selected attention, GEMM, convolution, VAE, and compile backends;
- measured allocator peak versus sampled `nvidia-smi` peak;
- consumer versus datacenter constraints and any proxy validation.

Do not assume an attention backend available on one NVIDIA architecture works on another. Do not infer latency from a memory-only run.

## Ascend NPU analysis

Treat Ascend as an independent software and operator stack. Record:

- exact Atlas/Ascend product, NPU count, memory, and HCCS/PCIe topology;
- driver and firmware, CANN, Python, PyTorch, `torch_npu`, the selected runtime, and vLLM/vLLM-Omni versions only when used;
- required external operator packages and their pinned revisions;
- NPU-specific platform hooks, attention/fusion kernels, quantization, compile behavior, and fallbacks;
- task, shape, precision, and parallel configuration actually validated;
- missing CI, unsupported operations, known crashes, and CPU/CUDA dependency leaks.

CUDA code presence is not Ascend evidence. An NPU recipe for one task/shape is not blanket model support. If the general support table, recipe, release note, and CI disagree, report each axis and the conflict.

## Platform matrix

Use one row per materially different configuration:

| Platform | Device/topology | Software stack | Workload | Precision/placement | Device memory | Host RAM/storage | Configuration class | Support status | Evidence |
|---|---|---|---|---|---|---|---|---|---|

For requested but untested targets, write `Not validated` and provide a bounded capacity estimate only if enough inputs exist. State what run would promote it to recipe-validated or CI-covered.

## Benchmark and qualification protocol

For performance claims:

1. Pin hardware, software, model, and workload.
2. Use identical inputs, seed, precision, and output contract for A/B comparisons.
3. Exclude compile and cache warmup unless cold-start is the metric.
4. Run enough repetitions to report variability; use mean plus a spread measure.
5. Capture stage latency, end-to-end latency, throughput/concurrency, and peak memory.
6. Pair performance with task-appropriate accuracy or quality gates.
7. Save commands/configuration and profiler artifacts.

For generative media, successful file creation is only a smoke gate. Also validate decoding, dimensions/duration, modality presence, finiteness, and an appropriate semantic/perceptual quality baseline.

## Minimum versus recommendation

Use “minimum” only when a smaller configuration has been systematically tested and fails or is explicitly unsupported. Otherwise report:

- smallest evidenced configuration;
- recommended configuration with operational headroom;
- unvalidated lower-capacity candidates;
- the dominant constraint and how offload/quantization changes it.
