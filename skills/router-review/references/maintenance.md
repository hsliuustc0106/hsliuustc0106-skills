# Personal daily selection and bounded Router audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and dated source-inspection results;
it does not authorize upstream reviews, labels, merges, or code changes.

## Freshness update, inspected 2026-10-14 Asia/Shanghai

This bounded update supersedes the historical release and L0 reachability
statements below; it does not replace the repository-owned checklist.

- Personal main inspected: `836a88e8e75d02292e996b817116d1b5f4c0a6ad`.
  Router main inspected: [442b8bb74fba09052428cf3af0513916a4f92b43](https://github.com/vllm-project/router/commit/442b8bb74fba09052428cf3af0513916a4f92b43),
  20 commits after the previous `10340964` snapshot. Commit metadata and the
  complete changed-file inventory were checked; this is not a full audit of
  those 20 commits. Main has no AGENTS.md or canonical review skill yet.
- [PR336](https://github.com/vllm-project/router/pull/336) remains open/draft at
  `3fa8e31e8eed24c10ee39cce842dbdeb7a5e8f09`; its actual skill bytes retain the
  Git blob and SHA-256 recorded below. It predates these 20 main commits.
  Read current implementation and this dated delta rather than treating that
  draft's architecture map as a complete description of current main.
- [v0.1.16](https://github.com/vllm-project/router/releases/tag/v0.1.16) was
  published on 2026-10-09 at 07:14 UTC, resolving through its annotated tag to
  `db02f358da401b60d4ae14eb286163763a0705cc`. Main is ten commits ahead.
  The release includes the initial multi-tier KV index and the L0 library,
  but not the subsequent gRPC L0 integration, EPD prototype, or KV segment
  contract below. Release notes describe Docker `v0.1.16.1` as a smoke-test
  CI correction with unchanged router code; registry artifacts were not tested.
- Open personal PR6 and PR17 retain the heads recorded below. Their full
  changed-file lists do not touch this supplement. The other open personal PRs
  were enumerated; no Router-specific competing skill update was identified.
  No shared routing, installer, human edits or open PRs were changed.

### Main-only contract deltas

- [gRPC L0 integration](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/src/backend/encode_cache.rs)
  is now reachable through `EngineFrontend`, model loading and chat encoding
  ([PR340](https://github.com/vllm-project/router/pull/340)). It remains off by
  default; `VLLM_ROUTER_L0_CACHE` enables it. Distinguish the per-model loaded
  frontend cache from the shared encoding cache. Exact keys include tokenizer
  instance, rendered text, special-token option and cache salt. Token IDs bypass
  encoding; unknown or stochastic tokenizer configurations bypass caching.
  Only successful encodings are retained. Rendering/validation still occur for
  each request, retries reuse prepared requests, and estimated bytes are not RSS.
  Review source and [fixture-backed parity tests](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/tests/grpc_frontend_l0.rs)
  together; they are not live-model performance or production qualification.
- [Experimental EPD](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/docs/epd.md)
  adds native Rust CLI JSON-metadata orchestration for static HTTP E+PD or E/P/D,
  DP=1, without IGW or Python-launcher configuration. Embeddings move through
  engine EC connectors; the router handles metadata and transfer handles, not
  tensors. Verify selected P/PD destination, media order, independent transfer
  IDs for repeated media, raw-media fallback and EC cleanup. Encoder failures
  must not forward partially prepared requests. There is no automatic EPD
  replay; abandoned Mooncake pushes use best-effort cancellation, with backend
  expiry as fallback. After successful consumer response headers, completion
  cleanup belongs to the consumer. Image evidence does not prove audio/video
  coverage. See [implementation and regression source](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/src/routers/http/epd.rs).
- KV indexing landed in the release, but main subsequently fixes partial-edge
  traversal ([PR366](https://github.com/vllm-project/router/pull/366)) and shared
  path hash aliases ([PR357](https://github.com/vllm-project/router/pull/357)).
  [PR370](https://github.com/vllm-project/router/pull/370) replaces scalar tier
  depth with maximal half-open held-block segments, retaining tails after gaps.
  Read the [current match type and aggregation](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/src/kv_index/indexer.rs#L22-L38),
  owner identity, holes and prefix-contiguity tests before policy/cost reasoning.
  An index/API change does not establish an enabled end-to-end KV-aware policy.
- Current [contribution instructions](https://github.com/vllm-project/router/blob/442b8bb74fba09052428cf3af0513916a4f92b43/CONTRIBUTING.md)
  require human contributor intent and evidence before contributor implementation
  or PR submission. They explicitly do not alter independent-review eligibility;
  retain the configured daily label/new-head policy below.

### Validation and limits of this update

The two historical defect families/four bounded outcomes below are retained;
no new accuracy sample or runtime verdict is claimed. Existing offline selector,
corpus, grounding, severity, routing and installation checks remain applicable.
The canonical skill has no linked reference bundle or executable helper to run.
Cargo/rustc are unavailable here, so Rust suites, live serving, tokenizer/model
parity, GPU/ROCm/RDMA, EPD backend cleanup and performance were not executed.
Focused commands for a capable isolated environment include:

- `cargo test --test grpc_frontend_l0`
- `cargo test --lib backend::encode_cache`
- `cargo test --lib routers::http::epd::tests`
- `cargo test --test test_pd_routing test_epd_handoff`
- `cargo test --test kv_index_prefix_contiguity`
- `cargo test --test kv_index_sequence_lifecycle`

These are suggested checks, not reported passes. Re-resolve source revisions on the next
review; this update does not advance a live PR-review or delivery checkpoint.

The personal-repository unittest suite passed 224 network-free tests. All 22
skill entrypoints passed frontmatter checks; scoped local links, JSON manifests,
Python parsing, shell syntax and diff whitespace passed. The suite exercises
Router installation/routing for Codex, Claude and Cursor in temporary folders,
including repeat installs and preservation of human edits. Eight historical
source records were re-fetched and matched their full Git blob/SHA-256 and
excerpt pins. The canonical draft bytes matched their recorded identities.
An independent source-inspection pass checked release/main separation, L0
reachability and KV-index evolution; neither pass executed upstream Rust.

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

## Historical sources and overlap, inspected 2026-10-07 Asia/Shanghai

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

## Historical bounded observations (2026-10-07)

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
