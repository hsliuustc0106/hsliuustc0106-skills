"""Offline eligibility and packaging checks; not reviewer-accuracy estimates."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/sciencediscovery-review"
SPEC = importlib.util.spec_from_file_location("sciencediscovery_daily", SKILL / "scripts/select_daily.py")
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
    return {"repository": daily.REPOSITORY, "day": "2026-10-08",
            "labels_complete": True, "prs_complete": True, "checkpoint_complete": True,
            "baseline_confirmed": True, "label_pages": [["high priority"], ["ready"]],
            "pr_pages": [[pr()]], "delivered": []}


def delivered(number=30, head="a" * 40, policy=daily.POLICY, day="2026-10-07", repo=daily.REPOSITORY):
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
            command = ["bash", str(ROOT / "scripts/sync-project.sh"), "--project", "sciencediscovery",
                       "--tools", "codex,claude,cursor", "--target", target]
            subprocess.run(command, check=True, capture_output=True)
            subprocess.run(command, check=True, capture_output=True)
            installed = Path(target) / "skills/sciencediscovery-review"
            for relative in ("scripts/select_daily.py", "scripts/replay_cases.mjs", "references/maintenance.md", "references/adjudicated-cases.json", "references/LICENSE.sciencediscovery.txt"):
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
        self.cases = {case["id"]: case for case in self.data["cases"]}

    def test_exact_source_excerpt_pins_and_bounded_adjudication(self):
        import hashlib
        self.assertEqual(self.data["repository"], daily.REPOSITORY)
        self.assertEqual(self.data["sample_size"]["defect_families"], 2)
        self.assertEqual(self.data["sample_size"]["outcomes"], 4)
        self.assertEqual(len(self.cases), 4)
        records = [case["source"] for case in self.cases.values()]
        records += [s for group in self.data["supporting_sources"].values() for s in group]
        for source in records:
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")
            self.assertRegex(source["git_blob_sha"], r"^[0-9a-f]{40}$")
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(source["line_url"], f'https://github.com/{daily.REPOSITORY}/blob/{source["commit"]}/{source["path"]}#L{source["line_start"]}-L{source["line_end"]}')
            self.assertEqual(len(source["excerpt"].splitlines()), source["line_end"] - source["line_start"] + 1)
            self.assertEqual(hashlib.sha256(source["excerpt"].encode()).hexdigest(), source["excerpt_sha256"])
        for case in self.cases.values():
            self.assertEqual(case["commit"], case["source"]["commit"])
            for field in ("trigger", "consequence", "independent_reasoning", "severity_reason", "test_reasoning"):
                self.assertTrue(case[field].strip())
            self.assertEqual(case["severity"], "P2" if case["outcome"] == "defect-present" else None)
            if case["outcome"] != "defect-present":
                self.assertEqual(case["outcome"], "specific-defect-absent")
                self.assertIn("not whole-PR approval", case["severity_reason"])

    def test_instruction_provenance_does_not_bundle_canonical_policy(self):
        for source in self.data["instruction_sources"]:
            self.assertNotIn("excerpt", source)
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(source["git_blob_sha"], r"^[0-9a-f]{40}$")
        self.assertFalse(self.data["validation"]["upstream_tests_run"])
        self.assertIn("not independent accuracy samples", self.data["sample_size"]["sampling"])

    def test_pagination_mechanism_model_exposes_unreachable_next_offset(self):
        # Bounded model of the exact OR terms, not execution of TypeScript.
        import re
        def has_more(case_id, remaining, truncated, partial):
            source = self.cases[case_id]["source"]["excerpt"]
            expression = re.search(r'const hasMore = ([^;]+);', source).group(1)
            values = {"endLine < lines.length": remaining,
                      "truncated": truncated, "page.partialLine": partial}
            return any(values[term.strip()] for term in expression.split("||"))
        old, new = "artifact-pagination-before", "artifact-pagination-fixed"
        for truncated, partial in ((True, False), (False, True), (True, True)):
            self.assertTrue(has_more(old, False, truncated, partial))
            self.assertFalse(has_more(new, False, truncated, partial))
        for case_id in (old, new):
            self.assertTrue(has_more(case_id, True, False, False))
            self.assertFalse(has_more(case_id, False, False, False))
        self.assertIn('Artifact', self.cases[new]["route"]["primary"])
        regression = self.data["supporting_sources"]["artifact-pagination"][0]["excerpt"]
        self.assertIn('nextOffset', regression)
        self.assertIn('hasMore', regression)
        self.assertIn('truncated', regression)

    def test_child_scope_is_grounded_in_callers_collector_and_owner_filters(self):
        old = self.cases["child-authority-scope-before"]
        new = self.cases["child-authority-scope-fixed"]
        self.assertIn("execution.turnId === runId", old["source"]["excerpt"])
        self.assertIn("store.listSubagents(sessionId)", old["source"]["excerpt"])
        source = new["source"]["excerpt"]
        self.assertIn("execution.turnId === executionId", source)
        self.assertIn("children: subagentId === undefined ? subagents : []", source)
        self.assertIn("store.captureSubagentAuthorities(sessionId, subagentId)", source)
        for service in ("notifications", "transfers", "shellExecutions"):
            self.assertIn(f"store.{service}.snapshot(sessionId, agentId)", source)
        support = self.data["supporting_sources"]["child-authority-scope"]
        self.assertIn("versioningAuthorities(store, sessionId, runId)", support[0]["excerpt"])
        self.assertIn("executionId: childExecution.identity.executionId", support[1]["excerpt"])
        self.assertIn("subagentId: subagent.id", support[1]["excerpt"])
        self.assertIn("orchestration", new["route"]["primary"])
        self.assertIn("does not establish", old["severity_reason"])

    def test_corrected_fixture_pin_is_distinct_from_product_fix(self):
        pair = self.data["pairs"]["child-authority-scope"]
        self.assertNotEqual(pair["fixed_commit"], pair["implementation_fix_commit"])
        self.assertEqual(pair["fixed_commit"], pair["regression_correction"]["commit"])
        tests = [s for s in self.data["supporting_sources"]["child-authority-scope"]
                 if s["path"].endswith("versioning-authorities.test.ts")]
        self.assertEqual(len(tests), 2)
        for source in tests:
            self.assertEqual(source["commit"], pair["fixed_commit"])
        self.assertIn('sandbox: "bubblewrap"', tests[0]["excerpt"])
        self.assertIn("not evidence that Bubblewrap ran", pair["regression_correction"]["detail"])


if __name__ == "__main__":
    unittest.main()
