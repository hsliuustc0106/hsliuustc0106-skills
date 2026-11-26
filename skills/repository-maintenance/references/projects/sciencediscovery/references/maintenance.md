# Personal daily selection and bounded ScienceDiscovery audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and dated source-inspection results;
it does not authorize upstream reviews, labels, merges, or code changes.

## Selection contract

For the explicitly configured daily brief, follow the [shared personal label/new-head contract](../../../daily-label-queue.md)
with repository `openJiuwen-ai/sciencediscovery`. The configured exact
`high priority` spelling overrides the canonical draft's `high-priority`
spelling for this personal queue only. Neither hyphenated labels nor
`priority/major` are aliases; do not mutate labels or broaden the queue.
Unknown current catalogs remain blocked.

Serialize concurrent selection and delivery or reconcile reservations against
the same ledger; the adapter does not enforce a cross-process cap. See
`tests/test_sciencediscovery_daily.py` for executable normalized snapshots.

## Current bounded audit, 2026-11-26 Asia/Shanghai

This Thursday-morning refresh (~10:20 Asia/Shanghai) supersedes the same-day
00:04 pin at `645dc7ba` and the November 19 routing below. The historical
case pins and personal exact-label queue are unchanged.

- Skills main before this change: `20674f33615661a27e72993e6984e1181cd57b94`.
  [ScienceDiscovery main](https://github.com/openJiuwen-ai/sciencediscovery/commit/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837):
  `991ba2cc5d33fd9ac49f6b1289c8db156e4cc837`
  (`fix(sessions): tear kernels down on archive, delete and approval-mode
  change even when the Runner probe fails`, committer date
  2026-11-25T18:05:35Z / 2026-11-26 02:05 AM Asia/Shanghai).
  Local Git comparison from the November 19 audited pin
  `59d05aa70a26801e2e907ca49060329028514608` enumerated 392 new commits and
  618 changed paths. Comparison from the same-day 00:04 pin
  `645dc7ba3dde868bf7dcdc6f674e937d42284d3a` is one commit and two files,
  both in that session-kernel teardown change
  (`services/api/src/http/index.ts`,
  `services/api/src/session-kernel-teardown.test.ts`). This is a complete
  path inventory and a partial semantic audit of CI and review routing, not
  a review of that product change.
- Root AGENTS.md and the configured canonical review entrypoint are still
  absent at this pin. [Source PR 231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains closed without merge (`draft=true`, `merged=false`, recorded head
  `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`); the head ref
  `codex/repository-review-skill-20261001` still returns 404. Do not revive
  it or use a CI/development skill as the project review checklist.
  Source-contract maintenance and an offline queue check do not unblock a
  product PR review.
- Stable [v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0)
  peels to `7acc1dcf62736f7e7bf06c6d51acb5114899f2de` (2 release-only,
  1,083 main-only commits); prerelease [v0.4.0-rc1](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.4.0-rc1)
  peels to `5cac2ce590f09f97164f4528c034170dbc5d1c63` (5 release-only,
  492 main-only). Neither bare nor prefixed 0.4.0 GA tag was present at
  this audit. The application package version on main is `0.4.0`; that is
  main-only evidence and does not qualify either released pin.
- Public API catalog: 60 labels and 77 open PRs; second pages empty. The
  exact `ready` label exists, but neither `high priority` nor
  `high-priority` exists. The one open `priority/major` item (PR 1256) is
  not eligible. No review, queue reservation, label, or user-facing PR
  action.
- Inspected the 13 open skills-repo PRs; all remain at their November 19
  heads, none modifies this overlay, and none was retargeted since the
  00:04 audit. PR 6 and PR 17 remain open at those pins, untouched.

### Read CI by event, then by actual job and artifact

Use the exact [policy](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.ci/tier-policy.mjs)
and [workflow](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.github/workflows/ci.yml),
not a static tier table:

- Ordinary PRs require policy, L1, UT, ST, Linux binary and Docker; changed
  paths can additionally select Web UI-ST/mock shards and Desktop mocked
  specs. Changes to shared desktop harness files select all mocked desktop
  specs. Real E2E and both installers are outside ordinary PR coverage.
  Explicit docs-only routing is a separate exception, not a product pass.
- Merge-group runs require full mocked web/desktop coverage and L3 real
  E2E, with no installer jobs. [Run 45671614221](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/45671614221)
  on the exact audited commit reports the mocked desktop and the L3 real
  desktop smoke successful, but the macOS/Windows installers, Linux
  binary, Docker image, and L4/L5 real jobs skipped. This is not
  installed-release or Windows recovery evidence.
- Daily and release require Linux, Docker and both desktop installers as
  well as scheduled real coverage. The macOS packaging workflow runs an
  ad-hoc packed-app launch with an absolute hang gate, not the performance
  regression judge or a signed DMG install. Windows uses `dist --publish
  never`; the explicit Verify step runs only for the package profile and
  checks that the sole matching EXE exists and is nonempty. It does not
  install or launch it. Match an actual runtime receipt to the installed
  artifact and build before judging native recovery.
- [Package](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.github/workflows/package.yml)
  is a distinct on-demand profile: `linux-windows`, `macos`, or `all`
  select their named packaging jobs and leave product test tiers inactive.
  [Release](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.github/workflows/release.yml)
  manual dispatch validates but does not publish; a matching tag push can
  create a draft after the gate, reusing checked build artifacts. Manual
  release gate [45586964125](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/45586964125)
  later completed successfully on `9c74af8ba4ee0e28115db7e94b500d7f8d9be4b3`,
  a different ancestor commit, not this tip. It is not a GA release
  receipt.
- [Nightly](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.github/workflows/nightly.yml)
  dispatch runs normally; the scheduled fallback first looks for a successful
  dispatch on the same branch since the latest 16:00 UTC boundary. A green
  guarded fallback can skip the gate. An API error fails the guard rather
  than proving no dispatch existed. Scheduled
  [run 45726448464](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/45726448464)
  on the exact tip completed successfully but skipped Stamp, Gate, and
  Report after the guard found successful dispatch
  [45659625993](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/45659625993)
  on parent `645dc7ba` since that 16:00 UTC boundary. The green fallback is
  not gate evidence for this tip. The dispatch itself is parent-commit
  evidence (installers, Docker, binaries, and L4/L5 real E2E succeeded
  there) and does not cover the session-kernel teardown commit.
- [Version policy](https://github.com/openJiuwen-ai/sciencediscovery/blob/991ba2cc5d33fd9ac49f6b1289c8db156e4cc837/.ci/release-version.mjs)
  reads the application package version. In PR runs, inspect the tested
  synthetic merge's first parent, not a potentially stale event base, and
  verify its second parent is the event PR head.

CI policy, workflow, Nightly, package, release, and version-policy files are
unchanged from the same-day 00:04 pin (the one new commit does not touch
them). The 60 local Node CI-policy fixtures verified at that pin still
apply to these unchanged files; they were not re-executed in this pass.
These are not product UT/ST/E2E, Windows acceptance, remote CI runs or
live-model tests. The two historical defect families / four outcomes remain
calibration only, not an accuracy estimate.

## Historical bounded audit, 2026-11-19 Asia/Shanghai

This Thursday-morning refresh (~10:12 Asia/Shanghai) supersedes the November 12
routing below and the same-day 00:08 SKILL.md pin at `d57fc26`; historical
calibration pins remain unchanged. It is a source-contract audit, not an
upstream PR review.

- Personal main baseline: `9ca0f9384945deb0ae8d95a48a88754428a99c85`
  (`docs(sciencediscovery-review): retire closed canonical source route`,
  2026-11-18T16:08:20Z / 2026-11-19 00:08 Asia/Shanghai).
  Target main: [59d05aa70a26801e2e907ca49060329028514608](https://github.com/openJiuwen-ai/sciencediscovery/commit/59d05aa70a26801e2e907ca49060329028514608)
  (`fix(idea-tree): retry transient model 429s`, committer date
  2026-11-18T17:36:19Z / 2026-11-19 01:36 Asia/Shanghai).
  Local Git comparison from the November 12 audited pin
  `807982f00da6253b41042146171554c51ecc2c3e` enumerated 174 new commits and
  436 changed files. Comparison from the same-day 00:08 pin
  `d57fc2693e0972b5c1040d47a4b74370eb011c3f` is one commit and 11 files, all
  in that Idea Tree 429-retry change. Semantic inspection is limited to source
  routing, the complete label and open-PR catalogs, release/tag ancestry,
  Nightly job results on this tip, and the CI contracts cited below, not all
  changed product code.
- Canonical [PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  closed without merge at 2026-11-16 11:43 AM Asia/Shanghai
  (`closed_at=2026-11-16T03:43:23Z`). It remains `draft=true` and
  `merged=false` at recorded head `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`;
  the head ref `codex/repository-review-skill-20261001` returns 404, though
  the commit object is still reachable. The configured file
  `.agents/skills/sciencediscovery-review/SKILL.md` and root `AGENTS.md` are
  absent (HTTP 404) at the current tip. `.agents/skills` still contains only
  `ci`, `create-github-pr`, `deploy`, `e2e-testing`, `frontend-quality`,
  `gitcode`, and `github`, not a sciencediscovery-review replacement.
  `skills/repository-review-source/sources.json` still lists PR231 as
  `proposed_source`; after state verification that closed, unmerged PR is
  historical, not a live draft-source fallback. This pass does not edit the
  shared loader manifest. Project-specific review remains blocked until a
  maintained entrypoint can be verified. Do not apply a sibling CI or
  development skill as a substitute.
- Latest stable remains [v0.3.0](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.3.0),
  published October 31, peeled to `7acc1dcf62736f7e7bf06c6d51acb5114899f2de`.
  Main has 691 unique commits and the release tag two. A newer prerelease
  [v0.4.0-rc1](https://github.com/openJiuwen-ai/sciencediscovery/releases/tag/v0.4.0-rc1)
  was published 2026-11-13 5:06 PM Asia/Shanghai
  (`published_at=2026-11-13T09:06:47Z`), built from
  `5cac2ce590f09f97164f4528c034170dbc5d1c63` on `releases/v0.4.0.rc1`. Main
  and the RC have diverged (100 main-only and 5 RC-only commits at this pin).
  The product changes below are main-only evidence, not a claim about
  released or RC behavior.
- All 13 open personal-skills PRs were re-enumerated (`per_page=100`, page 2
  empty). None is a sciencediscovery-review change. PR6 remains at
  `68d7b38df04c382e9e51c9fde28428181d3bc5a8` (open, draft) and PR17 at
  `f01a5df38f337e65d80f420e6b22e0b30a5237af` (open, not draft). Both remain
  untouched, including shared manifest/installer changes proposed by PR17.
- Labels were re-enumerated via GitHub REST
  (`GET /repos/openJiuwen-ai/sciencediscovery/labels?per_page=100`): one page,
  57 exact names, page 2 empty. Membership is unchanged from November 12,
  including `release/0.4.0-rc1`. The catalog contains `ready`,
  `priority/major`, `priority/unspecified`, and `agent-ready`; it does not
  contain `high priority` or `high-priority`.
- Open pull requests on `openJiuwen-ai/sciencediscovery` were re-enumerated at
  the same transport (`per_page=100`): 42 open, page 2 empty. The same-day
  00:08 SKILL.md checkpoint recorded 41 open PRs. Search and label-filtered
  issue/PR lists found zero items labeled `high priority`, `high-priority`,
  or exact `ready` (`incomplete_results=false`). One open PR carries
  `priority/major` (#1216) and is not eligible. With `ready` present the
  personal queue still requires exact `high priority` AND `ready`, so the
  eligible set is empty before new-head or delivery checks. Do not treat
  `priority/major`, `agent-ready`, or hyphenated spellings as aliases, and do
  not create labels to force eligibility. No live queue was selected and no
  review or delivery checkpoint changed.

### Executable CI routing at the current pin

CI blobs at this tip are identical to the 00:08 pin `d57fc26` and differ from
the November 12 pin. Read
[tier-policy.mjs](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.ci/tier-policy.mjs),
[ci.yml](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.github/workflows/ci.yml)
and [.ci/README.md](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.ci/README.md)
together, and current [CONTRIBUTING.md](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/CONTRIBUTING.md)
for the matching prose table. The canonical CI skill is still not a substitute
for these executable contracts, and a job graph is not evidence that those
jobs ran.

- `windows_desktop` is now a separate route flag from `distribution`.
  Ordinary `pr` profile: policy/L1/UT/ST plus Linux binary and Docker jobs;
  mocked E2E, real E2E, and the Windows desktop installer are skipped. A
  green PR gate does not prove browser E2E or a Windows installer build.
- `merge` profile: policy/L1/UT/ST plus mocked and real E2E; Linux binary,
  Docker, and Windows desktop jobs are skipped. Verify the merge-group SHA
  separately.
- `daily` and `release`: mocked and real E2E, Linux binary, Docker, and the
  Windows desktop installer are required. Local cumulative test profiles
  remain distinct from workflow job selection; `pnpm ci:e2e` still selects
  the mocked slice locally.
- Merged [#1194](https://github.com/openJiuwen-ai/sciencediscovery/pull/1194)
  (2026-11-17 5:50 PM Asia/Shanghai) is present at this pin: the Windows
  desktop job runs `pnpm --dir application dist --publish never`. That
  disables implicit installer publishing; it is not a runtime desktop
  acceptance test.
- The documentation-only exception is retained: policy/L1 success with the
  enumerated product jobs skipped, not executed product passes. Read actual
  diff classification and job results; unknown diffs retain the full profile.
- [Real E2E workflow](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.github/workflows/real-e2e.yml)
  still references `nightly-research` (blob unchanged since November 12).
  Workflow source does not verify live environment configuration or credentials.
- L5 is no longer the same case set as L4. Read the frozen plan and
  [real matrix](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.ci/real-matrix.mjs)
  (blob unchanged since November 12),
  [Biomni gate](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.ci/biomni-gate.mjs)
  and [configuration](https://github.com/openJiuwen-ai/sciencediscovery/blob/59d05aa70a26801e2e907ca49060329028514608/.ci/biomni-gate.json).
  Current configuration still declares 45 active versus 50 historical cases
  and a temporary, unapproved baseline (`baseline` remains null). Versus the
  November 12 pin, `total_tokens` and `tool_rounds` ratio thresholds were
  removed, and `sum_e2e_ms` warning/block ratios are now 0.3/0.5. Those are
  configuration facts, not measured 45-case results; do not claim an approved
  non-regression baseline from a green or failed run. This pass ran no
  benchmark, model or paid workflow.

### Nightly on this tip

The latest Nightly on the audited tip is
[run 44415877405](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/44415877405)
(Nightly run 99, attempt 2, event `schedule`, head `59d05aa70a26801e2e907ca49060329028514608`).
It completed with conclusion `failure` at 2026-11-19 10:12 AM Asia/Shanghai
(`updated_at=2026-11-19T02:12:31Z`). Of 34 jobs, Real E2E (research-6) failed
at "Run the frozen real E2E shard" and "Summarize actual planned and executed
cases"; Account for real cases, merge-gate, and Report the outcome also
failed. Succeeded jobs included Stamp the build, Select CI policy, L1, UT,
ST, Coverage, Freeze mocked and real E2E matrices, the mocked L2 shards,
Real E2E (basic) and the other research shards, Docker image, Binary release
(aarch64 and x86_64), and Windows desktop installer. L3 real E2E was skipped.
The same-day 00:08 SKILL.md cited successful
[Nov 18 Nightly 44199315530](https://github.com/openJiuwen-ai/sciencediscovery/actions/runs/44199315530)
on `b2075e4972a5`, which is not this tip; run 98 on `d57fc26` also failed.
Check-run annotations recorded process exit code 1 and a Node 20 deprecation
warning, not a recovered case-level failure reason. Do not infer installed
chat recovery, duplicate-tool prevention, or other runtime acceptance from
installer or binary success, and do not treat a green Nightly on another SHA
as evidence for this pin.

### Validation and limits for this refresh

The unchanged selector retains exact-label, pagination/error-as-unknown,
old-PR/new-head, stale-head and cross-policy deduplication fixtures. The two
historical defect families / four adjudicated outcomes remain bounded P2 and
fixed-clean cases, not whole-PR approval or an accuracy estimate. LICENSE
bytes still match main tip (SHA-256
`c5accbbd8546e94c34aed24afe689a617627d18eed5a6c48277e48db57c23851`). No
adjudicated-case pins changed.

Validation of this Thursday-morning refresh: all 268 personal-repository
tests passed, including 36 focused ScienceDiscovery selection/evidence/install
tests. Frontmatter for all 24 skill entrypoints, scoped local links in this
skill, immutable source paths and case pins, LICENSE SHA-256, installation
routing via the plugin `./skills/` glob and `scripts/sync-project.sh` (covered
by the existing installer tests), script syntax (`select_daily.py`,
`replay_cases.mjs`) and `git diff --check` passed. Optional
`replay_cases.mjs` still requires a checkout that already contains the pinned
Git objects; it was syntax-checked here under Node 22.21.0 and not
re-executed against a product checkout in this pass. No source-owned checklist
was copied into the supplement.

The source record is partial. No full application UT/ST/E2E, live models,
scientific validation, Docker/binary qualification, sandbox changes or remote
research were run by this maintenance pass. The failed upstream Nightly above
is cited only as dated job evidence. The offline selector trusts verified
collector flags; it does not fetch pages, prove ancestry, serialize deliveries
or establish remote freshness. Unknown API results are blockers, never
successful empties. Source-level adjudication does not measure reviewer
accuracy, precision or recall.

## Historical bounded audit, 2026-11-12 Asia/Shanghai

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
