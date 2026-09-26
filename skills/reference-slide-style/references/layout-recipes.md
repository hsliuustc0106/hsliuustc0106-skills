# Layout recipes

All coordinates are inches on a 13.333333 × 7.5 slide. Use the standard header and
footer in `SKILL.md` unless the recipe is the cover. Colors refer to the tokens in
`assets/design-tokens.json`. These recipes are source-derived unless explicitly
marked as recommended adaptations.

## A. Cover — source slide 1; starter slide 1

Purpose: subject, strategic promise, audience, perspective, and horizon.

| Element | x | y | w | h |
|---|---:|---:|---:|---:|
| Image zone | 0 | 0.70 | 13.333 | 4.60 |
| Opaque white panel | 0.52 | 1.45 | 8.05 | 3.55 |
| Blue kicker | 0.73 | 1.65 | 7.45 | 0.55 |
| Navy title | 0.73 | 2.42 | 7.50 | 1.65 |
| Slate description | 0.77 | 4.33 | 7.30 | 0.62 |
| Lower blue metadata | 0.77 | 5.63 | 10.70 | 0.56 source / 0.90 starter |

The source uses an isometric technology illustration with cool blue/purple
accents. That image is subject-specific, not an obligatory part of the style.
The starter leaves a neutral image placeholder. Place an approved image behind
the panel, crop proportionately, and keep the visible right side uncluttered.
Do not add the standard headline and top divider on top of the cover design.

## B. Three-band agenda — source slide 2; starter slide 2

Use three rounded bands at x=0.60, y=2.12 / 3.37 / 4.62, w=12.13, h=1.03.
Fills progress pale blue → pale purple → pale teal.

Each band has a blue number at x=0.86, a navy 23-pt section title at x=1.76,
and slate 19-pt detail at x≈6.069. Titles occupy about 4.08 inches; the right
column occupies about 6.47 inches. Keep the two columns clearly separate.

Use the standard takeaway strip at y=6.20 for a scope or appendix note. The
source repeats a section number where two bands belong to the same major
section; do not assume every band must have a unique number. Use numbering that
matches the new deck's actual hierarchy.

## C. Six-card overview — source slides 3 and 15; starter slide 3

Columns: x=0.58 / 4.74 / 8.90. Rows: y=2.13 / 4.26.
Each panel is 3.85 × 1.90 with pale-blue fill and rounded corners.

Relative to each card's top-left:

| Element | x offset | y offset | w | h |
|---|---:|---:|---:|---:|
| Number, 21 pt bold blue | 0.23 | 0.18 | 0.47 source | 0.40 |
| Subject, 20 pt bold navy | 0.23 | 0.74 | 3.39 | 0.39 |
| Body, 17 pt slate | 0.23 | 1.22 | 3.39 | 0.55 source / 0.60 starter |

The body is two concise lines. Use for comparable items, not a six-step process
that needs arrows. For a different number of real items, select another family
or deliberately adapt the grid; never fabricate a sixth point.

## D. Evidence triptych — source slides 4, 6, 8, 10; starter slide 4

Columns start at x=0.58 / 4.74 / 8.90; y=2.12. Each card is 3.85 × 3.93,
all pale blue. Top accent strips are 0.045 high in blue / purple / teal.
Text inset is 0.25; text width is 3.35.

| Element | Absolute y | h | Formatting |
|---|---:|---:|---|
| Category | 2.37 | 0.30 | 12 pt bold, card accent |
| Subject | 2.88 | 0.80 | 24 pt bold navy |
| Evidence body | ≈3.778 | 1.639 | 19 pt regular slate |
| Caveat / status | 5.55 | 0.33 | 13 pt bold, card accent |

The bottom takeaway strip starts at y=6.20. Add a genuine source/status note at
y=6.74 where needed. Use parallel evidence fields and avoid comparing an
established product, a proposal, and a research sample as if they had the same
status. The content must establish each category's boundary.

A short subject can remain one line; the tall title box allows a deliberate
second line. Do not let a two-line subject collide with the evidence body.

## E. Workflow + architecture — source slides 5, 7, 9, 11, 12, 14; starter slide 5

### Top workflow

Seven chips: start x=0.60, y≈2.014; each w≈1.636, h=0.50; gaps≈0.111.
Text is 15.5 pt bold and centered. Use very short verbs or noun phrases. The
observed accents generally follow blue / purple / teal / blue / purple / teal /
blue, with the last chip sometimes on pale purple.

### Left system stack

| Element | Rectangle |
|---|---|
| Pale-blue rounded system container | `[0.60, 2.639, 6.081, 3.264]` |
| System title | `[0.739, 2.667, 5.803, 0.430]` |
| Four white layers | x=0.739; y=3.181 / 3.861 / 4.542 / 5.222; w=5.803; h=0.597 |
| Purple platform band | `[0.60, 6.028, 6.081, 0.320]` |
| Teal dependency band | `[0.60, 6.444, 6.081, 0.250]` |

Each layer has a centered 16-pt bold heading and a 13.3-pt detail line. Use
heading accents blue / purple / blue / teal. Small native downward arrows connect
the layers. The lower bands communicate shared-platform responsibilities and
infrastructure/partner boundaries, not another long paragraph.

### Right callouts

Left accent-bar x≈7.092, w=0.05, h≈0.361. Text x=7.30, w≈5.417.
Heading y=2.722 / 3.694 / 4.667 / 5.639, h≈0.417, 20 pt bold.
Body y=3.167 / 4.139 / 5.111 / 6.083, h≈0.653, 16.5 pt slate.
Use two short lines of body copy, 1.0× line spacing.

