"""Exercise the nanodot review policy entirely offline (stdlib, Python 3.8+)."""

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/nanodot-review/scripts/select_prs.py"
SPEC = importlib.util.spec_from_file_location("nanodot_selection", SCRIPT)
selection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selection)
DAY = "2026-10-02"


def labels(*names):
    return [{"name": name} for name in names]


def page(items, next_page=None, **extra):
    return dict({"items": items, "next_page": next_page}, **extra)


def pr(number, head="head-new", names=("high priority", "ready"), **extra):
    return dict({
        "number": number,
        "title": "Example PR {}".format(number),
        "state": "open",
        "head": {"sha": head},
        "labels": labels(*names),
        "created_at": "2020-01-01T00:00:00Z",
    }, **extra)


def review(number, head="head-old", at="2026-10-02T00:00:00+08:00", **extra):
    return dict({
        "repo": selection.REPO,
        "number": number,
        "head_sha": head,
        "policy_version": selection.POLICY_VERSION,
        "reviewed_at": at,
    }, **extra)


class SelectionTests(unittest.TestCase):
    def select(self, prs=None, catalog=None, ledger=None, **kwargs):
        return selection.select_prs(
            [page(labels("high priority", "ready"))] if catalog is None else catalog,
            [page([pr(1)] if prs is None else prs)],
            [] if ledger is None else ledger,
            day=kwargs.pop("day", DAY),
            **kwargs
        )

    def numbers(self, result):
        return [candidate["number"] for candidate in result["candidates"]]

    def test_ready_present_requires_both_labels(self):
        result = self.select([
            pr(1), pr(2, names=("high priority",)), pr(3, names=("ready",)),
            pr(4, names=("high priority", "ready", "bug")), pr(5, names=()),
        ])
        self.assertEqual(self.numbers(result), [1, 4])
        self.assertTrue(result["ready_label_exists"])
        self.assertEqual(result["required_labels"], ["high priority", "ready"])

    def test_confirmed_absence_of_ready_uses_high_priority_only(self):
        result = self.select(
            [pr(1, names=("high priority",)), pr(2, names=("ready",)), pr(3)],
            catalog=[page(labels("bug", "high priority"))],
        )
        self.assertEqual(self.numbers(result), [1, 3])
        self.assertFalse(result["ready_label_exists"])
        self.assertEqual(result["required_labels"], ["high priority"])

    def test_empty_successful_catalog_is_different_from_unknown(self):
        result = self.select([], catalog=[page([])])
        self.assertFalse(result["ready_label_exists"])
        self.assertEqual(result["candidates"], [])
        for unknown in (None, [], [{"items": []}], [{"error": "denied"}], [page([], status=403)]):
            with self.subTest(catalog=unknown), self.assertRaises(selection.SelectionError):
                selection.select_prs(unknown, [page([])], [], DAY)

    def test_exact_whole_names_case_insensitive_but_not_aliases(self):
        result = self.select([
            pr(1, names=("High Priority", "READY")),
            pr(2, names=("high-priority", "ready")),
            pr(3, names=("high priority", "ready for review")),
            pr(4, names=("high priority ", "ready")),
            pr(5, names=("high priority", " ready")),
        ], catalog=[page(labels("HIGH PRIORITY", "Ready"))])
        self.assertTrue(result["ready_label_exists"])
        self.assertEqual(self.numbers(result), [1])
        for alias in ("ready for review", "ready ", " ready", "already"):
            self.assertFalse(self.select(catalog=[page(labels(alias))])["ready_label_exists"])

    def test_catalog_ready_on_later_page_changes_filter(self):
        result = self.select(
            [pr(1, names=("high priority",)), pr(2)],
            catalog=[page(labels("high priority"), 2), page(labels("ready"))],
        )
        self.assertEqual(self.numbers(result), [2])

    def test_all_pr_pages_include_old_pr_with_new_head(self):
        result = selection.select_prs(
            [page(labels("ready"))],
            [page([pr(1, "already-reviewed")], 2), page([pr(9, "new-head")])],
            [review(1, "already-reviewed"), review(9, "old-head")], DAY,
        )
        self.assertEqual(self.numbers(result), [9])
        self.assertEqual(result["candidates"][0]["head_sha"], "new-head")

    def test_reviewed_head_cannot_be_reselected_by_policy_change(self):
        result = self.select([pr(1)], ledger=[review(1, "head-new")], policy_version="v-next")
        self.assertEqual(result["candidates"], [])
        changed = self.select([pr(1, "head-newer")], ledger=[review(1, "head-new")], policy_version="v-next")
        self.assertEqual(self.numbers(changed), [1])
        self.assertEqual(changed["candidates"][0]["dedupe_key"], [selection.REPO, 1, "head-newer", "v-next"])

    def test_same_sha_in_different_pr_or_repository_is_not_excluded(self):
        result = self.select([pr(1), pr(2)], ledger=[
            review(9, "head-new"), review(1, "head-new", repo="other/project"),
        ])
        self.assertEqual(self.numbers(result), [1, 2])
        self.assertEqual(result["reviews_today"], 1)

    def test_repo_capitalization_cannot_bypass_ledger(self):
        result = self.select([pr(1)], ledger=[review(1, "head-new", repo="thinkflowlab/NANODOT")])
        self.assertEqual(result["candidates"], [])
        self.assertEqual(result["reviews_today"], 1)

    def test_daily_cap_is_ten_less_prior_reviews_across_policies(self):
        ledger = [review(i, policy_version="old-policy") for i in range(1, 9)]
        result = self.select([pr(i) for i in range(1, 20)], ledger=ledger)
        self.assertEqual(result["reviews_today"], 8)
        self.assertEqual(result["remaining_capacity"], 2)
        self.assertEqual(self.numbers(result), [1, 2])
        for count in (10, 12):
            full = self.select(ledger=[review(i) for i in range(1, count + 1)])
            self.assertEqual(full["remaining_capacity"], 0)
            self.assertEqual(full["candidates"], [])
        self.assertEqual(len(self.select([pr(i) for i in range(1, 30)])["candidates"]), 10)

    def test_shanghai_daily_reset_at_1600_utc_and_naive_times_rejected(self):
        ledger = [
            review(1, at="2026-10-01T15:59:59Z"),
            review(2, at="2026-10-01T16:00:00Z"),
            review(3, at="2026-10-02T15:59:59+00:00"),
            review(4, at="2026-10-02T16:00:00+00:00"),
        ]
        self.assertEqual(self.select(ledger=ledger)["reviews_today"], 2)
        self.assertEqual(self.select(ledger=ledger, day="2026-10-01")["reviews_today"], 1)
        self.assertEqual(self.select(ledger=ledger, day="2026-10-03")["reviews_today"], 1)
        self.assertEqual(selection.REVIEW_TZ.utcoffset(None).total_seconds(), 8 * 3600)
        for timestamp in ("2026-10-02", "2026-10-02T00:00:00", "bad"):
            with self.subTest(timestamp=timestamp), self.assertRaises(selection.SelectionError):
                self.select(ledger=[review(1, at=timestamp)])

    def test_daily_reset_does_not_clear_reviewed_head_history(self):
        result = self.select([pr(1)], ledger=[review(1, "head-new", at="2025-01-01T00:00:00Z")])
        self.assertEqual(result["reviews_today"], 0)
        self.assertEqual(result["candidates"], [])

    def test_duplicate_pages_records_and_ledger_jobs_are_deduplicated(self):
        item, completed = pr(1), review(9)
        result = selection.select_prs(
            [page(labels("ready", "ready"), 2), page(labels("READY"))],
            [page([item, item], 2), page([item, pr(2)])],
            [completed, completed, review(9, at="2026-10-02T01:00:00+08:00")], DAY,
        )
        self.assertEqual(self.numbers(result), [1, 2])
        self.assertEqual(result["reviews_today"], 1)
        self.assertEqual(result["remaining_capacity"], 9)

    def test_conflicting_duplicate_pr_heads_or_labels_fail_closed(self):
        for duplicate in (pr(1, "head-changed"), pr(1, names=("high priority",)), pr(1, state="closed")):
            with self.subTest(pr=duplicate), self.assertRaises(selection.SelectionError):
                self.select([pr(1), duplicate])

    def test_incomplete_error_or_broken_page_chain_never_returns_partial_result(self):
        bad_pages = [
            [page(labels("ready"), 2)],
            [page(labels("ready"), 2), {"error": "API unavailable"}],
            [page(labels("ready")), page([])],
            [page([], 3), page([])],
            [page([], 1), page([])],
            [page([], True), page([])],
            [page({}, None)],
        ]
        for pages in bad_pages:
            with self.subTest(pages=pages), self.assertRaises(selection.SelectionError):
                self.select(catalog=pages)
        for pages in ([], [page([pr(1)], 2)], [page([pr(1)], 2), page([], status=500)]):
            with self.subTest(pages=pages), self.assertRaises(selection.SelectionError):
                selection.select_prs([page(labels("ready"))], pages, [], DAY)

    def test_malformed_ledger_and_required_pr_evidence_block_selection(self):
        for ledger in ({}, [None], [{"repo": selection.REPO}], [review(1, head_sha="")]):
            with self.subTest(ledger=ledger), self.assertRaises(selection.SelectionError):
                self.select(ledger=ledger)
        for invalid in (None, {}, pr(True), pr(1, head=None), pr(1, labels=None), pr(1, state=None)):
            with self.subTest(pr=invalid), self.assertRaises(selection.SelectionError):
                self.select([invalid])
        for invalid in (["ready"], [{"name": ""}], [None]):
            with self.subTest(labels=invalid), self.assertRaises(selection.SelectionError):
                self.select(catalog=[page(invalid)])

    def test_closed_prs_are_excluded_without_extra_age_or_draft_filters(self):
        self.assertEqual(self.numbers(self.select([pr(1, state="closed"), pr(2, draft=True)])), [2])

    def test_selection_is_deterministic_and_does_not_mutate_inputs(self):
        catalog, pulls, ledger = [page(labels("ready"))], [page([pr(2), pr(1)])], [review(8)]
        originals = copy.deepcopy((catalog, pulls, ledger))
        first = selection.select_prs(catalog, pulls, ledger, DAY)
        second = selection.select_prs(catalog, pulls, ledger, DAY)
        self.assertEqual(first, second)
        self.assertEqual((catalog, pulls, ledger), originals)
        self.assertEqual(self.numbers(first), [1, 2])

    def test_invalid_day_or_policy_fail_closed(self):
        for day in ("2026-10-2", "2026-02-30", "unknown"):
            with self.subTest(day=day), self.assertRaises(selection.SelectionError):
                self.select(day=day)
        with self.assertRaises(selection.SelectionError):
            self.select(policy_version="")

    def test_revalidation_accepts_only_same_open_pr_head(self):
        self.assertTrue(selection.revalidate_head(pr(1), 1, "head-new")["current"])
        for current in (pr(1, "newer"), pr(1, state="closed"), pr(2), {}, None):
            with self.subTest(current=current), self.assertRaises(selection.SelectionError):
                selection.revalidate_head(current, 1, "head-new")


