# Default product-deep-dive template style

## Source and scope

The user selected the
[Claude Science deep-dive slide](https://docs.google.com/presentation/d/1OwV35KX4m_78F1DxqW-3y7LYVeyGIPHcm9ONU7e82d4/edit?slide=id.aiapp_claude_science_deepdive#slide=id.aiapp_claude_science_deepdive)
as the style reference. Native structure was read on 2026-09-26, revision
`Q6fPltKze3eq6g`: slide `aiapp_claude_science_deepdive`, fourth slide at that time,
layout `p30`, master `p27`. Use the slide ID rather than its ordinal for targeting.

The measurements below come from that slide's native elements. The connector's
PDF export did not materialize locally, and its thumbnail was not viewable in
the authoring environment; the source's rendered appearance was not verified.
These values support reconstruction, not a claim of pixel-perfect matching.
Inspect fresh renders of every generated deck before delivery.

Reuse the visual language, not the Claude-specific facts or screenshots. This is
the default for both business and technical pages unless the current task names
another template. Live source access is useful for exact duplication or checking
later changes; the saved measurements can be used without refetching the deck.

## Measured visual system

| Property | Source value |
| --- | --- |
| Canvas | 960 × 540 pt, 16:9, white `#FFFFFF` |
| Primary accent | Blue `#245BFF` |
| Narrative text | Dark navy `#182B4D` |
| Secondary text | Slate `#64748B` |
| Divider rules | Pale blue `#DCE5F1`, approximately 0.87 pt thick |
| Takeaway background | Very pale blue `#F3F6FD`, rounded rectangle, no outline/shadow |
| Font family | Arial; verify CJK fallback glyphs when using Chinese |
| Title | 30 pt, bold, blue |
| Subtitle | 16 pt, regular, slate |
| Numbered finding headings | 17 pt, bold, blue |
| Finding bodies | 14 pt, regular, dark navy; approximately 110% line spacing |
| Takeaway | 15 pt, bold, blue, centered vertically and horizontally |
| Visual caption / status label | 11 pt, regular, slate |
| Optional demo link | 12 pt, bold, blue |
| Source line | 9.5 pt, regular, slate |
| Footer label / page number | 10 pt, regular, slate |

Use the explicit slide-local RGB values. The inherited master has a different
theme palette, so applying its generic accent color would change this style.
Keep the white background, light rules, and restrained text hierarchy; avoid
adding a grid of decorative cards or a dark slide background.

## Geometry

Coordinates are in points from the upper-left corner of the 960 × 540 pt canvas.
For PowerPoint inches, divide by 72. If the canvas changes, scale the geometry
and type consistently rather than keeping the same point sizes on a smaller page.

| Element | x | y | Width | Height |
| --- | ---: | ---: | ---: | ---: |
| Title | 39.6 | 27.36 | 879.85 | 50.41 |
| Subtitle | 41.04 | 82.08 | 871.20 | 34.56 |
| Header rule | 41.04 | 105 | 876.97 | 0.87 |
| Left visual frame | 42 | 117 | 490 | 300.75 |
| Visual caption | 42 | 420 | 490 | 20 |
| Right heading rows | 551 | 115 / 194 / 273 / 352 | 367 | 27 |
| Right body rows | 551 | 143 / 222 / 301 / 380 | 367 | 48 |
| Optional demo / status labels | 42 / 551 | 433 | Fit the corresponding column | One line |
| Takeaway strip | 42 | 453 | 876 | 30 |
| Source line | 41.76 | 485.28 | 838.80 | 14.41 |
| Footer rule | 41.04 | 505.44 | 876.97 | 0.87 |
| Footer label | 41.04 | 514.08 | 540 | 15.85 |
| Optional brand slot | 803.52 | 511.20 | 81.36 | 18.25 |
| Page number | 896.4 | 513.36 | 21.59 | 15.85 |

Keep the subtitle to one visible line above the header rule. Aim for two short
lines per finding body. Shorten text that exceeds these slots, or reduce the
number of findings and redistribute the rows. Do not force four weak findings.
The source's demo/status text boxes have oversized bounds extending off-canvas;
preserve their visible position and style, but bound them to the one-line slot
when reconstructing. Keep the caption and optional link from colliding.

## Adapt the two pages

- **Business:** put a user-need/benefit mapping, customer workflow, or annotated
  product screenshot in the left frame. Prioritize supported improvement numbers
  in the right-hand findings, with the task, baseline and evidence status nearby.
  Numbers can use larger blue type or native comparison bars within that column;
  reduce the finding count to keep explanations at 14 pt. Keep the reason to try
  or return visible in the takeaway or a remaining finding. Label growth hypotheses.
- **Technical:** use the same left frame for an editable architecture or execution
  diagram. Use the right-hand findings to explain mechanisms and constraints.
  The takeaway connects the mechanism to the business-page benefit and limitation.
- Use a short `Product | takeaway` title and a one-line positioning or scope
  subtitle. Keep the slide language consistent with the request.
- Retain compact source references with full evidence in notes. Refresh the date,
  page numbers, links, status, and evidence qualifications for the actual product.

## Exemplar object mapping

When duplicating the native exemplar, edit its existing text frames and shapes.
Its composition is slide-local; creating from layout `p30` alone will not preserve
it. For a local `.pptx` reconstruction, reproduce those regions as native objects.

| Source element | Destination action |
| --- | --- |
| White background, divider rules, takeaway shape | Keep the visual structure |
| Title, subtitle, four finding pairs, takeaway text | Replace with the new product's supported findings |
| Claude Science screenshot | Replace with the current product visual, a user-benefit flow, or an editable technical diagram |
| Caption and demo link | Replace with matching provenance/link, or remove when unused |
| Beta/tier label | Replace with verified current status, or remove when irrelevant |
| Source line and hyperlinks | Replace with the actual supporting sources and dates |
| Footer breadcrumb | Replace with the current product and business/technical view |
| Footer logo | Use destination branding when requested; otherwise omit the logo |
| Page number | Replace with the final slide's number |

Fit screenshots and source figures proportionally inside the visual frame;
do not stretch them or crop away meaning-bearing labels. Treat the source deck
as read-only and work on a copy if using native duplication. Never flatten an
entire reference slide into the background of the delivered PowerPoint.
