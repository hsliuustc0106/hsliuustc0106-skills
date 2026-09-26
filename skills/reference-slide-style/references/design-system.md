# Design system: measurements and interpretation

## Evidence hierarchy

1. **Measured:** slide dimensions, object geometry, explicit text formatting,
   colors, table grid, and connectors from the uploaded PowerPoint's OOXML.
2. **Observed:** visual organization and recurring patterns in the supplied
   rendered slide images.
3. **Recommended:** portability, readability, density, and future-use rules
   introduced by this kit. These are identified below rather than attributed to
   the reference.

Source: `ai-application-innovation-20-pages.pptx`, 20 slides. This document analyzes
format and style only; it does not verify the deck's research content.

## Canvas and visible regions — measured

The PowerPoint is 13.333333 × 7.5 inches: 16:9. In normalized coordinates, the
left headline origin is approximately 4.1% of slide width and 5.1% of slide height.
Most content spans x≈0.58–12.75, leaving approximately 0.58-inch side margins.

| Region | Position and size, inches |
|---|---|
| Headline | x=0.55, y=0.38, w=12.22, h=0.70 |
| Scope/caveat subtitle | x=0.57, y=1.14, w=12.10, h=0.48 |
| Header rule | x=0.57, y=1.78, w=12.18, h=0.012 |
| General content start | y≈2.02–2.15, depending on family |
| Standard takeaway strip | x=0.58, y=6.20, w=12.17, h=0.43 |
| Evidence note | x=0.58, y=6.74, w=11.65, h=0.20 |
| Footer rule | x=0.57, y=7.02, w=12.18, h=0.012 |
| Breadcrumb | x=0.57, y=7.14, w=7.50, h=0.22 |
| Original wordmark area | x=11.16, y=7.10, w=1.13, h=0.253 |
| Page number | x=12.45, y=7.13, w=0.30, h=0.22 |

Coordinates identify reference rectangles, not a license to pack text to their
edges. Actual glyph extents and wrapping require rendering.

## Color — measured

| Name | Value | Observed application |
|---|---|---|
| Blue | `245BFF` | All regular headlines, numbered labels, prominent takeaways |
| Navy | `182B4D` | Cover title, subject titles, diagram detail |
| Slate | `64748B` | Secondary text, subtitles, notes |
| Purple | `7851D8` | Middle comparison category, shared-platform elements |
| Teal | `087F8C` | Third comparison category, dependency/output emphasis |
| Pale blue | `F3F6FC` | Most cards and takeaway strips |
| Pale purple | `F1EDFF` | Agenda row, workflow chip, shared-foundation panel |
| Pale teal | `EAF7F5` | Agenda row, workflow chip, lower dependency band |
| Divider | `DCE5F1` | Header/footer rules and table grid |
| White | `FFFFFF` | Canvas, text panel, nested layers, table rows |

There is no demonstrated red/amber/green status system. Do not interpret purple
as risk or teal as proven success unless labels establish that meaning. The
three-column accent order is blue → purple → teal, but six-card overview panels
all use blue as their main accent.

The original Office theme contains different default accent colors. Visible
objects use explicit RGB values. The starter updates theme colors to the measured
palette so newly inserted elements are less likely to drift.

## Typography — measured, with a font caveat

Ordinary text runs explicitly name Arial. The source theme also contains a
Simplified-Chinese script fallback of 宋体, while the rendered previews appear
sans-serif. Those facts do not establish a single reproducible CJK face across
renderers. The exact rendered Chinese fallback is therefore **not confirmed**.

The starter retains Arial for Latin text and specifies Noto Sans CJK SC for
CJK where configured. This is a recommended fallback, not a claim about the
reference. Verify any Chinese output in the target environment. No font binaries
are distributed.

