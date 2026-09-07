# vLLM-Omni Release Maintenance Record

- Upstream: `vllm-project/vllm-omni`
- Release: [v0.28.0](https://github.com/vllm-project/vllm-omni/releases/tag/v0.28.0)
- Commit: `eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c`
- Published: `2026-08-31T16:19:18Z`
- Reviewed: `2026-09-07` (Asia/Shanghai)
- Previous reviewed release: none recorded; this is the first targeted audit.
- Status: **partial — source inspection only**

## Checked areas and resulting guidance

| Area | Evidence at the release commit | Maintenance result |
| --- | --- | --- |
| Python requirements | [pyproject.toml](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/pyproject.toml) declares `>=3.10,<3.14`; dependencies are platform-specific | Removed the review reference's blanket Python >=3.11 requirement. Resolve the effective environment from both Omni and its dependencies. |
| CPU test selection | [Test execution guide](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/docs/contributing/ci/test_execution_guide.md) selects L1 with `core_model and cpu` | Removed the claim that `--run-level core_model` alone is CPU-safe. |
| Test placement and hardware marks | [Test writing guide](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/docs/contributing/ci/test_writing_guide.md), [marker helpers](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/tests/helpers/mark.py), [pytest plugins](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/tests/conftest.py) | Component tests can mirror source paths; E2E tests use separate locations. Hardware/SKU/card marks come from helpers. Derive selection from target source and fixtures. |
| Configuration design authority | [Configuration module document](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/docs/design/module/vllm_omni_config.md) is draft and explicitly defers contract definition | Removed the skill's unconditionally normative five-layer configuration proposal. Configuration requirements must come from the reviewed snapshot's accepted contracts and code/tests. |
| Deployment input discovery | [Pipeline/deploy configuration](https://github.com/vllm-project/vllm-omni/blob/eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c/docs/configuration/stage_configs.md) describes registered Python pipelines and deploy YAML | Removed the architecture reference's assumption that a legacy YAML adapter remains part of the current target contract. |

## Remaining release-impact work

The release notes identify additional changes that have not received a full
skill-reference audit here: output API migration, diffusion paged KV cache,
Host Weight Runtime/offload contracts, full-duplex lifecycle, model additions,
and platform-specific integrations. Check the owning source and tests before
using existing skill guidance for those areas. No model, benchmark, serving,
or accelerator execution was performed for this audit.

The cookbook and deck skills now require versioned technical evidence; their
examples and rendered assets have not been revalidated across the full release.
The absence of a reported issue in this record is not a compatibility claim.
