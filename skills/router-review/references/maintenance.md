# Personal daily selection and bounded Router audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and dated source-inspection results;
it does not authorize upstream reviews, labels, merges, or code changes.

## Selection contract

Require the exact label `high priority`. If the complete current label catalog
contains `ready`, require both; otherwise require `high priority` alone. Unknown
catalogs and API/pagination failures block selection. Do not substitute the
created-last-seven-days or ever-reviewed exclusions.
Old, previously reviewed, own, or draft PRs may qualify when the requested labels
and new-head criteria are met. Direct user-selected reviews bypass this queue.

Run `python3 scripts/select_daily.py < verified-snapshot.json` from this skill
directory. It never fetches, posts, executes target code, or updates checkpoints.
The collector supplies:

- Repository `vllm-project/router`, the Asia/Shanghai calendar `day`, complete
  `label_pages` (arrays of exact names), complete `pr_pages`, and affirmative
  `labels_complete`, `prs_complete`, `checkpoint_complete`, `baseline_confirmed`
- PR `number`, full `head` SHA, `state`, exact `labels`, `new_commits_verified`,
  and a final `current` observation of head/state/labels
- Confirmed `delivered` records with repository, number, full head, policy, day

Flags describe verified evidence, not assumptions. Empty pages are different
from unavailable pages. Conflicting duplicate observations invalidate the whole
snapshot; changed final head/state/labels block that PR. Label order is immaterial.
An unknown or malformed result has nonempty `blocked` and CLI exit status 2;
verified results, including no eligible candidates, exit 0. Inspect both output
and status; a blocked run must not be recorded as a successful empty review.

