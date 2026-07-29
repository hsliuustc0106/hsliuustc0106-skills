# Deck Specification

`deck-spec.yaml` is the semantic contract shared by planning, rendering, review,
and publishing tools. It describes what the deck means and what may change. It
does not describe PowerPoint shape coordinates.

## Contents

- Required structure and stable IDs
- Slide blueprints
- Change-set lifecycle
- Release manifest
- Sanitized examples

## Required Structure

- `deck`: identity, operation, audience, objective, language, and output targets.
- `profiles`: narrative profile plus optional brand and language profiles.
- `narrative`: thesis, chapters, and optional custom narrative roles.
- `sources`: reusable evidence records.
- `claims`: reusable claim records and their proof or acceptance contracts.
- `slides.order`: final order of stable semantic slide IDs.
- `slides.items`: slide blueprints keyed by those IDs.
- `change_sets`: proposed, approved, applied, or superseded changes.
- `qa`: configurable forbidden terms and claim-term rules.

Validate the complete contract with `references/deck-spec.schema.json`.

## Stable IDs

Use lower-case hyphenated IDs such as `market-context` or `design-tradeoffs`.
Never encode the page number in an ID. Inserting a slide changes only
`slides.order`; references, approval state, and dependencies remain stable.

## Slide Blueprints

Every slide records:

- purpose and one primary takeaway
- narrative roles, when the selected profile needs them
- real draft content rather than placeholders
- semantic layout intent and reading order
- referenced claim and source IDs
- typed dependencies and transition
- approval state and lock state

Keep exact x/y positions, theme tokens, font families, and target-specific object
IDs in the renderer or template adapter.

## Change Sets

Describe intended changes before editing approved content. Put the complete
candidate blueprint inside the change set; do not pre-apply it to
`slides.items` or `slides.order`.

```yaml
change_sets:
  - id: revise-operating-model
    status: proposed
    rationale: Clarify how the program will be executed.
    baseline_fingerprint: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    target_order: [context, operating-model, ecosystem-plan, conclusion]
    modify:
      - slide: operating-model
        blueprint:
          title: Operate through customer co-design and measurable gates
          purpose: Explain how the program wins.
          takeaway: A shared cadence turns capability into adoption.
          status: approved
          locked: true
    insert:
      - slide: ecosystem-plan
        blueprint:
          title: Build with customers and contributors
          purpose: Define the ecosystem motion.
          takeaway: Shared ownership improves adoption and upstream durability.
          status: approved
          locked: true
    preserve: [market-context, architecture]
```

The baseline fingerprint is the previous manifest's `manifest_fingerprint`,
which binds the active release to its applied-change and retired-ID history. Run
`deckc.py impact --baseline ...` to prove the active spec still matches that
baseline, lint the projected target, find downstream reviews, and compute the
projected release fingerprint. `target_order` is the sole placement authority;
insertions do not carry a second anchor rule. Set `reorder: true` when order is
the only intended change.

When claims, sources, narrative, profiles, QA policy, or deck metadata must
change, add `target_semantics` containing the complete desired semantic payload.
If omitted, all non-slide semantics are inherited exactly from the baseline.
Impact reports which semantic sections change.

Impact propagates changed sources through claims and supporting claims to
referencing slides. It also conservatively treats deck, profile, narrative, and
QA changes as deck-wide. Add every reported locked slide to the change set's
`review` acknowledgements and rerun impact.

Use early impact runs as previews. After the human approval decision, keep the
change set `proposed`, add and freeze any optional approval metadata, and rerun
impact over the complete history-bound record. Record that final run's
`projected_release_fingerprint` as `target_fingerprint` and
`projected_manifest_fingerprint` as `target_manifest_fingerprint`. Then apply
exactly the candidate target and set the change-set status to `approved` in one
spec update before emitting the new manifest with `--baseline` and
`--change-set`. Do not add or edit approval metadata after the final impact run.
The compiler rebuilds the candidate from the immutable baseline and compares it
with the active target. If approval metadata was added after projection, it emits
`approval-metadata-not-finalized` and requires another final impact run.

Delete removed slides from active `slides.items` and `slides.order`. The new
manifest records an immutable applied-change summary and accumulates
`retired_slide_ids`; retired semantic IDs cannot be reused. Use `superseded` for
a proposal replaced without shipping. `applied` is a manifest-history state, not
an authorization state for a new revision.

## Release Manifest

Manifest emission is a release gate:

- every active slide must be `approved` and `locked`
- no proposed change set may remain
- create operations require the explicit `--initial-release` flag
- revise, restyle, and migrate operations require the previous manifest plus one
  approved change set

The manifest contains the ordered, complete semantic blueprints, claims, sources,
and narrative; release, slide, history, and combined manifest fingerprints;
applied-change records; and retired IDs. Renderers can consume it without
reopening an unvalidated specification.

## Examples

Use the sanitized, valid examples under `scripts/fixtures/`:

- `valid-executive-strategy.yaml`
- `valid-technical-deep-dive.yaml`
- `valid-research-summary.yaml`
- `valid-product-update-zh.yaml`
- `valid-proposal.yaml`

They demonstrate different subjects, languages, narrative profiles, and claims
without introducing renderer or brand assumptions. The regression tests exercise
revision change scopes and release-manifest gates.
