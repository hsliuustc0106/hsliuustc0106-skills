"""Offline eligibility and packaging checks; not reviewer-accuracy estimates."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/nanodot-review"
SPEC = importlib.util.spec_from_file_location("nanodot_daily", SKILL / "scripts/select_daily.py")
daily = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(daily)


def pr(number=30, labels=None, head="a" * 40):
    value = {"number": number, "labels": ["high priority", "ready"] if labels is None else labels,
             "head": head, "state": "open", "new_commits_verified": True,
             "created_at": "2020-01-01", "ever_reviewed": True,
             "draft": True, "author_is_reviewer": True}
    value["current"] = {key: copy.deepcopy(value[key]) for key in ("head", "state", "labels")}
    return value


def snapshot():
    return {"repository": daily.REPOSITORY, "day": "2026-10-09",
            "labels_complete": True, "prs_complete": True, "checkpoint_complete": True,
            "baseline_confirmed": True, "label_pages": [["high priority"], ["ready"]],
            "pr_pages": [[pr()]], "delivered": []}


def delivered(number=30, head="a" * 40, policy=daily.POLICY, day="2026-10-08", repo=daily.REPOSITORY):
    return {"repository": repo, "number": number, "head": head, "policy": policy, "day": day}


class SelectionTests(unittest.TestCase):
    def test_old_previously_reviewed_own_draft_with_new_commit_remains_eligible(self):
        self.assertEqual([x["number"] for x in daily.select(snapshot())["selected"]], [30])

    def test_ready_on_later_catalog_page_is_required(self):
        value = snapshot(); value["pr_pages"] = [[pr(labels=["high priority"])]]
        self.assertFalse(daily.select(value)["selected"])

    def test_absent_ready_falls_back_to_high_priority(self):
        value = snapshot(); value["label_pages"] = [["high priority"]]
        value["pr_pages"] = [[pr(labels=["high priority"])]]
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_ready_alone_is_ineligible(self):
        value = snapshot(); value["pr_pages"] = [[pr(labels=["ready"])]]
        self.assertFalse(daily.select(value)["selected"])

    def test_exact_label_spelling(self):
        for alternate in ("high-priority", "High Priority"):
            value = snapshot(); value["label_pages"] = [[alternate, "ready"]]
            value["pr_pages"] = [[pr(labels=[alternate, "ready"])]]
            self.assertFalse(daily.select(value)["selected"])

    def test_empty_catalog_and_empty_pr_page_are_known_empty(self):
        value = snapshot(); value["label_pages"] = [[]]; value["pr_pages"] = [[]]
        self.assertEqual(daily.select(value), {"selected": [], "excluded": [], "blocked": []})

    def test_missing_or_incomplete_page_flags_block(self):
        for field in ("labels_complete", "prs_complete", "checkpoint_complete", "baseline_confirmed"):
            for flag in (False, None, 1):
                value = snapshot(); value[field] = flag
                result = daily.select(value)
                self.assertTrue(result["blocked"]); self.assertFalse(result["selected"])

    def test_api_error_and_nonarray_pages_block(self):
        for pages in (None, [], [{"message": "API rate limit exceeded"}], ["not a page"]):
            for field in ("label_pages", "pr_pages"):
                value = snapshot(); value[field] = pages
                self.assertTrue(daily.select(value)["blocked"])

    def test_unknown_pr_label_blocks_catalog_race(self):
        value = snapshot(); value["pr_pages"] = [[pr(labels=["high priority", "new label"])]]
        self.assertTrue(daily.select(value)["blocked"])

    def test_unknown_label_values_block(self):
        for labels in (None, "high priority", [None], [{"message": "403"}], [""]):
            value = snapshot(); value["pr_pages"][0][0]["labels"] = labels
            self.assertTrue(daily.select(value)["blocked"])

    def test_all_pages_and_daily_cap(self):
        value = snapshot(); value["pr_pages"] = [[pr(i) for i in range(1, 7)], [pr(i) for i in range(7, 13)]]
        result = daily.select(value)
        self.assertEqual([x["number"] for x in result["selected"]], list(range(1, 11)))
        self.assertEqual(len(result["excluded"]), 2)

    def test_repeated_pages_deduplicate(self):
        value = snapshot(); value["pr_pages"].append([pr()])
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_conflicting_paginated_head_blocks_entire_snapshot(self):
        value = snapshot(); value["pr_pages"].append([pr(head="b" * 40)])
        result = daily.select(value)
        self.assertFalse(result["selected"]); self.assertTrue(result["blocked"])

    def test_numeric_commit_evidence_cannot_hide_behind_duplicate_boolean(self):
        for invalid in (1, 0, 1.0, 0.0):
            for reverse in (False, True):
                value = snapshot(); bad = pr(); bad["new_commits_verified"] = invalid
                good = pr(); good["new_commits_verified"] = bool(invalid)
                value["pr_pages"] = [[bad], [good]]
                if reverse:
                    value["pr_pages"].reverse()
                result = daily.select(value)
                self.assertFalse(result["selected"]); self.assertTrue(result["blocked"])

    def test_stale_head_state_or_labels_blocks(self):
        for key, changed in (("head", "b" * 40), ("state", "closed"), ("labels", ["ready"])):
            value = snapshot(); value["pr_pages"][0][0]["current"][key] = changed
            result = daily.select(value)
            self.assertFalse(result["selected"]); self.assertTrue(result["blocked"])

    def test_label_order_is_not_staleness(self):
        value = snapshot(); value["pr_pages"][0][0]["current"]["labels"].reverse()
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_closed_pr_is_excluded(self):
        value = snapshot(); value["pr_pages"][0][0]["state"] = "closed"
        value["pr_pages"][0][0]["current"]["state"] = "closed"
        self.assertFalse(daily.select(value)["selected"])

    def test_comment_activity_and_policy_change_do_not_prove_new_commits(self):
        value = snapshot(); value["pr_pages"][0][0]["new_commits_verified"] = False
        value["delivered"] = [delivered(head="b" * 40, policy="previous")]
        self.assertFalse(daily.select(value)["selected"])

    def test_unknown_force_push_delta_blocks(self):
        for delta in (None, 1, "true"):
            value = snapshot(); value["pr_pages"][0][0]["new_commits_verified"] = delta
            self.assertTrue(daily.select(value)["blocked"])

    def test_same_head_is_covered_across_policies(self):
        for policy in (daily.POLICY, "previous"):
            value = snapshot(); value["delivered"] = [delivered(policy=policy)]
            self.assertFalse(daily.select(value)["selected"])

    def test_new_head_of_previously_reviewed_pr_is_eligible(self):
        value = snapshot(); value["delivered"] = [delivered(head="b" * 40)]
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_daily_cap_counts_distinct_prs_across_policy_versions(self):
        value = snapshot()
        value["delivered"] = [delivered(n, policy="previous", day=value["day"]) for n in range(1, 11)]
        value["delivered"].append(delivered(1, head="b" * 40, day=value["day"]))
        self.assertFalse(daily.select(value)["selected"])
        value["delivered"][0]["repository"] = "other/repo"
        self.assertFalse(daily.select(value)["selected"])
        value["delivered"].pop()
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_new_revision_of_already_counted_pr_does_not_consume_extra_slot(self):
        value = snapshot(); value["pr_pages"] = [[pr(1, head="b" * 40)]]
        value["delivered"] = [delivered(n, day=value["day"]) for n in range(1, 11)]
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_prior_day_does_not_consume_today_cap(self):
        value = snapshot(); value["delivered"] = [delivered(n) for n in range(1, 11)]
        self.assertEqual(len(daily.select(value)["selected"]), 1)

    def test_missing_or_malformed_history_blocks(self):
        for history in (None, {}, [{"message": "403"}], [delivered(number=True)], [delivered(day="not a day")]):
            value = snapshot(); value["delivered"] = history
            self.assertTrue(daily.select(value)["blocked"])

    def test_invalid_identity_and_head_block(self):
        for key, invalid in (("number", True), ("number", 0), ("head", None), ("head", ""), ("head", "abc")):
            value = snapshot(); value["pr_pages"][0][0][key] = invalid
            self.assertTrue(daily.select(value)["blocked"])

    def test_wrong_repository_and_bad_day_block(self):
        for key, invalid in (("repository", "other/repo"), ("day", "2026-02-30"), ("day", "20261005")):
            value = snapshot(); value[key] = invalid
            self.assertTrue(daily.select(value)["blocked"])

    def test_nonmapping_snapshot_is_unknown(self):
        for value in (None, [], {"message": "API error"}):
            self.assertTrue(daily.select(value)["blocked"])

    def test_snapshot_and_delivery_history_are_not_mutated(self):
        value = snapshot(); before = copy.deepcopy(value); daily.select(value)
        self.assertEqual(value, before)

    def test_cli_distinguishes_unknown_from_known_empty(self):
        command = ["python3", str(SKILL / "scripts/select_daily.py")]
        for data in ("not JSON", json.dumps({"message": "403"})):
            result = subprocess.run(command, input=data, text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertTrue(json.loads(result.stdout)["blocked"])
        value = snapshot(); value["pr_pages"] = [[]]
        result = subprocess.run(command, input=json.dumps(value), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)["selected"])


class PackagingTests(unittest.TestCase):
    def test_resources_install_without_source_policy_copy(self):
        with tempfile.TemporaryDirectory() as target:
            command = ["bash", str(ROOT / "scripts/sync-project.sh"), "--project", "nanodot",
                       "--tools", "codex,claude,cursor", "--target", target]
            subprocess.run(command, check=True, capture_output=True)
            subprocess.run(command, check=True, capture_output=True)
            installed = Path(target) / "skills/nanodot-review"
            for relative in ("scripts/select_daily.py", "references/maintenance.md", "references/adjudicated-cases.json"):
                self.assertEqual((installed / relative).read_bytes(), (SKILL / relative).read_bytes())
            result = subprocess.run(["python3", str(installed / "scripts/select_daily.py")],
                                    input=json.dumps(snapshot()), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)["selected"]), 1)
            (installed / "scripts/select_daily.py").write_text("human edit\n")
            result = subprocess.run(command, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((installed / "scripts/select_daily.py").read_text(), "human edit\n")


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL / "references/adjudicated-cases.json").read_text())

    def test_paired_outcomes_grounding_and_severity(self):
        pairs = self.data["historical_pairs"]
        self.assertEqual(len(pairs), 2)
        self.assertEqual(sum(len(pair["samples"]) for pair in pairs), 4)
        for pair in pairs:
            self.assertEqual([s["has_defect"] for s in pair["samples"]], [True, False])
            self.assertTrue(pair["severity_rationale"].startswith("P2 for the defective sample:"))
            for sample in pair["samples"]:
                self.assertRegex(sample["head_sha"], r"^[0-9a-f]{40}$")
                self.assertEqual(sample["expected_severity"], "P2" if sample["has_defect"] else None)
                grounding = sample["grounding"]
                self.assertEqual(grounding["expected_finding_count"], int(sample["has_defect"]))
                for field in ("trigger", "observable_outcome", "correction_or_preserved_contract", "scope"):
                    self.assertTrue(grounding[field].strip())
                self.assertTrue(sample["regression_tests"])
                for source in sample["sources"]:
                    self.assertGreaterEqual(source["start_line"], 1)
                    self.assertGreaterEqual(source["end_line"], source["start_line"])
                    self.assertEqual(source["url"], "https://github.com/ThinkFlowLab/nanodot/blob/"
                        + sample["head_sha"] + "/" + source["path"]
                        + f'#L{source["start_line"]}-L{source["end_line"]}')
                    self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
                self.assertIn(grounding["source_anchor"]["url"], [s["url"] for s in sample["sources"]])

    def test_pinned_canonical_ownership_and_route_expectations(self):
        owner = self.data["canonical_owner"]
        self.assertEqual(owner["head_sha"], self.data["snapshot"]["main_sha"])
        for name in ("inputs", "adjudication"):
            source = owner[name]
            self.assertIn("/blob/" + owner["head_sha"] + "/" + source["path"], source["url"])
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
        expected = {
            "optional-failure-required-pending": (["watch-state"], ["src/nanodot/core/github_eval.py"]),
            "crash-replay-notification-identity": (["persistence-delivery"], ["src/nanodot/native/notifier.py"]),
        }
        for pair in self.data["historical_pairs"]:
            routes, paths = expected[pair["family"]]
            self.assertEqual(pair["expected_routes"], routes)
            self.assertEqual(pair["route_paths"], paths)
        self.assertGreaterEqual(len(self.data["coverage_limits"]), 4)
        self.assertIn("upstream repository", self.data["purpose"])


if __name__ == "__main__":
    unittest.main()
