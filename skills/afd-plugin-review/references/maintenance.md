# Personal daily selection and bounded AFD audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and dated source-inspection results;
it does not authorize upstream reviews, labels, merges, or code changes.

## Selection contract

Require the exact label `high priority`. If the complete current label catalog
contains `ready`, require both; otherwise require `high priority` alone. Unknown
catalogs and API/pagination failures block selection. Do not substitute the
created-last-seven-days or ever-reviewed exclusions.
Old, previously reviewed, own, or draft PRs may qualify when the requested labels
and new-head criteria are met. Direct user-selected reviews bypass this queue.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from this skill
directory. It never fetches, posts, executes target code, or updates checkpoints.
The collector supplies:

- Repository `vllm-project/afd-plugin`, the Asia/Shanghai calendar `day`, complete
  `label_pages` (arrays of exact names), complete `pr_pages`, and affirmative
  `labels_complete`, `prs_complete`, `checkpoint_complete`, `baseline_confirmed`
- PR `number`, full `head` SHA, `state`, exact `labels`, `new_commits_verified`,
  and a final `current` observation of head/state/labels
- Confirmed `delivered` records with repository, number, full head, policy, day

Flags describe verified evidence, not assumptions. Empty pages are different
from unavailable pages. Conflicting duplicate observations invalidate the whole
snapshot; changed final head/state/labels block that PR. Label order is immaterial.
An unknown or malformed result has nonempty `blocked` and CLI exit status 2;
verified results, including no eligible candidates, exit 0. Inspect both output
and status; a blocked run must not be recorded as a successful empty review.

New commit evidence must compare the current head with the last completed review,
including ancestry or commit-set analysis after history rewrites. Comment times,
creation dates, a changed label, or a new policy version do not prove new code.
The first run requires an explicit baseline or first-run authorization. Missing
checkpoint history is unknown. See `tests/test_afd_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Normalize valid GitHub owner/repository identities case-insensitively before
consulting history; malformed identities make the checkpoint unknown.
Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. Serialize concurrent selection and
delivery or reconcile reservations against the same ledger; this snapshot adapter
does not enforce a cross-process cap. No delivery ledger belongs here.

## Current bounded refresh, 2026-11-10 Asia/Shanghai

This section supersedes older dated runtime assumptions below; it does not
replace the canonical review skill. [Source identities](audit-2026-11-10.json)
record this bounded inspection. Personal skills main was
`4c89c31db3addafbfc9f129c3102a2869242c428`; upstream main was
[e58fdec5876782b9c6a03683416611deea42af92](https://github.com/vllm-project/afd-plugin/commit/e58fdec5876782b9c6a03683416611deea42af92)
(2026-11-09 22:32:16 Asia/Shanghai). The complete comparison contains 21
commits and 274 changed paths after the November 3 pin (53 added, 184
modified, 17 removed, 20 renamed; the compare file list is under the 300-file
truncation limit). Targeted contracts were inspected, not every changed line.
Latest GitHub Release is now
[v0.32.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.32.0rc1)
(published 2026-11-04 22:08:42 Asia/Shanghai, `prerelease: true`). The tag is a
lightweight tag: the git ref object type is commit
`652e249872bc968fc645c68ba6683182e0f69368` (`fix(npu): keep profile routing
decisions inside an opaque op`, #500), not an annotated tag object. Main is
16 commits / 250 paths ahead of that RC; those 16 commits are **main-only**,
not released guarantees. Ancestry is confirmed: the five commits after
`c0e56c43` through #500 are in the RC (compare pin...RC is ahead_by 5,
behind_by 0, 56 paths).

- The canonical review skill was refreshed on main in #547 after the RC, so
  its current blob `c15faf1017b42950c4bf6a65c5eb38b2ca03fc00` is main-only
  until a later release includes it. Migration PR #420 stays closed unmerged;
  load current main rather than a closed migration branch. The skill points at
  `docs/UT_MAINTENANCE.md` and `docs/installation.md` for test rules and pins.
  It still lists "experimental FFN two-stream" as an FFN execution variant;
  that wording predates #550, which removed the implementation on current
  main. Resolve two-stream status from the reviewed head, not from the skill
  prose alone.
- Complete skills open-PR enumeration found 13 PRs (#28, #24, #22, #21, #20,
  #17, #15, #14, #13, #11, #9, #6, #4). PR #6 and #17 retain heads
  `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  `f01a5df38f337e65d80f420e6b22e0b30a5237af`; their complete file lists (PR #6:
  four vllm-omni-review files; PR #17: 18 files under omni skills, shared
  manifests, README, AGENTS.md, and `tests/test_helpers.py`) do not overlap
  these AFD-only changes. Shared manifests/routing and other projects remain
  untouched.
