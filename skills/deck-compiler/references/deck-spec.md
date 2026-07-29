# Minimal Deck Specification

`deck-spec.yaml` records presentation meaning before a renderer turns it into
PowerPoint, Google Slides, Keynote, PDF, or another format.

## Contract

- `schema_version`: currently `1`.
- `deck`: stable identity, title, audience, objective, and language.
- `narrative`: thesis plus a built-in `profile` or explicit `required_roles`.
- `slides.order`: the authoritative order of stable semantic slide IDs.
- `slides.items`: one semantic blueprint per ordered ID.
- `extensions`: optional domain- or renderer-specific metadata that the compiler
  preserves without interpreting.

Every slide requires `title`, `purpose`, `takeaway`, and `narrative_roles`.
Additional fields—draft content, claims, sources, layout intent, speaker notes,
or asset metadata—are allowed inside the slide blueprint.

## Copyable Example

```yaml
schema_version: 1
deck:
  id: platform-proposal
  title: Platform proposal
  audience: Leadership team
  objective: Approve a bounded first program
  language: en
narrative:
  profile: custom
  thesis: Shared primitives reduce repeated delivery work.
  required_roles: [problem, decision]
slides:
  order: [problem, decision]
  items:
    problem:
      title: Delivery work is repeatedly rebuilt
      purpose: Establish the problem.
      takeaway: Fragmentation slows adoption.
      narrative_roles: [problem]
    decision:
      title: Approve one shared workflow
      purpose: Request the decision.
      takeaway: A bounded program tests value before wider investment.
      narrative_roles: [decision]
      dependencies:
        - target: problem
          relation: concludes
extensions:
  template: corporate-light-16x9
```

## Narrative Profiles

Built-in profiles live in `narrative-profiles.yaml`:

- `executive-strategy`
- `technical-deep-dive`
- `research-summary`
- `product-update`
- `proposal`

The linter checks that each required role group appears and that the first
occurrence of those groups follows profile order. Set `required_roles` to use a
custom or intentionally smaller narrative.

## Dependencies and Impact

A slide dependency points from a dependent slide to the slide it relies on:

```yaml
dependencies:
  - target: architecture
    relation: motivates
    propagates: true
```

`impact --changed architecture` reports `architecture` plus every transitive
dependent in deck order. `propagates` defaults to `true`; set it to `false` for a
local relationship that should not trigger downstream review. Impact reports
review scope only—it does not authorize edits.

## Compiled Output

`compile` validates the deck and emits deterministic JSON containing deck and
narrative metadata plus ordered slides with derived `page_number`, stable `id`,
and the complete semantic blueprint. The selected renderer consumes that output.
