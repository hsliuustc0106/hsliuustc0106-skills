# Personal daily selection and bounded maintenance audit

This supplements the personal daily brief only. Repository-owned source remains
canonical for engineering review. It does not authorize posting or label changes.

## Exact selection contract

The explicit personal policy requires `high priority` (space), not
`high-priority` (hyphen). The latter appears in the proposed upstream daily
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

## Audited sources, 2026-10-03 Asia/Shanghai

- Personal repository baseline: `b768e79245a60ba506ff00c285fe6442c3955cec`
- [Canonical skill PR62](https://github.com/ThinkFlowLab/system1-omni/pull/62)
  remains open and unmerged, non-draft at inspection. Load the proposed source
  explicitly at `25bc586686875e842b5ad91a4361d2c7de490fbc`; it is absent on main
- [Current main](https://github.com/ThinkFlowLab/system1-omni/commit/1be7d41eb74d5b49fd25194042041319950e5dce)
  advances the map's baseline `d2665e1fa867360cd96e45a87b6bc0b1506eac47` through
  the five-commit Laya checkpoint merge history. This pass inspected that delta,
  current workspace/test routing, canonical SKILL and both references
- The release API returned an empty complete first page (100 requested). No
  published release was available at inspection. Main and open-PR behavior below
  must not be presented as released behavior
- Canonical bytes SHA-256: SKILL `e70988869049a45e6c3a4b3b75d6c086550ff018ed5bfd70ab6456288b446fa9`;
  repository-contracts `4af77bf5deb8a12ef19def260871253a903cc24ef7cf7becf1714621afc8dc28`;
  daily-selection `3b0e8e73662313a6f8f65f144f21dab31c73dcdf871aa91745712a764e467f93`

Main adds CPU Laya checkpoint loading: omni-laya workspace membership,
configuration validation, mapped safetensors, 206-tensor inventory and dtype
conversion. Rust tests are explicitly rooted at tests/laya/checkpoint.rs and
weights.rs; two full-checkpoint oracle tests are ignored by default. This is not
Laya inference or native Metal execution. The canonical map's older description
must be revalidated against this newer target code. The proposed CUDA extraction
and test relocation in PR55 are not present in this main snapshot.

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
`f2b7c6ad12d643ce3e981e6f3cbe94437471429c`. PR30 remains open. Source lines, blob
IDs and full-file SHA-256 values were checked against these commits. A clean case
means only that specific historical finding is fixed, never whole-PR approval.

The offline suite has 21 selection tests and two metadata/install tests added in
this pass. It checks exact labels, later pages, API unknowns, old PR/new code,
force-push uncertainty, stale head/labels, deduplication, day cap, nonmutation,
source-reference metadata, severity and component routing. The existing 18 tests cover
other packaging/loader invariants. This is deterministic fixture validation,
not measured reviewer accuracy. No live candidate selection, model/GPU execution,
full System1 runtime suite, or broad new architecture audit was performed.

Upstream policy and the repository map were not edited in this personal-only
maintenance pass. Their unmerged status and source-map delta remain explicit
limits. Revalidate actual source/head before every future review.
