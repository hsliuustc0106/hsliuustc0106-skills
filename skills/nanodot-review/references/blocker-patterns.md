# Evidence-backed blocker patterns

These patterns come from unmerged integration history, not main. Check the target
snapshot and reachable callers before reporting them. A matching name is not a bug.

## Required success and observed failure are separate

Unknown/hidden/empty required-check catalogs cannot prove terminal success. They
also must not suppress a visible current-head failure when the listing is complete.
Incomplete listings stay pending. Ignore old-head failures and superseded attempts;
retain source, app and suite identity when selecting latest runs.

The [a8c704e correction](https://github.com/ThinkFlowLab/nanodot/commit/a8c704e2b6390e14c7ff5eae810ec8d210faa2d9)
handles empty/hidden catalogs. The later
[661f4bae correction](https://github.com/ThinkFlowLab/nanodot/commit/661f4bae106e9f9718137812a803020b8954acc8)
also alerts on optional failure while known required checks are pending.
Confirmed required success still wins over unrelated optional failure. Do not
"fix" this by making every optional failure prevent terminal success.

Trace `evaluate_checks`, `failing_checks_on_current_commit`, and `statemachine.step`.
Test unknown, empty and known-pending requirements; incomplete evidence; old SHA;
latest rerun; confirmed required success. Failure notification is not a mergeability
or branch-protection verdict.

## Crash/replay must preserve event identity

A crash after durable inbox insertion but before the task checkpoint can replay
one occurrence with changed check evidence, text, or timestamp. Content-hash-only
identity creates a duplicate. At the
[pinned correction](https://github.com/ThinkFlowLab/nanodot/blob/a8c704e2b6390e14c7ff5eae810ec8d210faa2d9/src/nanodot/native/notifier.py#L39-L64),
sequenced events key on `(task_id, occurrence, kind, head_sha)`; distinct occurrences
must remain distinct. Legacy unsequenced fallback has a different contract.

Test restart plus mutable evidence and distinct occurrences, not just calling
notify twice with one identical object. Durable inbox dedup does not promise
exactly-once OS popups. Trace notify-before-checkpoint ordering and ensure optional
memory/provider work cannot prevent terminal-state persistence.

## Stop means no next queued task

A stop request during one fetch permits that task to finish/persist, then starts
no later queued task. Checking only outside the scheduling pass is too late.
Inspect `RunnerDaemon.tick`, `serve`, and CLI `_run_runner --once` together at the
[pinned correction](https://github.com/ThinkFlowLab/nanodot/commit/a8c704e2b6390e14c7ff5eae810ec8d210faa2d9).
Test both modes with at least two due tasks and a stop during the first fetch;
also test stop set before the tick. Leave later tasks pending and schedulable.
This is cooperative stop, not guaranteed forced cancellation of in-flight I/O.

## Scope, lifecycle and data boundaries

At execution time, validate/reload persisted scope, state, grant expiry and
revocation; stale queued objects cannot authorize delivery. Cover cancellation or
scope change while fetching and token-specific runner ownership. Treat auth loss
and hidden data as explicit blockers/unknowns, not permission to widen access.

Anonymous reads must not touch saved credentials. Summaries are optional bounded
presentation; they cannot override deterministic evidence or cause unbounded
worker growth. Inputs, logs, public reports and memory must not leak secret fields.
Report a concrete reachable violation, not generic security advice.
