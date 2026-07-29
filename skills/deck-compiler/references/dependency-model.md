# Dependency and Change Model

A dependency means that the current slide may need review when its target
changes:

```yaml
dependencies:
  - target: operating-model
    relation: summarized-by
    propagates: true
```

The relation is descriptive and extensible. Examples include:

- `follows`
- `supports`
- `supported-by`
- `summarized-by`
- `elaborates`
- `feeds-into`
- `updates-with`
- `must-preserve-with`

Set `propagates: false` when the relationship is informative but should not
trigger impact analysis.

## Impact Direction

If slide A lists slide B as a propagating dependency, changing B marks A for
review. Impact analysis follows this reverse dependency graph transitively.

It reports four distinct sets:

- `changed`: explicitly modified, inserted, or removed slides
- `dependent_reviews`: downstream slides that may now be inconsistent
- `preserved_reviews`: dependent slides explicitly protected from mutation
- `authorization_required`: locked changed slides not covered by an approved
  change set

Review does not imply permission to edit. A preserved slide may require a human
consistency decision while remaining byte-for-byte unchanged.

## Exact Authorization

A proposed change set carries complete target blueprints, optional complete
target semantics, and the prior combined manifest fingerprint. Impact analysis
reconstructs the candidate from that immutable baseline and lints it. Keep all
candidate changes outside the active deck until approval. Once approved:

- apply only the declared modifications, insertions, removals, and target order
- emit the revision manifest against the exact baseline and change-set ID

Record the projected release fingerprint from impact analysis in the approved
change set together with the projected manifest fingerprint. The latter binds
the target release to applied history and retired IDs. The compiler compares the
complete semantic payload, actual per-slide fingerprints, and order with the
approved scope. A changed locked slide, undeclared insertion, missing removal,
altered candidate blueprint, changed claim or narrative, or mismatched baseline
blocks release.

Source changes propagate to claims, supporting-claim changes propagate
transitively, and affected claims propagate to referencing slides. Deck, profile,
narrative, and QA changes require deck-wide review. Required locked-slide reviews
must appear in the change set's `review` acknowledgements before approval.

The release manifest stores applied action fingerprints and retired slide IDs.
Removed slides do not remain in the active specification, and their semantic IDs
cannot be reused.