Typical roles are customer/budget, build/reuse boundary, human approval,
acceptance/owner, or continuation conditions. These are reusable roles, not
mandatory product claims. Do not carry over the source's metric thresholds.

## F. Evidence table — source slide 13; starter slide 6

Native table begins at x≈0.569, y≈2.028. Source column widths are:

`1.9722 / 0.9722 / 2.0833 / 1.3611 / 5.8056`

Total grid width is approximately 12.1944. There are five columns, one header,
and ten body rows. The broad fifth column carries the task or interpretation.

Formatting: blue header; 13.5-pt white bold labels; alternating pale-blue/white
body rows with navy text; 0.75-pt divider-colored borders; selected cells may use
pale teal. Keep a textual status label as well as color. The source table uses
left-aligned values, including numeric fields.

**Source-file quirk:** the object's declared frame is about 3.281 × 3.281 even
though its column grid totals approximately 12.1944. Declared row heights are
about 0.3472. Renderers may resolve the inconsistency differently or expand cells
to fit text. These values must not be copied blindly as a valid table frame.

**Recommended normalized build:** w=12.1944; 0.42-inch rows; h equals the sum of
row heights; 0.10-inch horizontal and 0.06-inch vertical cell insets. With eleven
rows the table ends at approximately y=6.648, before the evidence note. Use fewer
rows or a follow-up slide when body cells wrap excessively. The starter follows
this normalized version.

## G. Shared platform — source slide 16; starter slide 7

Four application cards:
x=0.60 / 3.668 / 6.736 / 9.804; y≈2.097; w≈2.846; h=1.18.
Fills are pale blue / pale blue / pale purple / pale teal.

A pale-purple foundation panel spans `[0.60,3.806,12.05,2.028]`.
A centered heading names the shared layer. Five white capability chips begin at
x≈0.831 / 3.171 / 5.511 / 7.851 / 10.192, y=4.625, each 2.208 × 0.597.
A short responsibility statement sits beneath them at y≈5.319.

A pale-teal input/output band sits at `[0.60,6.028,12.05,0.611]` with two centered
lines. Thin arrows point upward from the platform toward the applications.

Choose this over the architecture layout when the main relationship is
**many products sharing a foundation**, not a single product's internal stack.

## H. Three-stage process — source slide 17; starter slide 8

Three cards at x=0.58 / 4.74 / 8.90, y=2.15, each 3.85 × 2.90.
Fills progress pale blue / pale purple / pale teal. Unlike the evidence
triptych, all three top accent strips are blue in the source.

Inside: small numbered label at y=2.40; bold 24-pt result title at y=2.91;
19-pt body at y=3.86. Native rightward arrows occupy the card gaps at y≈3.59.

The fuller process sequence sits at `[0.78,5.50,11.80,0.52]`, in strong navy
text. The standard takeaway strip at y=6.20 states accountability or an operating
principle. Do not repeat identical text in the card, sequence, and takeaway.

## I. Feedback loop — source slide 18; starter slide 9

The left visual system occupies x=0.60–7.93; the right explanation begins x=8.28.

| Left-side element | Rectangle |
|---|---|
| Input panel | `[0.60,2.08,7.33,1.20]` |
| Shared ledger | `[0.60,3.52,7.33,0.58]` |
| Diagnose box | `[0.60,4.38,2.01,1.12]` |
| Ownership box | `[2.96,4.38,2.00,1.12]` |
| Retest box | `[5.31,4.38,2.62,1.12]` |
| Return / release band | `[0.60,5.66,7.33,0.68]` |

The input panel contains four small labels and short supporting captions. The
ledger holds shared identifiers and evidence. The three lower boxes connect
left-to-right. The teal band closes the operational sequence, and an outer
connector at x≈8.10 returns upward to the input region.

Right side: internal-validation heading/body around y=2.10 / 2.65;
external-validation heading/body around y=4.48 / 4.97. A purple improvement strip
sits at `[8.28,6.27,4.34,0.43]`. Keep the two validation roles distinct.

Avoid broken words such as an identifier split across two lines. The starter
uses shorter labels than the original dense examples while retaining the logic.

## J. Roadmap and closing-decision variants — source slides 19 and 20

The roadmap uses the evidence-triptych geometry, not a separate timeline chart.
Starter slide 10 demonstrates it.

For each roadmap card:
**time window → phase title → deliverables → exit gate**.
The takeaway strip connects the near-term plan to the later horizon. Keep the
planning dates and evidence gates separate; a date alone is not proof of success.

For a closing decision, use:
**priority → support/ownership → continue/adjust/stop rule**.
The takeaway strip states the concrete decision or approval requested.

The builder accepts both `roadmap` and `decision`. It does not insert real dates,
budgets, or acceptance thresholds. Those belong to the user's current content.


# v2 additions

The ten legacy example recipes above are retained as a geometry record. The new
blank PPTX/POTX files have fourteen named custom layouts. See `template-workflow.md`
and the main skill for the Single content (03), Two columns (04), separately exposed
Closing decision (13), and Thank you (14) recipes. The first two and the thank-you
page are style-aligned extensions; the decision page reuses source slide 20.

The inserted cover picture is now restricted to [8.74, 0.70, 4.593333, 4.60] to avoid
occluding the white left panel. Blank tables have no selective status highlights.
The prepared native table is retained by duplicating slide 08, while a new slide
from its layout has an insertion placeholder. Empty footer/page fields are not
automatic numbers.
