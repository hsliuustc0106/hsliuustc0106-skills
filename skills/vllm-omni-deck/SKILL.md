---
name: vllm-omni-deck
description: Create and restyle editable, English-first vLLM-Omni PowerPoint decks with the bundled seven-layout branded template and typed python-pptx generator. Use when Codex needs to build a new vLLM-Omni .pptx, migrate or restyle existing vLLM-Omni slides, select layouts for an approved slide blueprint, or regenerate and validate the vLLM-Omni deck template.
---

# vLLM-Omni Deck

Create PowerPoint-first vLLM-Omni decks with native, editable objects and a
fixed visual system.

## Load the Design Contract

Read both references before creating or restyling slides:

- `references/design-system.md` defines the canvas, brand tokens, typography,
  footer, and component rules.
- `references/layout-catalog.md` defines the seven layouts, required inputs,
  selection rules, and safe content density.

Treat these files and `scripts/build_template.py` as the source of truth. Use
`assets/vllm-omni-template.pptx` as the canonical editable slide library. Never
modify that asset in place; copy it to a task-specific output path.

## Choose the Workflow

- For an ambiguous or net-new narrative, use the sibling
  `../build-slides-interactively/SKILL.md` workflow before drafting slides.
- For an explicitly approved outline and per-slide blueprint, proceed directly.
- For restyling, preserve approved wording, evidence, citations, and slide order
  unless the user authorizes changes.

Require the user to provide or approve each slide's purpose, key takeaway,
substantive content, and evidence. Select the best layout from the catalog. When
two layouts are plausible, recommend one and explain the tradeoff.

## Build or Regenerate the Template

Create a fresh environment before running the generator:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python python-pptx
.venv/bin/python scripts/build_template.py \
  --output assets/vllm-omni-template.pptx
```

Run the command from this skill directory. The generator refuses to overwrite an
existing file unless `--force` is passed. It validates the slide count, canvas,
font family, allowed sizes, example labels, and required native chart before it
returns successfully.

## Author Slides

1. Confirm the slide blueprint and references.
2. Choose a catalog layout by narrative role, not by superficial object count.
3. Preserve the approved 36/28/18/12 pt Arial hierarchy.
4. Keep text, shapes, diagrams, tables, and charts native and editable.
5. Reflow within the chosen layout when content is slightly long.
6. If content still does not fit, recommend shortening it or splitting the slide
   and wait for approval. Never shrink, omit, or split silently.
7. Mark fabricated demonstration values as `Illustrative data` directly on the
   slide. Never present them as measured results.
8. Preserve source notices and quantitative meaning when adapting figures.

Do not add animations, transitions, decorative gradients, glass effects, or
heavy shadows. Do not rasterize editable narrative content. Optimize for
PowerPoint and keep Google Slides compatibility best-effort.

## Verify Every Output

- Confirm that every delivered slide has one primary message.
- Confirm Arial and the allowed sizes only: 36, 28, 18, and 12 pt.
- Confirm no text is clipped, overlapped, or smaller than 12 pt.
- Confirm the vLLM-Omni logo appears on every slide.
- Confirm page numbers appear on every slide except the cover.
- Confirm white content slides reserve the source/footer line.
- Render the complete deck to PDF with LibreOffice and inspect every slide.
- Treat the generator's seven-slide count check as canonical-template validation.
  For a derived deck, validate against the user's approved slide inventory while
  preserving the same canvas, typography, branding, and editability checks.
- Treat PowerPoint as authoritative; report that Google Slides fidelity is
  best-effort when handing off the file.