| Component | Source formatting |
|---|---|
| Main headline | 30 pt bold blue; 1.12× line spacing |
| Subtitle | 17 pt regular slate; 1.12× |
| Cover kicker | 28 pt bold blue |
| Cover main title | 38 pt bold navy, two lines |
| Cover description | 21 pt regular slate |
| Cover lower metadata | 23 pt bold blue |
| Comparison category | 12 pt bold in that card's accent |
| Comparison subject | 24 pt bold navy |
| Comparison evidence | 19 pt regular slate |
| Comparison caveat/gate | 13 pt bold in that card's accent |
| Grid number / subject / body | 21 bold blue / 20 bold navy / 17 regular slate |
| Architecture system title | 24 pt bold blue, centered |
| Architecture layer text | 16 pt bold heading + 13.3 pt regular detail, centered |
| Workflow chips | 15.5 pt bold, centered |
| Callouts | 20 pt bold heading + 16.5 pt regular detail |
| Table | 13.5 pt; header bold white, body navy |
| Source and footer | 9.5 pt and 10 pt regular slate |

Most standalone text boxes have all four internal margins set to zero. Text
inside native shapes and table cells uses explicit insets. Most paragraphs have
zero before/after spacing. Diagram paragraphs use 1.0× spacing; feedback blocks
commonly use 1.06×.

## Shapes and connectors — measured and observed

Main cards are rounded rectangles, commonly with a PowerPoint shape adjustment
of 0.12. This is a shape-specific adjustment value, not a universal corner radius
of 12% in every rendering engine. Feedback shapes also use approximately 0.16667.
Translate visually when using a different engine.

Cards are flat with no visible shadow. Comparison-card accent strips are
0.045 inches high, equivalent to 3.24 pt. Header/footer dividers are thin filled
rectangles, 0.012 inches high. Native connectors are approximately 0.8 pt with
small triangular arrowheads. Table grid borders are approximately 0.75 pt.

Recommended implementation: explicitly disable local **and theme-inherited**
effects. Some renderers can show a default Office shadow even when a local
empty effect list is present. The builder clears both.

## Adaptations in the delivered starter

These are deliberate usability changes, not hidden source measurements:

| Adaptation | Reason |
|---|---|
| Neutral English instructional placeholders | Reuse without carrying over research or organization identity |
| Cover illustration replaced by a labeled placeholder | Avoid silently reusing the original asset |
| Original wordmark replaced by `[BRAND]` | Keep branding user-controlled |
| Cover metadata height increased from 0.56 to 0.90 | Give its two lines sufficient room |
| Agenda detail boxes enlarged/repositioned slightly | Fit two English lines without spilling into the row edge |
| Six-card body boxes increased from 0.55 to 0.60 high | More reliable line fit while preserving the card grid |
| Table frame rebuilt; rows set to 0.42 | Resolve source frame/grid mismatch and provide predictable native-table geometry |
| Table vertical cell padding reduced to 0.06 | Keep the dense 13.5-pt table within the evidence region |
| Compact feedback labels simplified | Avoid broken English words and identifiers |
| Theme aligned to direct object colors; effects cleared | Keep new objects consistent and prevent default shadows |
| CJK fallback made explicit where configured | Improve cross-environment predictability; still requires testing |

## Extensions, not extracted features

No general bar-chart, line-chart, animation, or transition system is demonstrated
by the source. For new needs, preserve the canvas, type hierarchy, and palette,
but identify the layout as a style-aligned extension. An editable chart may use
minimal rules, restrained accents, and direct labeling. Avoid claiming that this
is an exact source chart recipe.

Do not force the exact source density on a live presentation. When projection
or accessibility requires larger text, reduce content or add slides while
preserving the hierarchy. Source-note sizes are not a recommendation for hiding
important information in unreadable fine print.


## v2 template behavior

The measured source system above remains the visual baseline. v2 explicitly assigns
Noto Sans CJK SC to East Asian text, retains Arial for Latin text, and adds custom
layouts with empty formatted placeholders. New Single content, Two columns and
Thank you geometries are documented in the main skill and the JSON tokens.
Backgrounds live on layouts, not as easily displaced slide-level cards.
The supplied POTX packages declare the template main content type.
No font binaries are embedded or distributed.
