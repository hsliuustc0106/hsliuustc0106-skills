# Test quality and verification

Use the exact snapshot's `pyproject.toml`, CI workflow and existing tests to choose
commands. The [architecture map](architecture.md) distinguishes the small main
suite from the integration suite. Never carry integration test totals into main.

A useful test proves the changed contract with meaningful assertions and fails
when the relevant behavior is removed or inverted. Count test cases, fixture
scenarios, manual runs and untested paths separately.

For high-risk touched paths, look for:

- Complete/partial paginated API data, retryable errors, authentication loss and
  permission-denied/hidden required-check catalog
- Current-head versus old-head observations; source/app/suite identity; latest
  completed and pending attempts; optional failures while required checks pend
- Zero/one/multiple tasks, pause/cancel/revoke/expire during fetch, stop between
  queued tasks in daemon and `--once`, terminal tasks not rescheduled
- Crash after notification and before state persistence, replay after restart,
  stable event identity despite mutable evidence/message/time
- Temporary isolated files, atomic replacement, invalid saved rows remaining
  inspectable/cancellable, malformed input, no unintended network or credentials
- Provider timeout/error/malformed summary: deterministic watcher result survives
  and no unbounded thread/task growth occurs

Avoid mocks that bypass the gate under test, arbitrary sleeps, network dependence,
weak non-None assertions, and a test that repeats the implementation's decision.
Use events/barriers or injected clocks for interleavings. Test both defect and
neighboring clean behavior so that a blanket stop/failure rule cannot pass.

For main's scaffold, protocol/import and configuration tests are appropriate;
full watcher, daemon, notifier and provider claims remain untested there. For
integration code, run targeted regression tests and the full offline suite when
available. A green remote CI run applies only to its exact SHA and workflow.
Do not execute paid inference, notifications to real recipients, or GPU workloads
for a documentation/review-skill update.
