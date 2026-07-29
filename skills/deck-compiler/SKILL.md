---
name: deck-compiler
description: "Validate and manage general-purpose presentation specifications before rendering PowerPoint, Google Slides, Keynote, PDF, or other deck formats. Use when Codex has an approved or partially approved deck-spec.yaml and must check narrative completeness, claim evidence and acceptance criteria, semantic slide dependencies, locked-slide change authorization, stable ordering, or a deterministic build manifest. Use this after presentation ideation and approval; use build-slides-interactively first when the narrative or slide blueprint is still ambiguous."
---

# Deck Compiler

Compile an approved presentation blueprint into a validated, deterministic deck
manifest. Keep the compiler independent of subject matter, brand, language,
template, and output renderer.

## Operating Boundary

- Treat `deck-spec.yaml` as the semantic source of truth.
- Use stable semantic IDs. Derive page numbers from `slides.order`.
- Keep exact coordinates, fonts, colors, logos, and renderer-specific objects out
  of the core specification.
- Do not publish externally. A renderer or publisher consumes the validated
  manifest in a separately authorized step.
- Do not use this skill to invent an ambiguous narrative. Route that work through
  `../build-slides-interactively/SKILL.md`.

## Compile a Deck Specification

1. Read [references/deck-spec.md](references/deck-spec.md) and validate the input
   against [references/deck-spec.schema.json](references/deck-spec.schema.json).
2. Select a built-in narrative profile from
   [references/narrative-profiles.yaml](references/narrative-profiles.yaml), or
   declare custom required roles in the specification.
3. Read [references/claim-contracts.md](references/claim-contracts.md) when the
   deck contains facts, quantitative claims, comparisons, inferences, proposals,
   targets, or illustrative data.
4. Read [references/dependency-model.md](references/dependency-model.md) before
   adding a change set or changing an approved slide.
5. Run `validate`, then `lint`. Resolve errors before rendering.
6. Put candidate slide blueprints and any complete non-slide semantic target
   inside a proposed change set. Run `impact` against the previous release
   manifest before editing approved content. Report changed slides,
   dependent reviews, preserved slides requiring review, and locked slides that
   still require authorization. Record the projected release fingerprint when
   the exact proposal is approved, along with the projected manifest fingerprint
   that binds release content to revision history.
7. After approval, apply exactly the approved blueprints and target order.
8. Emit a deterministic release `manifest`. For revisions, compare against the
   previous manifest and selected approved change set. Pass the new manifest to
   the selected renderer.

Run the compiler from this skill directory:

```bash
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py validate /path/to/deck-spec.yaml
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py lint /path/to/deck-spec.yaml
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py impact /path/to/deck-spec.yaml \
  --baseline /path/to/previous-deck-manifest.json \
  --change-set change-id
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py manifest /path/to/deck-spec.yaml \
  --initial-release \
  --output /path/to/deck-manifest.json
uv run --with pyyaml --with jsonschema \
  python scripts/deckc.py manifest /path/to/revised-deck-spec.yaml \
  --baseline /path/to/previous-deck-manifest.json \
  --change-set approved-change-id \
  --output /path/to/revised-deck-manifest.json
```

## Preserve Approval Integrity

- Represent approval with `status`, `locked`, and optional approval metadata.
- Propose changes to locked slides in a named change set before editing them.
  Store complete candidate blueprints in that change set; do not pre-apply them.
- Treat an approved change set as authorization only for its explicit `modify`,
  `insert`, `remove`, target-order, and target-semantics entries against its exact
  baseline manifest fingerprint.
- Do not silently edit slides listed under `preserve`. Review dependent preserved
  slides without mutating them.
- Keep claims attached to stable claim IDs and sources attached to stable source
  IDs. Slides reference claims; they do not duplicate evidence definitions.
- Emit a release manifest only when every active slide is approved and locked.
- Preserve applied revisions and retired slide IDs in the immutable manifest
  history. Do not retain removed slides as active-spec tombstones or reuse their
  semantic IDs.
- Propagate source and claim changes to referencing slides. Record every required
  locked-slide review under the change set's `review` acknowledgements before
  approval.

## Keep the Core General

- Put narrative conventions in profiles rather than hard-coding one story arc.
- Put brand and language rules in renderer or template profiles.
- Put domain vocabulary in optional presets.
- Express quality rules through claim classes and configurable term rules rather
  than special-casing words from one presentation.
- Use sanitized fixtures from multiple deck types when changing the compiler.

## Verify Changes

Run the deterministic test suite and the skill validator:

```bash
uv run --with pyyaml --with jsonschema python scripts/test_deckc.py
```

Also run the host environment's standard skill-package validator when available.
