---
name: reference-slide-style
description: >-
  Create or restyle editable English or Simplified Chinese presentations in the
  visual style of ai-application-innovation-20-pages.pptx. Use a 16:9 white canvas,
  cobalt headlines, pale rounded cards, restrained purple and teal accents, and
  consistent headers and footers. Includes 14 genuine custom PowerPoint layouts,
  blank-content PPTX and POTX templates, bilingual field guides, and a final
  thank-you slide. Preserve supplied facts; do not copy source research or branding.
---

# Reference Slide Style — v2

## Repository distribution

This checkout contains the v2 source kit. Generate the six Office files before
following the asset paths below: `python scripts/build_templates.py` (after
installing `requirements.txt`). The builder reconstructs its geometry blueprint
from tracked JSON when the optional v1 PPTX is absent; no original presentation,
font binaries, network calls, or private files are needed during generation.
Raster previews are not checked in; use the generated labelled PPTX guides and
`templates/layout-index.json` to choose layouts. The GitHub Actions build uploads
the generated templates as a downloadable artifact when that workflow runs.

## Purpose

Reproduce the reference's visual grammar, not its subject matter. The user controls
content, audience, language, slide count and order. For a restyle, preserve meaning,
terminology, figures, caveats and requested slide order unless rewriting is authorized.
Do not use layout capacity as a reason to invent or omit evidence.

This skill is usable alone. For the closest match, also use the matching blank
PowerPoint in `templates/`. The Chinese edition of this guide is `SKILL.zh-CN.md`.

## Choose the right mode first

**Blank-template mode:** create empty editable placeholders inside predetermined
layouts. Retain cards, divider rules, accent bars, arrows, table grids and text
formatting; remove all sample business text, dates, brands, source notes and numbers.
Instructional prompts belong in the layout or speaker notes, not in presented content.
The supplied blank decks contain no visible text on slides 01–13. The only prefilled
content is the generic title and invitation on the final thank-you slide.

**Presentation mode:** populate the relevant layouts with the user's real material.
Choose only the layouts the story needs; 14 is the size of the layout library, not a
required deck length. Add the final thank-you slide unless the user requests another
ending. Do not silently append it when restyling a deck whose slide order must remain unchanged.

**Guide mode:** use the labelled layout guides to show field positions and roles.
Guide labels are instructions, not finished slide copy. Do not confuse these files
with the clean blank templates.

## Primary assets

| Asset | English | Simplified Chinese |
|---|---|---|
| Blank editable deck | `templates/blank-layouts-en.pptx` | `templates/blank-layouts-zh-CN.pptx` |
| Reusable PowerPoint template | `templates/reference-style-en.potx` | `templates/reference-style-zh-CN.potx` |
| Labelled layout guide | `templates/layout-guide-en.pptx` | `templates/layout-guide-zh-CN.pptx` |
| Layout index | `templates/layout-index.json` | `templates/layout-index.json` |

Each new PPTX/POTX has 14 named custom layouts and 14 prepared slides. Background
cards, rules and connectors live on the custom layout; content fields are native
editable placeholders. This supersedes the v1 examples-only workflow. The older JSON builder is retained for compatibility and as a geometry blueprint.
Its optional output `assets/starter-layouts.pptx` can be regenerated; it is not one
of the new blank templates.

## Quick workflow

1. Establish mode, audience, output language and factual basis. Do not ask for details
   already supplied or retrievable. Use the supplied material without silently adding research.
2. Select a language and layout. Duplicate the corresponding prepared blank slide, or
   use its named custom layout. Preserve fixed geometry unless adapting is necessary.
3. Fill placeholders and optional source/brand/footer fields. For the evidence table,
   duplicate prepared slide 08 to retain its native grid and cell formatting.
4. Keep English and Chinese in separate matched decks when both are requested.
   Translate faithfully; do not create different claims in the two editions.
5. Place the thank-you slide at the end of the main presentation, before an optional
   appendix. Render every slide, inspect wrapping and clipping, and correct issues.

## Fixed visual system

**Canvas:** 13.333333 × 7.5 inches, 16:9, white. Actual PowerPoint geometry is the
source of truth; reference previews may have been rescaled to another aspect ratio.

**Hierarchy:** one blue headline, a gray scope/subtitle line, a thin divider,
structured content, optional takeaway/evidence line, and an understated footer.
Cover and thank-you slides use their own open composition rather than the standard header.

**Containers:** flat, softly rounded rectangles with no shadows, bevels, glass,
gradient body panels or heavy borders. Keep outer margins generous and repeated
columns aligned. Blue leads; purple and teal differentiate secondary content.
Do not communicate meaning through color alone.

### Palette

| Role | Hex |
|---|---|
| Primary blue | `#245BFF` |
| Deep navy | `#182B4D` |
| Slate | `#64748B` |
| Purple | `#7851D8` |
| Teal | `#087F8C` |
| Pale blue | `#F3F6FC` |
| Pale purple | `#F1EDFF` |
| Pale teal | `#EAF7F5` |
| Divider / table rule | `#DCE5F1` |
| Canvas / insets | `#FFFFFF` |

