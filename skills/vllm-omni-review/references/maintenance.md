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

New commit evidence must compare the current head with the last completed review,
including ancestry or commit-set analysis after history rewrites. Comment times,
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
