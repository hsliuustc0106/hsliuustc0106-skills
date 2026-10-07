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

## Sources and overlap, inspected 2026-10-08 Asia/Shanghai

- Personal main baseline: `54ae39d64337aea4cafbcd00803d26212b3fd1bc`
- ScienceDiscovery main: [7a0324257eecb48b57f60b6a80ce2fff54e7dba7](https://github.com/openJiuwen-ai/sciencediscovery/commit/7a0324257eecb48b57f60b6a80ce2fff54e7dba7).
  This is the canonical map's audited baseline; no later main commits were found.
  There was no prior complete personal audit ledger; this begins a bounded
  source record, not a claim of an exhaustive main or release audit
- Canonical migration [PR231](https://github.com/openJiuwen-ai/sciencediscovery/pull/231)
  remains open and draft at `1a12b6e50369d00ae17c3161c5d1c3bc3b0ad15c`.
  Load this explicit revision until merged; do not attribute its skill to main.
  SKILL Git blob: `eab90983063839d3ab92abb63df87db85a859c67`;
  exact-byte SHA-256: `2bf261c60d527034b5fe90f2b5194d8e076e887e8a069515c17575a53d5a9dd1`.
  The daily-selection and repository-contracts references were also read at that
  revision (Git blobs `e28e81b1696c1a93817eb27384cc5ebc3d8919c1` and
  `11117a0cb6416c1da24e497cbf84c9cdf431f3e3`, respectively)
- [Release page](https://github.com/openJiuwen-ai/sciencediscovery/releases)
  lists `0.3.0-beta` as a prerelease and `0.2.0` as latest stable. The tags resolve
  to `6d3c49a882ff45e260dcbdb25ee2918fcb0571ae` and
  `29aae0d39281da66ccd2447532b8a3eb24e534d1`, respectively. The beta follows a
  release branch; main, website documentation and beta are not interchangeable.
  Release notes explicitly limit real-model E2E and experimental platform claims.
  This pass inspected publication notes and tag identities, not every release delta
- [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open. This scoped supplement
  leaves their Omni/shared-discovery work, human edits and PRs untouched
- A cached public label page was inspected, but it does not establish a complete
  fresh catalog. The available connector has no label-catalog read; direct API
  reads were unavailable. No live queue, delivery history or checkpoint was
  selected or changed. A stale page must not become a successful empty queue

## Freshness and validation routing

At the main pin, [CONTRIBUTING.md](https://github.com/openJiuwen-ai/sciencediscovery/blob/7a0324257eecb48b57f60b6a80ce2fff54e7dba7/CONTRIBUTING.md),
[package.json](https://github.com/openJiuwen-ai/sciencediscovery/blob/7a0324257eecb48b57f60b6a80ce2fff54e7dba7/package.json),
[CI notes](https://github.com/openJiuwen-ai/sciencediscovery/blob/7a0324257eecb48b57f60b6a80ce2fff54e7dba7/.ci/README.md) and
[CI skill](https://github.com/openJiuwen-ai/sciencediscovery/blob/7a0324257eecb48b57f60b6a80ce2fff54e7dba7/.agents/skills/ci/SKILL.md) were inspected. The root package declares Node
>=22.19 and pnpm 11.1.2; its CI skill distinguishes the PR/release mock plan
from the daily real-E2E slice. Older prose in `.ci/README.md` and CONTRIBUTING
contains historical counts/schedules; those are not a current run result.
Read the selected revision's actual workflow/profile and tagged summaries rather
than promoting those older prose examples to passing evidence. Full product
CI remains separate from this supplement's network-free Python tests.

## Corpus and validation limits

[Adjudicated cases](adjudicated-cases.json) record bounded historical defect/fix
pairs (four outcomes) with immutable source evidence. Both before outcomes are
bounded P2 judgments; fixed-clean means only the named defect is absent, not
whole-PR approval. The artifact case covers unreachable offsets past the decodable
window; the authority case covers child audit ownership, not a permission bypass.
The latter uses the test-fixture correction after the implementation fix. They are
calibration cases, not a current review or a second architecture checklist.
Quoted source retains the [upstream Apache-2.0 license](LICENSE.sciencediscovery.txt).

The optional read-only replay is `node scripts/replay_cases.mjs /path/to/sciencediscovery-checkout`
from this skill directory (tested with Node 24.19.0). It requires the pinned Git
objects already present; it does not fetch or install. It strips TypeScript and
removes imports to run exact pinned functions in isolation. Artifact projection
uses pinned bounding/classifier functions; authority collection uses explicit
in-memory store/CAS stubs. Four outcomes reproduced, including eight terminal/
beyond-window artifact probes. This is neither the upstream tests nor a complete
journey; real persistence, permissions and the sandbox were not exercised.

Validation: 30 selector tests, five corpus contract checks and one installation
test passed; the full personal-repository suite passed 185 tests (baseline 149).
An independent pass checked 10,000 seeded randomized snapshots (204,366 PR
observations), 243 malformed-field cases and 5,000 arbitrary JSON shapes. This is
selector robustness coverage, not review accuracy. All 17 source records matched
pinned Git objects; 15 product excerpts matched their exact lines and hashes.
All 20 skill entrypoints passed frontmatter validation; scoped links, manifests,
installation routing for Codex/Claude/Cursor, script syntax and diff whitespace
were checked. No source-owned checklist was copied into the supplement.

The source record is partial. No full application UT/ST/E2E, live models, scientific
validation, Docker/binary qualification, sandbox changes or remote research were
run. The offline selector trusts verified collector flags; it does not fetch pages,
prove ancestry, serialize deliveries or establish remote freshness. Unknown API
results are blockers, never successful empties. Source-level adjudication does not
measure reviewer accuracy, precision or recall.
