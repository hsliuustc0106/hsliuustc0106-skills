---
name: vllm-omni-deck
description: Create, restyle, or provide blank editable English-first vLLM-Omni PowerPoint decks from papers, blogs, pull requests, approved slide blueprints, or existing slides with a bundled eight-layout example template and a nine-page blank template that includes a minimally structured branded white canvas and a references layout. Use when Codex needs to turn vLLM or vLLM-Omni technical sources into a cited deck, preserve provided source figures intact without structural modification, build a new .pptx, migrate or restyle slides, select layouts, create paper/blog/PR references, or regenerate and validate the vLLM-Omni deck templates.
---

# vLLM-Omni Deck

Create PowerPoint-first vLLM-Omni decks with native, editable objects and a
fixed visual system.

## Load the Design Contract

Read both references before creating or restyling slides:

- `references/design-system.md` defines the canvas, brand tokens, typography,
  footer, and component rules.
- `references/layout-catalog.md` defines layouts 1–9: seven established
  structured layouts, layout 8 as the minimally structured white canvas, and
  layout 9 for references, plus required inputs, selection rules, and safe
  content density.

Treat these files and the template generators as the source of truth:

- Use `assets/vllm-omni-template.pptx` when layout examples and an editable
  demonstration chart or reference list help Codex author the deck.
- Use `assets/vllm-omni-blank-template.pptx` when the user requests a blank
  template or the source already supplies figures that should be placed
  directly. Use its eighth slide as the default for most body slides, especially
  original source figures and custom compositions. Use its ninth slide for
  paper, blog, and pull-request references.

Never modify either asset in place; copy the selected asset to a task-specific
output path.

## Choose the Workflow

- For an ambiguous or net-new narrative, use the sibling
  `../build-slides-interactively/SKILL.md` workflow before drafting slides.
- For an explicitly approved outline and per-slide blueprint, use the sibling
  `../deck-compiler/SKILL.md` to validate a `deck-spec.yaml` and produce the
  ordered manifest before authoring.
- For restyling, preserve approved wording, evidence, citations, and slide order
  unless the user authorizes changes.

Require the user to provide or approve each slide's purpose, key takeaway,
substantive content, and evidence. Start body-slide selection with layout 8.
Switch to layouts 3–7 only when their structure materially improves reading
order, comparison, or comprehension. When two layouts are plausible, recommend
one and explain the tradeoff.

## Preserve Provided Figures Intact

Treat every user-provided or source-provided figure as immutable:

- Insert it as one unedited image. Only move it and scale it proportionally.
- Never crop, split, redraw, trace, rearrange, relabel, recolor, restyle,
  simplify, replace, or overlay any part of it.
- Keep captions and explanatory annotations outside the figure boundary.
- If fit or legibility prevents intact reuse, place it alone on layout 8. If
  permission or resolution blocks reuse, request permission or a better source.
  If the issue remains unresolved, omit the figure and state why. Never
  reconstruct it as a workaround.
- Create a separate explanatory visual only when the user explicitly requests
  one. Do not present that visual as the source figure or as a modified version.

## Build from Papers, Blogs, or Pull Requests

Treat provided links and source documents as evidence, not as an approved slide
plan. Accept a minimal request such as:

```text
Use $vllm-omni-deck with these paper, blog, or PR links: <URLs>.
Audience: <audience>. Goal: <goal>.
```

Then:

1. Read each complete source. If a link is inaccessible, request the article text
   or an export instead of inferring missing content.
2. Create a compact source-and-claim map covering the thesis, supported technical
   claims, evidence, reusable figures, caveats, and source URL. Map each candidate
   figure as reuse intact on layout 8, reuse intact on a dedicated slide, or omit.
3. Preserve the model, hardware, software version, workload, metric definition,
   units, baseline, and test conditions for quantitative claims. Do not use an
   isolated benchmark value.
4. Distinguish source-backed claims from Codex synthesis. Label inferences and
   flag conflicting, outdated, or unsupported claims.