- The label catalog still contains both `high priority` and `ready`. No open
  PRs currently carry `high priority` (ready alone does not qualify), so there
  is no high-priority coverage set for this pass.

### Current contracts to rediscover

Released in or at v0.32.0rc1 (the five commits after the November 3 pin
through #500):

- NPU DSpark is no longer limited to legacy non-layered W4A8 FFN.
  [#525](https://github.com/vllm-project/afd-plugin/pull/525) enables DSpark
  target and draft layered experts;
  [#532](https://github.com/vllm-project/afd-plugin/pull/532) runs those
  experts on the existing FFN FULL graph.
  [feature_validation.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/compat/npu/feature_validation.py)
  still requires DeepSeek-V4, eager Attention/draft proposal, and target/draft
  TP=1, and keeps draft query capacity within `max_num_batched_tokens`. FFN
  may replay its expert transaction in FULL; Attention and native draft
  proposal stay eager.
  [deepseek_v4_dspark.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/model_executor/models/npu/deepseek_v4_dspark.py)
  exposes `get_async_cam_layered_weights` onto the existing FFN runner. The
  [AFDDSparkSpeculator](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/v1/worker/npu/dspark_speculator.py)
  blob is unchanged. Source acceptance of these gates is not NPU accuracy or
  speculative-acceptance proof; this path was not executed here.
- [#527](https://github.com/vllm-project/afd-plugin/pull/527) adds W8A8
  support in Async CAM layered execution;
  [#528](https://github.com/vllm-project/afd-plugin/pull/528) restores SwiGLU
  limits for layered W4A8 FFNs (configured limit `10.0`; layered W8A8 stays
  unclipped). These are in the RC.
- [#500](https://github.com/vllm-project/afd-plugin/pull/500) keeps profile
  routing decisions inside an opaque op (the RC tip).

Main-only after `652e2498` (not released guarantees):

- The root
  [README](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/README.md)
  is now a short entry point. Installation pins and the support matrix moved
  to
  [docs/installation.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/installation.md)
  and
  [docs/support.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/support.md).
  [pyproject.toml](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/pyproject.toml)
  still pins optional runtime `vllm==0.32.0`;
  [compat/vllm.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/compat/vllm.py)
  is unchanged and still asserts `TARGET_VLLM_VERSION = "0.32.0"`. The
  `afdep` extra now pins `afdep-comm @ …@v1.1.0` (the RC and the November 3
  pin still used commit `2b74d574e9d25cc794de8d2359f815fcfb48955a`).
  Installation evidence in `docs/installation.md` names vLLM `0.32.0` /
  `5df63a7203cdb9328d824a27b682e77c7b9928be` and vLLM-Ascend
  `bd42eea01d8312c4df469fabaed45f77a12df4d3`, plus a tested
  CANN/torch/torch-npu stack. A supported source pair is not a released
  Ascend wheel/container or proof of arbitrary-version compatibility.
- `docs/npu/TESTING.md` was removed. Current testing and documentation
  contracts are
  [docs/UT_MAINTENANCE.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/UT_MAINTENANCE.md)
  (linked from
  [AGENTS.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/AGENTS.md)),
  [tests/npu/README.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/tests/npu/README.md)
  (NPU runtime and operator tests; device tests remain outside CI),
  [docs/README.md](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/README.md)
  (documentation index), and
  [.buildkite/cuda/test-ready.yml](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/.buildkite/cuda/test-ready.yml)
  (L2 ready: CPU unit selection plus `tests/gpu/test_attention_routing.py` on
  `l4_1`, and the seven-case DeepSeek-V2-Lite GPU E2E gate on `l4_4`). Do not
  cite `docs/npu/TESTING.md` as a current-tip source.
- [DeepEPM2NAFDConnector](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/connectors/factory.py)
  remains registered beside P2P/CAM connectors.
  [#555](https://github.com/vllm-project/afd-plugin/pull/555) adds flexible
  Attention/FFN placement across pods.
  [layout.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/connectors/gpu/deepep_m2n/layout.py)
  and the
  [user guide](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/gpu/DEEPEP_M2N_CONNECTOR_USER_GUIDE.md)
  accept either an FFN-prefix placement or a per-domain layout where every pod
  holds the same FFN count (`N x <a>A<f>F`); mixed FFN counts or unequal pod
  sizes are rejected.
  [Recipes](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/recipe/gpu/DeepEPM2NAFDConnector/README.md)
  document `multipod_4a1f_4a1f_graph.sh` for that symmetric case.
  [validation.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/validation.py)
  still requires `compute_gate_on_attention=true`, FFN TP=1, and
  Attention-routing architectures `Qwen3MoeForCausalLM` or
  `DeepseekV2ForCausalLM`. Handshake-owned checks (payload, shapes, SM90+, EP
  layout, weight format) are not replaced by CPU unit coverage. Docs/unit
  presence is not GPU throughput, multi-node, or DeepGEMM correctness.
- Async CAM on current main:
  [#538](https://github.com/vllm-project/afd-plugin/pull/538) makes layered
  GMM the only Async CAM FFN path;
  [#550](https://github.com/vllm-project/afd-plugin/pull/550) removes FFN
  two-stream execution
  (`afd_plugin/v1/worker/npu/async_ffn_two_stream.py` is gone on the tip; the
  file was still present at the RC).
  [#517](https://github.com/vllm-project/afd-plugin/pull/517) adds opt-in
  pull-based MegaMoE (`ffn_mega_moe`, default false) via
  [async_cam_mega.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/model_executor/npu/async_cam_mega.py),
  which requires per-channel W4A8/W8A8 weights.
  [#551](https://github.com/vllm-project/afd-plugin/pull/551) clarifies
  session ownership in
  [async_cam_session.py](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/afd_plugin/connectors/npu/async_cam_runtime/async_cam_session.py):
  Push keeps a per-stage FIFO; Pull owns one in-flight Attention window and
  the fused FFN transaction. Pull may split one expert across receive rounds,
  so `validate_graph_capacity` and feature validation allow a receive capacity
  smaller than `max_num_batched_tokens` only when row slicing / MegaMoE is
  selected. The
  [CAM async user guide](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/docs/npu/CAM_ASYNC_CONNECTOR_USER_GUIDE.md)
  documents these contracts. None of this was executed here.
- The canonical
  [review-pr skill](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/.agents/skills/review-pr/SKILL.md)
  (#547) and
  [tests-docs-checklist](https://github.com/vllm-project/afd-plugin/blob/e58fdec5876782b9c6a03683416611deea42af92/.agents/skills/review-pr/references/checks/tests-docs-checklist.md)
  describe the current CI and docs evidence contract, including the
  `test-ready` selection above and `docs/UT_MAINTENANCE.md`. That refresh is
  main-only. New review-pr references include `dspark-draft.md` and
  `e2e-harness.md` (inspected as present; not separately byte-pinned).
- [#533](https://github.com/vllm-project/afd-plugin/pull/533) simplifies
  deploy-afd-k8s readiness, timeouts, and recipe parsing;
  [#556](https://github.com/vllm-project/afd-plugin/pull/556) updates the
  WeChat QR;
  [#557](https://github.com/vllm-project/afd-plugin/pull/557) adds path-based
  PR labels. These were not treated as review-skill contracts in this pass.

### Maintenance validation and limits

The AFD selector contract is unchanged: exact `high priority` (plus `ready`
when present in the catalog), new-head evidence, ten-distinct-PR Asia/Shanghai
day cap, case-insensitive owner/repository normalization, and delivery
deduplication. No selector code change in this pass.

The existing corpus remains two adjudicated defect families / four defect-clean
outcomes; twenty-five unique tip source artifacts were byte-verified against
pinned Git blobs and SHA-256 hashes. Four of the previous fourteen sources are
unchanged at the new tip (same blob as the November 3 pin):
`afd_plugin/compat/vllm.py`, `afd_plugin/connectors/factory.py`,
`afd_plugin/v1/worker/npu/dspark_speculator.py`, and
`.agents/skills/run-vllm-bench-k8s/SKILL.md`. No new adjudicated cases,
upstream tests, model inference, GPU/NPU execution or cluster deployment were
performed. Historical audits and `adjudicated-cases.json` are preserved.

Validation: the full personal-repository suite passed 266 network-free tests,
including 37 AFD daily tests (32 selector, four corpus/audit metadata, one
temporary-directory install/idempotence/conflict). All 24 skill frontmatters,
JSON/Python parsing (16 JSON files, 29 Python files), affected local links,
and diff whitespace passed. Twenty-five current-source files were
byte-verified against Git blob and SHA-256 pins. These fixture and packaging
checks are not upstream runtime tests or accuracy measurements. Installation
occurred only in temporary test directories.

## Historical bounded refresh, 2026-11-03 Asia/Shanghai

This historical section is superseded by the 2026-11-10 refresh above; it does
not replace the canonical review skill. [Source identities](audit-2026-11-03.json)
record this bounded inspection. Personal skills main was
`801da342d934a5d8bca67a49d4b480d3b0577b2d`; upstream main was
[c0e56c43e8a2f57ec164100c9d7e48e9a8588742](https://github.com/vllm-project/afd-plugin/commit/c0e56c43e8a2f57ec164100c9d7e48e9a8588742).
The complete comparison contains 8 commits and 182 changed paths after the
October 27 pin. Targeted contracts were inspected, not every changed line.
Latest release remains
[v0.30.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.30.0rc1)
(October 19, tag commit `9fcdbd1ff64698785fa0dcf2c61a817fd60f9f06`); main is
24 commits / 287 paths ahead of that RC. The new changes below are
**main-only**, not released guarantees.

- The canonical review skill's blob remains
  `81d94c95de61d37931111e770a791d1c0a2e5663`. Migration PR #420 stays closed
  unmerged; load current main rather than a closed migration branch.
- Complete skills open-PR enumeration found 13 PRs. PR #6 and #17 retain heads
  `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  `f01a5df38f337e65d80f420e6b22e0b30a5237af`; their complete file lists do not
  overlap these AFD-only changes. Shared manifests/routing and other projects
  remain untouched.
- The label catalog still contains both `high priority` and `ready`. No open
  PRs currently carry `high priority` (ready alone does not qualify), so there
  is no high-priority coverage set for this pass.

### Current contracts to rediscover

- [Dependency metadata](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/pyproject.toml)
  now pins optional runtime `vllm==0.32.0` (was 0.30.0) and the `afdep` extra to
  `afdep-comm @ …@2b74d574e9d25cc794de8d2359f815fcfb48955a`.
  [compat/vllm.py](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/compat/vllm.py)
  asserts exactly `TARGET_VLLM_VERSION = "0.32.0"`.
  [README installation evidence](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/README.md)
  names vLLM `0.32.0` / `5df63a7203cdb9328d824a27b682e77c7b9928be` and
  vLLM-Ascend `bd42eea01d8312c4df469fabaed45f77a12df4d3`. A supported source
  pair is not a released Ascend wheel/container or proof of arbitrary-version
  compatibility; earlier 0.30 pin statements are stale for current main.
- [DeepEPM2NAFDConnector](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/connectors/factory.py)
  is registered beside P2P/CAM connectors.
  [User guide](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/docs/gpu/DEEPEP_M2N_CONNECTOR_USER_GUIDE.md)
  and [recipes](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/recipe/gpu/DeepEPM2NAFDConnector/README.md)
  document Hopper SM90+ expert-routed M2N via afdEP-comm DeepEP + DeepGEMM.
  [validation.py](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/validation.py)
  requires `compute_gate_on_attention=true`, FFN TP=1, and Attention-routing
  architectures `Qwen3MoeForCausalLM` or `DeepseekV2ForCausalLM` (DeepSeek-V2-Lite
  recipes landed in #518). Handshake-owned checks (payload, shapes, SM90+, EP
  layout, weight format) are not replaced by CPU unit coverage. The README
  connector-table note that still says "Qwen3 MoE only" lags the guide and
  validator; resolve model support from validation + guide at the review target.
  Docs/unit presence is not GPU throughput, multi-node, or DeepGEMM correctness.
- NPU [DSpark eager A/F](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/model_executor/models/npu/deepseek_v4_dspark.py)
  patches role-local draft construction; the
  [AFDDSparkSpeculator](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/v1/worker/npu/dspark_speculator.py)
  scopes native proposal under the Attention AFD context and keeps the physical
  draft KV block size.
  [NPU feature validation](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/afd_plugin/compat/npu/feature_validation.py)
  limits DSpark to DeepSeek-V4, eager target/draft, TP=1, legacy (non-layered
  W4A8) FFN, and draft query capacity within `max_num_batched_tokens`. Source
  acceptance of these gates is not NPU accuracy or speculative-acceptance proof;
  this path was not executed here.
- [#465](https://github.com/vllm-project/afd-plugin/pull/465) adds the
  [run-vllm-bench-k8s](https://github.com/vllm-project/afd-plugin/blob/c0e56c43e8a2f57ec164100c9d7e48e9a8588742/.agents/skills/run-vllm-bench-k8s/SKILL.md)
  skill for one-run GPU colocation recipe benchmarking via `vllm bench serve`.
  Skill prose is workflow guidance, not a completed benchmark or published
  number from this maintenance pass. WeChat QR (#521) is asset-only.

### Maintenance validation and limits

The AFD selector contract is unchanged: exact `high priority` (plus `ready`
when present in the catalog), new-head evidence, ten-distinct-PR Asia/Shanghai
day cap, case-insensitive owner/repository normalization, and delivery
deduplication. No selector code change in this pass.

The existing corpus remains two adjudicated defect families / four defect-clean
outcomes; fourteen unique tip source artifacts were byte-verified against pinned
Git blobs and SHA-256 hashes. No new adjudicated cases, upstream tests, model
inference, GPU/NPU execution or cluster deployment were performed. Historical
audits and `adjudicated-cases.json` are preserved.

Validation: the full personal-repository suite passed 265 network-free tests,
including 37 AFD daily tests (32 selector, four corpus/audit metadata, one
temporary-directory install/idempotence/conflict). All 24 skill frontmatters,
JSON/Python parsing, affected local links, and diff whitespace passed. Fourteen
current-source files were byte-verified against Git blob and SHA-256 pins.
These fixture and packaging checks are not upstream runtime tests or accuracy
measurements. Installation occurred only in temporary test directories.

## Historical bounded refresh, 2026-10-27 Asia/Shanghai

This historical section is superseded by the 2026-11-03 refresh above; it does
not replace the canonical review skill. [Source identities](audit-2026-10-27.json)
record that bounded inspection. Personal skills main was
`93563df3abba4849ac60489e4bef05da14d1a1c3`; upstream main was
[2bcd76fcf318dda123124f4cfb1d08302f8a1ec9](https://github.com/vllm-project/afd-plugin/commit/2bcd76fcf318dda123124f4cfb1d08302f8a1ec9).
The complete comparison contains 12 commits after the October 20 pin. Targeted
contracts were inspected, not every changed line. Latest release remains
[v0.30.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.30.0rc1)
(October 19); the new changes below are **main-only**, not released guarantees.

- The canonical review skill's blob is unchanged. Migration PR #420 is closed
  unmerged; use current main rather than treating its branch as a fallback.
- Current `AGENTS.md` removed test-line budgets and the supporting baseline/hook.
  Earlier audit statements that those budgets apply are no longer current.
- Experimental FFN two-stream is off by default. Host ordering/lifetime tests do
  not establish native device safety, graph execution, overlap, or performance;
  the runtime documentation still requires device qualification. Keep this
  distinction when checking two-slot/two-stream and four-FULL-graph claims.
- Legacy `async_moe_ubatching`, `async_moe_num_ubatches`, and `async_moe_split`
  connector extras were removed. Native Attention DBO owns splitting; unknown
  extras are rejected. Connector extras now participate in configuration hashing.
- GPU P2P FFN peer exchanges use grouped NCCL receives/sends, including a single
  peer. Check peer wire order, stable buffers and output slicing rather than
  treating grouping as independently verified performance improvement.
- Multi-pod E2E explicitly disables MRV2 execution-evidence collection. Its
  accuracy-only success does not demonstrate graph replay or DBO execution.
- Layered W2/W13 validation is a supplied operator-only A3 report with three
  independent ABBA groups, not our execution. The rebased checkout was not
  separately rebuilt; do not sum cross-node gains or infer full-model throughput
  or long-running memory safety.

### Local selector repair and validation limits

The previously case-sensitive delivered-history identity could treat uppercase
GitHub owner/repository spelling as a different repository, bypassing covered-head
deduplication and the ten-distinct-PR daily cap. Normalize valid identities and
reject malformed ones as unknown. Two added test methods cover mixed-case
covered heads/cap history and malformed identities. On the old helper, the same
37-test suite produced three failures; on the repaired helper all 37 pass.
The full network-free repository suite passes 256 tests. These are helper and
packaging results, not production savings or review-accuracy measurements.

The existing corpus remains two adjudicated defect families / four defect-clean
outcomes; eight unique full source artifacts were reread and matched their pinned
Git blobs and SHA-256 hashes. No new adjudicated cases, upstream tests, model
inference, GPU/NPU execution or cluster deployment were performed. Complete
skills open-PR enumeration found 13 PRs; PR #6 and #17 file sets do not overlap
these AFD changes. Shared manifests/routing and other projects remain untouched.

## Historical bounded refresh, 2026-10-20 Asia/Shanghai

This section supersedes the dated runtime assumptions below, not the canonical
review skill. The earlier audit and defect/fixed-clean corpus remain historical
records; do not apply their old runner paths to a current deployment.
[Source identities](audit-2026-10-20.json) pin 15 reference/implementation files
by commit, Git blob, SHA-256, and byte length. Byte verification is not full
semantic coverage of every file or an upstream execution result.

### Release boundary and overlap

- Personal repository main inspected: `2a42d199ab94316023661d9d5309a1b818dc671b`.
- AFD main inspected: [0fff229b592bc489c8857cdabc39f247687acaf5](https://github.com/vllm-project/afd-plugin/commit/0fff229b592bc489c8857cdabc39f247687acaf5),
  27 commits after the previous audit. The full comparison's 27 commit entries
  were enumerated; only the runtime, review-guidance and test-contract surfaces
  described here were inspected in depth, not every changed line.
- [v0.30.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.30.0rc1)
  was published 2026-10-19 08:05:42 UTC with `prerelease: true`, no attached
  release assets, and tag commit `9fcdbd1ff64698785fa0dcf2c61a817fd60f9f06`.
  This RC includes the GPU/NPU MRV2 migration. Main is four commits beyond it:
  removal of unused PP adaptations (#469), test conventions (#470), unit-test
  consolidation (#467), and backend-aware sequence-parallel tests (#472).
  Do not describe these four changes as part of that released tag.
- PR420 remains open at `fbd0e5eb47128771994e0e9530fc230693d97b0a`.
  Canonical review content already exists on main; the proposed branch is not
  a mandatory replacement. The main checklist still says vLLM 0.26.0, asks for
  V1/V2 parity and says GPU V2 is gated off. Those statements conflict with
  current implementation. Resolve current compatibility from code and target
  dependency pins; do not reject a valid MRV2-only change using stale prose.
- Personal PR6 and PR17 remain open at the heads recorded below. All 13 open
  personal PRs were enumerated; PR6's four files and PR17's 19 files were
  inspected for path overlap. Neither touches this AFD supplement or selector.
  No existing PR, human edit, manifest or other project's policy is replaced.

### Runtime facts to revalidate at the review target

- [Dependency metadata](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/pyproject.toml)
  pins optional runtime `vllm==0.30.0`.
  [Installation evidence](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/README.md)
  names vLLM `ced6857afa0ea7b2e3f0846a62e1394e90f15607` and vLLM-Ascend
  `8d4409d6256d8a6729140ddcc0d1889e3f96cdd6`. A supported source pair is not
  proof of a released Ascend wheel/container or compatibility with arbitrary
  versions.
- [Deployment validators](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/validation.py)
  reject non-V2 GPU and NPU configurations. Both roles require the paired MRV2
  deployment, but GPU FFN remains an AFD-owned connector-driven runner, not
  native scheduler-driven MRV2 execution. PP/PCP/DCP sizes remain one; role
  ranks must equal DP times TP. Deleted V1 paths are not current fallback tests.
- [CUDA graph policy](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/v1/worker/cuda_graph.py)
  permits eager or FULL_DECODE_ONLY, with exactly two ubatches when enabled.
  NPU synchronous CAMP2P accepts eager/FULL/FULL_DECODE_ONLY; native DBO needs
  two ubatches, Attention DP greater than one, and no speculative decoding.
  [NPU feature validation](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/compat/npu/feature_validation.py)
  further requires FULL_DECODE_ONLY for plain MLA graph plus DBO. Do not
  flatten these model/connector-specific constraints into one platform matrix.
- Async CAM requires eager Attention with Attention-side gating and async DP.
  Its native DBO is Attention-only with two ubatches, including DP1. Independent
  FFN FULL is a separate, narrow W4A8 runtime contract, not blanket Async CAM
  graph support. Model, topology, device operator and cleanup evidence remain
  necessary; source acceptance of a flag is not proof of working hardware.
- PR421's Kubernetes recipes are now merged and included in v0.30.0rc1, unlike
  their open-proposal status in the earlier audit. This does not establish that
  every deployment variant has an executed Kubernetes acceptance test.

### Current testing guidance and limits

[Current AGENTS.md](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/AGENTS.md)
requires behavior/seam tests, shared fakes, mirrored source layout, and CPU-only
unit collection without torch/vLLM using guarded runtime imports. It forbids
production-Python substring assertions; test-line budgets and ownership also
apply. Historical AST/excerpt fixtures in this personal repository adjudicate
old defects only and are not a substitute for upstream behavior tests.

[Ready CI](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/.buildkite/cuda/test-ready.yml)
selects non-GPU/non-runtime unit tests plus seven named DeepSeek-V2-Lite cases
in the GPU V2 job, including `baseline-graph` and six `afd-v2-*` cases. [NPU testing](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/docs/npu/TESTING.md)
distinguishes real stream/event contract tests from transport and checkpoint
accuracy. Completed nonempty two-stage replays during actual requests, not
capture/profile/padded-only execution, qualify the stated graph+DBO gate.
DSV4 synchronous profiles with `check_answer=False` establish liveness, not
output correctness. Test #472's reported Ascend suite totals are author evidence,
not tests executed by this maintenance pass.

The existing two purposively selected defect/fixed-clean pairs (four correlated
outcomes), selection policy, ten-PR cap, and delivery ledger contract are
unchanged. No upstream PR review or daily queue execution was performed. No
GPU/NPU execution, model accuracy/performance measurement, distributed teardown,
Kubernetes deployment, or private project audit was performed.

Validation: the full personal-repository suite passed 250 network-free tests,
including 30 AFD selector cases, four AFD corpus/audit metadata checks, and the
AFD temporary-directory install/idempotence/conflict test. All 24 skill
frontmatters, JSON/Python parsing, affected local links, manifest/routing tests,
shell syntax and diff whitespace passed. Fifteen current-source files and eight
historical corpus files were byte-verified against Git blob and SHA-256 pins.
These fixture and packaging checks are not upstream runtime tests or accuracy
measurements. Installation occurred only in temporary test directories.

## Sources and overlap, inspected 2026-10-06 Asia/Shanghai

- Personal main baseline: `874421b1c16a14de54e497b29c33959353f067cd`
- AFD main: [9cae2d2ddaae7e1752fc12ead577d59540b17f27](https://github.com/vllm-project/afd-plugin/commit/9cae2d2ddaae7e1752fc12ead577d59540b17f27)
- Latest published release: [v0.26.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.26.0rc1),
  published 2026-08-19, tag commit `85e826ed8239dd9d8032375bb84a56116e24f0e0`.
  GitHub marks it `prerelease: false`, but its RC name is retained here; do not
  relabel it a fully validated stable release. Main is 63 commits ahead
- Last main review-skill edit: `76bd189c38a9d740bda5627be246f70da75160f4` (PR363), 20 main commits behind.
  This is source-edit history, not a previous complete-audit pin. No prior
  complete AFD audit ledger was present in this personal skill. This pass starts
  a bounded record rather than claiming all intervening architecture was audited
- The canonical review skill already exists on main. [PR420](https://github.com/vllm-project/afd-plugin/pull/420)
  is an open enhancement, pinned here at `fbd0e5eb47128771994e0e9530fc230693d97b0a`.
  It preserves AFD module routing and adds target-version and optional reviewer
  safeguards. Identify use of those enhancements as proposed-source use, never
  as merged policy. Load instructions and references from the same resolved SHA.
  Main SKILL Git blob: `81d94c95de61d37931111e770a791d1c0a2e5663`,
  exact-byte SHA-256: `bb5adbcfcec5910fd56220b822db4c88c8dfaec713aef86c119e8741c849359b`.
  Proposed SKILL Git blob: `498726dc2f21fa54f5db3506740ea85e4fabc538`,
  exact-byte SHA-256: `45efc81cbfe0cb5a63945a74174fbed96c5bb3bfdf61e57125f4593328ef4176`
- [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open.
  This AFD-only supplement neither replaces their human edits nor imports their
  Omni checklist or maintenance workflow

## Historical observations at the 2026-10-06 pin

Read the actual target's compatibility pins, dependency metadata, CI commands,
markers, fixtures, and module status before applying these dated observations.
Do not port Omni pipeline, diffusion, or stage-payload contracts into AFD's
attention/FFN split, connector handshakes, role workers, or runner V1/V2 paths.

- E2E runner changes have a live owning contract:
  [e2e_testing.md](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/design/module/e2e_testing.md).
  Route to that contract plus tests-quality evidence; add graph/DBO or platform
  overlays only for the scenario actually changed. Broad CODEOWNERS matching
  does not replace the module's more specific expertise
- [PR416](https://github.com/vllm-project/afd-plugin/pull/416) preserves caller
  chunked-prefill choices instead of automatically disabling the feature for
  DBO. Do not revive that removed default from old test advice
- Resolve accuracy gates from the frozen scenario, not the historical
  `GSM8K-7` shorthand in the performance reference. Current DeepSeek-V2-Lite
  DBO scenarios have a 24-sample floor; small-sample runs (up to 24) default
  to 0.25, larger runs and other models retain 0.27, and an explicit
  `AFD_GSM8K_THRESHOLD` takes precedence. At 24 samples this allows 6 correct
  answers rather than 7. This is smoke acceptance calibration, not proof of
  production accuracy, numerical equivalence, or paired validation on all backends
- [PR404](https://github.com/vllm-project/afd-plugin/pull/404) gates attention
  workspace warmup on graph-with-ubatching policy. Inspect worker-to-FFN
  workspace readiness when graph capture changes; ubatching alone does not
  justify extra eager warmup and synchronization
- Recent NPU changes need target-specific routing:
  [ubatch thread binding](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/afd_plugin/v1/worker/npu/ubatching.py#L37-L46)
  sets the device before stream queries/barriers;
  [layered W4A8 validation](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/npu/TESTING.md#L24-L66)
  crosses feature flags, FFN dataflow, native bindings and kernels. Trace both
  ends rather than applying a CUDA-only graph check to these NPU paths
- [Routed native operators](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/npu/CAM_ASYNC_ROUTED_OPS.md)
  tie HCCL buffer tiling and per-group allocations to source-built operator
  revisions. CPU goldens, Meta bindings, and dry runs do not establish device
  support. [Current Buildkite gates](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/.buildkite/cuda/test-ready.yml)
  select CPU-marked unit tests in a runtime-equipped image plus GPU E2E lanes;
  NPU evidence remains manual. Do not equate CPU selection with a dependency-free
  import requirement for every runtime module
- [PR421](https://github.com/vllm-project/afd-plugin/pull/421) remains open.
  Its GPU P2P colocation multi-pod deployment proposal is not landed architecture
  or a currently required Kubernetes E2E lane. Resolve its state anew before
  treating any proposed command or deployment contract as supported

## Calibration and limits

[Adjudicated cases](adjudicated-cases.json) contain two purposively selected
historical defect/fix pairs, four outcomes total. The fixed-clean cases mean
only that their specific defect is absent, not that the PR is approved or the
whole runtime is correct. Fixture checks are not reviewer precision, recall,
accuracy measurements, a blinded evaluation, or four independent samples.

PR416 covers caller-choice preservation and a reported Legacy startup stall;
it does not prove the separate large-message/SHM production deadlock is fixed.
PR404 covers the graph/eager warmup gate, with a public P2 review adjudication;
CPU/source evidence cannot establish GPU memory or synchronization performance.
The test fixtures parse only pinned excerpts without importing upstream code.

This is a partial public-source audit. GPU/NPU execution, model inference,
accuracy/performance, live distributed teardown and Kubernetes deployments were
not run. No live daily queue or delivery ledger was changed. The network-free
adapter trusts collector evidence; it does not itself prove remote pagination,
commit ancestry, or successful delivery. Missing evidence must remain unknown.

Validation for this pass: 30 network-free selector tests, three corpus
source/severity/routing/mechanism checks, and one AFD packaging test passed;
the full personal-repository suite passed 113 tests. An independent 19-test
selector pass included 1,000 seeded randomized cap/dedup scenarios. All 20 skill
entrypoints, local links, manifests, installation routing, shell syntax, Python
parsing and diff whitespace were checked. Eight full historical source files
matched Git blob and SHA-256 pins. The main/proposed canonical skill contains no
executable helpers, so source-helper execution is not applicable. These checks
validate this bounded supplement, not upstream GPU/NPU behavior.
