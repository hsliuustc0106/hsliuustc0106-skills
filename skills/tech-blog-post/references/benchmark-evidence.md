# Blog, slides, and benchmark evidence

Use when a technical article draws on both a blog and a slide deck, or compares
optimization results. This evidence work precedes the narrative blueprint.

## Source reconciliation

- Pin each source: public URL and retrieval date; repository commit/tag and
  file/line or PR revision; deck filename/version and slide number. For supplied
  files, retain a checksum or stable file version. Keep private source locations
  in the private working evidence, never in a public artifact or repository.
- Extract blog prose and tables plus slide text, speaker notes when relevant,
  tables, diagrams, footnotes, and embedded figures. Render and visually inspect
  the relevant slides: text extraction alone misses axis labels, legends,
  hardware qualifiers, and image-only results. Report unreadable or missing
  evidence instead of filling gaps from memory.
- Build a compact claim ledger with claim ID, proposed wording, source locator,
  exact value/unit, conditions, evidence type, caveat, and destination section
  or figure. Reconcile discrepancies before drafting; do not silently select
  the larger gain or merge two experiments.
- Public availability is not permission to copy. Check authorship, license,
  attribution, and permission for reused text/assets. Prefer original diagrams
  and short attributed descriptions when reuse rights are unclear. Redrawing a
  chart does not remove its data attribution or license obligations.

## Keep comparison boundaries visible

For every performance claim, record the hardware model, GPU count, architecture,
software version/commit, model, precision, batch/concurrency, input/output sizes,
resolution, steps, attention backend, parallelism, warmup, measurement scope,
metric/unit, and baseline as relevant. Unknown fields remain unknown.

- Different hardware or software versions are separate experiments, not a
  controlled before/after comparison. For example, a B300 result on v0.28.0 must
  not be relabeled as an 8× RTX PRO 6000 (SM120) result on v0.30.0. These are
  examples of environment labels, not bundled benchmark evidence.
- Separate kernel microbenchmarks, stage latency, throughput, and end-to-end
  latency. A 2× attention-kernel speedup is not a 2× application speedup.
- Distinguish exact attention from approximate/sparse attention and changes in
  sampling steps, resolution, caching, or quality settings. Do not imply equal
  quality or invent an accuracy score without a specified evaluation and data.
- Record released, merged-but-unreleased, open-PR, and experimental states at a
  pinned revision/date. A user-provided runtime version does not prove every
  optimization shipped in that release. Verify release ancestry or label the
  feature status unresolved; do not move PR results into a released-feature list.
- State the denominator: latency speedup is baseline time / candidate time;
  latency reduction is (baseline − candidate) / baseline. Keep units consistent.
  Independently measured gains are not additive or multiplicative unless the
  combined configuration was actually measured with the same baseline.
- Distinguish measured values from calculations, estimates, author statements,
  and inference. Preserve precision supported by the source. Carry limitations
  next to the claim and into charts, captions, summaries, and cover text.

## Before handoff

Trace every quantitative claim (including headlines and figure labels) back to
its ledger row. Check arithmetic, units, direction of improvement, denominators,
and conditions. Keep a section/claim/figure coverage map when adapting or
splitting a full article so a shorter derivative cannot silently lose caveats.
