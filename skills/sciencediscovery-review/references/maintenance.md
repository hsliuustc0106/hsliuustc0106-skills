# Personal daily selection and bounded ScienceDiscovery audit

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

- Repository `openJiuwen-ai/sciencediscovery`, the Asia/Shanghai calendar `day`, complete
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
checkpoint history is unknown. See `tests/test_sciencediscovery_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. Serialize concurrent selection and
delivery or reconcile reservations against the same ledger; this snapshot adapter
does not enforce a cross-process cap. No delivery ledger belongs here.

The configured exact `high priority` spelling intentionally overrides the
canonical draft's `high-priority` spelling for this personal queue only. Neither
hyphenated labels nor `priority/major` are aliases. Do not mutate labels or broaden
the queue to reconcile the discrepancy. Unknown current catalogs remain BLOCKED.

## Current bounded audit, 2026-11-12 Asia/Shanghai

This refresh supersedes the November 5 routing below; historical calibration
pins remain unchanged. It is a source-contract audit, not an upstream PR review.
A later Thursday-morning catalog retry (~09:54 Asia/Shanghai), from personal
main baseline `462c2c63769ffcf51377e95ec8e628a364639d13`, completed eligibility
evidence at the same target pin; the CI routing findings below are unchanged.

- Personal main baseline: `984096a4d1101d9ccf3cfb122589925c10a3f06a`.
  Target main: [807982f00da6253b41042146171554c51ecc2c3e](https://github.com/openJiuwen-ai/sciencediscovery/commit/807982f00da6253b41042146171554c51ecc2c3e).
  Local Git comparison from the previous audited pin `48848578d58f0ecd83798493bcf4f2cde8d02b26`
  enumerated 391 new commits and 895 changed files. The inventory is complete,
  but semantic inspection is limited to the CI contracts cited below, current
  contribution guidance and canonical-source routing, not all changed product code.
- Canonical [PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains open/draft at `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`.
  Main still has no root AGENTS.md or canonical review skill. Continue explicit
  draft-source loading; the canonical SKILL bytes retain SHA-256
  `2bf261c60d527034b5fe90f2b5194d8e076e887e8a069515c17575a53d5a9dd1`.
- Latest stable remains [v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0),
  published October 31, peeled to `7acc1dcf62736f7e7bf06c6d51acb5114899f2de`.
  Main has 517 unique commits and the release tag two. The changes below are
  main-only evidence, not a claim about released behavior.
- All 13 open personal-skills PRs were re-enumerated (`per_page=100`, page 2
  empty). None is a sciencediscovery-review change. PR6 remains at
  `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and PR17 at
  `f01a5df38f337e65d80f420e6b22e0b30a5237af`. Both remain untouched, including
  shared manifest/installer changes proposed by PR17.
- The earlier same-day catalog connector read returned `INVALID_ARGUMENT`
  (unsupported endpoint) and local GitHub CLI had no authenticated session, so
  eligibility was recorded as **unknown**, not empty. The Thursday-morning retry
  succeeded via GitHub REST (`GET /repos/openJiuwen-ai/sciencediscovery/labels?per_page=100`,
  paginated): one page, 57 exact names, page 2 empty. November 5 recorded 56
  names; the current catalog includes `release/0.4.0-rc1`, which was not in that
  historical write-up. No `v0.4.0-rc1` or other newer GitHub Release or tag
  exists; latest stable remains v0.3.0 as recorded above. The catalog contains
  `ready`, `priority/major`, `priority/unspecified`, and `agent-ready`; it does
  not contain `high priority` or `high-priority`.
