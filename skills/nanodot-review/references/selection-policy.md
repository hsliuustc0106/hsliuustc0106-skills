# Explicit batch-selection policy

The helper is fixed to `ThinkFlowLab/nanodot`; it neither posts nor changes labels.
Use it only for a requested batch. A direct review of a named PR/branch does not
need the batch labels. Policy version: `nanodot-review-v1`.

1. Read every repository-label page. If the catalog contains `ready`, require both
   `high priority` and `ready` on an open PR. Otherwise require `high priority`.
   Whole names are case-insensitive; whitespace/substring aliases are not accepted.
2. Read every open-PR page, pin each head, deduplicate identical records, and reject
   conflicting duplicates. Unknown/malformed/error/unterminated pages fail closed.
3. Read the confirmed-review ledger. An unchanged reviewed head is ineligible,
   including across policy revisions. Old PRs with new heads remain eligible.
4. Count unique `(repo, PR, head, policy)` completed review jobs for the repository
   in the Asia/Shanghai calendar day, across policy versions. Return at most the
   remaining capacity under 10, ordered by PR number for deterministic selection.
5. Selection does not reserve work or record completion. Serialize sessions or
   use an external atomic reservation mechanism; refresh ledger/cap and selection
   before an authorized post. Revalidate head/state and existing comments again.

A missing/corrupt ledger is unknown, not an empty history. Initialize `[]` only
when prior review history really is empty or has been reconciled. Keep the ledger
outside public source files. One confirmed review record looks like:

```json
{
  "repo": "ThinkFlowLab/nanodot",
  "number": 28,
  "head_sha": "661f4bae106e9f9718137812a803020b8954acc8",
  "policy_version": "nanodot-review-v1",
  "reviewed_at": "2026-10-02T00:00:00+08:00"
}
```

This is a schema example, not a claim that that head was reviewed. Timestamps must
carry an offset. Contemporary review dates use UTC+08:00; the helper does not
model historical Shanghai timezone transitions.

```bash
python3 skills/nanodot-review/scripts/select_prs.py --ledger /path/to/reviews.json
python3 skills/nanodot-review/scripts/select_prs.py --ledger /path/to/reviews.json --day 2026-10-02 --input snapshot.json
python3 skills/nanodot-review/scripts/select_prs.py --revalidate 28 661f4bae106e9f9718137812a803020b8954acc8
```

Live mode pins `--hostname github.com` despite an enterprise `GH_HOST` setting.
It requires existing `gh` access and uses GET-only REST requests, including
Link-header pagination. It does not configure credentials. Fixture mode is fully
network-free. Fixture objects have `repo`, `label_pages`, and `pull_pages`; each
page has `items` and explicit `next_page` (next integer or final null). Revalidation
fixtures instead supply `repo` and `current_pr`.

On errors, exit status is nonzero and no candidate list is emitted. Do not fall
back to no-ready policy after an API failure. Stale-head revalidation checks
identity and open state only; it does not replace a fresh label/ledger selection,
diff review, required-check assessment, or duplicate-comment check.

At the 2026-10-02 inspection, the complete catalog had 10 labels and neither
`ready` nor `high priority`; the sole open PR had no labels. That snapshot yields
zero batch candidates. It does not permanently exempt any PR or supply future
review history.
