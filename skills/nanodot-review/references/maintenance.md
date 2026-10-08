# Personal daily selection and bounded maintenance audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and records bounded source inspection;
it does not authorize upstream reviews, labels, merges, or code changes.

## Selection contract

Require the exact label `high priority`. If the complete current label catalog
contains `ready`, require both; otherwise require `high priority` alone. Unknown
catalogs and API/pagination failures block selection. Do not add creation-date
or ever-reviewed exclusions.
Old, previously reviewed, own, or draft PRs may qualify when the requested labels
and new-head criteria are met. Direct user-selected reviews bypass this queue.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from this skill
directory. It never fetches, posts, executes target code, or updates checkpoints.
The collector supplies:

- Repository `ThinkFlowLab/nanodot`, the Asia/Shanghai calendar `day`, complete
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
checkpoint history is unknown. See `tests/test_nanodot_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. No delivery ledger belongs here.

## Sources and overlap, inspected 2026-10-09 Asia/Shanghai

- Personal main baseline: `e49e98e92032eeb7722c711a2cb17e36c8174aec`.
- Canonical migration [PR29](https://github.com/ThinkFlowLab/nanodot/pull/29)
  merged on 2026-10-03. The maintained source is now on default-branch main,
  audited at [80c6feec31dc423f7efdcea12e854eab394dad9e](https://github.com/ThinkFlowLab/nanodot/commit/80c6feec31dc423f7efdcea12e854eab394dad9e).
  The [canonical skill](https://github.com/ThinkFlowLab/nanodot/blob/80c6feec31dc423f7efdcea12e854eab394dad9e/.agents/skills/nanodot-review/SKILL.md)
  has Git blob `a46cf365705364c35009ecf8655f70b20f054b06` and exact-byte SHA-256
  `99f2b27f35137192d290867d73ef6705cc0d828ee2a80b643bf2892803b04cf8`.
- Latest published stable GitHub release at inspection is
  [v0.2.0](https://github.com/ThinkFlowLab/nanodot/releases/tag/v0.2.0), published
  2026-10-04, at `328302996e19082966aeb9c6630744bbb67e6ff8`.
  The newer public [v0.2.1 tag](https://github.com/ThinkFlowLab/nanodot/tree/v0.2.1)
  is `a4a2ec5f572a703392de3518ce9f1f4a1e5ebfd2`; a tag and source package version
  do not establish a published release or npm availability. Neither was tested.
- The canonical architecture map still pins
  [711b45c77988df70837bc45126072f4a8d0ac0c2](https://github.com/ThinkFlowLab/nanodot/commit/711b45c77988df70837bc45126072f4a8d0ac0c2).
  Its routing and test-quality references also retain scaffold-era prose.
  The canonical skill itself requires refreshing snapshots: resolve actual paths
  and tests before applying those older descriptions. This bounded audit records
  the drift; it neither edits upstream nor creates a second canonical checklist.
- Personal [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  (`68d7b38df04c382e9e51c9fde28428181d3bc5a8`) and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  (`f01a5df38f337e65d80f420e6b22e0b30a5237af`) remain open. Their optional-reviewer
  and release-workflow work is not merged, replaced, or copied by this pass.

## Personal queue versus canonical helper

The upstream selector already covers pagination, old PR/new head, deduplication,
unknown evidence and stale-head rejection. Its batch policy counts completed
review jobs (each head/policy), accepts case-insensitive label names, and excludes
unchanged recorded heads. The explicitly configured personal queue instead uses
exact labels and at most ten distinct PRs/day, and requires affirmative new-commit
proof after the last completed review (including rewritten histories). Use this
supplement only for that personal daily queue, never to reinterpret the upstream
helper or silently change a directly requested review.

No live daily candidates or last-reviewed baseline were established in this
maintenance pass. A catalog read through the available connector was unsupported;
that is unknown, not evidence that `ready` is absent. The fixture collector contract
above must be satisfied by a supported complete read before a real selection.

## Bounded architecture refresh

The [pinned evidence record](adjudicated-cases.json) records exact source anchors,
not an alternative review policy. Compare tag trees instead of taking release
prose as proof that a feature exists at a release commit:

- Published v0.2.0 already includes DSH CLI integration, the comment-writer port,
  content-bound approval/AUTO/READONLY flow, separate write credentials, quota,
  and the provider registry with OpenAI-compatible and Anthropic adapters.
- By the v0.2.1 source tag, model-usage accounting, bounded provider retry,
  digest/stale/flaky watch dimensions, watch update, corrupt-row quarantine,
  timestamped logs and the Python 3.11/3.12 CI matrix have arrived. These are not
  attributed to the older published release merely because its prose lists them.
- Main after that tag adds #103 soak tests, #106 AUTO adversarial tests, #107
  malformed-provider response tests and usage-accounting fixes, and #114 the
  loopback UI shell/health endpoint. UI screen names are placeholders, not
  implemented task/inbox/approval screens. These are main-only observations.

New paths need call-graph/context inspection: the canonical router falls back to
`inspect-context` for areas without a dedicated route. Do not transfer Omni/GPU
assumptions or infer runtime safety from passing routing tests.

## Regression evidence and limits

The evidence record references two adjudicated historical defect/clean pairs
(four samples) from the canonical eight-sample/four-family corpus:
optional failure while required checks are pending, and changed-evidence
notification replay. It retains exact source anchors, hashes, scoped outcomes,
severity, routing expectations and upstream regression-test anchors. The corpus
and executable behavior checks remain canonical upstream resources.

At the pinned main, all 44 canonical network-free skill tests passed, covering
selection, grounding, severity, routing and historical executable controls.
All 24 canonical source fixture items were separately compared with exact
historical Git objects. This is a tiny curated, unblinded regression exercise;
it is not a new review-accuracy estimate or certification of clean commits.
The personal tests verify the normalized queue contract, evidence metadata and
self-contained installation with human-edit preservation. Metadata checks do
not independently prove the truth of a finding or replace the upstream corpus.

Affected main-only pytest tests were not collected because pytest was unavailable.
No full runtime, live provider/GitHub calls, OS notifications, npm bootstrap,
actual browser/server interaction, performance benchmark or personal install ran.
A source-inspected AUTO scope-change test has a vacuous pending-capability loop;
the evidence record explains why it does not establish its claimed race coverage.
That is a coverage gap, not a demonstrated runtime defect. Upstream edits remain
outside this maintenance scope.
