# Evaluation contract and limits

## Baseline and reproducible checks

Before this bootstrap, the skills repository at `db83ff0a9c4c97ae512b1aa1b0447405dc79070a`
had no `nanodot-review` skill or nanodot batch selector. Its 21 existing helper and
NCU packaging tests passed. The Omni review structure was a starting point, not
an adjudicated nanodot quality baseline; no before/after model-performance claim
is supported.

Run from the skills repository with Python 3.8+, Bash and jq (the existing Omni
suite needs jq):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

- `tests/test_nanodot_selection.py`: complete pagination, catalog errors/unknowns,
  label conjunction, old PR/new head, unchanged head across policies, daily cap and
  timezone rollover, deduplication, read-only ledger, and stale-head rejection
- `tests/test_nanodot_review.py`: routing seams, explicit grounding/severity fields,
  diff coordinates, frontmatter, links, UI metadata, plugin discovery and isolated
  Codex/Claude/Cursor installation
- `tests/test_nanodot_corpus.py`: pinned source hashes and executable narrow
  historical defect/clean controls, using local excerpts and minimal test doubles

The corpus lives in `tests/fixtures/nanodot-review/`. `inputs.json` pins source
SHAs, exact file/line URLs and SHA256 for every excerpt. `adjudication.json` records
expected scoped outcomes and exact upstream regression-test sources. Fixtures are
data, not install-time code; they are not copied into a user's project.

## Pinned corpus

Four integration-only families each have a defective snapshot and a narrow clean
control, for eight samples total:

| Family | Defect sample / control | Historical change |
| --- | --- | --- |
| Hidden/empty required catalog suppresses observed failure | n05 / n01 | c1e03de → a8c704e |
| Optional failure while required checks pending | n04 / n08 | a8c704e → 661f4ba |
| Crash replay with changed evidence duplicates notification | n07 / n03 | c1e03de → a8c704e |
| Stop between queued tasks, daemon and once call sites | n02 / n06 | c1e03de → a8c704e |

Full commits: [c1e03de](https://github.com/ThinkFlowLab/nanodot/commit/c1e03dedd42e78b86229f8aeb1daf6ebc9020e05),
[a8c704e](https://github.com/ThinkFlowLab/nanodot/commit/a8c704e2b6390e14c7ff5eae810ec8d210faa2d9),
[661f4ba](https://github.com/ThinkFlowLab/nanodot/commit/661f4bae106e9f9718137812a803020b8954acc8).

A source-review pass using the skill and inputs (without the adjudication file)
identified all four expected P2 defects and none in the four scoped clean controls;
all eight had source anchors and no unknown result. This is a tiny, curated,
unblinded regression exercise: guidance itself names historical corrections.
It demonstrates recognition of those patterns, not general precision/recall or
an unbiased estimate of review quality. Clean labels do not certify whole files.

The executable tests reproduce the historical evaluator, replay-key and scheduler
behaviors with doubles. CLI `--once` stop forwarding is checked structurally at
its call site; a real CLI process is not executed by this corpus. Source-hash checks
prove fixture consistency, not independent truth of the adjudication. Severity
schema validation accepts P0–P3; a human still evaluates actual impact.

## Coverage not established

No live GitHub PR review or comment, upstream mutation, personal-machine install,
full nanodot runtime suite, OS notification test, live credential/provider call,
GPU/model run, performance benchmark, or generalized review-quality evaluation
is part of these offline skill checks. Broader permission, memory, HTTP, runner
ownership and egress guidance is source-grounded but not measured by this corpus.

Refresh cases when contracts change. Add both a defect and a neighboring clean
control; verify public source pins, preserve separate expected answers, and record
sample count and remaining gaps. Do not raise a quality claim merely because more
assertions or checklist wording were added.
