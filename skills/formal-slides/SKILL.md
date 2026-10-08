---
name: formal-slides
description: Create or edit editable PowerPoint slides using the user's saved formal presentation templates. Use for new PPT slides, template selection, consistent presentation styling, and creating matching layouts when the existing library cannot support the content. Not a substitute for researching the slide topic.
---

# Formal Slides

Produce editable slides using the user's established blue-and-white style. The
bundled deck is a library of reusable compositions, not a prescribed presentation
sequence. Prefer a small, useful slide set over an elaborate planning document.

## Establish the brief

Use the requested topic, sources, audience, language, slide count, and selected
templates. Continue from an existing deck when identified. A template or branding
specified for the current task overrides this saved default.

If the audience or purpose is unspecified, state a reasonable assumption and
proceed. Ask only when an unresolved gap changes the message or scope materially.
Do not add a cover, agenda, or closing page to a request for content slides alone.

For each page, keep a compact working plan: **message → layout → evidence or
figure → takeaway**. A long Markdown schema is optional, not a prerequisite.

## Choose and populate a layout

Read [references/layouts.md](references/layouts.md) for layout names, positions,
style defaults, and the product-insight and closing-page conventions. Inspect the
[library preview](assets/templates-preview.png) when visual matching helps.

The editable source is [assets/templates.pptx](assets/templates.pptx). Resolve
these paths from this skill's directory; do not depend on an earlier chat or a
temporary workspace. Discover available presentation tools and reuse an existing
environment before setting up dependencies.

Select by narrative role, evidence type, orientation, and content density. Honor
the user's chosen layout unless a concrete fit or semantic problem requires an
adaptation; explain that change briefly. The selection helper can copy unique
exemplars into a working deck while preserving their native objects:

```bash
# Set these to the discovered skill path, a Python with python-pptx, and task output.
"$SLIDES_PYTHON" "$SLIDE_SKILL_DIR/scripts/select_templates.py" \
  --slides 9,6,7 --output "$SLIDE_OUTPUT_DIR/working.pptx"
```

Duplicate selected pages with the authoring tool when one layout is needed more
than once; each copy must be independently editable. Replace template labels,
example text, source placeholders, chapter badges, dates, and page numbers with
the actual presentation content. Preserve the title, media frame, cards, table,
diagram, takeaway band, and footer where they serve the destination content.

Keep narrative text, tables, diagram labels, and connections native and editable.
Use original images for screenshots or photographs; fit meaningful images without
stretching or losing important content. An explanatory mockup must be identified
as an illustration. Define what an architecture arrow or grouping means before
styling it; capability layers do not automatically imply a runtime sequence.

Use concise source labels near claims or figures and full citations, dates,
qualifications, and speaking guidance in notes. Distinguish sourced facts, reported
results, interpretation, proposals, and unknowns. Verify changing product facts
when research is in scope; a previous slide is not independent product evidence.

## Adapt or create a new template

Try a local adaptation first: change card count, column balance, image allocation,
or table dimensions while retaining the visual family. A content variation does
not automatically need a new template.

Create a new composition when the existing types cannot communicate the message
readably or correctly—for example, a results chart with uncertainty, a tensor
layout, or a detailed sequence. State the concrete reason. Do not solve an
unsuitable layout by shrinking all text, omitting required analysis, or inventing
content to fill slots. Respect the requested page budget.

New layouts use the same canvas, typography, palette, header hierarchy, spacing,
and footer conventions in [references/layouts.md](references/layouts.md), adapted
to the evidence. Keep a clear reading order, one principal visual or argument,
and an implication or next action. Reuse existing frame and label treatments.

When this workflow creates a genuinely reusable new layout, save a clean exemplar
alongside the completed slides. Replace task-specific facts, confidential content,
and source media with useful generic fields or neutral media placeholders.
Append that exemplar to the end of the saved library, keeping existing layout
positions stable; update the catalog and preview. Stage and visually validate the
expanded library before replacing the installed assets, and preserve the previous
revision in the task's output directory. Tell the user which template was added.

For a task using a different supplied design, follow that design in the output;
do not silently mix it into this saved visual family. Leave unrelated skills and
configuration unchanged.

## Validate and deliver

Render the completed presentation and inspect every delivered page. Check text
fit, readable labels, alignment, image proportions, figure semantics, source
placement, stale placeholders, page order, and native editability. For closing
pages, check the actual hyperlink targets. Repair concrete defects together;
normally one consolidated repair pass is sufficient.

Deliver the editable `.pptx` with a PDF or image preview. Provide `.potx` when a
PowerPoint template is requested. If a new template was saved, also link the
expanded library. Report relevant verification and material access limitations
concisely. Upload to Drive or create native Google Slides only when requested;
use the available corresponding workflow for that destination.
