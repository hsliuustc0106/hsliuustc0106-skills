# NCU Report Skill

For CUDA kernel profiling with Nsight Compute on B200/sm_100, use the bundled
[ncu-report-skill](../skills/ncu-report-skill/SKILL.md).

## Provenance

- Source: https://github.com/mit-han-lab/ncu-report-skill
- Pinned upstream commit: [`74a12918e9f64d78036f14da5f8765e435b949a4`](https://github.com/mit-han-lab/ncu-report-skill/commit/74a12918e9f64d78036f14da5f8765e435b949a4)
- Imported: 2026-10-01
- License: [MIT, Copyright (c) 2026 hanlab](../skills/ncu-report-skill/LICENSE)

All 23 upstream files are included under `skills/ncu-report-skill/`, preserving
the upstream directory layout. The only local adaptation is a runtime-safety
and CLI-usage note in `SKILL.md`; helper code, references, README, and license
are unchanged.
The upstream README is retained for provenance; this repository's bundled copy
does not require cloning a second repository. Upstream directs bug reports and
feature requests to https://github.com/mit-han-lab/kernel-design-agents.

## Runtime requirements and safety

- Full profiling needs CUDA Toolkit (`nvcc`), Nsight Compute (`ncu`), a supported
  NVIDIA GPU, and access to performance counters. Upstream reports testing CUDA
  13.2 and Nsight Compute 2026.1, with B200/sm_100-specific metric guidance.
- Report-analysis helpers need the `ncu_report` Python module shipped with
  Nsight Compute. Dataset browsing uses local flashinfer-trace data.
- Use trusted reports, workload files, and output paths. The bundled minimal
  C++ safetensors loader does not fully validate untrusted file lengths/offsets.
- The upstream troubleshooting reference includes privileged and persistent
  GPU-counter configuration changes. Do not apply them automatically; obtain
  explicit authorization from the machine's administrator first.
- This import does not install dependencies, execute the upstream helpers,
  run GPU profiling, or change system permissions. Runtime profiling remains
  unverified until the required NVIDIA environment and representative inputs
  are available.
