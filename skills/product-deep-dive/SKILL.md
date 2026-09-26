---
name: product-deep-dive
description: Research a new or unfamiliar product and distill it into an editable PowerPoint with two substantive slides, one business and one technical. Use for concise product deep dives, product teardowns, and business-plus-technology briefings grounded in current sources. Respect an explicitly requested single-slide format. Not a general pitch-deck or long market-report workflow.
---

# Product Deep Dive

Research broadly enough to explain the product; select narrowly enough for the
audience to understand it in two slides. Connect customer value to the mechanisms
that enable it and the constraints that limit it.

## Establish the brief

- Identify the exact product, vendor, relevant version or tier, and research date.
  Ask for a name or URL if the product is missing or ambiguous.
- Use the requested audience, decision, language, and template. When unspecified,
  state the default: a briefing for product and engineering colleagues, in the
  language of the request, using the linked product-deep-dive reference style
  documented in [references/template-style.md](references/template-style.md).
  A template specified for the current task overrides this saved default.
- Default to exactly two content slides: **business** followed by **technical**.
  Do not consume the page budget with a cover, agenda, or reference slide. If the
  user explicitly requests one slide, combine the two views and reduce detail.
- Proceed from the available brief; ask only about gaps that materially change
  the research. An explanation need not become a buy/build recommendation unless
  the user asks for that decision.

## Build an evidence base

Read supplied materials and follow their relevant references. Unless the user
limits research to supplied sources, verify current facts on the web. Open and
read the underlying pages; search snippets are discovery aids, not evidence.

Start with official product documentation, release notes, pricing, demos, and
technical papers or repositories. For market claims, look for attributable
customer evidence and independent reporting. Technical claims should trace to
primary documentation, code, papers, or reproducible measurements. A vendor page
establishes what the vendor claims; it does not independently prove effectiveness.

Keep a compact evidence ledger in the working notes:

| Claim | Evidence status | Source and locator | Date/version | Scope or caveat | Slide |
| --- | --- | --- | --- | --- | --- |
| One checkable assertion | Documented / vendor-reported / independently measured / inferred / unknown | URL plus section, page, or code location | Publication/update and retrieval dates when known | Tier, workload, region, or uncertainty | Business / technical / notes |

Research these questions, then select what materially explains this product:

- **Business:** Who uses it and who pays? What painful task and existing workflow
  does it change? Why choose it over the status quo or closest alternatives? How
  is it priced and distributed? What evidence supports adoption, outcomes, and
  any claimed defensibility? What could prevent purchase or sustained use?
- **Technical:** What happens from input to useful output in one representative
  task? What components, interfaces, dependencies, and data flows are documented?
  Which design choices explain the value or differentiation? What are the main
  performance, reliability, deployment, integration, or data-handling limits?

Keep these distinctions explicit:

- Shipped features, restricted previews, and roadmap promises are different.
- Price needs its currency, billing unit, tier, region when relevant, and date.
  Funding, registered users, active users, and revenue are different measures.
- Benchmark claims need attribution and their workload, baseline, and conditions.
  Do not compute comparisons from incompatible measurements.
- A differentiator needs a named alternative and a shared comparison dimension.
  The current manual workflow may be the most relevant alternative. Omit arbitrary
  scores, unsupported market sizes, and invented customer counts or unit economics.
- Separate an original technical contribution from integration or packaging of
  existing technology. Neither automatically establishes a business moat.
- Public behavior does not reveal private internals. If internals are undocumented,
  show a sourced capability/data-flow view and label the unknowns. Mark any
  inference on the diagram or claim itself, not only in hidden notes.

Resolve contradictions that would change the main takeaway. Otherwise retain the
dated disagreement or unknown. Stop expanding research when both slide theses
and their decisive claims are supported, or a focused follow-up cannot resolve
the remaining gap. Report inaccessible sources and their effect on the conclusion.

## Synthesize the two views

Use [references/slide-blueprints.md](references/slide-blueprints.md) when drafting
the slide content and layout. It contains the business and technical blueprints
and the single-slide adaptation. Read
[references/template-style.md](references/template-style.md) for the default
layout, measured typography, colors, and source slide. Both pages use that visual
family, with a product visual on the business page and a mechanism diagram on the
technical page.

Write a one-sentence takeaway for each slide before laying it out. Use the same
representative use case on both pages. Tie at least one business differentiator
to a documented technical mechanism and its tradeoff, or explicitly state that
the mechanism is undisclosed. Avoid repeating the feature list on both pages.

Select a few decisive findings. Keep the main limitation visible beside the
benefit it qualifies. Put research depth and secondary evidence in speaker notes
or the evidence ledger; do not make the audience read a miniature report.

## Produce the PowerPoint

- Create an actual `.pptx` unless the user requests content or an outline only.
  Use the available presentation tools and inspect their supported operations.
  In Codex desktop, use `load_workspace_dependencies` when available to locate
  the bundled presentation runtime. Otherwise reuse an available local authoring
  library and renderer, such as PptxGenJS or python-pptx plus LibreOffice. Check
  the actual environment before choosing a toolchain.
- Keep authored text, tables, charts, and explanatory diagrams editable with
  native objects. Use screenshots or source figures only when they explain the
  product better; retain attribution and meaning. Do not flatten whole slides.
- Follow the current task's template, or the saved reference style when none is
  specified. For the saved reference, preserve the large left visual, numbered
  findings on the right, blue headline hierarchy, and bottom takeaway/source
  bands. Use the blueprint's density guidance; shorten or reflow content rather
  than shrinking it to fit.
  Replace the exemplar's product content, links, and media with relevant evidence.
- Add visible source markers beside factual claims and short, linked references
  in each slide's footer. Record full URLs, locators, dates, qualifications, and
  evidence status in speaker notes or a companion `<product>-sources.md`.
  Keep caveats that change the meaning of a claim on the slide itself.

## Verify and deliver

1. Reopen the saved file and confirm the requested slide count, editable content,
   working citation targets, and absence of template placeholders.
2. Render every slide and inspect the images at presentation size. Check clipping,
   text wrapping, contrast, crowded labels, overlaps, and diagram reading order.
   Fix problems and rerender affected slides. A structural check alone cannot
   establish legibility; disclose when rendering or target-app checks cannot run.
3. Check the two pages together: same product/version/date, consistent terms and
   numbers, business claims supported by the technical view, and visible material
   uncertainty. Distinguish a verified feature from a verified outcome.
4. Deliver the `.pptx`, slide previews when available, and the evidence ledger
   when stored separately. Summarize the main finding and any consequential gap.
   If file generation is blocked, deliver the completed content and evidence and
   state the concrete blocker; do not call an outline a finished PowerPoint.