These are measured visible object colors, not the source's unrelated Office theme defaults.
The v2 templates explicitly configure a matching theme.

### Typography

The reference declares Arial for ordinary text runs; that does not uniquely identify
its rendered Chinese glyphs. The templates use **Arial for Latin text** and explicitly
set **Noto Sans CJK SC for Chinese**. This is a portability choice, not a claim about
an original custom font. When that CJK face is unavailable, consistently replace it
with Microsoft YaHei or PingFang SC and re-render. Never distribute font binaries.

| Role | Size and treatment |
|---|---|
| Standard headline | 30 pt, bold, blue |
| Subtitle | 17 pt, regular, slate |
| Cover kicker / headline / subtitle | 28 bold / 38 bold / 21 regular |
| Cover metadata | 23 pt, bold, blue |
| Three-column label / title / body / note | 12 bold / 24 bold / 19 regular / 13 bold |
| Six-card number / title / body | 21 bold / 20 bold / 17 regular |
| Takeaway | 17 pt, bold, blue |
| Workflow chips | 15.5 pt, bold |
| Architecture layer heading / detail | 16 bold / 13.3 regular |
| Right callout heading / detail | 20 bold / 16.5 regular |
| Native evidence table | 13.5 pt |
| Source note / footer | 9.5 / 10 pt |
| Thank-you headline, EN / ZH | 52 / 46 pt, bold, blue |
| Thank-you invitation | 22 pt, regular, slate |
| Optional closing presenter / contact | 18 / 14 pt |

Normal paragraph spacing is 1.12×, with no extra before/after spacing. Compact
architecture labels use 1.0×; feedback blocks use approximately 1.06×. Standalone
text frames have zero margins; native table cells retain intentional insets.
Preserve formatting in empty paragraphs, not only in runs that will be deleted.
Essential prose should not be shrunk into footnote sizes to fit more content.

### Standard frame

Coordinates are in inches as `[x, y, width, height]`.

| Element | Rectangle |
|---|---|
| Headline | `[0.55, 0.38, 12.22, 0.70]` |
| Subtitle | `[0.57, 1.14, 12.10, 0.48]` |
| Header divider | `[0.57, 1.78, 12.18, 0.012]` |
| Optional source note | `[0.58, 6.74, 11.65, 0.20]` |
| Footer divider | `[0.57, 7.02, 12.18, 0.012]` |
| Footer project / section | `[0.57, 7.14, 7.50, 0.22]` |
| Brand | `[11.16, 7.10, 1.13, 0.253]` |
| Page number | `[12.45, 7.13, 0.30, 0.22]` |

Content normally starts near y=2.02–2.15. Keep evidence notes separate from the
footer zone. Blank templates intentionally leave footer text and page numbers empty;
fill and update them when producing the actual deck. They are not automatic counters.

## Layout library

| No. | Layout | Use / source |
|---|---|---|
| 01 | Cover | Opening context; source 1 |
| 02 | Agenda | Three narrative bands; source 2 |
| 03 | Single content | One key idea or visual; new v2 extension |
| 04 | Two columns | Parallel content; new v2 extension |
| 05 | Six-card overview | Six parallel units; source 3, 15 |
| 06 | Three-column comparison | Comparable evidence; source 4, 6, 8, 10 |
| 07 | Workflow + architecture | Seven steps, four layers, four callouts; source 5, 7, 9, 11, 12, 14 |
| 08 | Evidence table | Five columns, ten prepared body rows; source 13 |
| 09 | Shared platform | Four applications, five capabilities; source 16 |
| 10 | Three-stage process | Sequential delivery; source 17 |
| 11 | Feedback loop | Inputs, issue log, return loop, validation; source 18 |
| 12 | Roadmap + gates | Three periods and exit gates; source 19 |
| 13 | Closing decision | Priorities, support and next decision; source 20 |
| 14 | Thank you | Final acknowledgement; new v2 extension |

The original reference has no dedicated thank-you slide. The new closing slide,
single-content slide and two-column slide extend its design language; do not
misrepresent them as directly extracted source layouts.

### Construction recipes

**Cover:** pale full-width image band `[0,0.70,13.333,4.60]`, with an opaque white
left panel `[0.52,1.45,8.05,3.55]`. The v2 picture placeholder is restricted to the
exposed right zone `[8.74,0.70,4.593333,4.60]` so an inserted image cannot obscure
that panel. Crop images rather than stretching them. Do not reuse the source's
illustration or logo without authorization.

**Single content:** pale-blue panel `[0.58,2.12,12.17,3.93]`. Heading at
`[0.85,2.40,11.63,0.45]`; content at `[0.85,3.05,11.63,2.65]`. Add a native chart,
approved image or short text inside this area; the template itself has no data.

**Two columns:** x=0.58 and 6.82, y=2.12, each 5.93×3.93; left pale blue, right
pale purple, with matching blue/purple top accents. Titles are 24 pt; body text
is 19 pt. Keep the two sides structurally comparable.

