# Personal daily selection and bounded maintenance audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and records bounded source inspection;
it does not authorize upstream reviews, labels, merges, or code changes.

## Selection contract

Require the exact label `high priority`. If the complete current label catalog
contains `ready`, require both; otherwise require `high priority` alone. Unknown
catalogs and API/pagination failures block selection. Do not substitute the
canonical legacy helper's created-last-seven-days or ever-reviewed exclusions.
Old, previously reviewed, own, or draft PRs may qualify when the requested labels
and new-head criteria are met. Direct user-selected reviews bypass this queue.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from this skill
directory. It never fetches, posts, executes target code, or updates checkpoints.
The collector supplies:

- Repository `vllm-project/vllm-omni`, the Asia/Shanghai calendar `day`, complete
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

New commit evidence must preserve coverage across all completed review heads and
policies, including ancestry or commit-set analysis after history rewrites. A
previously covered ancestor can have a different SHA from every recorded head;
comparing only with the latest completed head is insufficient after a rewind or
branch switch. Keep the last successfully reviewed head and the earlier coverage
needed to prove the delta; unresolved history is unknown, not new code. Comment times,
creation dates, a changed label, or a new policy version do not prove new code.
The first run requires an explicit baseline or first-run authorization. Missing
checkpoint history is unknown. See `tests/test_omni_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. No delivery ledger belongs here.

## Current bounded audit, 2026-10-19 Asia/Shanghai

Personal main before this update: `8a8d071ffef45b3242d61c648f18b714a1a6c99e`.
Upstream main was frozen at
[1c0bde507dfbffd25b32f6092dbe4526c945b7dd](https://github.com/vllm-project/vllm-omni/commit/1c0bde507dfbffd25b32f6092dbe4526c945b7dd).
The [153-commit delta](https://github.com/vllm-project/vllm-omni/compare/198c2105930bd1bac0b0966ffd0997cdd84d4790...1c0bde507dfbffd25b32f6092dbe4526c945b7dd)
was enumerated in two pages (100 + 53); source inspection below is targeted,
not a review of all changed code. Latest published stable remains
[v0.30.0](https://github.com/vllm-project/vllm-omni/releases/tag/v0.30.0)
(2026-09-25). The following main-only observations do not establish release behavior.

The [canonical skill](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/.claude/skills/review-pr/SKILL.md)
was read in full: Git blob `96e9116e1c902e7197130d44fdfe9584ca1d4c34`,
exact-byte SHA-256 `23ff085a2e6e00bcae644217adb43c94432d773e78d13e124f33b3283af77a53`.
Current AGENTS, contribution instructions, lessons, routing, runtime-stage and
test-evidence references were read at this same revision. All 13 open personal
repository PRs were enumerated, followed by an empty page. PR6 and PR17 remain
at their previously recorded heads; their file scopes were inspected, but no
proposal content or human edits were imported or overwritten.

### Changed defaults and ownership to rediscover at the target

- [Event-driven orchestration](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/vllm_omni/engine/orchestrator.py#L89-L109)
  is now the default; `VLLM_OMNI_EVENT_DRIVEN_ORCH=0` selects the legacy polling
  loop. The [focused tests](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/tests/engine/test_orchestrator_event_driven.py#L74-L100)
  cover unset/opt-out dispatch. For related changes, inspect reader reconciliation,
  output draining and shutdown as well as both loop paths. This inspection did
  not run those upstream tests or measure latency.
- Prefix-cache ownership is split between the
  [manager](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/vllm_omni/core/prefix_cache/manager.py#L3-L14)
  (request/slot identity, scheduling and state lock) and the
  [controller](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/vllm_omni/core/prefix_cache/controller.py#L3-L20)
  (staging, byte budget, copy queues and CPU-pool committer). Trace the live write
  handle and release path across both; do not treat a manager-only diff as proof
  that asynchronous copy ownership is unchanged. CPU eager checks cannot prove
  CUDA transfer ordering or device-memory cleanup.
- [Local replica pinning](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/vllm_omni/engine/stage_pool.py#L482-L501)
  explicitly rejects unavailable/conflicting pins rather than selecting a fallback;
  session reservations belong to the duplex placement owner, not the per-request
  affinity ledger. Keep these lifetimes distinct when routing a session change.

### Operating-guide boundaries and validation

The new [maintainer operations guide](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/docs/contributing/ci/pr_merge_loop.md)
and [lessons](https://github.com/vllm-project/vllm-omni/blob/1c0bde507dfbffd25b32f6092dbe4526c945b7dd/docs/contributing/ci/lessons.md)
distinguish contributor local repair evidence from maintainer CUDA admission.
They are not a replacement for this explicitly configured ten-PR selection
contract, a live authorization, or a reason to change another loop's cadence,
quotas or permissions. Resolve current explicit owner settings separately from
dated operating-guide defaults; do not copy those settings into this loader.

All 249 personal-repository offline unittests passed, including the existing
31 selection fixtures, three corpus checks and Omni packaging test. Twelve
unique historical corpus sources were re-fetched and matched to their stored
Git blob and SHA-256 identities. The two defect families/four bounded outcomes
are unchanged: no additional accuracy sample or reviewer-quality claim.
Frontmatter, local links, source pins, manifests/routing, installer behavior,
Python/shell syntax and diff whitespace were checked. No upstream hardware,
model, serving, performance tests or live daily-selection collector ran. Hosted
checks are recorded separately after publication, never inferred from offline tests.

## Previous bounded audit, 2026-10-12 Asia/Shanghai

Personal main was `6a601ccdac242143ee67b12008653dbc2e7969c1` before this update.
Upstream main is frozen at
[198c2105930bd1bac0b0966ffd0997cdd84d4790](https://github.com/vllm-project/vllm-omni/commit/198c2105930bd1bac0b0966ffd0997cdd84d4790).
The [133-commit delta](https://github.com/vllm-project/vllm-omni/compare/c9bee166fb0f0b250eb227df5d1455c03a0509a1...198c2105930bd1bac0b0966ffd0997cdd84d4790)
from the prior audited main was enumerated in two commit pages (100 + 33).
The compare file list was capped at 300; this is a targeted audit, not full
coverage of every changed file or all architecture/platform combinations.

### Source selection and version boundaries

The [canonical main skill](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/.claude/skills/review-pr/SKILL.md)
was read in full: Git blob `5907e13f31245ac7063519108348ca6804d949cd`,
exact-byte SHA-256 `acdee5a45961d5f7b715a0d2f046f382dfa40d6607639d139863f405bf12566a`.
Its routing, runtime-stage and test-evidence references were read at the same
commit. PR8410 is still draft/open at `d29a35bb659a19eef5b520e85c449421a932b605`;
its proposed helpers/backend additions are not evidence that the existing main
skill is missing. Prefer the maintained main skill for ordinary reviews.
PR6 and PR17 remain open at the same heads recorded below; no proposal content
was imported or overwritten. All 12 open personal-repository PRs were enumerated,
with a following empty page; no overlapping branch was changed.

Latest published stable release is still [v0.30.0](https://github.com/vllm-project/vllm-omni/releases/tag/v0.30.0),
published 2026-09-25. Main's [CUDA container](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/docker/Dockerfile.cuda#L1-L2)
now bases on vLLM 0.31.0 following [#8459](https://github.com/vllm-project/vllm-omni/commit/0b0d2d70090e1df820de95ef599e109981bf06d0).
Do not extrapolate main-only behavior into the released v0.30.0 package.
Read target metadata and hardware requirements again rather than treating any
prior audit's dependency versions or CPU test selectors as current.

### Newly sampled ownership boundaries

These pointers supplement source discovery, not the canonical review checklist:

- [Ray diffusion executor](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/vllm_omni/diffusion/executor/ray_executor.py)
  and [its tests](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/tests/diffusion/test_ray_executor.py),
  introduced by #7938: Ray owns actor placement/lifecycle while PyTorch owns
  collectives. Review both boundaries, including owned versus caller-provided
  placement-group cleanup. Mock actor tests do not prove multi-node execution.
- [Serving route matrix](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/docs/serving/README.md#L147-L165),
  [connection implementation](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/vllm_omni/entrypoints/openai/realtime/connection.py)
  and [Qwen3 turn-based tests](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/tests/entrypoints/openai_api/test_qwen3_omni_realtime_websocket.py):
  generalized turn-based realtime (#8339) is distinct from continuous duplex.
  Resolve deployment mode, route/query and live handler together; the endpoint
  name alone does not establish duplex behavior.
- [MiniCPM-o duplex MRv2 profile](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/vllm_omni/deploy/minicpmo_4_5_duplex_mrv2.yaml)
  and [configuration tests](https://github.com/vllm-project/vllm-omni/blob/198c2105930bd1bac0b0966ffd0997cdd84d4790/tests/config/test_minicpmo_4_5_duplex_mrv2_deploy.py),
  from #8536: explicitly opt-in CUDA profile, all three stages use V2, and listed
  non-CUDA platform overrides retain V1. Do not infer a global/default MRv2 switch
  or GPU correctness from configuration tests.

Validation: 20 current instruction/code/test/document files were materialized and
matched against the frozen Git tree; 12 unique historical corpus files were
re-fetched and matched against both stored Git blob and SHA-256 identities.
The same two historical defect families/four outcomes remain; no new accuracy
sample or performance result is claimed. All 224 personal-repository offline
unittests pass, including 31 selection tests, three corpus checks and one Omni
packaging test. The added fixture consumes a collector-proven covered ancestor
across older policies; it does not implement ancestry discovery. Frontmatter,
local/pinned links, routing, installability, Python syntax, shell syntax and diff
whitespace were checked. No upstream tests, inference, distributed actors,
GPU/NPU execution or live daily-selection collector were run. Hosted checks are
reported separately after publication, not inferred from these local tests.

## Sources and overlap, inspected 2026-10-05 Asia/Shanghai

- Personal main baseline: `ebec75972ddbf2076ff9be3ce16009b756b34423`
- Prior partial release audit: [v0.28.0 record in open PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/blob/f01a5df38f337e65d80f420e6b22e0b30a5237af/skills/update-vllm-omni-skills/references/release-status.md),
  pinned upstream `eb11446b7f2e30ca582f8aff3afe12e9a2e66f6c`
- Latest published stable release at inspection: [v0.30.0](https://github.com/vllm-project/vllm-omni/releases/tag/v0.30.0),
  published 2026-09-25, tag commit `a8576ccb725c4e21cd13c3eb5f9a546b21149d2b`.
  Current main is separately pinned at
  [c9bee166fb0f0b250eb227df5d1455c03a0509a1](https://github.com/vllm-project/vllm-omni/commit/c9bee166fb0f0b250eb227df5d1455c03a0509a1);
  main-only findings are not release compatibility claims
- [Source migration PR8410](https://github.com/vllm-project/vllm-omni/pull/8410)
  remains open. The audited proposed source is
  [d29a35bb659a19eef5b520e85c449421a932b605](https://github.com/vllm-project/vllm-omni/blob/d29a35bb659a19eef5b520e85c449421a932b605/.claude/skills/review-pr/SKILL.md),
  skill Git blob `7646f8eed0168bcde2b5589411a7cf920ad639a7`, exact-byte SHA-256
  `7e8b4250f013aa26299fd606d0aed9739192d1e217c323c2339ec0e6b5abf00d`.
  It preserves the canonical architecture routing and incorporates backend and
  target-version safeguards; this is draft-source use, not a merged-source claim
- [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open. This pass does not
  merge, replace, or import their older bundled checklist or release workflow

## Bounded coverage observations

The source's target-version/hardware preflight and live-code-over-stale-docs rules
remain appropriate. No new architecture mandate was justified. Three newer feature
owners are absent from its feature tables; use these audit pointers when checking
freshness, resolving the actual target's versions before applying any contract:

- Unified duplex [ownership design](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/docs/design/fullduplex.md)
  and [session tests](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/tests/engine/duplex/test_session_runner.py):
  [merged #7413](https://github.com/vllm-project/vllm-omni/commit/99ff4f307040e85ba99e849ef013fdee89525378)
  moved session authority into the engine rather than the API entrypoint
- Paged diffusion KV [manager](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/vllm_omni/diffusion/diffusion_kv/manager.py)
  and [tests](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/tests/diffusion/diffusion_kv/test_manager.py):
  [merged #7719](https://github.com/vllm-project/vllm-omni/commit/205aa01c7b8e8a135ca7498cd6e6cf60919ac4ec)
  enables optional cross-request prefix caching, despite the
  [design's stale disabled statement](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/docs/design/feature/diffusion_paged_kv_cache.md#L230-L234).
  Do not treat paged allocation as an approximate TeaCache/Cache-DiT cache
- NIXL [lifetime design](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/docs/design/feature/omni_connectors/nixl_connector.md),
  [shared payload contract](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/docs/design/feature/omni_connectors/stage_payload.md),
  and [active-DMA close regression](https://github.com/vllm-project/vllm-omni/blob/c9bee166fb0f0b250eb227df5d1455c03a0509a1/tests/distributed/omni_connectors/test_nixl_connector.py#L817-L884)
  distinguish transfer timeout from completed ownership release

Output materialization, parallel stage startup, and the current CUDA/L4 test lane
were also sampled; existing I/O, startup-cleanup, and hardware-selection guidance
covers them. The old offload documentation URL redirects correctly and does not
justify cosmetic churn. The upstream checklist was not edited.

## Calibration and limits

[Adjudicated cases](adjudicated-cases.json) retain pinned defect and corresponding
fixed-clean examples. Clean means that specific historical defect is absent, not
that the whole PR is correct or approved. Fixture validation is not a measured
reviewer precision/recall or accuracy claim.

The four outcomes are two purposively selected merged defect/fix pairs:
[PR8279](https://github.com/vllm-project/vllm-omni/pull/8279), typed-config realtime
dispatch (P1 on that supported route), and
[PR8453](https://github.com/vllm-project/vllm-omni/pull/8453), unnecessary layerwise
weight restoration during shutdown (P2; OOM/timing impact is workload-dependent).
The exact base/head source files were checked against Git blob and SHA-256 pins;
29 supporting source/document files were verified. These are historical examples,
not new findings on main, four independent samples, or a blinded evaluation.

Validation in this pass: 30 network-free selection tests, three corpus
grounding/severity/routing/mechanism checks, and one packaging test. The full
personal repository suite has 75 passing tests. The separately materialized,
blob-verified source helper suite has 11 passing offline tests with GitHub stubbed.
All 20 skill entrypoints passed frontmatter/scaffold validation; pinned source
links, local links, manifests, install routing, shell syntax, Python parsing and
whitespace were checked. Fixtures were rerun with `PYTHONDONTWRITEBYTECODE=1`
from a clean tree because the existing installer test enumerates generated bytecode.

The release-to-main history contains 601 commits; the compare API exposed only
300 file records. This was targeted public-source sampling, not an exhaustive
architecture audit. Full model/platform integration, serving, hardware, inference,
performance, and accuracy remain untested. No live daily queue was selected and
no real delivery checkpoint was changed. The offline adapter trusts collector
proof; it does not prove live pagination completeness or commit ancestry itself.
