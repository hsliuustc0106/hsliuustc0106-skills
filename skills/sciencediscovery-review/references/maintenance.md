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

## Current bounded audit, 2026-10-29 Asia/Shanghai

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

### Current contracts to rediscover at the target

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

## Freshness and validation routing

At the main pin above, CONTRIBUTING.md (Git blob `6c5dd807e1ab8eeb6b364c48edb40fa556cc451b`),
package.json, `.ci/README.md` (Git blob `8e8da0f551133c5320007bc55a3b05765acaa7cd`)
and the CI skill were re-inspected. Read the selected revision's actual
workflow/profile and tagged summaries rather than promoting older prose examples
to passing evidence. Full product CI remains separate from this supplement's
network-free Python tests.

## Corpus and validation limits

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
