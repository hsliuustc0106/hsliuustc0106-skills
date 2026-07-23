# vLLM-Omni layout catalog

Select layouts by narrative role and evidence type. The user owns slide logic,
content, and evidence; Codex owns layout selection.

## Selection guide

| Need | Layout |
| --- | --- |
| Open or close a presentation | 1. Cover / closing |
| Mark a narrative transition or state one major idea | 2. Section / key message |
| Orient the audience or summarize a sequence | 3. Agenda / summary |
| Explain one idea with supporting structure | 4. General content |
| Explain components, flow, ownership, or interfaces | 5. Architecture / diagram |
| Show a source figure or prove a comparison | 6. Evidence / source figure |
| Show dependency, timing, status, or ownership | 7. Roadmap / status |

Do not choose a visually similar layout when its narrative role is wrong. If the
approved content exceeds the safe density below, recommend shortening or splitting
and wait for approval.

## 1. Cover / closing

**Use for:** opening identity, final takeaway, or call to action.

**Required inputs:** title, subtitle or closing statement, presenter/team, date or
context.

**Arrangement:** white brand plate at top left; large title in the left two-thirds;
small context line below; restrained modality motif on the right.

**Safe density:** one title of at most two lines, one supporting statement, and two
short metadata lines. Omit the page number.

## 2. Section divider / key message

**Use for:** chapter transitions or a single statement that should reset audience
attention.

**Required inputs:** section label, one-sentence message, one supporting sentence.

**Arrangement:** message on the left; a simple editable flow or semantic motif on
the right; page number only in the lower-right corner.

**Safe density:** one 36 pt message of at most two lines and one 18 pt explanation.

## 3. Agenda / summary

**Use for:** agenda, executive summary, questions answered, or chapter recap.

**Required inputs:** slide title and three or four ordered items. Each item needs a
short heading and one supporting line.

**Arrangement:** numbered vertical sequence or two-by-two grid, with one clearly
emphasized reading order.

**Safe density:** four items maximum; headings at 18 pt and support at 12 pt.

## 4. General content

**Use for:** capability explanation, problem framing, principles, or text-plus-
visual narratives.

**Required inputs:** assertion title, key takeaway, and up to three supporting
points or visual groups.

**Arrangement:** roughly 38% narrative and 62% editable visual structure. Reflow to
two balanced columns only when the content has equal semantic weight.

**Safe density:** one 18 pt takeaway and three supporting groups with 12 pt labels.

## 5. Architecture / technical diagram

**Use for:** request lifecycle, system components, interfaces, ownership, or data
flow.

**Required inputs:** system boundary, four or five primary stages, relationships,
and one takeaway.

**Arrangement:** full-width left-to-right pipeline beneath the title, with one
supporting annotation band. Keep arrows and nodes native and editable.

**Safe density:** five primary nodes, two-line 12 pt node labels, and one 18 pt
takeaway. Split deeper subflows onto another slide.

## 6. Evidence: source figure / chart / table / benchmark / comparison

**Use for:** a relevant original source figure, quantitative proof, tradeoff
comparison, benchmark, or decision table.

**Required inputs:** claim; selected figure, chart, or table; primary source URL;
provenance and usage-rights status; caption; and one or two conclusions. For
quantitative evidence, also provide metric definitions, units, values, and
comparison baseline. Mark fabricated examples as `Illustrative data`.

**Arrangement:** fit the complete source figure, chart, or table in the left
two-thirds without distortion or loss of meaning; place concise conclusion cards
on the right. Preserve a suitable original figure as an image. Use native
PowerPoint data objects for newly authored charts and tables.

**Safe density:** one source figure, chart, or table and two concise conclusions.
For newly authored charts, use at most four categories and three series.

## 7. Roadmap / status

**Use for:** roadmap, delivery sequence, dependency plan, project status, or risk
overview.

**Required inputs:** three time horizons or phases, owners, dependencies, status,
and one decision or risk statement.

**Arrangement:** horizontal Now/Next/Later sequence with aligned cards and a single
risk or decision strip below.

**Safe density:** three phases, two items per phase, and one risk statement.

## Reuse rules

- Copy the example template when layout demonstrations are useful. Copy the blank
  template when the user wants empty layouts or the source already supplies
  figures.
- Preserve the layout geometry and approved visual hierarchy.
- Replace the lightweight examples with approved content; do not leave sample
  claims or illustrative values in a delivered deck.
- Prefer direct reuse of a relevant, rights-verified, presentation-legible source
  figure. Do not redraw it solely to match the brand.
- Preserve aspect ratio and all meaning-bearing labels, legends, units,
  qualifiers, and notices. Use `Source` for unchanged figures and `Adapted from`
  for minimally edited figures.
- Keep repeated narrative roles on the same layout family.
- Preserve native editability and source notices.
- Render and inspect every changed slide before delivery.
