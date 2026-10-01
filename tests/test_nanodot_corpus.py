"""Pinned source-excerpt regression controls; no network or nanodot installation.

These execute vetted pure evaluator/event-key functions and a scheduler method
with minimal test doubles. They are not nanodot's full runtime/integration suite.
"""

import ast
import hashlib
import json
import logging
import textwrap
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

FIXTURES = Path(__file__).parent / "fixtures/nanodot-review"
INPUTS = json.loads((FIXTURES / "inputs.json").read_text())["cases"]
CASES = {case["id"]: case for case in INPUTS}


def source(case_id, symbol):
    item = next(item for item in CASES[case_id]["sources"] if item["symbol"] == symbol)
    return (FIXTURES / item["fixture"]).read_text()


def load_evaluator(case_id):
    raw = (FIXTURES / CASES[case_id]["behavior_source"]["fixture"]).read_text()
    tree = ast.parse(raw)
    # Dataclass type names are postponed annotations; ports are test doubles.
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.ImportFrom) and (node.module or "").startswith("nanodot."))]
    namespace = {}
    exec(compile(tree, "pinned_evaluator", "exec"), namespace)
    return namespace["evaluate_checks"]


def check(name="lint", conclusion="failure", head="current", run_id=1, status="completed"):
    return SimpleNamespace(name=name, conclusion=conclusion, head_sha=head, run_id=run_id,
                           status=status, source="check_run", app_id=1, suite_id=1)


class Snapshot:
    def __init__(self, required_checks, checks, complete=True):
        self.required_checks = required_checks
        self.checks_complete = complete
        self.checks = tuple(checks)
        self.head_sha = "current"

    def checks_for(self, sha):
        return tuple(run for run in self.checks if run.head_sha == sha)


class NanodotCorpusTests(unittest.TestCase):
    def test_every_excerpt_and_behavior_file_has_matching_hash_and_exact_pin(self):
        for case in INPUTS:
            self.assertEqual(len(case["head_sha"]), 40)
            items = case["sources"] + ([case["behavior_source"]] if "behavior_source" in case else [])
            for item in items:
                with self.subTest(case=case["id"], file=item["fixture"]):
                    data = (FIXTURES / item["fixture"]).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                    self.assertIn("/blob/" + case["head_sha"] + "/" + item["path"], item["url"])
            for item in case["sources"]:
                self.assertEqual(len((FIXTURES / item["fixture"]).read_text().splitlines()),
                                 item["end_line"] - item["start_line"] + 1)

    def test_four_narrow_defects_and_four_clean_controls_have_adjudication(self):
        expected = json.loads((FIXTURES / "adjudication.json").read_text())["cases"]
        self.assertEqual({x["id"] for x in expected}, set(CASES))
        self.assertEqual(sum(x["has_defect"] for x in expected), 4)
        self.assertEqual(len(expected), 8)
        for item in expected:
            self.assertEqual(item["expected_severity"], "P2" if item["has_defect"] else None)
            self.assertTrue(item["adjudication"])
            self.assertTrue(item["regression_tests"])

    def test_unknown_and_empty_catalog_regression_and_clean_control(self):
        before, after = load_evaluator("n05"), load_evaluator("n01")
        for required in (None, ()):
            snapshot = Snapshot(required, [check()])
            self.assertIn(before(snapshot).value, ("pending", "no_checks"))
            self.assertEqual(after(snapshot).value, "failing")
        self.assertEqual(after(Snapshot((), [check()], complete=False)).value, "pending")

    def test_optional_failure_pending_required_regression_and_success_precedence(self):
        before, after = load_evaluator("n04"), load_evaluator("n08")
        required = (SimpleNamespace(name="required", app_id=1),)
        runs = [check("required", None, status="in_progress"), check("optional")]
        self.assertEqual(before(Snapshot(required, runs)).value, "pending")
        self.assertEqual(after(Snapshot(required, runs)).value, "failing")
        runs[0] = check("required", "success")
        self.assertEqual(after(Snapshot(required, runs)).value, "passing")
        self.assertEqual(after(Snapshot(required, runs, complete=False)).value, "pending")

    def test_stale_head_and_superseded_failure_do_not_create_false_alert(self):
        after = load_evaluator("n08")
        self.assertEqual(after(Snapshot((), [check(head="old")])).value, "no_checks")
        runs = [check(run_id=1), check(conclusion="success", run_id=2)]
        self.assertEqual(after(Snapshot((), runs)).value, "no_checks")

    def key(self, case_id):
        namespace = {"json": json, "hashlib": hashlib}
        exec("from __future__ import annotations\n" + source(case_id, "event_key"), namespace)
        return namespace["event_key"]

    def test_replay_identity_regression_and_mutable_evidence_clean_control(self):
        before, after = self.key("n07"), self.key("n03")
        first = SimpleNamespace(task_id="task", occurrence=4, kind="checks_failed",
                                message="failed", evidence={"head_sha": "head", "checks": ["a"]})
        replay = SimpleNamespace(**vars(first))
        replay.message = "still failed"
        replay.evidence = {"head_sha": "head", "checks": ["a", "b"]}
        self.assertNotEqual(before(first), before(replay))
        self.assertEqual(after(first), after(replay))
        for field, value in (("task_id", "other"), ("occurrence", 5), ("kind", "merged"),
                             ("evidence", {"head_sha": "new-head"})):
            changed = SimpleNamespace(**{**vars(first), field: value})
            self.assertNotEqual(after(first), after(changed))

    def run_scheduler(self, case_id):
        namespace = {"threading": threading, "logger": logging.getLogger(__name__)}
        exec("from __future__ import annotations\n" + textwrap.dedent(
            source(case_id, "RunnerDaemon.tick")), namespace)
        exec("from __future__ import annotations\n" + textwrap.dedent(
            source(case_id, "RunnerDaemon.serve")), namespace)
        stopped = threading.Event()
        completed = []

        def run_once(task, now):
            completed.append(task)
            stopped.set()

        runner = SimpleNamespace(_clock=SimpleNamespace(time=lambda: 0),
                                 _store=SimpleNamespace(list_schedulable=lambda now: ["one", "two"]),
                                 _loop=SimpleNamespace(run_once=run_once),
                                 _tick=0)
        runner.tick = lambda **kwargs: namespace["tick"](runner, **kwargs)
        namespace["serve"](runner, stopped)
        return completed

    def test_cooperative_stop_regression_and_clean_scheduler_control(self):
        self.assertEqual(self.run_scheduler("n02"), ["one", "two"])
        self.assertEqual(self.run_scheduler("n06"), ["one"])

    def test_once_and_daemon_call_sites_forward_same_stop_event(self):
        for case_id, expected in (("n02", False), ("n06", True)):
            for symbol in ("_run_runner", "RunnerDaemon.serve"):
                tree = ast.parse(textwrap.dedent(source(case_id, symbol)))
                calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Attribute) and node.func.attr == "tick"]
                self.assertEqual(len(calls), 1)
                self.assertEqual(any(kw.arg == "stop" and isinstance(kw.value, ast.Name)
                                     and kw.value.id == "stop" for kw in calls[0].keywords), expected)


if __name__ == "__main__":
    unittest.main()
