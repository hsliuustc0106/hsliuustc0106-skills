# Explicit personal label/new-head queues

This contract applies only when an explicitly configured personal daily brief's
project selection guidance links here. It is not a default queue for other
repositories, the System1 override, private queues, or directly requested
reviews. Explicit project-specific personal overrides govern this selection;
the repository-owned skill remains canonical for the actual review.

Require the exact label `high priority`; if the complete current label catalog
contains `ready`, require both, otherwise require `high priority` alone. Unknown
catalogs, incomplete pages, and API failures block selection. Do not add
creation-date or ever-reviewed exclusions. Old, previously reviewed, own, or
draft PRs can qualify when the labels and verified new-head criteria are met.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from the matching
project resource directory under `references/projects/`. This offline adapter
does not fetch, post, run target code, collect evidence, or update checkpoints.
The collector supplies:

- The repository identity from the project overlay, Asia/Shanghai calendar
  `day`, complete `label_pages` (arrays of exact names) and `pr_pages`, and affirmative
  `labels_complete`, `prs_complete`, `checkpoint_complete`, `baseline_confirmed`.
- Each PR's `number`, full `head` SHA, `state`, exact `labels`,
  `new_commits_verified`, and final `current` observation of head/state/labels.
- Confirmed `delivered` records containing repository, number, full head, policy,
  and day. The flags must represent verified evidence, not assumptions.

Distinguish empty pages from unavailable pages. Conflicting duplicates invalidate
the snapshot; changed final head/state/labels block that PR, while label order is
immaterial. Unknown or malformed input returns nonempty `blocked` and exit 2;
verified results, including no candidates, exit 0. Inspect both output and status.

Compare the current head with completed review history, using ancestry or
commit-set analysis after history rewrites. Comments, creation dates, label
changes, or policy versions do not prove new code. Establish the first-run
baseline or obtain first-run authorization; missing checkpoint history is unknown.

Deduplicate repository/PR/head/policy and keep a head reviewed under an older
policy covered. Select at most ten distinct PRs per repository and Asia/Shanghai
day across confirmed deliveries and current candidates; a new head on a counted
PR uses no new slot. Keep deferred heads pending. Selection is not delivery:
update checkpoints only after confirmed delivery and reconcile uncertain delivery
before retrying. The adapter does not enforce a cross-process cap; follow the
project's concurrency and identity-normalization requirements. No delivery
ledger belongs here.