- Open pull requests on `openJiuwen-ai/sciencediscovery` were re-enumerated at
  the same transport (`per_page=100`): 42 open, page 2 empty. Search and
  label-filtered issue/PR lists found zero items labeled `high priority` or
  `high-priority` (`incomplete_results=false`). Zero open PRs carry exact
  `ready`. Two open PRs carry `priority/major` (#1105, #1053) and are not
  eligible. With `ready` present the personal queue still requires exact
  `high priority` AND `ready`, so the eligible set is empty before new-head or
  delivery checks, until that exact label exists in the catalog. Do not treat
  `priority/major`, `agent-ready`, or hyphenated spellings as aliases, and do
  not create labels to force eligibility. The earlier same-day unknown state
  and November 5's 56-label catalog are retained only as dated evidence. No
  live queue was selected and no review or delivery checkpoint changed.

### Executable CI routing takes precedence over stale tier prose

At the target pin, read [tier-policy.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.ci/tier-policy.mjs),
[ci.yml](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.github/workflows/ci.yml)
and [.ci/README.md](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.ci/README.md)
together. The canonical CI skill's tier table still describes the older split;
it is not evidence that those jobs ran. The policy change is pinned by
[0dc16ce7682a3ee717924a7e50c0cb0f94dfb765](https://github.com/openJiuwen-ai/sciencediscovery/commit/0dc16ce7682a3ee717924a7e50c0cb0f94dfb765).

- Ordinary `pr` profile: policy/L1/UT/ST plus binary and Docker jobs;
  mocked and real E2E are skipped. A green PR gate does not prove browser E2E.
- `merge` profile: policy/L1/UT/ST plus mocked and real E2E;
  binary and Docker jobs are skipped. Verify the merge-group SHA separately.
- `daily` and `release`: both E2E and distribution jobs are required.
  Local cumulative test profiles are distinct from workflow job selection;
  `pnpm ci:e2e` still selects the mocked slice locally.
- The documentation-only exception is retained: policy/L1 success with the
  enumerated product jobs skipped, not executed product passes. Read actual
  diff classification and job results; unknown diffs retain the full profile.
- [Real E2E workflow](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.github/workflows/real-e2e.yml)
  now references `nightly-research`, not the older `nightly-ci-ds` environment.
  Workflow source does not verify live environment configuration or credentials.
- L5 is no longer the same case set as L4. Read the frozen plan and
  [real matrix](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.ci/real-matrix.mjs),
  [Biomni gate](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.ci/biomni-gate.mjs)
  and [configuration](https://github.com/openJiuwen-ai/sciencediscovery/blob/807982f00da6253b41042146171554c51ecc2c3e/.ci/biomni-gate.json).
  Current configuration declares 45 active versus 50 historical cases and a
  temporary, unapproved baseline. Population-scaled additive resource budgets
  are not measured 45-case results; historical mean/P95 are not recalibrated
  capability evidence. Do not claim an approved non-regression baseline from a
  green run. This pass ran no benchmark, model or paid workflow.

### Validation and limits

The selector is unchanged. Its network-free pagination, unknown/error,
old-PR/new-head, exact-label, stale-head and cross-policy cap/dedup tests remain
required. The corpus remains two adjudicated defect families/four outcomes,
not an accuracy estimate. Validation passed: 267 Python unittests (including 36 focused ScienceDiscovery
selection/evidence/install tests), four pinned-source replay outcomes under
Node 24.22.1, installer preservation, frontmatter/local-link/source-pin checks,
manifest parsing, script syntax and diff whitespace. Historical Git objects were
materialized before a second replay with lazy fetching disabled. No upstream review, product
UT/ST/E2E, native Windows run, scientific validation or remote CI pass is implied.

## Historical bounded audit, 2026-11-05 Asia/Shanghai

This afternoon verification (~10:10 Asia/Shanghai) supersedes the earlier same-day
morning routing below. Historical October 29 calibration pins remain unchanged.

- Personal main baseline before this refresh: `8f47c966a9755028476c3465307b7cb451fc1b1f`
  (`docs(sciencediscovery-review): refresh release and CI evidence routing`,
  2026-11-04T16:07:42Z / 2026-11-05 00:07 Asia/Shanghai).
  Target main: [48848578d58f0ecd83798493bcf4f2cde8d02b26](https://github.com/openJiuwen-ai/sciencediscovery/commit/48848578d58f0ecd83798493bcf4f2cde8d02b26)
  (`fix(web): translate the tool-result headings at render time`,
  2026-11-04T18:36:14Z). Compare against the morning pin
  `89cd2d30c93e11c6e98e264cc08b171f6a3705f0` reports `ahead_by=10`, `behind_by=0`,
  ten web-only files under `apps/web/` (CSV empty-version, unknown activity/execution,
  compact token rounding, tool-result locale headings). Compare against the prior
  October 29 pin `5e56ea77cfcc5447947be8342d7781dc7891d004` reports `ahead_by=220`,
  `behind_by=0` (GitHub file array still truncates at 300). This pass re-checked
  source and CI contract identity at the new tip; it did not re-audit all product
  lines.
- [Canonical migration PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains open, draft and unmerged at `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`.
  Its recorded base is not current main. Main still lacks the review skill and
  root AGENTS.md. Continue explicit draft-source loading, recording the revision
  and hash; re-discover current target contracts rather than copying its old base.
  Main has removed `.agents/skills/sciencediscovery-dev/`; do not restore or treat
  its historical handbook as current repository instructions. The web-local
  AGENTS.md and frontend-quality skill still require visual UI inspection.
- Latest stable [v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0)
  remains published October 31 at peeled tag commit
  `7acc1dcf62736f7e7bf06c6d51acb5114899f2de`. Main and the release tag diverge: 126
  commits are unique to main and two unique to the tag (was 116 unique to main at
  the morning pin). RC1 and beta remain prereleases. No newer stable or prerelease
  tag appeared. A release's `target_commitish=main` is not a source pin; use its
  peeled tag. Do not call post-tag behavior released.
- All 13 open personal-skills PRs and their changed-file lists were re-enumerated;
  none overlaps this skill or repository-review-source. PR6 remains at
  `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and PR17 at
  `f01a5df38f337e65d80f420e6b22e0b30a5237af`. No other PR or human edit changed.
- Fresh complete label catalog succeeded via GitHub REST
  (`GET /repos/openJiuwen-ai/sciencediscovery/labels?per_page=100`, paginated): one
  page, 56 exact names, page 2 empty. Catalog contains `ready`, `priority/major`,
  `priority/unspecified`, and `agent-ready`; it does not contain `high priority` or
  `high-priority`. Search found zero issues/PRs labeled `high priority` or
  `high-priority`. With `ready` present the personal queue still requires exact
  `high priority` AND `ready`, so the eligible set is empty until that exact label
  exists in the catalog. Do not treat `priority/major`, `agent-ready`, or hyphenated
  spellings as aliases, and do not create labels to force eligibility. October 29's
  45-label catalog and the morning `INVALID_ARGUMENT` unknown state are retained only
  as dated evidence. No live queue was selected and no review or delivery checkpoint
  changed.

### Current CI evidence routing

Read the selected revision's executable workflow and policy together. The CI
skill's ordinary tier table alone omits a newer documentation-only exception.
Blob identity for the CI contracts is unchanged from the morning pin
`89cd2d30…` through tip `48848578…`. At the current tip,
[changed-paths.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/.ci/changed-paths.mjs),
[tier-policy.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/.ci/tier-policy.mjs),
[ci.yml](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/.github/workflows/ci.yml)
and [the docs-only explanation](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/.ci/README.md#L183-L202)
establish:

- PR, push and merge-group diffs wholly in the explicit documentation allowlist
  run `pnpm docs:check` instead of product tests. `.agents/skills/**/*.md`
  qualifies; arbitrary `skills/**/*.md` and other `.agents` files do not.
  Renames check both paths. Unknown, empty or unavailable diffs preserve the full
  profile. Manual/reusable and scheduled profiles do not infer this exception.
- Non-draft docs-only PRs, pushes and merge groups require policy/L1 success and
  the enumerated product jobs skipped. Draft PRs run documentation checks but
  skip the merge-gate. UT/ST, browser E2E, real E2E, binary and Docker skips are not executed
  passes. Inspect the actual policy output and job results before making a test
  coverage claim; a green aggregate does not prove those suites ran.
- Ordinary L1–L5 routing remains as described in the historical audit, with
  live environment now `nightly-ci-ds`. L5 currently uses the same eligible real
  cases/evaluation modes as L4, not a calibrated capability baseline.
- [Provider-fault classification](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/test/support/tagged/provider-fault.mjs),
  [attempt handling](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/test/support/tagged/shared.mjs)
  and [plan accounting](https://github.com/openJiuwen-ai/sciencediscovery/blob/48848578d58f0ecd83798493bcf4f2cde8d02b26/test/support/tagged/plan.mjs)
  distinguish a remaining `PROVIDER_FAULT`: executed but neither passed nor
  product-failed, still non-green. Eligible early transient faults lasting at most 300 seconds
  may retry once; product assertions, authentication and rate limits are not
  that exception. When every case in a batch faults, at most two eligible cases
  repeat as outage probes. A successful retry may replace a fault and permit a
  green run, with `retriedAfterProviderFault` recorded. Retain attempt evidence;
  do not describe retry success as a
  clean first attempt or provider failure as a passing gate.

### Validation and limits for this refresh

The unchanged selector retains exact-label, pagination/error-as-unknown,
old-PR/new-head, stale-head and cross-policy deduplication fixtures. The two
historical defect families / four adjudicated outcomes remain bounded P2 and
fixed-clean cases, not whole-PR approval or an accuracy estimate. LICENSE bytes
still match main tip. No adjudicated-case pins changed.

Validation of the earlier same-day CI refresh recorded 266 personal-repository
tests. The Thursday-morning catalog retry re-ran the same gates at this
working tree: all 267 personal-repository tests passed, including 36 focused
ScienceDiscovery selection/evidence/install tests. Frontmatter for all 24 skill
entrypoints, scoped local links, immutable source paths and case pins, source
routing, plugin `./skills/` discovery, installer preservation behavior,
Python/Node syntax and diff whitespace were checked. No live models, Windows
runs, browser journeys, full product UT/ST/E2E, binary/Docker qualification,
remote CI pass, or exhaustive architecture audit is claimed. No source-owned
checklist, selection policy, adjudicated-case pins, LICENSE bytes, or upstream
code changed.

## Historical same-day morning audit, 2026-11-05 Asia/Shanghai

Earlier same-day morning refresh at personal tip `8f47c966a9755028476c3465307b7cb451fc1b1f`.
Superseded by the current afternoon audit above; retained as dated evidence.
Historical calibration pins remain unchanged.

- Personal main baseline: `85398e9ed0631d7a263316f37833ef9c2994ef8e`.
  Target main: [89cd2d30c93e11c6e98e264cc08b171f6a3705f0](https://github.com/openJiuwen-ai/sciencediscovery/commit/89cd2d30c93e11c6e98e264cc08b171f6a3705f0).
  Complete local Git history counts 210 commits and 637 changed files since
  `5e56ea77cfcc5447947be8342d7781dc7891d004`. This pass inspected source and CI
  contracts, not all 55,168 added / 4,047 removed lines or product correctness.
- [Canonical migration PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains open, draft and unmerged at `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`.
  Its recorded base is not current main. Main still lacks the review skill and
  root AGENTS.md. Continue explicit draft-source loading, recording the revision
  and hash; re-discover current target contracts rather than copying its old base.
  Main has removed `.agents/skills/sciencediscovery-dev/`; do not restore or treat
  its historical handbook as current repository instructions. The web-local
  AGENTS.md and frontend-quality skill still require visual UI inspection.
- Latest stable [v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0)
  was published October 31 at peeled tag commit
  `7acc1dcf62736f7e7bf06c6d51acb5114899f2de`. Main and the release tag diverge: 116 commits are unique to main and two
  unique to the tag.
  RC1 and beta remain prereleases. A release's `target_commitish=main` is not a
  source pin; use its peeled tag. Do not call post-tag behavior released.
- All 13 open personal-skills PRs and their changed-file lists were enumerated;
  none overlaps this skill or repository-review-source. PR6 and PR17 retain the
  full heads recorded in the historical audit. No other PR or human edit changed.
- Fresh label-catalog access through the connector returned unsupported-endpoint
  `INVALID_ARGUMENT`. Current catalog and queue eligibility therefore remain
  unknown, not empty. October 29's catalog is retained only as dated evidence.
  No live queue was selected and no review or delivery checkpoint changed.

### Current CI evidence routing

Read the selected revision's executable workflow and policy together. The CI
skill's ordinary tier table alone omits a newer documentation-only exception.
At the current pin, [changed-paths.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/.ci/changed-paths.mjs),
[tier-policy.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/.ci/tier-policy.mjs),
[ci.yml](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/.github/workflows/ci.yml)
and [the docs-only explanation](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/.ci/README.md#L183-L202)
establish:

- PR, push and merge-group diffs wholly in the explicit documentation allowlist
  run `pnpm docs:check` instead of product tests. `.agents/skills/**/*.md`
  qualifies; arbitrary `skills/**/*.md` and other `.agents` files do not.
  Renames check both paths. Unknown, empty or unavailable diffs preserve the full
  profile. Manual/reusable and scheduled profiles do not infer this exception.
- Non-draft docs-only PRs, pushes and merge groups require policy/L1 success and
  the enumerated product jobs skipped. Draft PRs run documentation checks but
  skip the merge-gate. UT/ST, browser E2E, real E2E, binary and Docker skips are not executed
  passes. Inspect the actual policy output and job results before making a test
  coverage claim; a green aggregate does not prove those suites ran.
- Ordinary L1–L5 routing remains as described in the historical audit, with
  live environment now `nightly-ci-ds`. L5 currently uses the same eligible real
  cases/evaluation modes as L4, not a calibrated capability baseline.
- [Provider-fault classification](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/test/support/tagged/provider-fault.mjs),
  [attempt handling](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/test/support/tagged/shared.mjs)
  and [plan accounting](https://github.com/openJiuwen-ai/sciencediscovery/blob/89cd2d30c93e11c6e98e264cc08b171f6a3705f0/test/support/tagged/plan.mjs)
  distinguish a remaining `PROVIDER_FAULT`: executed but neither passed nor
  product-failed, still non-green. Eligible early transient faults lasting at most 300 seconds
  may retry once; product assertions, authentication and rate limits are not
  that exception. When every case in a batch faults, at most two eligible cases
  repeat as outage probes. A successful retry may replace a fault and permit a
  green run, with `retriedAfterProviderFault` recorded. Retain attempt evidence;
  do not describe retry success as a
  clean first attempt or provider failure as a passing gate.

### Validation and limits for this refresh

The unchanged selector retains exact-label, pagination/error-as-unknown,
old-PR/new-head, stale-head and cross-policy deduplication fixtures. The two
historical defect families / four adjudicated outcomes remain bounded P2 and
fixed-clean cases, not whole-PR approval or an accuracy estimate. Their isolated
replay reproduced all four outcomes using Node 24.22.1 and already-present Git
objects, with imports stripped and explicit in-memory authority stubs. It did
not execute the upstream application suite. LICENSE bytes still match main.

Validation: all 266 personal-repository tests passed, including 36 focused
ScienceDiscovery selection/evidence/install tests. Frontmatter, scoped local
links, immutable source paths and case pins, source routing, plugin manifest,
installer preservation behavior, Python/Node syntax and diff whitespace were
checked. No live models, Windows runs, browser journeys, full product UT/ST/E2E,
binary/Docker qualification, remote CI pass, or exhaustive architecture audit is
claimed. No source-owned checklist, selection policy or upstream code changed.

## Historical bounded audit, 2026-10-29 Asia/Shanghai

This refresh supersedes the dated pins and catalog notes below from the
2026-10-08 pass; it does not replace the canonical review checklist.

- Personal main baseline before this refresh:
  `e1305e6b7f4ef758a6bdef0c2a0538f47923f0eb`.
  ScienceDiscovery main:
  [5e56ea77cfcc5447947be8342d7781dc7891d004](https://github.com/openJiuwen-ai/sciencediscovery/commit/5e56ea77cfcc5447947be8342d7781dc7891d004)
  (`fix(desktop): cap the SSE frame buffer so an unterminated frame stays bounded`,
  2026-10-29 01:36:27Z). Compare against the prior audit pin
  `7a0324257eecb48b57f60b6a80ce2fff54e7dba7` reports `ahead_by=429`,
  `behind_by=0`. The compare payload truncates at GitHub's
  250-commit and 300-file array limits, so this is a counted delta with a
  truncated path inventory, not a line-by-line semantic audit of every change
- Canonical migration [PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains open and draft at `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`
  (updated 2026-10-22). Main still has no `AGENTS.md` and no
  `.agents/skills/sciencediscovery-review/`. Load that explicit revision until
  merged; do not attribute its skill to main. SKILL Git blob:
  `eab90983063839d3ab92abb63df87db85a859c67`; exact-byte SHA-256:
  `2bf261c60d527034b5fe90f2b5194d8e076e887e8a069515c17575a53d5a9dd1`.
  The daily-selection and repository-contracts references were re-resolved at
  that same revision (Git blobs `e28e81b1696c1a93817eb27384cc5ebc3d8919c1` and
  `11117a0cb6416c1da24e497cbf84c9cdf431f3e3`)
- [Release page](https://github.com/openJiuwen-ai/sciencediscovery/releases)
  now lists prerelease [`v0.3.0-rc1`](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0-rc1)
  (annotated tag peels to `844947da87b27528d9a34d0ee6d0efd591e57749`,
  published 2026-10-16), prerelease [`0.3.0-beta`](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/0.3.0-beta)
  (peels to `6d3c49a882ff45e260dcbdb25ee2918fcb0571ae`), and latest stable
  [`0.2.0`](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/0.2.0)
  (peels to `29aae0d39281da66ccd2447532b8a3eb24e534d1`). Main is 376 commits
  ahead of the rc1 peel. Release notes remain prerelease guidance; main,
  website documentation and release tags are not interchangeable. This pass
  inspected publication notes and tag identities, not every release delta
- All 13 open personal skills PRs were enumerated. [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open with unchanged
  heads. No open personal PR's file list overlaps
  `skills/sciencediscovery-review/`. This scoped supplement leaves their
  Omni/shared-discovery work, human edits and PRs untouched
- A complete label catalog was read through the authenticated GitHub API
  (`GET /repos/openJiuwen-ai/sciencediscovery/labels?per_page=100`): one page,
  45 exact names, no `Link` next page. The catalog contains `ready` and
  `priority/major`; it does not contain `high priority` or `high-priority`.
  Search found zero issues/PRs labeled `high priority` or `high-priority`.
  With this complete catalog the personal queue still requires exact
  `high priority` plus `ready`, so the eligible set is empty until that exact
  label exists in the catalog. Do not treat `priority/major`, `agent-ready`,
  or hyphenated spellings as aliases, and do not create labels to force
  eligibility. No live queue, delivery history or checkpoint was selected or
  changed in this maintenance pass

### Historical contracts observed October 29

- [CI skill](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/.agents/skills/ci/SKILL.md)
  (Git blob `b3641cbf9c242069082afa969dd77fe9804b9519`; prior audit pin used
  `c088239a26502aa7024200d58ad5f46fbf8d4c40`) documents L1–L5 tiers: L1 on every
  CI run; L2/`pr` hermetic UT/ST and mocked browser E2E; L3/`merge` adds basic
  real API journeys plus binary/Docker smokes; L4/`daily` and L5/`release` add
  eligible real research journeys. `pnpm ci:e2e` is the mocked browser subset;
  real E2E needs `CI_ALLOW_REAL=1` and credentials. A green release certifies
  selected assertions, not a calibrated capability baseline. Prefer this skill
  and the selected revision's workflows over older prose counts in
  [`.ci/README.md`](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/.ci/README.md)
  or [CONTRIBUTING.md](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/CONTRIBUTING.md)
- Root [package.json](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/package.json)
  still declares Node `>=22.19.0` and `pnpm@11.1.2` (Git blob
  `b1b54ae7f53fa38ac79162bf395e69461d306fee`; engines text unchanged from the
  prior pin's declaration). CONTRIBUTING now points contributors at
  `pnpm test:shared` / `pnpm test:list` / `pnpm test:policy` and the JiuwenSwarm
  setup path; treat those as the current command surface when rediscovering tests
- Main `.agents/skills/` gained
  [`frontend-quality`](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/.agents/skills/frontend-quality/SKILL.md)
  (apps/web UI/layout guidance) and
  [`sciencediscovery-dev`](https://github.com/openJiuwen-ai/sciencediscovery/blob/5e56ea77cfcc5447947be8342d7781dc7891d004/.agents/skills/sciencediscovery-dev/SKILL.md)
  (issue/fix/feature development handbook) since the prior pin. Neither is the
  repository-owned review skill; do not substitute them for PR231's draft review
  checklist
- Published rc1 notes highlight sandbox/Runner readiness decoupling, withheld
  unparsable tool calls, custom-model settings fail-soft behavior, and L1–L5 CI
  layering. Re-read the cited merges at the review target rather than treating
  release prose as executable evidence. Main tip work after rc1 includes desktop
  SSE frame-buffer bounds, Runner symlink/sandbox preflight, and skills-catalog
  startup hardening; those are main-only until a later release tag

## Historical freshness and validation routing

At the main pin above, CONTRIBUTING.md (Git blob `6c5dd807e1ab8eeb6b364c48edb40fa556cc451b`),
package.json, `.ci/README.md` (Git blob `8e8da0f551133c5320007bc55a3b05765acaa7cd`)
and the CI skill were re-inspected. Read the selected revision's actual
workflow/profile and tagged summaries rather than promoting older prose examples
to passing evidence. Full product CI remains separate from this supplement's
network-free Python tests.

## Historical corpus and validation limits

[Adjudicated cases](adjudicated-cases.json) record bounded historical defect/fix
pairs (four outcomes) with immutable source evidence. Both before outcomes are
bounded P2 judgments; fixed-clean means only the named defect is absent, not
whole-PR approval. The artifact case covers unreachable offsets past the decodable
window; the authority case covers child audit ownership, not a permission bypass.
The latter uses the test-fixture correction after the implementation fix. They are
calibration cases, not a current review or a second architecture checklist.
All four case revisions remain ancestors of the refreshed main pin (compare
`behind_by=0` from each case commit). Quoted source retains the
[upstream Apache-2.0 license](LICENSE.sciencediscovery.txt) (exact-byte SHA-256
unchanged vs main tip LICENSE).

The optional read-only replay is `node scripts/replay_cases.mjs /path/to/sciencediscovery-checkout`
from this skill directory (tested with Node 24.19.0). It requires the pinned Git
objects already present; it does not fetch or install. It strips TypeScript and
removes imports to run exact pinned functions in isolation. Artifact projection
uses pinned bounding/classifier functions; authority collection uses explicit
in-memory store/CAS stubs. Four outcomes reproduced, including eight terminal/
beyond-window artifact probes. This is neither the upstream tests nor a complete
journey; real persistence, permissions and the sandbox were not exercised.

Validation: 36 ScienceDiscovery skill tests and the full personal-repository
suite of 259 tests passed. An independent pass checked 2,000 seeded randomized
snapshots plus malformed-shape cases against the offline selector. Selector
robustness coverage is not review accuracy. Frontmatter for all skill
entrypoints, scoped local links, corpus pins, LICENSE SHA-256, installation
routing via the plugin `./skills/` glob and `scripts/sync-project.sh`, script
syntax (`select_daily.py`, `replay_cases.mjs`) and diff whitespace were checked.
No source-owned checklist was copied into the supplement. Optional
`replay_cases.mjs` still requires a checkout that already contains the pinned
Git objects; it was syntax-checked here and not re-executed against a product
checkout in this pass.

The source record is partial. No full application UT/ST/E2E, live models, scientific
validation, Docker/binary qualification, sandbox changes or remote research were
run. The offline selector trusts verified collector flags; it does not fetch pages,
prove ancestry, serialize deliveries or establish remote freshness. Unknown API
results are blockers, never successful empties. Source-level adjudication does not
measure reviewer accuracy, precision or recall.
