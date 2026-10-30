# Personal daily selection and bounded maintenance audit

This supplements the personal daily brief only. Repository-owned source remains
canonical for engineering review. It does not authorize posting or label changes.

## Explicit System1 daily-review override (October 29, 2026)

For the owner-configured **Daily reviews and opportunities** workflow, pass
`policy: "system1-nondraft-new-commits-v1"` to the offline adapter. This explicit
System1-only policy overrides the label filter below and the upstream optional
daily-selection reference: ignore labels, require open **non-draft** PRs and
verified new commits. The legacy/default label-filter mode below remains for
workflows that have not been explicitly assigned this override. An unknown policy
fails closed. This adapter covers only System1 Omni, not other repositories.

The final snapshot must include identical `head`, `state` and Boolean `draft`;
label discovery and label changes are irrelevant in override mode. Complete PR
pagination and checkpoint history remain mandatory. The collector must verify
push/commit activity since the previous completed review/brief, not infer it from
`updated_at` or a commit's author date. On first check, supply `first_run: true`,
`first_run_baseline_verified: true`, and each candidate's
`verified_activity_last24h: true` only after establishing the baseline and
verifying that activity. The adapter trusts those assertions; it does not query
GitHub or independently establish timestamps/ancestry.

The verified repository rename from `ThinkFlowLab/system1-omni` to
`InferMatrixLab/system1-omni` retains repository ID `1386454853`. The adapter
accepts both names and emits the historical ledger identity so the rename cannot
reset completed-head deduplication or daily capacity. A policy change alone is
not new code: unchanged completed heads stay covered across policy versions.
The ten-distinct-PR daily ceiling is a ceiling, not a review target; selection is
not substantive review, approval, publication or confirmed delivery. Re-fetch
mutable state again at actual review and finalization boundaries.

## Exact selection contract

The explicit personal policy requires `high priority` (space), not
`high-priority` (hyphen). The latter appears in the canonical upstream daily
reference at the pinned revision below; do not silently substitute it. If the
complete current catalog contains `ready`, require both exact labels; otherwise
require `high priority`. API failures and incomplete pagination are unknown and
block selection. Directly requested reviews do not use this daily filter.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from this skill's
directory. The helper is network-free and read-only. It consumes `repository`,
Asia/Shanghai `day`, complete `label_pages` and `pr_pages`, and affirmative
`labels_complete`, `prs_complete`, `checkpoint_complete` flags. These flags
must describe verified evidence, not assumptions. Each PR supplies number, head,
state, exact labels, `new_commits_verified` and a final `current` snapshot of
head/state/labels. Missing or stale evidence blocks that candidate. See
`tests/test_system1_daily.py` in the source repository for executable examples.

The collector must resolve new head commits since the previous delivered review,
including ancestry/commit-set comparison after a force push; timestamps alone do
not prove new commits. False means no new code; unknown means blocked. Old PRs
and previously reviewed PRs remain eligible when their heads contain new code.
A first run requires an explicit baseline or first-run authorization.

Delivered entries record repository, number, head, policy and Asia/Shanghai day.
Deduplication uses repository/PR/head/policy; an already delivered head remains
covered even if the policy changes. Missing delivery history blocks selection.
The cap is ten distinct PRs per
repository/day across deliveries, including previous policy versions. Deferred
heads remain pending. Selection never records delivery; only commit checkpoint
updates after confirmed delivery. Reconcile uncertain delivery before retrying.
The helper trusts the collector's evidence; it does not implement GitHub fetching,
ancestry validation, persistence, or dispatch.

## Bounded update, 2026-10-31 Asia/Shanghai

