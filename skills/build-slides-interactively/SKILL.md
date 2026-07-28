---
name: build-slides-interactively
description: "Plan and create PowerPoint, PPTX, Google Slides, Keynote, or other slide decks through explicit user-feedback gates. Use when Codex should collaborate on a presentation in stages: validate the topic and visual direction with a two-slide cover-and-TOC checkpoint; approve the chapter narrative and every slide's title, draft content, evidence, and layout arrangement; then build and revise the draft without changing approved slides silently."
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
- Use 10 pt as the hard minimum for every visible text run, including sources,
  footers, captions, labels, annotations, legends, and page numbers. If content
  does not fit, shorten, split, reflow, or enlarge its text box; never shrink it
  below 10 pt.
- For every slide, inspect user-supplied and researched sources before drawing a
  new figure. Trace researched figures to the primary source and verify their
  caption and context; do not reuse search previews or third-party reposts.
  Prefer direct reuse when the figure supports the approved message, is legible
  at presentation scale, and its usage and modification rights are verified. If
  rights are unclear, do not reuse it; list them as a dependency and request
  authorization evidence or select a rights-safe alternative. Make only minimal
  presentation-focused edits: crop, scale, clean the background,
  translate or restyle labels, or add callouts and highlights. Do not remove
  credits, watermarks, required notices, or essential legends, axes, units,
  qualifiers, uncertainty, or semantic color encodings. Preserve quantitative
  and semantic meaning; cite unmodified figures as `Source` and modified figures
  as `Adapted from`. Create or redraw only when no suitable rights-safe figure
  exists or direct reuse would reduce clarity, accessibility, legibility, or
  accuracy.
- Use other presentation-format skills or tools only inside the currently approved
  stage.

If the user already provides an outline, template, or slide plan, map it to the
stages below, identify what is already approved, and confirm the proposed starting
stage before creating slide content.

## Stage 1: Topic, Template, and Two-Slide Checkpoint

When the user requests a named organizational template, check
[references/template-references.md](references/template-references.md) for a
matching source. Verify current access, file format, and authorization before
using it.

Clarify and propose:

- audience, goal, presentation context, language, duration, and expected depth
- scope, main topics, exclusions, and the intended final takeaway
- reference decks, brand sources, and asset provenance
- template direction: aspect ratio, typography, colors, logos, footer, page numbers,
  and citation treatment
- a minimal layout library, such as title, section, architecture, process,
  comparison, benchmark, evidence, and summary slides

Inspect supplied decks and assets read-only while agreeing on the brief. Define the
intended detailed-slide layout library, but do not render detailed-slide examples at
this stage.

First deliver a short creative brief plus a template/layout proposal. Surface
assumptions and meaningful alternatives, then obtain explicit agreement before
writing the checkpoint deck.

After agreement, create or update the working presentation and output exactly two
slides:

1. **Cover** — approved topic, subtitle, duration, language, template direction,
   branding, footer, and page number.
2. **Provisional table of contents** — chapter names, order, narrative arc, and rough
   time allocation, presented in the approved visual system.

The second slide is a narrative hypothesis for Stage 2, not an approved detailed
outline. Do not add chapter openers, sample architecture diagrams, detailed content
slides, or a layout gallery. Keep the Stage 1 deck at exactly two slides.

When Google Drive is the chosen destination, create a dedicated folder, preserve any
source deck, and save an editable native Google Slides working copy there. Verify the
deck identity, the two-slide count, and both slides visually before sharing the link.

Stop for feedback on the topic, chapter direction, visual template, logo placement,
and branding. Stage 1 is approved only when the user explicitly accepts both slides.

## Stage 2: Narrative and Slide Blueprint Approval

Complete Stage 2 through two separate approval gates. Do not create detailed slides
until both gates are approved.

### Gate 2A: Deepen and Approve the Table of Contents

Treat the Stage 1 table-of-contents slide as provisional. Deepen the narrative
structure from the approved brief. For each proposed chapter, show:

| Field | Required content |
| --- | --- |
| Chapter | Working title |
| Motivation | The audience problem or question that makes the chapter necessary |
| Purpose | Why the chapter exists |
| Core message | What the audience should remember |
| Evidence | Main claims or proof expected |
| Slide budget | Estimated number of slides |
| Transition | How it connects to the next chapter |

Also state the overall narrative arc, total slide estimate, and intentionally
excluded topics. Check that the ordering answers the audience's questions in a
natural sequence.

Stop for feedback. Reorder, merge, split, or remove chapters until the user approves
the table of contents. Update the second slide to reflect the approved structure.
Keep the chapter motivation visible as a concise `Why` statement when the layout
allows it.

### Gate 2B: Define Every Slide

After the table of contents is approved, define every intended slide before drafting
it. Include the approved cover and table of contents as locked entries so the full
slide count and numbering remain explicit.

| Field | Required content |
| --- | --- |
| Slide number and title | Stable working identity |
| Motivation or purpose | The audience question, problem, or narrative job that makes this slide necessary |
| Key takeaway | One sentence the audience should retain |
| Draft content list | Proposed headline, labels, supporting points, evidence, and conclusion; use real draft wording rather than placeholders |
| Layout arrangement | Reading order, spatial zones, relative emphasis, and visual form; describe where content sits, not only the archetype name |
| References | Source deck, document, paper, benchmark, dataset, or URL |
| Asset needs | Selected reusable figure or candidates; primary source, rights status, planned edits, attribution text, and any missing logos, screenshots, data, or illustrations |
| Dependencies | Open decisions or claims requiring confirmation |
| Transition | How this slide sets up the next slide |

Prefer visuals that explain relationships over decorative graphics. Keep one primary
message per slide. Flag unsupported claims rather than filling gaps with plausible
content. Check that the draft content fits the proposed layout at presentation-readable
sizes. If it does not, shorten, split, or change the layout during planning instead of
deferring the problem to drafting.

After presenting a chapter's blueprints, stop for feedback. Do not blueprint the next
chapter or build slides until the user approves the current chapter, unless the user
explicitly asks to review a larger batch.

Stage 2 is complete only when the chapter structure and the complete slide inventory
are explicitly approved.

## Stage 3: Draft, Review, and Revision

Build only approved blueprints using the approved template and layouts. Draft in
reviewable batches, normally one chapter at a time.

After each batch:

1. Render or preview every created or changed slide.
2. Report the exact slides and elements changed.
3. For each reused or adapted figure, report its primary source, rights status,
   edits, and on-slide attribution; compare it against the original context.
4. Note unresolved content, missing assets, and reference gaps.
5. Ask for feedback and stop before continuing.

Apply revision feedback surgically. Change only the requested slides and elements.
Treat approved chapters as read-only. If a requested deck-wide change affects approved
slides, explain its scope and obtain permission first.

## Stage 4: Final Assembly

After all draft batches are approved, review the complete deck as one presentation.
Resolve only cross-slide issues such as terminology, transitions, numbering, citations,
and template consistency. Do not add new substantive claims or redesign approved
slides without permission.

## Final Verification

After all chapters are approved, perform a final pass for:

- narrative continuity and chapter transitions
- terminology, numbers, and claim consistency
- citations and source provenance
- reused-figure fidelity to its original context, presentation-scale legibility,
  attribution, required notices, and modification scope
- template, logo, typography (including the 10 pt minimum), color, alignment, and
  spacing consistency
- image quality, legibility, clipping, overlap, and page-number integrity
- unintended changes outside the authorized slide regions

Use before-and-after renders or structural diffs when available. Deliver the final
deck with a concise change summary and list any property that could not be verified.
