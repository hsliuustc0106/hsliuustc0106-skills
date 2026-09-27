# Optional JSON builder

The editable PowerPoint can be used without code. This document is for generating
new decks or rebuilding the starter using `scripts/build_deck.py`.

## Basic invocation

From the kit folder:

```bash
python -m pip install -r requirements.txt
python scripts/build_deck.py --content my-content.json --output my-deck.pptx
python scripts/check_deck.py my-deck.pptx
```

The default content is `assets/starter-content.json`; the default output is
`assets/starter-layouts.pptx`. Paths are resolved from the script location for
default assets, so the script can also be invoked from another directory.
No network calls are made by the builder itself.

Tested dependency: `python-pptx==1.0.2`. Python 3.10 or newer is required by the
script's type syntax. The build uses native editable text boxes, shapes, tables,
and connectors. Existing-source measurements are recorded in the token file.

## Root structure

```json
{
  "meta": {
    "title": "Presentation title",
    "deck_label": "PROJECT NAME",
    "brand": "YOUR BRAND"
  },
  "slides": [
    {
      "layout": "comparison",
      "section": "Options",
      "title": "A short, evidence-supported conclusion",
      "subtitle": "Audience, scope, baseline, or material caveat.",
      "cards": [
        {
          "label": "OPTION A",
          "title": "First option",
          "body": "Evidence line 1\nEvidence line 2",
          "note": "A short boundary"
        },
        {
          "label": "OPTION B",
          "title": "Second option",
          "body": "Evidence line 1\nEvidence line 2",
          "note": "A short boundary"
        },
        {
          "label": "OPTION C",
          "title": "Third option",
          "body": "Evidence line 1\nEvidence line 2",
          "note": "A short boundary"
        }
      ],
      "takeaway": "The specific implication or next decision.",
      "source_note": "Actual evidence identifiers and date, where relevant.",
      "speaker_notes": "Full source attribution and presenter guidance."
    }
  ]
}
```

The text above describes fields; replace it with real content. It is not evidence.
JSON `\n` creates a deliberate paragraph line break. Do not pre-break text in the
middle of a word or identifier. The builder does not automatically shorten,
research, verify, or fit the copy.

## Common fields

Every slide needs `layout` and `title`. Regular slides may use `subtitle`,
`section`, `source_note`, and `speaker_notes`. The source note is optional when
no evidence annotation is needed. Slide numbers are generated from current order.
The footer uses `meta.deck_label`, the slide section, and `meta.brand`.

The cover uses its own title and subtitle geometry; it does not use the standard
headline area. All other types share the standard header and footer.

## Per-layout fields

| Layout value | Required layout content |
|---|---|
| `cover` | `title`; optional `kicker`, `subtitle`, `meta` (lower cover text) |
| `agenda` | `items`: exactly 3 objects with `number`, `title`, `detail`; optional `takeaway` |
| `overview` | `cards`: exactly 6 objects with `title`, `body`; optional `number` per card |
| `comparison` | `cards`: exactly 3 objects with `label`, `title`, `body`, `note`; optional `takeaway` |
| `decision` | Same fields and geometry as `comparison`; use priority/support/decision roles |
| `roadmap` | Same fields and geometry as `comparison`; use window/phase/deliverable/gate roles |
| `architecture` | `steps`: 7 strings; `system_title`; `layers`: 4 title/body objects; `platform_label`; `dependency_label`; `callouts`: 4 title/body objects |
| `table` | `headers`: 5 strings; `rows`: 1–10 arrays of 5 values; optional `highlight_cells` |
| `platform` | `apps`: 4 title/body objects; `platform_name`; `capabilities`: 5 strings; `platform_note`; `io_text` |
| `process` | `cards`: 3 label/title/body objects; `sequence`; optional `takeaway` |
| `feedback` | `input_title`; `inputs`: 4 title/body objects; `ledger`; `stages`: 3 title/body objects; `return_text`; `internal_title`; `internal_body`; `external_title`; `external_body`; `improvement` |

For `table`, `highlight_cells` contains zero-based `[body_row_index, column_index]`
pairs; the header is not counted as a body row. For example, `[[2,3]]` highlights
the fourth cell of the third body row. The fill is pale teal; the label must still
convey its meaning without color.

## Content that does not match a fixed recipe

The builder deliberately rejects the wrong number of cards/chips because these
recipes encode measured geometry. This is a layout constraint, not a content
requirement. Never invent evidence or pad a deck with fictional items to pass
validation. Select another recipe, split content across slides, or adapt the
layout function and token geometry intentionally.

The starter's ten slides are examples, not a fixed sequence. The JSON can contain
any number of compatible slide entries in the order required by the user's story.

## Cover images and branding

The builder creates an image placeholder, not an AI-generated cover illustration.
In PowerPoint, replace `HERO_REPLACE_WITH_IMAGE` with an approved image and remove
`HERO_PLACEHOLDER_LABEL`. Keep the white panel above it and crop the image to the
13.333 × 4.60 zone. For automated image insertion, adapt `build_cover` using a
local user-approved image; preserve aspect ratio and z-order.

`meta.brand` is a text placeholder for the brand area. A real logo can replace it
when supplied or explicitly authorized. Do not silently use the original deck's
wordmark.

## QA and limitations

`check_deck.py` checks slide dimensions, canvas bounds, named frame placement,
page numbers, table-frame consistency, explicit shadows, and placeholder-like
text. Intentional bracketed text, such as some citation styles, may need manual
review. `--allow-placeholders` is intended for reusable starters.

The checker does not prove that paragraphs fit inside text boxes or that arrows
avoid actual text. It does not verify sources, interpret the story, or guarantee
cross-application font rendering. Render and inspect every output slide.
