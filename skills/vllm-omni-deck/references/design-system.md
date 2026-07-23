# vLLM-Omni deck design system

## Canvas and grid

- Canvas: 10 × 5.625 inches, 16:9.
- Safe margins: 0.50 inches left/right, 0.30 inches top, 0.38 inches bottom.
- Content slides reserve the bottom 0.42 inches for source, logo, and page number.
- Align primary objects to a 0.10-inch grid.
- Prefer 0.24-inch gaps between related panels and 0.40-inch gaps between
  independent regions.

## Palette

| Token | Hex | Use |
| --- | --- | --- |
| Navy | `#0D2340` | Cover and section backgrounds |
| Blue | `#3B82F6` | Primary emphasis and selected data |
| Orange | `#F5A623` | Secondary emphasis and decision points |
| Cyan | `#45B7E8` | Supporting modality or pipeline accents |
| Purple | `#7C4DCC` | Limited output-stage accent |
| Ink | `#172033` | Primary text on white |
| Muted | `#5E6B7A` | Supporting labels |
| Rule | `#D8E2EC` | Dividers and quiet borders |
| Panel | `#F4F7FB` | Neutral content panels |
| White | `#FFFFFF` | Content canvas and dark-slide text |

Use navy, blue, orange, and neutrals as the dominant system. Cyan and purple are
reserved for semantic distinctions in architecture or evidence graphics. Never
use color only as decoration.

## Typography

Use Arial throughout. Do not use automatic font fitting.

| Size | Role |
| --- | --- |
| 36 pt | Cover titles and section statements |
| 28 pt | Content-slide titles and key messages |
| 18 pt | Narrative body text and primary supporting statements |
| 12 pt | Diagram labels, charts, tables, captions, citations, footers, and numbers |

Use bold weight for titles, card headings, and key values. Use regular weight for
body text. Keep line spacing compact but readable: approximately 1.05 for titles
and 1.15 for body copy. If approved content does not fit, reflow, shorten with
permission, or split with permission. Never introduce another font size.

## Backgrounds and persistent elements

- Use navy for the cover and section-divider layouts.
- Use white for all content layouts.
- Place the supplied vLLM-Omni wordmark on every slide.
- Treat `assets/vllm-omni-logo.png` as the unmodified wordmark extracted from the
  user-supplied public reference deck, `vLLM-Omni Slides (Public) 2026-04
  latest.pptx`.
- On dark slides, place the wordmark inside a small white brand plate.
- Omit the page number on the cover. Use two-digit page numbers elsewhere.
- On white slides, use a thin rule above a 12 pt source/footer line.
- Keep section dividers free of source lines and taglines.

## Components

### Panels

- Use flat fills and 0.08-inch corner radii.
- Use one-pixel-equivalent rules in `Rule`; avoid heavy outlines.
- Do not use drop shadows, glass effects, bevels, or decorative gradients.

### Source figures

- Prefer a relevant original source figure when its provenance and usage rights
  are verified and it is legible at presentation scale.
- Fit the complete meaning-bearing figure within its frame and preserve its
  intrinsic aspect ratio. Never stretch it or crop essential labels, legends,
  axes, units, qualifiers, watermarks, or uncertainty.
- Preserve the figure's semantic colors and quantitative meaning. Do not redraw,
  recolor, or restyle it solely to match the deck palette.
- Cite an unchanged figure as `Source` and a minimally edited figure as
  `Adapted from`. Keep required notices visible.
- Redraw only when direct reuse is not permitted, the original is illegible, or
  a new editable explanation materially improves accuracy or clarity.

### Architecture diagrams

- Show one reading direction, normally left to right.
- Use blue for ingress or control, orange for core decisions, cyan for modality
  processing, and purple for output stages.
- Keep every node editable and use 12 pt labels.
- Prefer four to five primary stages; move implementation detail into supporting
  labels or another slide.

### Charts and tables

- Use native PowerPoint charts and tables.
- Highlight the comparison that supports the slide title; mute other series.
- Start quantitative axes at zero unless the approved evidence requires and
  explains another baseline.
- Include units and a source or `Illustrative data` notice.
- Do not encode unrelated units on one axis.

### Roadmaps and status

- Organize work by dependency and time horizon.
- Use status colors sparingly and pair each color with text.
- Keep owners, dates, and risks at 12 pt and decision statements at 18 pt.

## Editability and compatibility

Build narrative text, panels, newly authored diagrams, tables, and charts as
native PowerPoint objects. Preserve suitable original source figures in their
native image format instead of rebuilding them. Use raster images only for logos,
screenshots, or source figures that are intrinsically raster. Target PowerPoint
behavior first. Avoid fragile effects, unsupported fonts, and unnecessary
grouping to improve Google Slides import.
