---
name: paper-repo-deepdive
description: Deep-dive into a research paper, a GitHub repository, or both and turn the analysis into exactly one editable PowerPoint slide with cited evidence and speaker notes. Use for requests to understand a method or implementation and explain its mechanism, results, tradeoffs, and practical significance in a single technical slide. Not a general multi-slide deck or pull-request review workflow.
---

# Paper & Repo Deep Dive

Understand the technical contribution before compressing it. Produce a useful
explanation of how it works, what the evidence establishes, and where it applies.

## Inputs and deliverables

Accept a paper URL, DOI, arXiv identifier, local PDF, GitHub URL, local checkout,
or a paper together with its implementation. Either a paper or a repository is
sufficient; do not require both. Ask for a source if none is identifiable.

Use the user's audience, focus, language, and template when supplied. Otherwise,
state a brief assumption: technically literate engineering audience, the user's
language, and the saved blue-and-white reference-slide style. A newly supplied
template overrides this default. Clarify only choices that materially change the
analysis; continue source inspection while optional preferences are pending.

Deliver to a task-specific output directory:

- `one-slide.pptx`: exactly one editable slide, including detailed speaker notes.
- `deep-dive.md`: the reasoning, evidence map, source versions, and limitations.
- `one-slide.png`: a preview rendered from the actual deck, when a renderer is
  available. Disclose when visual verification could not be performed.

The slide count includes hidden slides. Keep references and supporting detail in
notes and the analysis file; do not add cover, appendix, or references slides.
Create the artifacts directly within the user's request. Do not introduce a
multi-stage deck approval process unless the user requests one.

## Establish the sources

Open the primary source; search snippets, abstracts, and README claims are
starting points. Record the paper title, authors, version/date, and canonical
URL when known. For a repository, record its URL, inspected commit SHA, relevant
configuration, and any working-tree modifications that affect the analysis.
Respect a supplied revision; otherwise resolve and record the inspected default
branch revision. Use commit-pinned links for code evidence.

For a paper, read the full main text and inspect its figures, tables, equations,
and captions. Read appendices needed to establish the central claims. Record
unread or inaccessible portions; never imply complete coverage when extraction
or access is partial. Prefer the PDF when text extraction loses mathematical
notation or table structure.

For a repository, start with its README, package/build metadata, documentation,
and tests to identify purpose and supported usage. Select the execution path
that explains its main contribution, then trace that path through actual source.
State the inspected scope rather than implying every file was reviewed.

When paper and code are both available, verify that the repository is actually
associated with the paper and distinguish paper behavior from the inspected
implementation. Follow primary references only when needed to resolve the
mechanism, baseline, or an important claim. Report missing evidence instead of
replacing it with guesses. If the central mechanism cannot be established, ask
for the missing material before presenting a completed deep dive.

## Explain the mechanism

Answer these questions in `deep-dive.md`, choosing detail that serves the source:

1. **Problem and baseline:** What limitation motivates the work? How does the
   relevant conventional approach handle it?
2. **Core change:** What specifically changes, and why should that change solve
   the problem? Distinguish a new idea from implementation or integration work.
3. **Mechanism:** Trace the inputs, transformations, intermediate state, and
   outputs. Explain the important equation, algorithm, component interaction, or
   data structure in plain language. Define the symbols and assumptions that
   carry the argument.
4. **Concrete walkthrough:** Follow one small example through the mechanism.
   Label invented examples as illustrative. Use the example to expose causality
   and invariants; do not turn it into a fabricated benchmark.
5. **Evidence:** What result supports the central claim, and what does it leave
   untested? Consider the relevant comparison, ablation, correctness property,
   or test rather than merely repeating the largest headline number.
6. **Tradeoff and significance:** What is gained, what is paid, when does the
   approach fail or stop helping, and who could use it?

For paper inputs, connect equations and figures to the explanation. Assess the
baseline, evaluation setup, ablations, and stated limitations; identify your own
interpretations separately. Do not equate an author's novelty claim with a
verified literature-wide result.

For repository inputs, follow a concrete entry point through the core algorithm
or orchestration to its outputs. Cite the relevant symbols and code locations.
Inspect tests and configuration for the claimed behavior, including a material
boundary case. A defined helper is not proof that the main path calls it; a test
file is not proof its tests passed. Note material differences between README
claims and the inspected code. Static inspection is the default; running source
code, benchmarks, or GPU workloads requires the task's execution authorization.

## Keep a compact evidence map

Use source IDs such as `[P1]` for papers and `[R1]` for repositories, with precise
locators: section, equation, figure, table, or commit-pinned file and lines.
The analysis should include a small table:

| Claim | Evidence and locator | Status | Qualification |
| --- | --- | --- | --- |
| The claim being assessed | Primary source or code permalink | Reported / observed in code / inferred / reproduced | Scope, conditions, or uncertainty |

Use `reproduced` only for an actual recorded run. For quantitative results retain
the metric, units, direction, baseline, workload/data, hardware, and relevant
configuration. Preserve qualifiers such as "up to" and distinguish peak from
average results. Mark absent conditions as unreported. Do not compare numbers
across incompatible setups or treat implementation structure as a measured
speedup. Preserve conflicting results and their contexts.

Keep the report concise but sufficient to reconstruct the main argument. Include
source coverage, the mechanism walkthrough, the strongest evidence, the key
limitation, and unresolved questions. Save sources or excerpts only as needed;
do not automatically ingest them into a separate knowledge base.

## Distill and build the slide

Read [references/template-style.md](references/template-style.md) and inspect
its linked reference image for the default visual style selected by the user.
Use the large left visual, four numbered right-side sections, blue headings,
and bottom takeaway bar. Read [references/one-slide.md](references/one-slide.md)
for PowerPoint construction and verification.

Choose one central takeaway and the minimum evidence needed to support it.
A good slide answers: **what problem, what changes, how it works, what supports
it, and what limits it**. Give the mechanism most of the visual space. Adapt the
composition to the source: an algorithm/dataflow diagram, architecture, relevant
source figure, or a compact before/after comparison can each be appropriate.

Write speaker notes that explain the mechanism in more depth than the slide,
include the example and caveats, and give full source URLs and evidence locators.
Include critical qualifiers visibly on the slide; notes must not repair a
misleading headline. Use the evidence map to audit every substantive slide claim.

## Verify and hand off

Reopen the saved `.pptx` and verify one slide, editable narrative text and
explanatory objects, speaker notes, and working citation targets. Render and
inspect it when possible. Fix clipping, overlap, unreadable labels, missing
qualifiers, and misleading visual relationships before delivery.

Link the PowerPoint, analysis, and available preview. Briefly state the central
insight and any material access or verification limitation. Never substitute an
outline, screenshot, or PDF for the requested `.pptx` without clearly reporting
that the PowerPoint deliverable remains incomplete.