**Three columns:** x=0.58 / 4.74 / 8.90, width=3.85, y=2.12, height=3.93.
Use a 0.045-inch top accent in blue/purple/teal, with 0.25-inch text insets.
Order category → subject → evidence → caveat or gate. The same geometry serves
comparison, roadmap and closing-decision roles; choose prompts accordingly.

**Six cards:** same column positions; y=2.13 / 4.26; each 3.85×1.90.
Number → heading → two short explanatory lines. Do not manufacture a sixth item.

**Takeaway strip:** background `[0.58,6.20,12.17,0.43]`; blue bold text at
`[0.79,6.27,11.75,0.30]`. Keep it to one line without colliding with source notes.

**Workflow + architecture:** seven short chips across the top; a 6.081-inch-wide
left panel with four white layers, platform/dependency strips below, and four
right callouts beginning at x=7.30. Do not mix system activity with human approval.

**Evidence table:** native five-column table with a blue/white header, alternating
pale-blue/white rows, light borders and 13.5-pt text. Blank tables have no selective
status highlights. Prepared slide 08 includes the formatted grid; a newly inserted
custom layout supplies a table placeholder only. Duplicate the prepared slide to
retain all cell styles. Delete unused rows; never invent rows to fill the table.

**Shared platform:** four application cards above a pale-purple foundation with
five white capability chips, plus a pale-teal input/output band. Native connectors
must reflect the actual relationships in the supplied content.

**Process / feedback:** retain sequence and direction. Avoid splitting words,
identifiers or Chinese semantic units simply to stay within a narrow box.

**Thank you:** no dense content or decision cards. Pale-blue rounded panel
`[0.58,1.80,12.17,3.55]`; three short accent strokes; centered headline at
`[1.20,2.68,10.93,0.92]`; invitation at `[1.20,3.78,10.93,0.48]`.
Use “Thank you” / “Questions & discussion”, or “谢谢聆听” / “欢迎交流与提问”.
Optional presenter and contact fields are below the panel and remain blank until
supplied. This page is not a substitute for the substantive closing-decision page.

## Chinese localization rules

Use Simplified Chinese for the Chinese edition unless another variant is requested.
Translate prompts, speaker notes, headings, labels, source descriptions and closing
copy—not only the large title. Keep official product names, acronyms, identifiers,
units and numerals intact where translating would change meaning.

Use natural Chinese rather than word-for-word English line breaks. Prefer Chinese
punctuation in Chinese prose, avoid an opening bracket at a line end or a closing
punctuation mark at a line start, and keep numbers attached to their units. Do not
add manual spaces between every Chinese character to simulate a Latin font.

As starting guardrails, a one-line 30-pt headline often needs fewer than about
28 full-width Chinese characters; a narrow 19-pt card body may hold about 10–12
per line. These are new practical guides, not measured source limits. Actual
rendered fit is authoritative. Rewrite only with permission; otherwise choose a
wider layout or split the slide. Do not squeeze both complete languages into the
same field when separate decks are requested.

## Content integrity and density

Use conclusion-led titles only when the provided evidence supports a conclusion.
Preserve scope, uncertainty and material caveats. Keep verified facts, interpretations,
proposals and acceptance targets distinguishable. Do not import the reference's
research IDs, historical dates, prices, thresholds, claims or branding.

For ordinary content, prefer one headline line and one subtitle line; two short
body lines in small cards; no more than four concise evidence lines in a tall card.
The prepared table's ten rows are a capacity, not a minimum. A material caveat must
remain visible rather than being hidden in a tiny evidence note.

When content does not fit, choose a more suitable layout, split the slide or move
secondary detail to notes without hiding material qualifications. Shortening must
not change meaning. Never horizontally condense fonts or stretch the slide.

The reference does not define a general chart, animation or transition system.
Any new chart styling is a declared extension, not an extracted feature. Keep
charts editable and data sourced. Use static slides unless motion is requested.

## Building and checking

To regenerate the v2 assets with the bundled geometry blueprint:

```bash
python -m pip install -r requirements.txt
python scripts/build_templates.py
python scripts/check_templates.py templates/blank-layouts-en.pptx templates/blank-layouts-zh-CN.pptx templates/reference-style-en.potx templates/reference-style-zh-CN.potx
```

The older `scripts/build_deck.py` remains a v1 content builder. It is not the v2
custom-layout generator. See `references/template-workflow.md` for manual and AI
workflows, and `references/validation.md` for checks and limitations.

Before delivery, verify the correct mode and language, true 16:9 geometry, blank
fields where requested, correct closing copy, intact native placeholders/tables,
consistent fonts, no clipped text or detached connectors, valid sources, and no
unintended inherited branding. Inspect every rendered slide, not just the cover.

The supplied templates were rendered with LibreOffice; Microsoft PowerPoint on
the recipient's machine was not separately tested. Font availability and future
content may change wrapping. Structural checks do not prove visual fit or factual
correctness. State any untested rendering limitations rather than implying a guarantee.
