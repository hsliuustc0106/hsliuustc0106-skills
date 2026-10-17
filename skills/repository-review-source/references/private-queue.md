# Optional runtime-local queue selection

This is an opt-in adapter for a separately authorized label/new-head queue. It is
not the default review policy, does not alter source loading, and must not be
applied to an independently configured all-non-draft or manually requested review
workflow. Resolve the owner's active workflow first. Do not infer opt-in from a
repository name, the presence of this file, or a canonical skill's existence.

Run `python3 scripts/select_private_queue.py` from this skill directory, supplying
one JSON envelope on stdin with `config` and `snapshot`. All repository identity,
checkpoints and source mappings remain in the authorized private execution
context. Do not commit real inputs, output, logs, fixtures, private source paths,
architecture, findings or links to a public repository.

## Contract

`config` contains the runtime `repository`, `policy` equal to
`explicit-label-new-head-v1`, and `explicit_opt_in: true`. The collector must have
explicit authorization for precisely this policy; these fields do not grant it.

`snapshot` contains:
- The same `repository` and `policy`, plus the `day` in YYYY-MM-DD computed in
  Asia/Shanghai. The helper validates the date, not the collector's clock.
- `labels_complete`, `prs_complete`, `checkpoint_complete`, `baseline_confirmed`:
  all true only after successful collection and checkpoint reconciliation.
- `label_pages` and `pr_pages`: nonempty lists of pages, including `[[]]` for an
  actually empty result. Fully paginate both queries. An API error or missing
  page is unknown, never an empty catalog. The helper cannot independently
  prove the collector fetched every page.
- Each PR has `number`, full lowercase 40-character `head`, `state`, boolean
  `draft`, `labels`, `new_commits_verified`, and a fresh `current` observation
  containing `head`, `state`, `draft`, `labels`. Conflicting duplicate pages fail
  the whole snapshot. Final refetch changes leave that PR pending.
- `reviews`: verified prior records with `repository`, `number`, `head`, `policy`,
  boolean `completed`, boolean `published`. Completed analysis and confirmed
  publication are separate. A completed unchanged head stays deduplicated even
  if publication failed or the policy changed. Do not backfill posts from this
  selector; incomplete reviews remain pending.
- `daily_charges`: reconciled `{repository, number, day}` records for actual
  work already charged, including incomplete attempts. Discovery alone is not
  charged. Do not reset this history when a policy changes or double-count a PR.

Eligibility requires an open, non-draft PR labeled exactly `high priority` and,
if `ready` exists in the complete repository label catalog, also `ready`.
Only verified new, unreviewed head commits qualify; first-run baseline must be
explicitly established and unreviewed eligible heads verified. Do not use
creation dates, `updated_at` alone, or an ever-reviewed exclusion. At most ten
distinct PRs per repository/day can be charged; a pending previously charged PR
may resume within that count. Repository identities are normalized case-insensitively
for snapshot matching, deduplication and daily charges. Preserve caller order after
complete deduplication. Parallel collectors must serialize or atomically reserve
selected work in their shared private ledger before starting; this pure selector
does not implement cross-process locking or reserve capacity.

The result separates `selected`, `excluded`, and `blocked`; blocked input causes
CLI exit 2. The collector must preserve pending work. Selection is neither a
substantive review nor posting authorization. Re-fetch mutable state and head at
the review/finalization/posting boundaries required by the active workflow.

## Review grounding and coverage

Load the canonical skill and relevant references from one authorized immutable
source revision and record their hashes privately, separately from the target
head. Discover current architecture and testing instructions inside that target;
this public package intentionally contains no private project checklist. Verify
dated guidance against implementation and distinguish releases from main-only
changes. A private baseline comparison belongs only in the private audit record.

For any proposed finding require a current-head file/line, failure scenario,
evidence, severity justified by impact, concise fix and nonduplicate discussion
check. Distinguish executed tests, source-only analysis, author claims and absent
checks. Missing source or evidence blocks a project-specific review claim.

The accompanying tests use fabricated `example/private-project` records and
synthetic SHAs. They are policy contract fixtures, not adjudicated real defect or
clean PR cases and not review-accuracy evidence. Keep any private adjudicated
corpus outside this public repository. No project code, runtime or model tests
are executed by the helper; no accuracy estimate is claimed.
