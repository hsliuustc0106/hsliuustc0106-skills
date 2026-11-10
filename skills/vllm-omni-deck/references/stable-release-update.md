# Stable-release deck updates

Use this workflow to update an established vLLM-Omni release deck. Treat the
task as evidence triage and a controlled deck migration before authoring slides.

## Establish the release boundary

Record the previous and current stable tags, target commit, release cutoff date,
baseline deck, audience, slide budget, and sections that must remain unchanged.
Use stable slide keys and semantic roles in the release brief; page numbers may
change during editing.

Treat unchanged introduction, mission, community, and closing material as
locked unless the user explicitly requests a refresh. Approve only the release
delta and its slide-change map.

## Collect evidence in priority order

1. Exact stable tag and official release notes.
2. Commits and merged pull requests included between the two stable tags.
3. Tagged documentation, examples, recipes, tests, and support tables.
4. Official project blogs, papers, and model cards for explanation and figures.
5. Post-tag or open pull requests and issues as roadmap context only.
6. User-provided decks or attachments, cross-checked against tagged sources.

An issue or discussion alone does not prove that a feature shipped. Preserve the
model, hardware, software version, workload, metric definition, units, baseline,
and test conditions for every quantitative claim. Treat old quantitative
evidence as stale until it is revalidated for the target release.

## Audit the previous deck

Classify every prior claim, metric, model logo, source figure, version string,
and citation as `preserve`, `update`, `remove`, or `add`. Remove unverified
carry-over evidence instead of silently retaining it. Label historical,
experimental, post-tag, reconstructed, and roadmap evidence on-slide.

Keep a persistent instruction ledger in the release brief. Record requested
exemplar slides, placements, two-slide splits, locked slides, links, figures,
and wording constraints so that later edits cannot erase earlier approvals.

## Select release highlights

Cluster changes by user outcome rather than by pull request. Useful clusters
include new capabilities or models, realtime interaction, performance and
scaling, runtime or platform breadth, deployment and reliability, adoption, and
roadmap or community work.

Apply these hard gates before ranking a shipped highlight:

- it is present in the target tag;
- it has tag-pinned first-party evidence; and
- every quantitative claim has complete benchmark context.

Then rank clusters by user impact, breadth, architectural novelty, evidence
quality, operational importance, and presentation value. Select a balanced
three to five main highlights when the evidence supports them. Put
implementation depth in the appendix and record why excluded candidates were
omitted.

Follow `problem -> mechanism -> evidence -> adoption implication`. When both the
mechanism and extensive results matter, budget two slides: one for why and how,
and one for results, conditions, and caveats.

## Define the slide and layout contract

Create a task-local `release-brief.json` from the fields enforced by
`scripts/validate_release_brief.py`. For each slide to add or update, record:

- a stable slide key and semantic role;
- the approved exemplar slide;
- title and subtitle line budgets;
- protected footer behavior and source placement;
- placement notes for body, figure, card, and connector zones; and
- the highlight or instruction that authorizes the change.

For every source used to prove shipment, record
`included_in_target_tag: true` only after verifying it against the target tag.
This explicit audit result is required in addition to a source URL or commit.

Reuse geometry from the approved deck before selecting a generic blank layout.
Do not place body content until the title and subtitle have their final rendered
line counts. Follow `layout-qa.md` for text flow, connector gutters, footer
clearance, target rendering, and whole-deck inspection.

## Preserve source assets

Search for figures in this order: current deck, target-tag repository and docs,
official project blog or pull-request assets, official model card, then user
attachments. Keep the canonical asset URL, source revision, hash, dimensions or
aspect ratio, and usage basis in the release brief.

Keep SVG as the canonical source. If the target editor cannot ingest it, create
a faithful high-resolution proportional render, retain both hashes and aspect
ratios, insert it uncropped, and link to the canonical SVG. Never use an
expiring blob URL or redraw a source figure as a workaround.

## Validate before authoring

Run:

```bash
python scripts/validate_release_brief.py /path/to/release-brief.json
```

Resolve every error before authoring. Review warnings before blueprint approval.
After authoring, validate the declared slide scope, run structural checks, render
the complete deck with the target platform, build contact sheets, inspect every
changed or dense slide at full resolution, repair failures, and rerender the
complete deck. A zero-result structural checker is not completion evidence.

Use the v0.26.0 decisions as a regression scenario: preserve the general
introduction; remove stale Qwen3-TTS and Wan scaling evidence; distinguish
tagged highlights from MiniMax-H3 roadmap work; split DLO mechanism and results;
and keep the detailed Qwen3-Omni performance stack in the appendix.
