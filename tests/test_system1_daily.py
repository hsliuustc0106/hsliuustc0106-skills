"""Network-free policy boundary cases, not estimates of review accuracy."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("system1_daily", ROOT / "skills/system1-omni-review/scripts/select_daily.py")
daily = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(daily)


def pr(number=30, labels=None, head="new"):
    value = {"number": number, "labels": labels if labels is not None else ["high priority", "ready"],
             "head": head, "state": "open", "new_commits_verified": True,
             "created_at": "2020-01-01", "ever_reviewed": True}
    value["current"] = {k: copy.deepcopy(value[k]) for k in ("head", "state", "labels")}
    return value


def snapshot():
    return {"repository": daily.REPOSITORY, "day": "2026-10-03",
            "labels_complete": True, "prs_complete": True, "checkpoint_complete": True,
            "label_pages": [["high priority"], ["ready"]], "pr_pages": [[pr()]], "delivered": []}


class SelectionTests(unittest.TestCase):
    def test_old_pr_new_commit_is_eligible(self):
        self.assertEqual(len(daily.select(snapshot())["selected"]), 1)

    def test_creation_date_and_review_history_are_not_filters(self):
        for created_at in ("2020-01-01", "2026-10-03"):
            for ever_reviewed in (True, False):
                s = snapshot()
                s["pr_pages"][0][0].update(created_at=created_at, ever_reviewed=ever_reviewed)
                self.assertEqual(len(daily.select(s)["selected"]), 1)

    def test_changed_state_blocks_final_snapshot(self):
        s = snapshot(); s["pr_pages"][0][0]["current"]["state"] = "closed"
        self.assertTrue(daily.select(s)["blocked"])
        self.assertFalse(daily.select(s)["selected"])

    def test_ready_from_later_catalog_page_is_required(self):
        s = snapshot(); s["pr_pages"] = [[pr(labels=["high priority"])]]
        self.assertEqual(daily.select(s)["selected"], [])

    def test_catalog_without_ready(self):
        s = snapshot(); s["label_pages"] = [["high priority"]]
        s["pr_pages"] = [[pr(labels=["high priority"])]]
        self.assertEqual(len(daily.select(s)["selected"]), 1)

    def test_exact_space_label_not_hyphen_alias(self):
        s = snapshot(); s["label_pages"] = [["high-priority", "ready"]]
        s["pr_pages"] = [[pr(labels=["high-priority", "ready"])]]
        self.assertFalse(daily.select(s)["selected"])

    def test_unknown_api_pages_are_blocked(self):
        for key in ("labels_complete", "prs_complete", "checkpoint_complete"):
            s = snapshot(); s[key] = None
            self.assertTrue(daily.select(s)["blocked"])
            self.assertFalse(daily.select(s)["selected"])

    def test_malformed_api_error_is_unknown(self):
        for s in (None, {"message": "API error"}, {**snapshot(), "label_pages": [{"error": 403}]}):
            self.assertTrue(daily.select(s)["blocked"])

    def test_all_pr_pages_and_ten_distinct_daily_cap(self):
        s = snapshot(); s["pr_pages"] = [[pr(i) for i in range(1, 7)], [pr(i) for i in range(7, 13)]]
        result = daily.select(s)
        self.assertEqual([p["number"] for p in result["selected"]], list(range(1, 11)))
        self.assertEqual(len(result["excluded"]), 2)

    def test_stale_head_blocks(self):
        s = snapshot(); s["pr_pages"][0][0]["current"]["head"] = "changed"
        self.assertTrue(daily.select(s)["blocked"])
        self.assertFalse(daily.select(s)["selected"])

    def test_changed_labels_blocks(self):
        s = snapshot(); s["pr_pages"][0][0]["current"]["labels"] = []
        self.assertTrue(daily.select(s)["blocked"])

    def test_closed_pr_is_excluded(self):
        s = snapshot(); p = s["pr_pages"][0][0]; p["state"] = p["current"]["state"] = "closed"
        self.assertFalse(daily.select(s)["selected"])

    def test_drafts_remain_eligible(self):
        s = snapshot(); s["pr_pages"][0][0]["draft"] = True
        self.assertTrue(daily.select(s)["selected"])

    def test_comments_are_not_new_commits(self):
        s = snapshot(); s["pr_pages"][0][0]["new_commits_verified"] = False
        self.assertFalse(daily.select(s)["selected"])

    def test_unverified_rewrite_is_blocked(self):
        s = snapshot(); s["pr_pages"][0][0]["new_commits_verified"] = None
        self.assertTrue(daily.select(s)["blocked"])

    def test_repeated_page_and_delivered_head_dedup(self):
        s = snapshot(); s["pr_pages"].append([pr()])
        self.assertEqual(len(daily.select(s)["selected"]), 1)
        s["delivered"] = [{"repository": daily.REPOSITORY, "number": 30, "head": "new",
                           "policy": daily.POLICY, "day": "2026-10-02"}]
        self.assertFalse(daily.select(s)["selected"])

    def test_prior_policy_does_not_override_new_commit_evidence(self):
        s = snapshot(); s["delivered"] = [{"repository": daily.REPOSITORY, "number": 30,
             "head": "old", "policy": "previous", "day": "2026-10-02"}]
        self.assertTrue(daily.select(s)["selected"])
        s["pr_pages"][0][0]["new_commits_verified"] = False
        self.assertFalse(daily.select(s)["selected"])

    def test_prior_daily_count_and_other_repo_isolation(self):
        s = snapshot(); s["delivered"] = [{"repository": daily.REPOSITORY, "number": n,
            "head": "old", "policy": "previous", "day": s["day"]} for n in range(10)]
        self.assertFalse(daily.select(s)["selected"])
        s["delivered"][0]["repository"] = "other/repo"
        self.assertTrue(daily.select(s)["selected"])

    def test_snapshot_and_checkpoint_not_mutated(self):
        s = snapshot(); before = copy.deepcopy(s); daily.select(s)
        self.assertEqual(s, before)

    def test_null_or_empty_head_blocks(self):
        for head in (None, "", 123):
            s = snapshot(); s["pr_pages"] = [[pr(head=head)]]
            self.assertFalse(daily.select(s)["selected"])
            self.assertTrue(daily.select(s)["blocked"])

    def test_missing_delivery_history_blocks(self):
        s = snapshot(); del s["delivered"]
        self.assertFalse(daily.select(s)["selected"])
        self.assertTrue(daily.select(s)["blocked"])

    def test_same_head_previously_delivered_under_other_policy_is_covered(self):
        s = snapshot(); s["delivered"] = [{"repository": daily.REPOSITORY, "number": 30,
            "head": "new", "policy": "previous", "day": "2026-10-02"}]
        self.assertFalse(daily.select(s)["selected"])

    def test_wrong_repository_blocks(self):
        s = snapshot(); s["repository"] = "other/repo"
        self.assertTrue(daily.select(s)["blocked"])

class EvidenceTests(unittest.TestCase):
    def test_canonical_source_routes_to_merged_main(self):
        import json
        sources = json.loads((ROOT / 'skills/repository-review-source/sources.json').read_text())
        self.assertEqual(sources['system1-omni'], {
            'repository': 'ThinkFlowLab/system1-omni',
            'path': '.agents/skills/system1-omni-review/SKILL.md',
        })
        skill = (ROOT / 'skills/system1-omni-review/SKILL.md').read_text()
        self.assertTrue(skill.startswith('---\nname: system1-omni-review\ndescription: '))
        self.assertIn('/blob/main/.agents/skills/system1-omni-review/SKILL.md', skill)

    def test_clean_cases_have_fixed_side_adjudication(self):
        import json
        cases = json.loads((ROOT / 'skills/system1-omni-review/references/adjudicated-cases.json').read_text())
        for case in cases:
            if case['status'] == 'clean-for-this-finding':
                self.assertEqual(case['evidence'],
                    'https://github.com/ThinkFlowLab/system1-omni/pull/30#issuecomment-5952020258')

    def test_pinned_grounding_severity_and_component_routing(self):
        import json
        import re
        cases = json.loads((ROOT / 'skills/system1-omni-review/references/adjudicated-cases.json').read_text())
        self.assertEqual(len(cases), 4)
        self.assertEqual(sum(c['status'] == 'defect' for c in cases), 2)
        for case in cases:
            self.assertRegex(case['commit'], r'^[0-9a-f]{40}$')
            self.assertRegex(case['blob_sha'], r'^[0-9a-f]{40}$')
            self.assertRegex(case['file_sha256'], r'^[0-9a-f]{64}$')
            self.assertIn('/blob/' + case['commit'] + '/' + case['path'], case['url'])
            self.assertTrue(case['exact_line'].strip())
            self.assertTrue(case['trigger'] and case['consequence'] and case['scope'])
            self.assertEqual(case['route'], 'benchmark-report' if 'report.py' in case['path'] else 'model-lifecycle')
            expected = ('P2' if case['route'] == 'benchmark-report' else 'P3') if case['status'] == 'defect' else None
            self.assertEqual(case['severity'], expected)

    def test_system1_resources_install_and_links_resolve(self):
        import subprocess
        import tempfile
        import re
        with tempfile.TemporaryDirectory() as target:
            subprocess.run(['bash', str(ROOT / 'scripts/sync-project.sh'), '--project', 'system1-omni',
                            '--tools', 'codex,claude,cursor', '--target', target], check=True, capture_output=True)
            skill = Path(target) / 'skills/system1-omni-review'
            self.assertTrue((skill / 'scripts/select_daily.py').is_file())
            self.assertTrue((skill / 'references/adjudicated-cases.json').is_file())
            for md in skill.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)', md.read_text()):
                    if not link.startswith(('https://', '#')):
                        self.assertTrue((md.parent / link.split('#')[0]).exists(), (md, link))


if __name__ == "__main__":
    unittest.main()