5. Propose a complete deck blueprint within the user's slide limit, or seven
   slides by default. For every slide, provide its title, purpose, key takeaway,
   draft content, recommended layout, evidence and citation, asset needs, and
   open dependencies. Prefer layout 8 for body slides unless a specialized
   layout communicates the approved logic more clearly.
6. Stop for explicit blueprint approval before authoring slides.
7. After approval, build the editable deck. Use 12 pt on-slide citations, label
   fabricated values as `Illustrative data`, and preserve source qualifications.
   Prefer a relevant original source figure when its provenance and usage rights
   are verified. Preserve it intact even when another composition would look
   cleaner.
8. Use layout 9 when the approved blueprint includes a dedicated references
   slide. Keep per-slide citations; the references slide supplements rather than
   replaces them.

## Build or Regenerate the Template

Create a fresh environment before running the generator:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python python-pptx
.venv/bin/python scripts/build_template.py \
  --output assets/vllm-omni-template.pptx
.venv/bin/python scripts/build_blank_template.py \
  --output assets/vllm-omni-blank-template.pptx
```

Run the commands from this skill directory. Each generator refuses to overwrite
an existing file unless `--force` is passed. The example generator validates the
native chart and illustrative labels; the blank generator validates the layout
inventory, placeholders, and source-figure frames.

## Author Slides

1. Confirm the slide blueprint and references.
2. Use layout 8 for most body slides. Choose a specialized catalog layout only
   when its narrative structure adds clarity.
3. Preserve the approved 36/28/18/12 pt Arial hierarchy.
4. Keep narrative text, shapes, diagrams, tables, and charts native and editable.
5. Place each provided figure as one intact image. Permit only proportional
   scaling and positioning. Cite it as `Source`.
6. Use layout 8 or a dedicated slide when intact placement needs more space.
   Request a better source or omit the figure when it remains unusable; never
   rebuild it.
7. Reflow within the chosen layout when content is slightly long.
8. If content still does not fit, recommend shortening it or splitting the slide
   and wait for approval. Never shrink, omit, or split silently.
9. Mark fabricated demonstration values as `Illustrative data` directly on the
   slide. Never present them as measured results.
10. Preserve every source notice and keep all added explanation outside the
    figure boundary.
11. For layout 9, preserve canonical identifiers and links: authors, venue,
    year, DOI or arXiv ID for papers; publisher and publication or update date
    for blogs; repository, PR number, status, merge or close date, and commit
    when relevant for pull requests.

Do not add animations, transitions, decorative gradients, glass effects, or
heavy shadows. Do not rasterize editable narrative content. Optimize for
PowerPoint and keep Google Slides compatibility best-effort.

## Verify Every Output

- Confirm that every delivered slide has one primary message.
- Confirm Arial and the allowed sizes only: 36, 28, 18, and 12 pt.
- Confirm no text is clipped, overlapped, or smaller than 12 pt.
- Confirm the vLLM-Omni logo appears on every slide.
- Confirm page numbers appear on every slide except the cover.
- Confirm blank-template slide 8 retains its template label, editable title,
  source/footer line, logo, and page number while its body remains empty.
- Confirm blank-template slide 9 contains editable paper, blog, and pull-request
  entries with canonical-link placeholders, logo, footer, and page number.
- Confirm layout 8 is normally the most-used body layout in a mixed deck; do not
  impose a quota when the approved content clearly benefits from other layouts.
- Confirm white content slides reserve the source/footer line.
- Keep bracketed placeholders only when delivering the blank template itself.
  Confirm no blank-template placeholders remain in an authored deck.
- Compare every reused figure with its source. Confirm it is one intact image,
  has no crop or overlay, preserves its full aspect ratio and structure, and
  carries `Source` attribution.
- Render the complete deck to PDF with LibreOffice and inspect every slide.
- Treat the generators' count checks as canonical-template validation: eight
  slides for the example template and nine for the blank template. For a
  derived deck, validate against the user's approved slide inventory while
  preserving the same canvas, typography, branding, and editability checks.
- Treat PowerPoint as authoritative; report that Google Slides fidelity is
  best-effort when handing off the file.
