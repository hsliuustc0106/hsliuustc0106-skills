# Personal daily selection and bounded AFD audit

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

- Repository `vllm-project/afd-plugin`, the Asia/Shanghai calendar `day`, complete
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
checkpoint history is unknown. See `tests/test_afd_daily.py` for executable
normalized snapshots; this helper does not implement the evidence collector.

Deduplicate repository/PR/head/policy, and keep a head already reviewed under an
older policy covered. Cap at ten distinct PRs per repository/Asia/Shanghai day
across confirmed deliveries and policy versions. A new head on an already counted
PR does not consume another distinct-PR slot. Preserve deferred heads as pending.
Selection is not delivery: update checkpoints only after confirmed delivery and
reconcile uncertain delivery before retrying. Serialize concurrent selection and
delivery or reconcile reservations against the same ledger; this snapshot adapter
does not enforce a cross-process cap. No delivery ledger belongs here.

## Current bounded refresh, 2026-10-20 Asia/Shanghai

This section supersedes the dated runtime assumptions below, not the canonical
review skill. The earlier audit and defect/fixed-clean corpus remain historical
records; do not apply their old runner paths to a current deployment.
[Source identities](audit-2026-10-20.json) pin 15 reference/implementation files
by commit, Git blob, SHA-256, and byte length. Byte verification is not full
semantic coverage of every file or an upstream execution result.

### Release boundary and overlap

