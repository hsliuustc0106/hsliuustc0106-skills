# Reference Slide Style — v2

A reusable bilingual style skill and **blank, fixed-layout PowerPoint template kit**,
based on the user-provided `ai-application-innovation-20-pages.pptx`.

## Build the repository edition first

This is a source distribution of the v2 kit. The six PPTX/POTX files and raster
previews from the downloadable chat kit are not committed as binary files.
Generate the Office templates with:

```bash
cd skills/reference-slide-style
python -m pip install -r requirements.txt
python scripts/build_templates.py
```

The build works from a clean checkout without the original reference deck or a
prebuilt `assets/starter-layouts.pptx`. The labelled PPTX guides replace raster
previews for layout selection in this distribution. The dedicated GitHub Actions
workflow validates the output and publishes all six Office files as the
`reference-slide-style-templates` artifact. Existing v2 validation records below
refer to the original generated kit; each new build still needs its own checks.

## Start here

For ordinary editing, open **`templates/blank-layouts-en.pptx`** or
**`templates/blank-layouts-zh-CN.pptx`**, save a working copy, and duplicate the layout
that fits your content. The first thirteen slides have no visible text; the final
slide has the generic thank-you title and invitation. Placeholders retain geometry,
font, size, color and paragraph defaults even when empty.

For a reusable PowerPoint template, use **`templates/reference-style-en.potx`** or
**`templates/reference-style-zh-CN.potx`**. These are template-format OOXML packages,
not renamed PPTX files. Both include fourteen named custom layouts. The same custom
layouts are also present in the editable PPTX versions.

For AI-assisted work, attach **`SKILL.md`** (English) or **`SKILL.zh-CN.md`** (Chinese)
with your real material and the corresponding blank PPTX. The skill files describe
the same design system; use the language appropriate for the task. This package does
not install itself or create an account-wide preference.

## What changed from v1

The original ten-slide instructional starter is now supplemented by a **fourteen-layout
blank library**. Single-content and two-column layouts were added, the reference's
closing-decision geometry is exposed separately, and a dedicated thank-you page closes
the deck. The thank-you, single-content and two-column designs are explicit extensions
of the reference style, not layouts found verbatim in the original reference.

English and Simplified Chinese versions include localized layout names, placeholder
prompts, speaker notes and closing copy. The Chinese skill and getting-started guide
are included. CJK text is assigned Noto Sans CJK SC; font files are not included.

## Files

| Folder / file | Purpose |
|---|---|
| `SKILL.md` / `SKILL.zh-CN.md` | Main reusable style instructions in English / Chinese |
| `README.zh-CN.md` | Chinese getting-started guide |
| `templates/blank-layouts-*.pptx` | Blank editable decks, 14 slides each |
| `templates/reference-style-*.potx` | Reusable templates, 14 named custom layouts each |
| `templates/layout-guide-*.pptx` | Labelled field guides; not blank production decks |
| `templates/layout-index.json` | Shared bilingual layout index |
| Generated labelled PPTX guides | Layout selection without checked-in raster previews |
| `references/template-workflow.md` | Editing, template behavior and language workflow |
| `references/validation.md` | Actual validation scope and compatibility limitations |
| `references/design-system.md`, `layout-recipes.md`, `source-map.md` | Source measurements and layout recipes, with v2 additions |
| `assets/design-tokens.json` | Geometry, palette, typography and v2 extension metadata |
| `scripts/build_templates.py` | Rebuilds all v2 PPTX/POTX files from the bundled blueprint |
| `scripts/check_templates.py` | Structural validation for v2 blank/guide templates |
| `assets/starter-content.json`, `scripts/build_deck.py` | Retained v1 geometry source and optional content builder; regenerates `assets/starter-layouts.pptx` |

## Layouts

01 Cover · 02 Agenda · 03 Single content · 04 Two columns · 05 Six-card overview ·
06 Three-column comparison · 07 Workflow + architecture · 08 Evidence table ·
09 Shared platform · 10 Three-stage process · 11 Feedback loop · 12 Roadmap + gates ·
13 Closing decision · 14 Thank you.

This is a menu, not a mandatory presentation order or slide count.

## Important editing details

Cards and connectors are placed on the custom layouts to keep them stable during
normal editing. Text fields are editable on the slide; structural changes can be
made in the corresponding layout. Brand, source and page-number fields start empty.
Page numbers are not automatic counters in this kit.

**Table:** duplicate prepared slide 08 to preserve its five-column styled grid.
A newly inserted table layout contains an empty table placeholder only. Inserted
native tables may need their row fills and borders reapplied.

**Cover:** the inserted-picture area is restricted to the right side so it cannot
cover the white title panel. The underlying full-width pale band remains part of
the fixed layout. No sample illustration or original wordmark is carried over.

**Closing:** duplicate prepared slide 14 for the ready-to-use “Thank you” / “谢谢聆听”
page. A newly inserted layout has prompts; the prepared page has the two real
closing strings. Optional presenter/contact fields remain empty.

**Chinese fonts:** the tested CJK face is Noto Sans CJK SC. When unavailable, replace
it consistently with Microsoft YaHei or PingFang SC and inspect all line breaks.
The source's Arial declarations do not prove which Chinese font it originally rendered.

## Future request

> Use the attached reference-slide-style v2 skill and blank PowerPoint to create
> a [number]-slide presentation about [topic] for [audience], in [language]. Use my
> supplied material as the factual basis. Select the appropriate predefined layouts;
> keep the white 16:9 canvas, blue titles, pale cards, purple/teal accents and footer.
> Keep text, tables and diagrams editable. Include the matching thank-you slide at
> the end of the main presentation. Do not invent claims or citations. Render and
> check every slide before delivery.

For blank assets rather than a populated presentation:

> Use blank-template mode. Preserve the fixed layouts and editable placeholders,
> but leave all content fields empty. Keep only the generic thank-you text on the
> final slide. Produce matched English and Simplified Chinese PPTX/POTX versions.

For a restyle, request formatting changes only and explicitly preserve existing
meaning, facts, caveats, terminology and slide order.

## Rebuild and validate

```bash
python -m pip install -r requirements.txt
python scripts/build_templates.py
python scripts/check_templates.py templates/blank-layouts-en.pptx templates/blank-layouts-zh-CN.pptx templates/reference-style-en.potx templates/reference-style-zh-CN.potx
```

Add `--guide` when checking a labelled guide. The script does not render files or
verify content accuracy. Re-render after adding real content. The delivered files
were rendered with LibreOffice; they were not separately tested in Microsoft
PowerPoint on the recipient's computer.

Run source-distribution regression tests from the repository root:

```bash
python -m unittest discover -s skills/reference-slide-style/tests -v
```
