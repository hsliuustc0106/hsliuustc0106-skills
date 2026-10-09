# Personal daily selection and bounded maintenance audit

This supplements the personal daily brief only. Repository-owned source remains
canonical for engineering review. It does not authorize posting or label changes.

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

## Release boundary and current routing

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
