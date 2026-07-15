---
name: build-slides-interactively
description: "Plan and create PowerPoint, PPTX, Google Slides, Keynote, or other slide decks through explicit user-feedback gates. Use when Codex should collaborate on a presentation in stages: define topics, templates, and layouts; approve the table of contents; design each chapter's slide-by-slide content skeleton and references; then build and revise the draft without changing approved slides silently."
---

# Build Slides Interactively

Create slide decks as a gated collaboration. Do not jump directly from a broad
request to a finished deck.

## Operating Contract

- Start at the earliest unapproved stage.
- End each stage with a concrete review artifact and request explicit feedback.
- Treat silence as no approval. Do not advance until the user approves or revises
  the artifact.
- Keep a compact decision log with `approved`, `open`, and `superseded` items.
- Ask only questions whose answers materially change the result. Recommend a
  default when presenting choices.
- If feedback invalidates an earlier decision, explain the downstream impact and
  return to the affected stage.
- Do not modify an approved stage, chapter, slide, template, or layout without
  permission.
- Use other presentation-format skills or tools only inside the currently approved
  stage.

If the user already provides an outline, template, or slide plan, map it to the
stages below, identify what is already approved, and confirm the proposed starting
stage before creating slide content.

## Stage 1: Topics, Template, and Layouts

Clarify and propose:

- audience, goal, presentation context, language, duration, and expected depth
- scope, main topics, exclusions, and the intended final takeaway
- reference decks, brand sources, and asset provenance
- template direction: aspect ratio, typography, colors, logos, footer, page numbers,
  and citation treatment
- a minimal layout library, such as title, section, architecture, process,
  comparison, benchmark, evidence, and summary slides

Inspect supplied decks and assets read-only at this stage unless the user explicitly
requests a visual prototype.

Deliver a short creative brief plus a template/layout proposal. Surface assumptions
and meaningful alternatives. Stop for feedback and obtain Stage 1 approval.

## Stage 2: Table of Contents

Build the narrative structure from the approved brief. For each proposed chapter,
show:

| Field | Required content |
| --- | --- |
| Chapter | Working title |
| Purpose | Why the chapter exists |
| Core message | What the audience should remember |
| Evidence | Main claims or proof expected |
| Slide budget | Estimated number of slides |
| Transition | How it connects to the next chapter |

Also state the overall narrative arc, total slide estimate, and intentionally
excluded topics. Check that the ordering answers the audience's questions in a
natural sequence.

Stop for feedback. Reorder, merge, split, or remove chapters until the user approves
the table of contents.

## Stage 3: Chapter and Slide Blueprints

Work chapter by chapter. Define every slide before drafting it:

| Field | Required content |
| --- | --- |
| Slide number and title | Stable working identity |
| Purpose | Why this slide is necessary |
| Key takeaway | One sentence the audience should retain |
| Content skeleton | Headline, supporting points, evidence, and conclusion |
| Layout and visual | Diagram, chart, table, comparison, timeline, or other form |
| References | Source deck, document, paper, benchmark, dataset, or URL |
| Asset needs | Logos, figures, screenshots, data, or illustrations still needed |
| Dependencies | Open decisions or claims requiring confirmation |

Prefer visuals that explain relationships over decorative graphics. Keep one primary
message per slide. Flag unsupported claims rather than filling gaps with plausible
content.

After presenting a chapter's blueprints, stop for feedback. Do not blueprint the next
chapter or build slides until the user approves the current chapter, unless the user
explicitly asks to review a larger batch.

## Stage 4: Draft, Review, and Revision

Build only approved blueprints using the approved template and layouts. Draft in
reviewable batches, normally one chapter at a time.

After each batch:

1. Render or preview every created or changed slide.
2. Report the exact slides and elements changed.
3. Note unresolved content, missing assets, and reference gaps.
4. Ask for feedback and stop before continuing.

Apply revision feedback surgically. Change only the requested slides and elements.
Treat approved chapters as read-only. If a requested deck-wide change affects approved
slides, explain its scope and obtain permission first.

## Final Verification

After all chapters are approved, perform a final pass for:

- narrative continuity and chapter transitions
- terminology, numbers, and claim consistency
- citations and source provenance
- template, logo, typography, color, alignment, and spacing consistency
- image quality, legibility, clipping, overlap, and page-number integrity
- unintended changes outside the authorized slide regions

Use before-and-after renders or structural diffs when available. Deliver the final
deck with a concise change summary and list any property that could not be verified.