Public visibility and repository ID `1386454853` were verified after the move to
`InferMatrixLab/system1-omni`. Personal baseline is
`839c69fbd269946f1742cfbf21210dfe9fd666b0`. The new
[upstream pin](https://github.com/InferMatrixLab/system1-omni/commit/e573260cc467a3bf4119311ebda2bfc351667e1a)
is 278 commits beyond the October 24 audit. Commit pagination covered 100/100/78;
the compare file list capped at 300, so complete non-truncated trees were
reconciled: 334 added/changed blobs, zero removed. This is a bounded instruction
and test-routing audit, not a correctness review of those commits/files.

The sole release remains October 6
[`release/v0.1.0`](https://github.com/InferMatrixLab/system1-omni/releases/tag/release/v0.1.0)
at `7f39ac40902c374803992407bb26eeba29c8a588`; current main is 593 commits ahead.
The following changes are main-only, not released behavior:

- The [canonical review skill](https://github.com/InferMatrixLab/system1-omni/blob/e573260cc467a3bf4119311ebda2bfc351667e1a/.agents/skills/system1-omni-review/SKILL.md)
  now includes Public231 fast-screen provenance, same-request-ID baselines,
  bucket shortfalls, real hardware smoke, auditable DROP timestamps and the
  distinction between screening and full-C1 KEEP gates. Load its current source;
  this wrapper does not copy hardware numbers or claim to reproduce them.
  Canonical blob is `f3633eed045992caa8886847afcfc64cdbc417c7`, SHA-256
  `3a4b876162da14eee8db56af86664576aa5755b8f3e80b3072e944018647c3bc`.
  Both canonical reference blobs are unchanged from October 24. Their historical
  architecture and optional label policy must not override current code or the
  owner's explicit daily System1 policy above.
- [Current CI](https://github.com/InferMatrixLab/system1-omni/blob/e573260cc467a3bf4119311ebda2bfc351667e1a/.github/workflows/ci.yml)
  adds a CUDA 13.0 / TileLang 0.1.14 compile job with declared-backend build and
  ELF inspection. It does not execute device kernels. Benchmark routing adds
  JEV-VL vision-export and Clef Python tests; Rust retains `omni-laya/serve`.
- [Runtime routing](https://github.com/InferMatrixLab/system1-omni/blob/e573260cc467a3bf4119311ebda2bfc351667e1a/src/runtime/README.md)
  includes optional bounded admission/execution context with cancellation,
  deadlines and reservation lifetimes. Decider opts in; other workers are not
  automatically covered, and cancellation does not preempt device work.
- [Architecture](https://github.com/InferMatrixLab/system1-omni/blob/e573260cc467a3bf4119311ebda2bfc351667e1a/docs/architecture.md)
  now includes StartLux Instant, Clef's single Python executor behind Rust
  serving, online JEV-VL vision, and bounded Cua text-prefix reuse. Shared
  cross-request dynamic batching remains planned. Prior proposal-only PR127 is
  now merged. Current CUDA ABI remains 9.
- The [support matrix](https://github.com/InferMatrixLab/system1-omni/blob/e573260cc467a3bf4119311ebda2bfc351667e1a/docs/supported-models.md)
  adds multiple native/reference paths, but evidence remains model/hardware
  specific. StartLux's CUDA-unverified row must not be silently replaced with a
  broad correctness claim based on historical benchmark prose.

CONTRIBUTING and PR template were read and unchanged; no AGENTS.md, CLAUDE.md or
CURSOR.md was found in the complete upstream tree. Skills PR6 and PR17 remain
open at their previously recorded heads; their complete 4/18-file inventories
have no overlap with this four-file System1-only patch. Neither was modified.

The adapter now supports the explicit owner override while retaining the legacy
label-filter default. Offline regression cases cover non-draft freshness,
label-independent selection, unknown evidence/pages, first-run evidence,
renamed-repository accounting and cross-policy completed-head deduplication.
All five historical calibration source entries were re-fetched: exact lines,
Git blobs and full-file SHA-256 match. The four cases remain two related pairs
from one PR, not independent accuracy samples. No accuracy claim is made.
Validation commands/results accompany the maintenance commit and report.
No live queue selection, upstream review/publication, model/GPU execution,
benchmark campaign, personal installation or upstream changes occurred.

## Bounded update, 2026-10-24 Asia/Shanghai

Public repository visibility was verified before inspecting or publishing source
information. Personal baseline: `fd9a96460492efe2084a7216963a7f640cc21dfc`.
The new [upstream snapshot](https://github.com/ThinkFlowLab/system1-omni/commit/a893f0cf55135623fb093f401d8ce4713330d801)
is 92 commits beyond the October 17 pin
[`e66ff34996760a84ad56690f0ae4cf434e669e65`](https://github.com/ThinkFlowLab/system1-omni/commit/e66ff34996760a84ad56690f0ae4cf434e669e65)
and 315 beyond the unchanged `release/v0.1.0` tag. The release API still lists
only that October 6 release at `7f39ac40902c374803992407bb26eeba29c8a588`.
This is a bounded maintenance pass, not a correctness audit of those 92 commits.

Canonical SKILL SHA-256 remains
`ae2dfac116376ae2ec41f65122cc1bf5aea10751b8b907198a56154e5d67230e`,
Git blob `392df4c8881624ad8b9670101d51869562f6c68a`. Both canonical references
retain the October 10 blob IDs (`repository-contracts`
`b6ace00bf8a7486cd20b0ed2e5d19515ef6d1ef0`, `daily-selection`
`e28e81b1696c1a93817eb27384cc5ebc3d8919c1`). The canonical skill tree was
byte-identical at the prior and current pins. The source-owned checklist remains
canonical; this wrapper needs no copied checklist or SKILL.md text change.

Material routing changes since the October 17 snapshot:

- [CONTRIBUTING validation matrix](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/CONTRIBUTING.md)
  and [CI](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/.github/workflows/ci.yml)
  are unchanged at the pinned blobs from October 17. Prior notes about
  `--features omni-laya/serve`, Decider Python helpers, and conditional CUDA
  contract-checker steps still apply.
- [Architecture](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/docs/architecture.md)
  now inventories [JEMM](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/src/models/jemm/README.md)
  on the shared Qwen executor with separate unmerged FP32 adapters: selected BF16
  label-head logits on CUDA, typed calibration on CPU, one complete text or
  1–4-image request, both streams synchronized before release. Cua-S1 unmerged
  text finishing rounds answer-letter logits to the tied `lm_head` BF16 output
  dtype before FP64-normalized FP32 probabilities; legacy merged text and
  screenshot readouts retain FP32 logits. Do not treat an architecture paragraph
  that omits JEMM as a complete implementation inventory.
- Root [Cargo workspace](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/Cargo.toml)
  adds `src/models/jemm/native`. Workspace membership alone is not GPU or
  released-behavior proof.
- [Supported models](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/docs/supported-models.md)
  adds the JEMM native worker row (A800 frozen text/1–4-image corpus; host checks
  only on CPU) and a Cua-S1 native screenshot worker row; the experimental
  JEV-VL row now requires rebuilt ABI 9. [MkDocs](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/mkdocs.yml)
  surfaces JEMM, native screenshots, and Cua text-parity docs.
- [CUDA contract](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/src/backends/cuda/contract.md)
  is no longer marked proposed-only: the `cuda-contract` CI job runs checker,
  backend and metadata tests on CPU. Those steps do not compile CUDA or prove
  device numerical parity. Current `CS1_ABI_VERSION` in
  [`ops.h`](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/src/backends/cuda/qwen3_5/ops.h)
  is **9**; historical PR ABI numbers are not the current build requirement.
- [Benchmarks README](https://github.com/ThinkFlowLab/system1-omni/blob/a893f0cf55135623fb093f401d8ce4713330d801/benchmarks/README.md)
  documents Score wire precision (`--score-decimals`), Decider's two-decimal
  Score versus four-decimal probabilities, JEV-VL `--protocol jev-vl`, strict
  UTF-8 body bytes, and warmup. The serving-matrix client remains a frozen-oracle
  HTTP client, not a model launcher. Default four-decimal Score validation can
  reject valid Decider responses.

Notable merges in range (partial inventory, not a full correctness review):
[#117](https://github.com/ThinkFlowLab/system1-omni/pull/117) Qwen 27B vision,
[#118](https://github.com/ThinkFlowLab/system1-omni/pull/118)/[#122](https://github.com/ThinkFlowLab/system1-omni/pull/122)/[#123](https://github.com/ThinkFlowLab/system1-omni/pull/123)/[#155](https://github.com/ThinkFlowLab/system1-omni/pull/155)
JEMM native stack, [#135](https://github.com/ThinkFlowLab/system1-omni/pull/135)
Cua execution pipeline, [#143](https://github.com/ThinkFlowLab/system1-omni/pull/143)
Cua text parity, [#93](https://github.com/ThinkFlowLab/system1-omni/pull/93)
bench Score wire rounding, [#100](https://github.com/ThinkFlowLab/system1-omni/pull/100)
Laya TileLang target pin, [#131](https://github.com/ThinkFlowLab/system1-omni/pull/131)
decision-latency evidence. Other areas touched but not exhaustively audited
include qwen3_5 shared vision/CUDA Graph work, Cua resident features, and
benchmark protocol hardening. Their complete source, model-quality and
performance qualification are outside this maintenance pass.

Open high-priority proposals remain proposal-only. Label catalog was fully
enumerated (15 names across the Labels API; exact `high priority` present; no
`ready` and no `high-priority`). Personal daily selection therefore still
requires exact `high priority` alone. Nineteen open PRs currently carry that
label (numbers 156, 152, 151, 149, 148, 147, 146, 140, 139, 134, 129, 127, 124,
113, 112, 109, 101, 99, and draft 82). No verified collector snapshot with
affirmative completeness flags, delivery history and new-commit ancestry was
built in this pass, so `scripts/select_daily.py` was not run against live data.
Listing labeled open PRs is not a daily-queue delivery and does not authorize
reviews. Personal [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
(`68d7b38df04c382e9e51c9fde28428181d3bc5a8`) and
[PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
(`f01a5df38f337e65d80f420e6b22e0b30a5237af`) remain open at the same heads;
neither was merged, closed or overwritten.

Selection contract, offline adapter and historical calibration are unchanged.
All four pinned adjudication rows (two PR30 defect/fix pairs) were re-fetched
and matched exact lines, full-file SHA-256 and Git blob IDs. Four rows remain two
related pairs from one historical PR, not four independent accuracy samples.
No accuracy percentage is claimed.

Validation for this pass is recorded in the commit message and the Saturday
maintenance report: repository unit tests with bytecode disabled, skill
frontmatter/link/pin checks as covered by existing System1 tests, and Bash
syntax for `scripts/select_daily.py`. No live candidate selection, upstream
Rust/model/GPU tests, benchmark campaign, paid execution or personal installation
is part of this pass. The October 17 and October 10 sections below retain their
original dates, counts and scope.

## Bounded update, 2026-10-17 Asia/Shanghai

Public repository visibility was verified before inspecting or publishing source
information. Personal baseline: `76697726e8a93d1a02633bbbaf3da8fc72410308`.
The new [upstream snapshot](https://github.com/ThinkFlowLab/system1-omni/commit/e66ff34996760a84ad56690f0ae4cf434e669e65)
is 156 commits beyond the October 10 audit and 223 beyond the unchanged
`release/v0.1.0` tag. The release API still lists only that October 6 release.
This is a bounded maintenance pass, not a correctness audit of those 156 commits.

Canonical SKILL SHA-256 is
`ae2dfac116376ae2ec41f65122cc1bf5aea10751b8b907198a56154e5d67230e`,
Git blob `392df4c8881624ad8b9670101d51869562f6c68a`. Both canonical references
retain the hashes recorded below. All three were read at the new snapshot.
The source-owned checklist remains canonical; this wrapper needs no copied
checklist or source-registry change.

Material routing changes since the prior snapshot:

- [Contributor validation matrix](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/CONTRIBUTING.md#choose-validation-by-changed-area)
  and canonical review routing now point to current CI. Rust Clippy, workspace
  tests and release build use `--features omni-laya/serve`; the explicit frontend
  target remains. The human contributor-intent gate does not block independent
  read-only reviews or alter automated daily selection.
- [CI](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/.github/workflows/ci.yml)
  adds Decider Python helper checks and text-only CUDA backend/contract checks.
  The contract-checker steps are conditional on checker files being present;
  a skipped step is not proof the checker ran. Strict MkDocs remains separate.
- [Frontend in-process transport](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/src/frontend/src/engine.rs)
  now serves the runtime Engine interface as well as the existing forwarding
  path. Route changes through root `tests/frontend/in_process.rs` and
  `tests/runtime/engine.rs`; an architecture paragraph describing only forwarding
  is no longer a complete implementation inventory.
- [Decider packing](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/src/models/decider/native/src/batching.rs)
  is bounded within one admitted request: one row by default, configurable up to
  four rows and 4096 tokens, retaining order and running over-budget rows alone.
  This does not establish cross-request dynamic batching. The native manifest
  routes contract/config/batching and separately hardware-dependent GPU tests.
- [OmniJev](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/src/models/omnijev/README.md)
  currently supplies CPU contract/preparation/heads/finishing; its vision/language
  execution and worker integration remain future work. Do not infer a working
  native multimodal server from workspace membership.
- [Native multimodal Graph regressions](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/tests/qwen3_5/README.md)
  now include three ignored device cases and a runner requiring exactly three
  passes plus capture-failure diagnostics. Default CPU Cargo success cannot
  qualify them. The [serving matrix](https://github.com/ThinkFlowLab/system1-omni/blob/e66ff34996760a84ad56690f0ae4cf434e669e65/benchmarks/serving_matrix.md)
  is a frozen-oracle HTTP client, not a model launcher or GPU allocator; metadata
  presence does not independently prove hardware execution.

Other merged areas were discovered but not exhaustively audited: Laya graph/cache
changes, CLM serving, D3 and LFM2 reference integrations. Their complete source,
model-quality and performance qualification are outside this maintenance pass.
PR127 remains open, now non-draft at
`03b111ce3f97dd97c57cc6a9023de2aa7ee56be6`, targeting `codex/qwen-vision-27b`.
Its updated author-reported GPU evidence does not make it main/released behavior
or a personally rerun measurement. The October 10 draft/head statement below is
historical. Personal PR6 and PR17 still have the recorded heads and remain open;
neither was merged, closed or overwritten.

Selection remains unchanged: exact `high priority`, conditional `ready`, verified
new code, ten distinct PRs per repository/day, and delivered-head deduplication.
Four additional offline cases cover a later-page API error, unknown new-code
status, a new head on an already-counted PR at the daily cap, and delivery-history
repository isolation. Historical calibration remains four rows from two related
PR30 defect/fix pairs, not an independent accuracy sample. All five pinned source
files/companion entries were checked against Git blobs, SHA-256 and exact lines.

Validation: all 228 repository tests passed with bytecode disabled, including
31 System1 tests (27 selection and four evidence/install tests). Temporary Codex,
Claude and Cursor installs passed their resource/link checks. Skill frontmatter,
plugin directory discovery, eight pinned source links, five calibration source
entries, Bash syntax and whitespace checks passed. The three public adjudication
comments were re-read. These deterministic checks do not measure review accuracy.
No live candidate selection, upstream Rust/model/GPU tests, benchmark campaign,
paid execution or personal installation is part of this pass. The earlier audit
below retains its original date, counts and scope.

## Audited sources, 2026-10-10 Asia/Shanghai

- Personal repository baseline: `c8bb06da269adcf8c39eb1c61f2b576ae4f70fb0`
- [Canonical skill PR62](https://github.com/ThinkFlowLab/system1-omni/pull/62)
  merged on October 3 at `f830fcbeb76977649c566ddf94564004668758f4`. The canonical
  skill and both references are now on main; the source registry no longer
  advertises an unmerged proposal for this project
- [Current main](https://github.com/ThinkFlowLab/system1-omni/commit/6b51652b69c761994f9c944505d2527c92b5d254)
  is the immutable source for this audit, replacing the prior inspected main
  `1be7d41eb74d5b49fd25194042041319950e5dce`. Load current canonical instructions
  through the loader rather than treating this maintenance snapshot as policy
- Canonical bytes SHA-256: SKILL `58be3bc60806c4c5af7038a0c6a80fadb94f3360d714556a3e965c8903dde108`;
  repository-contracts `d6ae9650e4e18e8986926a790339412f52750fd1eeb19d358e5d91cd547f1202`;
  daily-selection `3b0e8e73662313a6f8f65f144f21dab31c73dcdf871aa91745712a764e467f93`
- Corresponding Git blob IDs: SKILL `7f245253cd05072507c63581ecd2f3e62bd2f97f`;
  repository-contracts `b6ace00bf8a7486cd20b0ed2e5d19515ef6d1ef0`;
  daily-selection `e28e81b1696c1a93817eb27384cc5ebc3d8919c1`

## October 10 release boundary and routing

[Release `release/v0.1.0`](https://github.com/ThinkFlowLab/system1-omni/releases/tag/release/v0.1.0)
was published October 6 at `7f39ac40902c374803992407bb26eeba29c8a588`. Audited
main is 67 commits ahead of that tag and 231 ahead of the prior audited main.
This was a bounded source/status pass, not a correctness review of all 231 commits.

The canonical repository map is explicitly historical at
`873655b4484dc2f537658644ebefd03630e9d507`. Consult current
[architecture](https://github.com/ThinkFlowLab/system1-omni/blob/6b51652b69c761994f9c944505d2527c92b5d254/docs/architecture.md),
code, Cargo targets and CI for actual routing. The workspace now includes frontend,
runtime, CLM, Cua-S1, Qwen, Open-Jev, JEV-VL, Laya and CUDA crates. Serial FIFO
admission/blocking dispatch is implemented; cross-request dynamic batching and
shared processing orchestration remain planned. Laya has English native Hopper
CUDA execution; native Metal remains unimplemented. Open-Jev bounded within-request
packed prefill uses groups of at most 16 candidates / 4096 tokens, with longer
prompts alone. This is not general dynamic batching. The runtime README's older
one-prompt Qwen statement must be reconciled with actual implementation. Shared
Qwen ABI is now 6; the map's older ABI description is not the current contract.

[PR96](https://github.com/ThinkFlowLab/system1-omni/pull/96) merged October 9 at
`0d2521035107e35a2670b4df716f9728a074d520`: experimental native JEV-VL and prefix
caching are current-main additions after the release. Its single-decision envelope
and offline image features differ from ordinary model/state/questions serving.
[PR108](https://github.com/ThinkFlowLab/system1-omni/pull/108) native vision Graph
replay is also on main, retaining the latest exact-grid scratch/Graph allocation
and replacing it on a grid change. In contrast,
[PR127](https://github.com/ThinkFlowLab/system1-omni/pull/127) is still open draft at
`82a5facdb785170720d5bbf75df367b3bbdcebf1`; its bounded multi-grid LRU, entry/byte
knobs and author-reported historical benchmark are proposal-only. Do not present
that experiment as current-main or released behavior, or as newly verified GPU
performance.

Current CI routes Rust fmt, strict all-target Clippy, workspace tests, release
build and an explicit `cargo test -p omni-jev --test frontend --locked` check.
Benchmark Python checks and strict MkDocs remain separate. Root test targets
include JEV-VL contract/images/prefix, Open-Jev contract/prefill_batch, Qwen
config/kernels, Laya checkpoint/weights/preprocess/packing/decision/batch, CLM
checkpoint and frontend forwarding_limits. Cua vision GPU regression requires
`--lib vision_graph_ -- --ignored`; CPU success cannot cover it. Applicable
CONTRIBUTING, contributor skills, architecture, canonical instructions, CI and
relevant manifests were inspected. The complete non-truncated tree contained no
AGENTS.md, CLAUDE.md or CURSOR.md.

[PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
(`68d7b38df04c382e9e51c9fde28428181d3bc5a8`) and
[PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
(`f01a5df38f337e65d80f420e6b22e0b30a5237af`) remain open. Their Omni backend and
release-maintenance changes are outside this System1 pass; no branch was merged,
closed or overwritten.

## Calibration fixtures and limits

[Four adjudicated cases](adjudicated-cases.json) cover two historical PR30
findings and their respective fixed forms: P2 failed-answer denominator omission
and P3 mutable resident checkpoint revision. The defect source is
`543acef57ddde36eba84e50c05c954d23e1353d7`; the fixed source is
`f2b7c6ad12d643ce3e981e6f3cbe94437471429c`. PR30 merged on October 3. Source lines, blob
IDs and full-file SHA-256 values were checked against these commits. A clean case
means only that specific historical finding is fixed, never whole-PR approval.

The current offline suite has 27 System1 tests: 23 selection tests and four
metadata/install/evidence tests. It checks exact labels, later pages, API unknowns,
old PR/new code, creation-date/review-history independence, force-push uncertainty,
stale head/labels/state, deduplication, day cap, nonmutation, source-reference
metadata, severity and component routing. All 222 repository tests passed with
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` in a clean
workspace. An initial 218-test baseline run encountered an existing installer
fixture's generated-bytecode sensitivity; removing generated caches and disabling
bytecode resolved that environmental artifact without changing shared packaging.

All four pinned case files plus the clean resident-revision companion were
re-fetched and matched their exact lines, full-file SHA-256 and Git blob IDs.
The clean rows now cite the author's explicit
[fixed-side confirmation](https://github.com/ThinkFlowLab/system1-omni/pull/30#issuecomment-5952020258).
Four rows represent two related defect/fix pairs from one historical PR, not four
independent samples. Component routes are taxonomy inferred from the source paths
and behavior; the public comments explicitly establish the defect severities.
A clean case proves only the named historical fix. This is deterministic fixture
and source-grounding validation, not measured reviewer accuracy or a false-positive
rate. No live candidate selection, model/GPU execution, full System1 runtime suite,
or exhaustive architecture audit was performed. Source inspection and upstream
CI/test routing are not claims that those upstream checks were personally run.

The upstream policy and repository map were not edited. Main-only functionality,
open proposals and the bounded sample remain explicit limits. Revalidate actual
source/head before every future review.
