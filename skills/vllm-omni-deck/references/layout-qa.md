# Rendered layout QA

Use this workflow for authored decks and existing-deck repairs. Structural
validation protects the file; rendered inspection protects the audience.

## Plan occupancy before placing objects

Reserve three non-overlapping regions on every content slide:

- a story band for the title and subtitle;
- a body region for figures, cards, tables, and diagrams; and
- the protected footer band defined in `design-system.md`.

Do not place body content until the title and subtitle have their final rendered
line counts. Keep the footer rule, source, page number, and logo out of the body
region. Reserve an empty connector gutter between diagram nodes whenever arrows
or handoff labels need their own lane.

### Treat text as a vertical flow

Treat an eyebrow, heading, value, and body inside a card as one ordered text
stack. Position each item from the rendered bottom of the preceding item, not
from a fixed coordinate copied from another card.

- A text box inside a panel is not proof that its rendered text fits.
- Keep visible padding above the first line, below the last line, and between
  heading, value, and body roles.
- Allow at most two rendered lines for a title or card heading. Keep a subtitle
  to one line unless the body is deliberately moved down for a second line.
- After changing wording, font, size, weight, or text-box width, invalidate the
  downstream positions in that text stack and render it again.
- If a stack does not fit, widen or reflow it, shorten wording without changing
  the approved claim, or split the content with approval. Never hide the
  problem with overlap, clipping, automatic fit, or text below 12 pt.

### Keep connectors in dedicated gutters

Keep native arrows and connector labels outside node and card bounds. Terminate
arrows at object edges, preserve one reading direction, and place handoff labels
entirely inside the reserved connector gutter. If the gutter cannot hold the
label at 12 pt, simplify the label or move the detail to a supporting card.

### Keep source figures presentation-legible

Preserve source figures intact as required by `design-system.md`. The labels,
axes, legends, and qualifiers that support the slide claim must remain readable
in a full-slide presentation view. If they are not, dedicate a slide to the
figure, obtain a higher-resolution source, or omit it; do not crop or redraw it.

## Repair an existing deck

Before editing, capture the slide order and IDs, wording, hyperlinks, source
figures and their aspect ratios, footer elements, and a rendered baseline. Make
the smallest native-object changes that preserve the authorized narrative.

For native Google Slides, read a fresh revision before each write and guard the
batch update against that revision when the editing surface supports it. Keep
stable object IDs and hyperlinks. A font normalization or text replacement is a
layout change because it can alter line wrapping even when the object geometry
is unchanged.

## Run the rendered QA loop

1. Run the available structural checks for slide count, canvas, typography,
   placeholders, links, object bounds, branding, and source-figure integrity.
2. Render every slide with the delivery platform after the first complete pass.
3. From the skill directory, build labeled contact sheets for the whole-deck
   sweep:

   ```bash
   .venv/bin/python scripts/build_contact_sheets.py \
     --input-dir /path/to/rendered-pngs \
     --output-dir /path/to/contact-sheets
   ```

4. Inspect the contact sheets for hierarchy, density, alignment, repetition,
   footer consistency, and slides that need full-size review.
5. Inspect every changed or dense slide at full-slide resolution. Check rendered
   wrapping, clipping, text collisions, connector lanes, table rows, source
   labels, and footer clearance.
6. Repair failures by reflowing geometry or tightening approved wording. Render
   each repaired slide again before moving on.
7. After the final repair, rerender the complete deck and repeat the contact-sheet
   sweep. Do not deliver from a changed-slide-only sample.

A zero-result structural or geometry checker is not evidence that rendered text
fits. Rendered pixels on the requested delivery platform are authoritative for
wrapping, clipping, overlap, and legibility.

## Use the target renderer

- For a PowerPoint deliverable, render the final `.pptx` with PowerPoint when
  available or LibreOffice as the compatibility check.
- For native Google Slides, fetch fresh large thumbnails after the latest write;
  do not validate with thumbnails captured before a mutation.
- For a cross-platform handoff, validate the requested primary surface first and
  report any compatibility limits on the secondary surface.