New commit evidence must compare the current head with the last completed review,
including ancestry or commit-set analysis after history rewrites. Comment times,
creation dates, a changed label, or a new policy version do not prove new code.
The first run requires an explicit baseline or first-run authorization. Missing
checkpoint history is unknown. See `tests/test_router_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. Serialize concurrent selection and
delivery or reconcile reservations against the same ledger; this snapshot adapter
does not enforce a cross-process cap. No delivery ledger belongs here.

## Sources and overlap, inspected 2026-10-07 Asia/Shanghai

- Personal main baseline: `563a25235f295eb10f52783ff7eadb4aa32cccef`
- Router main: [10340964bd8c64a25fcd36458c43edf924dfe2e0](https://github.com/vllm-project/router/commit/10340964bd8c64a25fcd36458c43edf924dfe2e0)
- The releases API returned an empty collection. The latest version tag is
  [v0.1.15](https://github.com/vllm-project/router/tree/v0.1.15), resolving to
  `1fbcde7443d75b36befb61bc081f64c2a1f13a4b`; main is 42 commits ahead.
  A version tag is not evidence of a published GitHub release or runtime validation
- The canonical skill is still proposed in [PR336](https://github.com/vllm-project/router/pull/336),
  open and draft at `3fa8e31e8eed24c10ee39cce842dbdeb7a5e8f09`.
  Its sole parent is the current main pin above, so there are no newer main
  changes since its architecture snapshot. Main does not contain the skill.
  Load this explicit draft revision until merged; never attribute it to main.
  SKILL Git blob: `75e7b940c1eb0eabddc588259b659a87117cd340`;
  exact-byte SHA-256: `ca3b87f02ff52c6548aeca0c7e6f3d1082a12a4670bb8e271c5f3f531ceb7b0f`
- There was no prior complete Router audit ledger in this personal skill.
  This starts a bounded source record, not a claim that all 42 commits or the
  runtime have been audited. The repository-owned skill remains canonical
- [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open.
  Their changed-file lists concern Omni review/maintenance and shared discovery.
  This Router-only supplement leaves those files, human edits and PRs untouched

## Bounded freshness and calibration observations

Read actual target metadata, instructions, callers and fixtures before applying
these dated observations. The canonical draft already covers the landed NIXL
push-mode PR187, gRPC PR283, Progress-TTL scheduling PR286, WASM PR251, and CI
split PR282. Do not port Omni model/stage or AFD attention/FFN contracts here.

- [gRPC contract](https://github.com/vllm-project/router/blob/10340964bd8c64a25fcd36458c43edf924dfe2e0/docs/backend/grpc.md)
  distinguishes HTTP transparent proxying from tokenized gRPC requests. The
  current gRPC path explicitly rejects active tool calling, reasoning_effort,
  and multimodal input. Missing parity with these rejected capabilities is not
  automatically an introduced defect. Model cache keys and wire model identity
  are separate; trace the actual frontend lowering and dependency pins
- [Program scheduling](https://github.com/vllm-project/router/blob/10340964bd8c64a25fcd36458c43edf924dfe2e0/docs/program_scheduling.md)
  is enabled explicitly and has per-request opt-in. Default canonical metadata
  and optional `auto` identity inputs differ. Do not demand queue/admission
  behavior for requests that intentionally stay on the native path
- [Tokenizer L0 cache](https://github.com/vllm-project/router/blob/10340964bd8c64a25fcd36458c43edf924dfe2e0/src/tokenizer/cache.rs#L1-L70)
  is an opt-in library wrapper with deterministic/fixed-setting requirements;
  its estimated retained bytes are not process RSS. No production callsite was
  found for that wrapper or the exported `StopSequenceDecoder` in the pinned
  tree. Neither is the per-model cache in `src/backend/preprocess.rs`.
  The gRPC frontend uses external `vllm_tokenizer::IncrementalDecoder`, so the
  historical stop-decoder case below does not establish a gRPC service outage
- [PR271](https://github.com/vllm-project/router/pull/271) preserves repeated
  allowed response headers with append rather than replacement. Its fixed
  case covers repeated Set-Cookie and the existing name filter, not all proxy
  semantics or dynamic Connection-nominated headers
- [PR272](https://github.com/vllm-project/router/pull/272) fixes arbitrary-byte
  UTF-8 suffix slicing in the exported tokenizer library. Follow hidden and
  visible stops, byte-length jail accounting, mismatch release and ASCII
  behavior. Do not infer production reachability merely from a public export
- [Current Buildkite gates](https://github.com/vllm-project/router/blob/10340964bd8c64a25fcd36458c43edf924dfe2e0/.buildkite/pipeline.yml)
  use Rust 1.95.0/bookworm with OpenSSL/pkg-config/protobuf prerequisites;
  WASM unit tests need the example component. Focused pair replay commands are
  `cargo test --lib routers::header_utils::tests` and
  `cargo test --lib tokenizer::stop::tests` (not run in this pass).
  [grpc_vs_http_e2e](https://github.com/vllm-project/router/blob/10340964bd8c64a25fcd36458c43edf924dfe2e0/tests/grpc_vs_http_e2e.rs#L1-L12)
  uses in-process mocks and fake IDs; its name does not establish live model,
  GPU or tokenizer parity. Python CI builds/installs the package first;
  GPU P/D, ROCm MoRI and RDMA lanes remain distinct hardware evidence

## Corpus and limits

[Adjudicated cases](adjudicated-cases.json) contain two purposively selected
historical defect/fix pairs, four outcomes total. Public merged fixes, regression
source, pinned callers and independent source inspection support the labels.
Severity is this corpus's bounded adjudication, not a quoted upstream rating.
Fixed-clean means only that the named defect is absent; neither merged PR is a
current introduced blocker, whole-runtime approval or readiness verdict.

Network-free tests validate exact excerpt hashes, source/routing/severity
contracts and supplementary Python mechanism models tied to the pinned Rust
operations. They do not compile or execute Rust and are not reviewer accuracy,
precision, recall, a blinded evaluation, or four independent samples. Exact full
historical file hashes and excerpt bytes were checked against the Git objects.

This is a partial public-source audit. Cargo and rustc were unavailable; no
upstream Rust/Python suites, live HTTP/gRPC, model inference, GPU/ROCm/RDMA,
performance, scheduler stress or distributed teardown were run. No live daily
queue or delivery ledger was changed. The adapter trusts verified collector
flags; it does not fetch pages, prove ancestry, serialize deliveries or establish
remote freshness. Unknown API results remain blockers, never successful empties.

Validation for this pass: 30 network-free selector tests, five corpus
source/severity/routing/mechanism checks and one Router packaging test passed;
the full personal-repository suite passed 149 tests. An independent 20-test
selector pass included 2,000 seeded randomized snapshots. All 20 skill
entrypoints passed frontmatter validation; scoped local links, JSON manifests,
installation routing for all three supported tools, shell syntax, Python parsing
and diff whitespace were checked. Eight historical source records matched full
Git blob/SHA-256 and excerpt pins. The canonical draft contains no executable
helpers. These checks validate the bounded supplement, not upstream behavior.
