"""Fail-closed required-check evaluation, pinned to the current head SHA."""

from __future__ import annotations

from enum import Enum

from nanodot.ports.github import CheckRun, Snapshot

PASSING_CONCLUSIONS = frozenset({"success"})
FAILING_CONCLUSIONS = frozenset({"failure", "timed_out", "cancelled", "action_required", "stale", "error"})
IGNORED_CONCLUSIONS = frozenset({"skipped", "neutral"})


class CheckOutcome(str, Enum):
    PASSING = "passing"
    FAILING = "failing"
    PENDING = "pending"
    NO_CHECKS = "no_checks"


def _latest(runs: tuple[CheckRun, ...]) -> list[CheckRun]:
    """Reruns replace only the same source/app/suite/name, never another app.

    Suite identity preserves independently required same-name workflow jobs.
    Without ordered IDs, retain every result rather than guessing a winner.
    """
    groups: dict[tuple, list[CheckRun]] = {}
    for run in runs:
        key = (run.source, run.name.casefold(), run.app_id, run.suite_id)
        groups.setdefault(key, []).append(run)
    selected = []
    for group in groups.values():
        if all(type(run.run_id) is int and run.run_id > 0 for run in group):
            newest = max(run.run_id for run in group)
            selected.extend(run for run in group if run.run_id == newest)
        else:
            selected.extend(group)
    return selected


def evaluate_checks(snapshot: Snapshot) -> CheckOutcome:
    """Require a complete, known required set and actual success for each.

    This intentionally remains stricter than GitHub's merge gate: skipped
    and neutral conclusions are not a confirmed success. No required checks
    is not a vacuous terminal pass. This is not a mergeability assessment.
    """
    if snapshot.checks_complete is not True or snapshot.required_checks is None:
        return CheckOutcome.PENDING
    if not snapshot.required_checks:
        return CheckOutcome.NO_CHECKS
    runs = _latest(snapshot.checks_for(snapshot.head_sha))
    relevant: list[CheckRun] = []
    pending = False
    for required in snapshot.required_checks:
        if not isinstance(required.name, str) or not required.name or (required.app_id is not None and (
            type(required.app_id) is not int or required.app_id <= 0
        )):
            return CheckOutcome.PENDING
        # A rerequested suite can still expose its previous successful runs
        # before the new jobs appear. Its unresolved state must block success.
        if any(run.source == "check_suite" and (
            not run.name or run.name.casefold() == required.name.casefold()
        ) and (
            required.app_id is None or run.app_id in (None, required.app_id)
        ) for run in runs):
            pending = True
        named = [run for run in runs if run.source != "check_suite"
                 and run.name.casefold() == required.name.casefold()]
        if required.app_id is not None:
            # Legacy statuses don't expose their GitHub App. Their creator
            # user ID is not an app ID and must never be used as one.
            if any(run.source == "status" and run.app_id is None for run in named):
                pending = True
            named = [run for run in named if run.app_id == required.app_id]
        if not named or any(run.source not in {"check_run", "status"} for run in named):
            pending = True
        # GitHub requires both when a check run and legacy status share a name.
        relevant.extend(named)
    if any(run.status == "completed" and run.conclusion in FAILING_CONCLUSIONS for run in relevant):
        return CheckOutcome.FAILING
    if pending or any(run.status != "completed" for run in relevant):
        return CheckOutcome.PENDING
    if all(run.conclusion in PASSING_CONCLUSIONS for run in relevant):
        return CheckOutcome.PASSING
    return CheckOutcome.PENDING


def checks_passing_on_current_commit(snapshot: Snapshot) -> bool:
    """All known required checks succeeded on the complete current snapshot."""
    return evaluate_checks(snapshot) is CheckOutcome.PASSING
