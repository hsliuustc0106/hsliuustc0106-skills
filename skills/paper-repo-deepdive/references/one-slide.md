# One-slide PowerPoint construction

Use this reference after the source analysis establishes the central mechanism
and takeaway. Follow [template-style.md](template-style.md) and its source-slide
image by default; an explicit user template or style request takes precedence.

## Compose around one insight

Use the reference's blue title and muted subtitle above a thin rule. Place the
mechanism visual on the left and four compact numbered sections on the right.
Map those sections to problem/baseline, mechanism, evidence, and limitations;
use the pale-blue bottom bar for the practical takeaway. Put short source labels
beneath the bar and detailed evidence in speaker notes.

The left visual can be a relevant paper figure, an editable algorithm diagram,
a repository execution path, or a compact comparison. Do not force a linear
pipeline onto a feedback loop or graph. For repository analysis, a concrete
request/data lifecycle often explains more than a directory tree. Explain why
a defining equation matters instead of displaying unexplained mathematics.

Aim for roughly 100–150 visible words, excluding citations and essential visual
labels; for Chinese, use the reference's line budget instead of a word count.
Preserve the reference's typography and approximately two body lines per numbered
section. Shorten or recompose crowded content; move supporting detail to notes.
Do not add a second slide or shrink body copy below the reference size to fit.
Keep claim-critical conditions visible even when that requires shortening less
important content. Use the style reference's colors, spacing, and type hierarchy
unless the user's new template overrides them.

## Build an actual editable file

Use an available local presentation toolkit or native PowerPoint API. In Codex,
use `load_workspace_dependencies` to discover the bundled runtime when that tool
is available. Otherwise inspect existing tooling and reuse an appropriate
environment. `python-pptx` or PptxGenJS can create local `.pptx` files; verify the
installed API and dependencies before relying on them. No cloud editor or
external upload is required for this workflow.

- Build text, boxes, connectors, callouts, and simple charts as native editable
  objects. Keep a chart's data editable when authoring it from source values.
- Reuse a supplied template when requested, preserving its visual system and
  reducing the output to the single authored slide without altering the source.
- A relevant source figure may remain a raster image inside the editable slide.
  Inspect its original caption and context, keep it legible, and preserve axes,
  legends, units, attribution, and claim-critical qualifiers. Respect any user
  requirement to keep source figures intact. Do not rasterize the whole slide.
- Clearly identify a new explanatory diagram as a synthesis/adaptation when it
  could otherwise be mistaken for the authors' original figure.
- Put short source IDs next to evidence and hyperlink readable footer labels.
  Include full URLs, paper locators, and repository SHAs/permalinks in notes.
- Add actual PowerPoint speaker notes, not a hidden slide or an off-canvas text
  box. Notes should contain the technical explanation, illustrative walkthrough,
  result conditions, limitations, and the cited evidence map.
- Save under a new task-specific filename. Keep any generation code needed to
  make subsequent revisions in the task output directory.

If using `python-pptx`, speaker text belongs in
`slide.notes_slide.notes_text_frame.text`; hyperlinks belong on text runs via
`run.hyperlink.address`. Reopen with `Presentation(output_path)` to verify the
saved package. Inspect the installed library if a feature differs by version.

## Check the saved output

1. **Structure:** Count slides from the saved deck, including hidden slides;
   require exactly one. Confirm actual editable text, meaningful speaker notes,
   and citation hyperlink targets. Remove unintended template placeholders.
2. **Evidence:** Trace every substantive claim and value back to the analysis.
   Check that a code observation has not become a measured result, source
   qualifications survive compression, and the visual implies only supported
   relationships. Verify all cited locations actually support their claims.
3. **Style and geometry:** Compare against the selected reference: blue title,
   left visual, numbered right column, and takeaway/source bands. Check that
   shapes lie within the canvas, connectors point to the intended objects, and
   text has adequate space. Bounds alone do not prove that rendered text fits.
   Check for stale source text, links, logos, and numbering from the exemplar.
4. **Rendering:** Render the saved `.pptx` with PowerPoint or an available office
   renderer, then inspect the whole slide and dense regions. A headless
   LibreOffice export followed by a PDF-to-PNG conversion is a useful fallback;
   identify it as that renderer, not as validation in PowerPoint. Verify the
   installed commands before using them. Fix issues and rerender after changes.
5. **Delivery:** The preview must come from the final saved deck. Do not offer a
   separately drawn approximation as its render. If no renderer is available,
   deliver the structurally checked `.pptx` and disclose that visual QA remains
   unverified; do not claim the slide was inspected visually.
