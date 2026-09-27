# Validation of the delivered starter

Historical report for the original v1 download. Its binary PPTX and PNG preview
are not checked in with the repository source distribution.

## Result

The delivered `assets/starter-layouts.pptx` passed the kit's structural checker
and a separate rendered-canvas overflow check. All ten slides were rendered and
reviewed on a contact sheet, with detailed inspection of dense architecture,
feedback, and roadmap examples. The preview in `assets/layout-preview.png`
reflects the final flat, shadow-free version.

| Check | Result |
|---|---|
| Slide count | 10 |
| Canvas | 13.333333 × 7.5 inches, 16:9 |
| Native objects | 297 total; 188 nonempty text objects; 1 native table |
| File integrity | ZIP integrity check and python-pptx reopen succeeded |
| Header/footer geometry | Passed named-frame checks |
| Slide numbering | 01–10 in current order |
| Canvas-bound geometry | No out-of-bounds objects found |
| Table frame vs. grid | Coherent in the rebuilt table |
| Explicit shadows | None detected in slide objects |
| Rendered outside-canvas check | Passed; no overflow detected |
| Instructional placeholders | Present by design; checker run with `--allow-placeholders` |
| Original cover image / wordmark | Not copied into the starter |
| Font binaries | None distributed |

## Corrections during review

Inherited default Office shape shadows were removed from both object styles and
the theme. A long roadmap takeaway was shortened to remain one line. The source
cover metadata, agenda details, and overview bodies received slightly safer text
boxes. The source table's inconsistent frame was rebuilt as a coherent native
table. These changes preserve the style rather than repeating fragile file quirks.

## Environment and limitations

The builder was executed with Python 3.13.5 and python-pptx 1.0.2. Rendering used
the available LibreOffice-based presentation renderer. The environment resolves
Arial to Arimo; the PPTX retains its Arial declarations. Microsoft PowerPoint on
the user's target machine was not separately tested. CJK fallback behavior may
also vary across machines and must be checked with the final Chinese content.

The source deck's research was not fact-checked because this task concerns a
format/style skill. Starter text is instructional, not a factual market report.
A passing geometry check does not prove correct meaning, citations, reading
order, accessibility, or future text fit. Every new deck needs a fresh rendered
review after replacing the placeholders.

## Repeat the structural check

```bash
python scripts/check_deck.py assets/starter-layouts.pptx --allow-placeholders
```

For a final presentation, omit `--allow-placeholders`, review any intentional
bracketed text it flags, and render all slides. Do not rely solely on a successful
PowerPoint save or on a clean structural report.