- Personal repository main inspected: `2a42d199ab94316023661d9d5309a1b818dc671b`.
- AFD main inspected: [0fff229b592bc489c8857cdabc39f247687acaf5](https://github.com/vllm-project/afd-plugin/commit/0fff229b592bc489c8857cdabc39f247687acaf5),
  27 commits after the previous audit. The full comparison's 27 commit entries
  were enumerated; only the runtime, review-guidance and test-contract surfaces
  described here were inspected in depth, not every changed line.
- [v0.30.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.30.0rc1)
  was published 2026-10-19 08:05:42 UTC with `prerelease: true`, no attached
  release assets, and tag commit `9fcdbd1ff64698785fa0dcf2c61a817fd60f9f06`.
  This RC includes the GPU/NPU MRV2 migration. Main is four commits beyond it:
  removal of unused PP adaptations (#469), test conventions (#470), unit-test
  consolidation (#467), and backend-aware sequence-parallel tests (#472).
  Do not describe these four changes as part of that released tag.
- PR420 remains open at `fbd0e5eb47128771994e0e9530fc230693d97b0a`.
  Canonical review content already exists on main; the proposed branch is not
  a mandatory replacement. The main checklist still says vLLM 0.26.0, asks for
  V1/V2 parity and says GPU V2 is gated off. Those statements conflict with
  current implementation. Resolve current compatibility from code and target
  dependency pins; do not reject a valid MRV2-only change using stale prose.
- Personal PR6 and PR17 remain open at the heads recorded below. All 13 open
  personal PRs were enumerated; PR6's four files and PR17's 19 files were
  inspected for path overlap. Neither touches this AFD supplement or selector.
  No existing PR, human edit, manifest or other project's policy is replaced.

### Runtime facts to revalidate at the review target

- [Dependency metadata](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/pyproject.toml)
  pins optional runtime `vllm==0.30.0`.
  [Installation evidence](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/README.md)
  names vLLM `ced6857afa0ea7b2e3f0846a62e1394e90f15607` and vLLM-Ascend
  `8d4409d6256d8a6729140ddcc0d1889e3f96cdd6`. A supported source pair is not
  proof of a released Ascend wheel/container or compatibility with arbitrary
  versions.
- [Deployment validators](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/validation.py)
  reject non-V2 GPU and NPU configurations. Both roles require the paired MRV2
  deployment, but GPU FFN remains an AFD-owned connector-driven runner, not
  native scheduler-driven MRV2 execution. PP/PCP/DCP sizes remain one; role
  ranks must equal DP times TP. Deleted V1 paths are not current fallback tests.
- [CUDA graph policy](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/v1/worker/cuda_graph.py)
  permits eager or FULL_DECODE_ONLY, with exactly two ubatches when enabled.
  NPU synchronous CAMP2P accepts eager/FULL/FULL_DECODE_ONLY; native DBO needs
  two ubatches, Attention DP greater than one, and no speculative decoding.
  [NPU feature validation](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/afd_plugin/compat/npu/feature_validation.py)
  further requires FULL_DECODE_ONLY for plain MLA graph plus DBO. Do not
  flatten these model/connector-specific constraints into one platform matrix.
- Async CAM requires eager Attention with Attention-side gating and async DP.
  Its native DBO is Attention-only with two ubatches, including DP1. Independent
  FFN FULL is a separate, narrow W4A8 runtime contract, not blanket Async CAM
  graph support. Model, topology, device operator and cleanup evidence remain
  necessary; source acceptance of a flag is not proof of working hardware.
- PR421's Kubernetes recipes are now merged and included in v0.30.0rc1, unlike
  their open-proposal status in the earlier audit. This does not establish that
  every deployment variant has an executed Kubernetes acceptance test.

### Current testing guidance and limits

[Current AGENTS.md](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/AGENTS.md)
requires behavior/seam tests, shared fakes, mirrored source layout, and CPU-only
unit collection without torch/vLLM using guarded runtime imports. It forbids
production-Python substring assertions; test-line budgets and ownership also
apply. Historical AST/excerpt fixtures in this personal repository adjudicate
old defects only and are not a substitute for upstream behavior tests.

[Ready CI](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/.buildkite/cuda/test-ready.yml)
selects non-GPU/non-runtime unit tests plus seven named DeepSeek-V2-Lite cases
in the GPU V2 job, including `baseline-graph` and six `afd-v2-*` cases. [NPU testing](https://github.com/vllm-project/afd-plugin/blob/0fff229b592bc489c8857cdabc39f247687acaf5/docs/npu/TESTING.md)
distinguishes real stream/event contract tests from transport and checkpoint
accuracy. Completed nonempty two-stage replays during actual requests, not
capture/profile/padded-only execution, qualify the stated graph+DBO gate.
DSV4 synchronous profiles with `check_answer=False` establish liveness, not
output correctness. Test #472's reported Ascend suite totals are author evidence,
not tests executed by this maintenance pass.

The existing two purposively selected defect/fixed-clean pairs (four correlated
outcomes), selection policy, ten-PR cap, and delivery ledger contract are
unchanged. No upstream PR review or daily queue execution was performed. No
GPU/NPU execution, model accuracy/performance measurement, distributed teardown,
Kubernetes deployment, or private project audit was performed.

Validation: the full personal-repository suite passed 250 network-free tests,
including 30 AFD selector cases, four AFD corpus/audit metadata checks, and the
AFD temporary-directory install/idempotence/conflict test. All 24 skill
frontmatters, JSON/Python parsing, affected local links, manifest/routing tests,
shell syntax and diff whitespace passed. Fifteen current-source files and eight
historical corpus files were byte-verified against Git blob and SHA-256 pins.
These fixture and packaging checks are not upstream runtime tests or accuracy
measurements. Installation occurred only in temporary test directories.

## Sources and overlap, inspected 2026-10-06 Asia/Shanghai

- Personal main baseline: `874421b1c16a14de54e497b29c33959353f067cd`
- AFD main: [9cae2d2ddaae7e1752fc12ead577d59540b17f27](https://github.com/vllm-project/afd-plugin/commit/9cae2d2ddaae7e1752fc12ead577d59540b17f27)
- Latest published release: [v0.26.0rc1](https://github.com/vllm-project/afd-plugin/releases/tag/v0.26.0rc1),
  published 2026-08-19, tag commit `85e826ed8239dd9d8032375bb84a56116e24f0e0`.
  GitHub marks it `prerelease: false`, but its RC name is retained here; do not
  relabel it a fully validated stable release. Main is 63 commits ahead
- Last main review-skill edit: `76bd189c38a9d740bda5627be246f70da75160f4` (PR363), 20 main commits behind.
  This is source-edit history, not a previous complete-audit pin. No prior
  complete AFD audit ledger was present in this personal skill. This pass starts
  a bounded record rather than claiming all intervening architecture was audited
- The canonical review skill already exists on main. [PR420](https://github.com/vllm-project/afd-plugin/pull/420)
  is an open enhancement, pinned here at `fbd0e5eb47128771994e0e9530fc230693d97b0a`.
  It preserves AFD module routing and adds target-version and optional reviewer
  safeguards. Identify use of those enhancements as proposed-source use, never
  as merged policy. Load instructions and references from the same resolved SHA.
  Main SKILL Git blob: `81d94c95de61d37931111e770a791d1c0a2e5663`,
  exact-byte SHA-256: `bb5adbcfcec5910fd56220b822db4c88c8dfaec713aef86c119e8741c849359b`.
  Proposed SKILL Git blob: `498726dc2f21fa54f5db3506740ea85e4fabc538`,
  exact-byte SHA-256: `45efc81cbfe0cb5a63945a74174fbed96c5bb3bfdf61e57125f4593328ef4176`
- [PR6](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/6)
  at `68d7b38df04c382e9e51c9fde28428181d3bc5a8` and
  [PR17](https://github.com/hsliuustc0106/hsliuustc0106-skills/pull/17)
  at `f01a5df38f337e65d80f420e6b22e0b30a5237af` remain open.
  This AFD-only supplement neither replaces their human edits nor imports their
  Omni checklist or maintenance workflow

## Historical observations at the 2026-10-06 pin

Read the actual target's compatibility pins, dependency metadata, CI commands,
markers, fixtures, and module status before applying these dated observations.
Do not port Omni pipeline, diffusion, or stage-payload contracts into AFD's
attention/FFN split, connector handshakes, role workers, or runner V1/V2 paths.

- E2E runner changes have a live owning contract:
  [e2e_testing.md](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/design/module/e2e_testing.md).
  Route to that contract plus tests-quality evidence; add graph/DBO or platform
  overlays only for the scenario actually changed. Broad CODEOWNERS matching
  does not replace the module's more specific expertise
- [PR416](https://github.com/vllm-project/afd-plugin/pull/416) preserves caller
  chunked-prefill choices instead of automatically disabling the feature for
  DBO. Do not revive that removed default from old test advice
- Resolve accuracy gates from the frozen scenario, not the historical
  `GSM8K-7` shorthand in the performance reference. Current DeepSeek-V2-Lite
  DBO scenarios have a 24-sample floor; small-sample runs (up to 24) default
  to 0.25, larger runs and other models retain 0.27, and an explicit
  `AFD_GSM8K_THRESHOLD` takes precedence. At 24 samples this allows 6 correct
  answers rather than 7. This is smoke acceptance calibration, not proof of
  production accuracy, numerical equivalence, or paired validation on all backends
- [PR404](https://github.com/vllm-project/afd-plugin/pull/404) gates attention
  workspace warmup on graph-with-ubatching policy. Inspect worker-to-FFN
  workspace readiness when graph capture changes; ubatching alone does not
  justify extra eager warmup and synchronization
- Recent NPU changes need target-specific routing:
  [ubatch thread binding](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/afd_plugin/v1/worker/npu/ubatching.py#L37-L46)
  sets the device before stream queries/barriers;
  [layered W4A8 validation](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/npu/TESTING.md#L24-L66)
  crosses feature flags, FFN dataflow, native bindings and kernels. Trace both
  ends rather than applying a CUDA-only graph check to these NPU paths
- [Routed native operators](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/docs/npu/CAM_ASYNC_ROUTED_OPS.md)
  tie HCCL buffer tiling and per-group allocations to source-built operator
  revisions. CPU goldens, Meta bindings, and dry runs do not establish device
  support. [Current Buildkite gates](https://github.com/vllm-project/afd-plugin/blob/9cae2d2ddaae7e1752fc12ead577d59540b17f27/.buildkite/cuda/test-ready.yml)
  select CPU-marked unit tests in a runtime-equipped image plus GPU E2E lanes;
  NPU evidence remains manual. Do not equate CPU selection with a dependency-free
  import requirement for every runtime module
- [PR421](https://github.com/vllm-project/afd-plugin/pull/421) remains open.
  Its GPU P2P colocation multi-pod deployment proposal is not landed architecture
  or a currently required Kubernetes E2E lane. Resolve its state anew before
  treating any proposed command or deployment contract as supported

## Calibration and limits

[Adjudicated cases](adjudicated-cases.json) contain two purposively selected
historical defect/fix pairs, four outcomes total. The fixed-clean cases mean
only that their specific defect is absent, not that the PR is approved or the
whole runtime is correct. Fixture checks are not reviewer precision, recall,
accuracy measurements, a blinded evaluation, or four independent samples.

PR416 covers caller-choice preservation and a reported Legacy startup stall;
it does not prove the separate large-message/SHM production deadlock is fixed.
PR404 covers the graph/eager warmup gate, with a public P2 review adjudication;
CPU/source evidence cannot establish GPU memory or synchronization performance.
The test fixtures parse only pinned excerpts without importing upstream code.

This is a partial public-source audit. GPU/NPU execution, model inference,
accuracy/performance, live distributed teardown and Kubernetes deployments were
not run. No live daily queue or delivery ledger was changed. The network-free
adapter trusts collector evidence; it does not itself prove remote pagination,
commit ancestry, or successful delivery. Missing evidence must remain unknown.

Validation for this pass: 30 network-free selector tests, three corpus
source/severity/routing/mechanism checks, and one AFD packaging test passed;
the full personal-repository suite passed 113 tests. An independent 19-test
selector pass included 1,000 seeded randomized cap/dedup scenarios. All 20 skill
entrypoints, local links, manifests, installation routing, shell syntax, Python
parsing and diff whitespace were checked. Eight full historical source files
matched Git blob and SHA-256 pins. The main/proposed canonical skill contains no
executable helpers, so source-helper execution is not applicable. These checks
validate this bounded supplement, not upstream GPU/NPU behavior.
