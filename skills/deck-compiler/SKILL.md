---
name: deck-compiler
description: "Lint and compile general-purpose semantic deck specifications before rendering PowerPoint, Google Slides, Keynote, PDF, or other presentation formats. Use after a deck narrative or slide inventory is approved to check stable slide IDs, profile-driven narrative completeness and order, slide dependencies, transitive revision impact, or deterministic page ordering. Use build-slides-interactively first when the narrative is still ambiguous."
---

# Deck Compiler

Keep presentation meaning separate from renderer-specific layout. Treat
`deck-spec.yaml` as the semantic source of truth and derive page numbers from its
slide order.

## Workflow

1. Read [references/deck-spec.md](references/deck-spec.md).
2. Create or update a task-local `deck-spec.yaml` with semantic slide IDs.
3. Run `lint` after the narrative and complete slide inventory are approved.
4. Before revising an approved slide, run `impact --changed <slide-id>` for each
   directly changed slide and report every transitive dependent slide.
5. Apply only the user-approved changes. Human approval remains owned by the
   interactive deck workflow; impact analysis is advisory.
6. Run `compile` to produce ordered, page-numbered JSON for the selected renderer.

Run from this skill directory:

```bash
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py lint /path/to/deck-spec.yaml
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py impact /path/to/deck-spec.yaml \
  --changed architecture --changed operating-model
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py compile /path/to/deck-spec.yaml \
  --output /path/to/compiled-deck.json
```

## Core Rules

- Use stable semantic IDs such as `operating-model`; never encode page numbers.
- Keep exact coordinates, fonts, colors, logos, and target object IDs outside the
  semantic specification.
- Give every slide one purpose and one primary takeaway.
- Use a built-in narrative profile or explicit `required_roles` for a custom
  story shape.
- Point a dependency from the dependent slide to the slide it relies on. Set
  `propagates: false` when a change should not trigger downstream review.
- Put domain-specific claims, evidence, layout hints, and renderer metadata in
  slide fields or top-level `extensions`; the core compiler preserves but does
  not interpret them.

## Non-goals

Do not use this skill as an approval database, release-control system, renderer,
or publishing tool. Baseline history, claim contracts, and visual preflight can
be added as independent capabilities after the minimal semantic workflow proves
useful.

## Verify Changes

```bash
uv run --with pyyaml --with jsonschema python scripts/test_deckc.py
```
