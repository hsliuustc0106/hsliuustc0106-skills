# Personal daily selection and bounded Router audit

The repository-owned review skill remains canonical. This supplement covers the
explicitly configured personal daily queue and dated source-inspection results;
it does not authorize upstream reviews, labels, merges, or code changes.

## Current bounded refresh, 2026-10-28 Asia/Shanghai

This refresh supersedes dated reachability, reservation and test-command facts
below, not the canonical repository-owned review checklist. The
[source manifest](audit-2026-10-28.json) pins 23 current-main files and the
separate draft skill by Git blob, SHA-256 and byte length.

- Personal main baseline: `0185aac674208a993a0c5d003c16f33792c4cefe`.
  Router main: [a774cdda09237da16e33e67f725998ff4db920a3](https://github.com/vllm-project/router/commit/a774cdda09237da16e33e67f725998ff4db920a3).
  The complete delta inventory since the prior audit pin is 19 commits and 262
  changed paths; the same-day tip moved one commit after the morning pin
  (`9e58176e`), touching only `docs/cli_reference.md` and
  `scripts/check_cli_reference.py`. Source inspection is targeted, not a
  semantic audit of every changed line.
- Latest published release remains [v0.1.16](https://github.com/vllm-project/router/releases/tag/v0.1.16)
  at `db02f358da401b60d4ae14eb286163763a0705cc`; main is 40 commits ahead.
  The contracts below are main-only, not a released-artifact qualification.
- Main still has no AGENTS.md or canonical review skill. PR336 remains
  open/draft at `3fa8e31e8eed24c10ee39cce842dbdeb7a5e8f09`; use that explicit
  source and revalidate its dated architecture/test map against the target.
- All 13 open personal PRs were enumerated, followed by an empty page. PR6
  and PR17 retain their previously recorded heads
  (`68d7b38df04c382e9e51c9fde28428181d3bc5a8`,
  `f01a5df38f337e65d80f420e6b22e0b30a5237af`); their complete file lists do not
  overlap these Router-only files. No proposal or human edit is replaced.
- The High Priority label catalog entry exists, but no open High Priority PRs
  were present for coverage inspection (ready alone does not qualify).

### Current contracts to rediscover

- [KV-aware selection](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/src/policies/kv_aware.rs)
  now selects and reserves atomically: the receipt already owns worker-load and
  request-slot reservations, plus any affinity reference. The HTTP
  [RequestLoadGuard::from_selection](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/src/routers/http/router.rs)
  adopts that reservation rather than incrementing again. The earlier blanket
  “selection alone must not reserve” advice no longer applies to this API.
  Check dispatch failure, retries, cancellation and body drop for exactly-once
  release. Optional affinity is off by default, and a preparation hint must be
  revalidated at selection; retry exclusions do not themselves invalidate a
  still-valid binding. HTTP paths can now render/tokenize for KV placement,
  superseding the earlier universal HTTP load-only description. A placement
  score is still not proof of an actual backend cache hit.
- [CLI reference](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/docs/cli_reference.md)
  now documents static KV-event source flags (`--kv-event-source`,
  `--kv-event-replay-source`, `--kv-event-block-size`, `--kv-event-model`) and
  `--kv-aware-session-affinity-ttl-secs`, with the documented
  `--max-tree-size` default aligned to `1 << 25` / `33554432`. The companion
  [check_cli_reference.py](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/scripts/check_cli_reference.py)
  treats `Option<…>` scalar fields as their inner types with an `unset` default
  marker. Docs/check agreement is not live KV-event or affinity evidence.
- [L1 encoding cache](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/src/backend/l1_encode_cache/mod.rs)
  stores router-side prefix token IDs, not worker KV. It is off by default
  (`VLLM_ROUTER_L1_CACHE`), after the exact L0 lookup and before full encoding.
  Prefix reuse requires validated added-token boundaries; the scope is text
  gRPC, not HTTP workers or multimodal placeholders. Follow tokenizer namespace,
  salt, fallback and optional verification-mismatch disablement together.
  Estimated retained heap is not RSS, and fixture parity is not live-model or
  performance evidence.
- The [gRPC adapter](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/src/backend/grpc.rs)
  now reaches `/v1/completions` token-ID dispatch. Distinguish it from
  [completion preparation](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/src/backend/completion.rs),
  a pure preparation layer that does not automatically rewrite or dispatch HTTP
  requests. Follow supported fields, tokenizer frontend and response conversion
  together; do not infer live serving parity from preparation tests alone.
- [Current Cargo test inventory](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/Cargo.toml)
  relocates integration tests to `tests/rust/`; Rust tests are gated by `cpu`
  and `ready`. Current CI uses `cargo test --features cpu,ready --lib --bins`
  and `cargo test --features cpu,ready --test '*'`. Bare historical commands
  may execute no gated tests. Python tests are under `tests/python/`, with
  the `ready and cpu` marker selection. Inspect actual test counts and
  prerequisites rather than accepting a zero-test success as coverage.
- [Buildkite XGMI](https://github.com/vllm-project/router/blob/a774cdda09237da16e33e67f725998ff4db920a3/.buildkite/pipeline.yml)
  is restored for default-branch non-PR builds, merge queue and same-repository
  PRs, plus trusted UI/API `RUN_ROCM_XGMI=1`; fork PRs remain excluded from that
  automatic PR condition. RDMA is still a separate nightly/manual lane.
  Configured eligibility is not a successful run or GPU correctness evidence.

### Maintenance validation and limits

The Router selector still validates owner/name delivery identities and normalizes
repository casing before deduplication and daily accounting. Three baseline
failure assertions demonstrate that casing previously lost same-head coverage
and the ten-distinct-PR cap, and malformed history was treated as another repo.
The cap, exact-label policy, source ownership and delivery authority are unchanged.

The existing two historical defect/fix families retain four correlated outcomes;
eight historical source records were previously matched for full hashes and
excerpts. No new reviewer-accuracy sample is claimed. The network-free suite
passes 259 tests, including Router selection/corpus/packaging tests, with
frontmatter, source pins, local links, manifests/routing, temporary-folder
installation, Python/JSON/shell parsing and whitespace checks. Fixtures validate
normalized collector snapshots, not live pagination, ancestry or concurrency.

Cargo/rustc are unavailable here. No upstream Rust/Python suites, native serving,
tokenizer/model parity, GPU/ROCm/RDMA, performance or distributed cleanup ran.
No live review or delivery checkpoint was advanced, no upstream code changed,
and no other project's selection policy was edited.

## Historical freshness update, inspected 2026-10-21 Asia/Shanghai

This bounded refresh supersedes the dated main-only reachability and CI facts
below, not the repository-owned review checklist. [Source identities](audit-2026-10-21.json)
pin 19 current implementation, documentation and test files by commit, Git blob,
SHA-256 and byte length. Byte verification is not full semantic coverage.

- Personal main inspected: `d741ca228e29d01f9b4a61e68e69b4ab43ad5e9e`.
  Router main: [5a840370e054dc3c4615be2d5a7a9e6a304ca354](https://github.com/vllm-project/router/commit/5a840370e054dc3c4615be2d5a7a9e6a304ca354),
  11 commits after the October 14 pin. The complete commit and changed-file
  inventories were enumerated; this is not a full audit of every changed line.
- The latest published release remains [v0.1.16](https://github.com/vllm-project/router/releases/tag/v0.1.16),
  at `db02f358da401b60d4ae14eb286163763a0705cc`; main is 21 commits ahead.
  The changes below are main-only, not additions to that released artifact.
- Main still has no AGENTS.md or canonical review skill. PR336 remains
  open/draft at `3fa8e31e8eed24c10ee39cce842dbdeb7a5e8f09`; its skill bytes
  match the Git blob and SHA-256 recorded below. Its architecture snapshot
  predates the new policy; resolve implementation at the actual review target.
- All 13 open personal PRs were enumerated. PR6 and PR17 retain the heads
  recorded below; their complete four-file and 19-file inventories do not
  overlap this Router supplement or its tests. No PR, human edit, shared
  installer, manifest or other project's review policy is replaced.

### Main-only contracts to revalidate

- [KV-aware selection](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/src/policies/kv_aware.rs)
  is now reachable through the regular/co-located router, superseding the
  earlier index-only state. Effective P/D policies reject `kv_aware`.
  The gRPC chat path supplies prepared token IDs; HTTP falls back to load-only
  scoring, not observed KV reuse. Discovery failure likewise loses placement
  credit rather than proving an empty backend cache. Follow cache identity,
  worker/rank binding and per-request LoRA hashing; nonempty cache salt disables
  placement credit because event identity cannot establish that namespace.
- The scorer includes remaining prefill work plus active prefill work, times
  the projected request count (the maximum observed count plus this request).
  Device reuse starts at a contiguous prefix; transfer credit uses a compatible
  continuation, not a sum of overlapping tiers or disconnected tails. Preserve
  last-token logits work and round fractional remaining work up. Temperature
  zero minimizes cost; positive temperature samples. These are source
  contracts, not latency, throughput or cache-hit measurements.
- [Request accounting](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/src/routers/http/router.rs)
  uses selection receipts and shared guards across dispatch, response
  consumption, cancellation and body drop. Selection alone must not reserve a
  slot. gRPC's first model output, rather than any SSE role frame, transitions
  prefill accounting; HTTP uses its first body frame. Check retry/failure,
  buffering, stream completion and disconnect paths for exactly-once release.
- [Strict structural decoding](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/src/kv_index/decode.rs)
  rejects malformed MessagePack, trailing bytes, invalid UTF-8, duplicate or
  unknown fields and unsupported events atomically. Its payload, depth and
  event-count limits do not establish a hard decoded-heap budget. The live
  subscriber uses this shared decoder and remains multi-tier/ownership aware.
  Do not conflate it with [separate device admission](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/src/kv_index/admit.rs):
  the narrow GPU/group-0/local, complete-block, 32-byte-hash checks preserve
  batch rank and do not establish publisher identity, freshness or independently
  addressable/native-DP routing. Shape acceptance is not routing eligibility.
- [Endpoint validation](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/src/kv_index/endpoints.rs)
  rejects duplicate/shared publishers and unspecified connect hosts, including
  IPv4-mapped IPv6 aliases. It retains exact registry ownership strings;
  syntactic canonicalization is not DNS resolution or publisher authentication.
- Other landed fixes need target-specific regression checks: PR360 forces
  prefill `min_tokens=1` as well as `max_tokens=1`; PR319 excludes unhealthy
  workers from cache-aware imbalance statistics; PR232 skips unhealthy workers
  for proxy GET endpoints. PR281 adds token-bucket-derived, upward-rounded,
  minimum-one-second `Retry-After` hints to queue-full and no-queue/no-token
  429 paths, not every error response. A hint is not
  a reservation or a guarantee that a retry will be admitted.
- [The MoRI XGMI lane](https://github.com/vllm-project/router/blob/5a840370e054dc3c4615be2d5a7a9e6a304ca354/.buildkite/pipeline.yml)
  is temporarily disabled for automatic builds while the MI300X host-image
  issue is unresolved; trusted manual UI/API runs with `RUN_ROCM_XGMI=1`
  remain configured. A missing automatic lane is not passing ROCm evidence.

### Validation and limits

The two historical defect/fix families and four correlated outcomes remain
unchanged. Eight historical source records were re-fetched and matched full
Git blob/SHA-256 and excerpt pins. No new accuracy sample is claimed.
The label/new-head policy, ten-distinct-PR daily cap and delivery deduplication
are unchanged; no live review queue or delivery checkpoint was advanced.

The personal-repository suite passed 251 network-free tests, including the
Router selector, corpus grounding/severity, source manifests and temporary-folder
installation checks. Frontmatter, affected links, JSON/Python parsing, routing,
shell syntax and diff whitespace passed. These tests exercise normalized
collector snapshots, not live API pagination or ancestry verification.

Cargo and rustc are unavailable. No upstream Rust/Python suites, live serving,
model/tokenizer parity, GPU/ROCm/RDMA, performance or distributed cleanup ran.
Suggested focused checks in a capable isolated environment are
`cargo test --lib policies::kv_aware`, `cargo test --lib kv_index::decode`,
`cargo test --test kv_device_consumer`, `cargo test --test kv_endpoint_worker_hosts`,
and the relevant HTTP-router, prefill, cache-aware and rate-limit regression
tests. These commands are suggestions, not reported passes. The canonical
draft contains no linked helper/reference bundle to execute.

## Historical freshness update, inspected 2026-10-14 Asia/Shanghai

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

Validate delivered repository identities as owner/name and compare them case-insensitively,
so collector spelling changes cannot reset coverage or the daily cap. Malformed
identities are unknown, not evidence of a different repository.

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