class GhTransportTests(unittest.TestCase):
    def response(self, body, link=None, returncode=0, status=200):
        headers = "HTTP/2.0 {} OK\nContent-Type: application/json\n".format(status)
        if link is not None:
            headers += "Link: " + link + "\n"
        return subprocess.CompletedProcess([], returncode, headers + "\n" + json.dumps(body), "API unavailable")

    def link(self, resource, page_number, relation="next"):
        return '<https://api.github.com/repos/{}/{}?per_page=100&page={}>; rel="{}"'.format(
            selection.REPO, resource, page_number, relation,
        )

    def test_fetches_every_catalog_and_open_pr_page_via_get_only(self):
        responses = [
            self.response(labels("high priority"), self.link("labels", 2)),
            self.response(labels("ready"), self.link("labels", 1, "prev")),
            self.response([pr(1)], self.link("pulls", 2)),
            self.response([pr(2)]),
        ]
        with patch.object(selection.subprocess, "run", side_effect=responses) as run:
            catalog = selection.fetch_pages("labels")
            pulls = selection.fetch_pages("pulls")
        self.assertEqual(len(catalog), 2)
        self.assertEqual(len(pulls), 2)
        endpoints = [call.args[0][-1] for call in run.call_args_list]
        self.assertEqual(endpoints, [
            "repos/{}/labels?per_page=100&page=1".format(selection.REPO),
            "repos/{}/labels?per_page=100&page=2".format(selection.REPO),
            "repos/{}/pulls?per_page=100&page=1&state=open".format(selection.REPO),
            "repos/{}/pulls?per_page=100&page=2&state=open".format(selection.REPO),
        ])
        for call in run.call_args_list:
            self.assertEqual(call.args[0][:7],
                             ["gh", "api", "--hostname", "github.com", "--method", "GET", "--include"])
            self.assertNotIn("created:", " ".join(call.args[0]))

    def test_enterprise_environment_cannot_redirect_public_repo_reads(self):
        with patch.dict(os.environ, {"GH_HOST": "enterprise.example"}), patch.object(
                selection.subprocess, "run", return_value=self.response([])) as run:
            selection.fetch_pages("labels")
        command = run.call_args.args[0]
        self.assertEqual(command[command.index("--hostname") + 1], "github.com")

    def test_http_command_json_and_later_page_errors_fail_closed(self):
        bad_responses = [
            self.response([], returncode=1), self.response([], status=403),
            self.response({"message": "rate limited"}),
            subprocess.CompletedProcess([], 0, "[]", ""),
            subprocess.CompletedProcess([], 0, "HTTP/2.0 200 OK\n\nnot json", ""),
        ]
        for response in bad_responses:
            with self.subTest(response=response), patch.object(selection.subprocess, "run", return_value=response):
                with self.assertRaises(selection.SelectionError):
                    selection.fetch_pages("labels")
        with patch.object(selection.subprocess, "run", side_effect=[
            self.response(labels("high priority"), self.link("labels", 2)),
            self.response([], returncode=1),
        ]), self.assertRaises(selection.SelectionError):
            selection.fetch_pages("labels")
        for error in (FileNotFoundError("gh"), subprocess.TimeoutExpired("gh", 60)):
            with patch.object(selection.subprocess, "run", side_effect=error):
                with self.assertRaises(selection.SelectionError):
                    selection.fetch_pages("labels")

    def test_github_numeric_repository_link_is_supported(self):
        link = self.link("labels", 2).replace("/repos/" + selection.REPO, "/repositories/12345")
        with patch.object(selection.subprocess, "run", side_effect=[
            self.response(labels("high priority"), link),
            self.response(labels("ready")),
        ]) as run:
            self.assertEqual(len(selection.fetch_pages("labels")), 2)
        self.assertEqual(run.call_args_list[1].args[0][-1],
                         "repos/{}/labels?per_page=100&page=2".format(selection.REPO))

    def test_malformed_cyclic_or_wrong_endpoint_pagination_is_unknown(self):
        links = [
            "broken", self.link("labels", 1), self.link("labels", 3),
            self.link("pulls", 2), self.link("labels", 2).replace("api.github.com", "other.example"),
            self.link("labels", 2) + ", " + self.link("labels", 2),
            self.link("labels", 3, "last"), self.link("labels", 1, "prev"),
            self.link("labels", 1, "unknown"),
            self.link("labels", 2) + ", " + self.link("labels", 1, "last"),
        ]
        for link in links:
            with self.subTest(link=link), self.assertRaises(selection.SelectionError):
                selection.next_page({"link": link}, "labels", 1)


class CliTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.ledger = self.root / "ledger.json"
        self.ledger.write_text("[]\n")
        self.fixture = self.root / "fixture.json"
        self.fixture.write_text(json.dumps({
            "repo": selection.REPO,
            "label_pages": [page(labels("high priority"), 2), page(labels("ready"))],
            "pull_pages": [page([pr(1, names=("high priority",))], 2), page([pr(2)])],
            "current_pr": pr(2),
        }))

    def run_cli(self, *args):
        # Empty PATH makes any unintended network command fail; Python is absolute.
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            env=dict(os.environ, PATH="", PYTHONDONTWRITEBYTECODE="1"),
            capture_output=True, text=True, check=False,
        )

    def test_offline_cli_produces_candidates_without_mutating_ledger(self):
        before = self.ledger.read_bytes()
        result = self.run_cli("--ledger", str(self.ledger), "--input", str(self.fixture), "--day", DAY)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual([item["number"] for item in output["candidates"]], [2])
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_missing_or_corrupt_ledger_fails_with_no_candidates(self):
        for data in (None, "not json", "{}"):
            if data is None:
                self.ledger.unlink()
            else:
                self.ledger.write_text(data)
            result = self.run_cli("--ledger", str(self.ledger), "--input", str(self.fixture))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("Selection blocked:", result.stderr)

    def test_unknown_or_wrong_repo_fixture_does_not_fall_back_to_live(self):
        for data in (None, {}, {"repo": "other/project"}, {"repo": selection.REPO}):
            self.fixture.write_text(json.dumps(data))
            result = self.run_cli("--ledger", str(self.ledger), "--input", str(self.fixture))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("Cannot run gh", result.stderr)

    def test_stale_head_cli_guard(self):
        ok = self.run_cli("--revalidate", "2", "head-new", "--input", str(self.fixture))
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue(json.loads(ok.stdout)["current"])
        stale = self.run_cli("--revalidate", "2", "head-old", "--input", str(self.fixture))
        self.assertNotEqual(stale.returncode, 0)
        self.assertEqual(stale.stdout, "")
        self.assertIn("head changed", stale.stderr)


if __name__ == "__main__":
    unittest.main()
