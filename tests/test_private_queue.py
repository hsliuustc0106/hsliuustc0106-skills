"""Synthetic policy contracts only; no private source or adjudicated PR corpus."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/repository-review-source/scripts/select_private_queue.py'
spec = importlib.util.spec_from_file_location('private_queue', SCRIPT)
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)
REPO = 'example/private-project'


def pr(n=1, head='a' * 40, tags=None):
    value = dict(number=n, head=head, state='open', draft=False,
                 labels=['high priority', 'ready'] if tags is None else tags,
                 new_commits_verified=True)
    value['current'] = {k: copy.deepcopy(value[k]) for k in ('head', 'state', 'draft', 'labels')}
    return value


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.config = dict(repository=REPO, policy=queue.POLICY, explicit_opt_in=True)
        self.snapshot = dict(repository=REPO, policy=queue.POLICY, day='2026-10-18',
                             labels_complete=True, prs_complete=True, checkpoint_complete=True,
                             baseline_confirmed=True, label_pages=[['high priority'], ['ready']],
                             pr_pages=[[pr()]], reviews=[], daily_charges=[])

    def run_queue(self):
        return queue.select(self.snapshot, self.config)

    def test_paginated_old_pr_new_head(self):
        self.snapshot['pr_pages'] = [[pr(7)], [pr(8)]]
        self.snapshot['pr_pages'][0][0]['created_at'] = '2020-01-01'
        self.snapshot['reviews'] = [dict(repository=REPO, number=7, head='b'*40,
                                         policy=queue.POLICY, completed=True, published=True)]
        self.assertEqual([x['number'] for x in self.run_queue()['selected']], [7, 8])

    def test_ready_catalog_requires_both_labels(self):
        self.snapshot['pr_pages'] = [[pr(tags=['high priority'])]]
        self.assertEqual(self.run_queue()['selected'], [])
        self.assertTrue(self.run_queue()['excluded'])

    def test_no_ready_catalog_requires_only_high_priority(self):
        self.snapshot['label_pages'] = [['high priority']]
        self.snapshot['pr_pages'] = [[pr(tags=['high priority'])]]
        self.assertEqual(len(self.run_queue()['selected']), 1)

    def test_no_high_priority_does_not_broaden(self):
        self.snapshot['label_pages'] = [['ready']]
        self.snapshot['pr_pages'] = [[pr(tags=['ready'])]]
        self.assertFalse(self.run_queue()['selected'])

    def test_explicit_opt_in_and_identity(self):
        for key, value in [('explicit_opt_in', False), ('policy', 'all-non-draft'), ('repository', 'example/wrong')]:
            with self.subTest(key=key):
                config = dict(self.config, **{key: value})
                result = queue.select(self.snapshot, config)
                self.assertFalse(result['selected'])
                self.assertTrue(result['blocked'])

    def test_api_error_or_incomplete_page_is_unknown(self):
        for key in ('labels_complete', 'prs_complete', 'checkpoint_complete', 'baseline_confirmed'):
            with self.subTest(key=key):
                snapshot = dict(self.snapshot, **{key: False})
                self.assertTrue(queue.select(snapshot, self.config)['blocked'])
        for value in ([], None, {'error': 'rate limited'}):
            self.snapshot['pr_pages'] = value
            self.assertTrue(self.run_queue()['blocked'])

    def test_verified_empty_page(self):
        self.snapshot['pr_pages'] = [[]]
        self.assertEqual(self.run_queue(), dict(selected=[], excluded=[], blocked=[]))

    def test_duplicate_pages_and_conflicting_heads(self):
        self.snapshot['pr_pages'] = [[pr()], [pr()]]
        self.assertEqual(len(self.run_queue()['selected']), 1)
        self.snapshot['pr_pages'][1][0]['head'] = 'b'*40
        result = self.run_queue()
        self.assertFalse(result['selected'])
        self.assertTrue(result['blocked'])

    def test_stale_final_state_head_labels_draft(self):
        for key, value in [('head', 'b'*40), ('state', 'closed'), ('draft', True), ('labels', [])]:
            with self.subTest(key=key):
                p = pr()
                p['current'][key] = value
                self.snapshot['pr_pages'] = [[p]]
                self.assertFalse(self.run_queue()['selected'])
                self.assertTrue(self.run_queue()['blocked'])

    def test_closed_and_draft_excluded(self):
        for key, value in [('state', 'closed'), ('draft', True)]:
            p = pr()
            p[key] = p['current'][key] = value
            self.snapshot['pr_pages'] = [[p]]
            self.assertFalse(self.run_queue()['selected'])
            self.assertTrue(self.run_queue()['excluded'])

    def test_completed_unpublished_dedup_and_policy_change(self):
        self.snapshot['reviews'] = [dict(repository=REPO, number=1, head='a'*40,
                                         policy='previous-policy', completed=True, published=False)]
        self.assertFalse(self.run_queue()['selected'])

    def test_incomplete_review_stays_pending(self):
        self.snapshot['reviews'] = [dict(repository=REPO, number=1, head='a'*40,
                                         policy=queue.POLICY, completed=False, published=False)]
        self.assertEqual(len(self.run_queue()['selected']), 1)

    def test_unknown_delta_is_not_new_code(self):
        self.snapshot['pr_pages'][0][0]['new_commits_verified'] = None
        self.assertTrue(self.run_queue()['blocked'])
        self.snapshot['pr_pages'][0][0]['new_commits_verified'] = False
        self.assertTrue(self.run_queue()['excluded'])

    def test_ten_distinct_daily_capacity_and_resume(self):
        self.snapshot['daily_charges'] = [dict(repository=REPO, number=n, day='2026-10-18') for n in range(1, 11)]
        self.snapshot['pr_pages'] = [[pr(11), pr(1, 'b'*40)]]
        result = self.run_queue()
        self.assertEqual([p['number'] for p in result['selected']], [1])
        self.assertEqual(result['blocked'][0]['number'], 11)

    def test_cap_within_selection_and_duplicate_charges(self):
        self.snapshot['daily_charges'] = [dict(repository=REPO, number=1, day='2026-10-18')]*4
        self.snapshot['pr_pages'] = [[pr(n) for n in range(1, 13)]]
        self.assertEqual(len(self.run_queue()['selected']), 10)
        self.assertEqual(len(self.run_queue()['blocked']), 2)

    def test_other_repository_and_old_day_do_not_use_capacity(self):
        self.snapshot['daily_charges'] = [dict(repository='example/other', number=n, day='2026-10-18') for n in range(20)]
        # Zero is malformed, rather than silently ignored as another repository.
        self.assertTrue(self.run_queue()['blocked'])
        self.snapshot['daily_charges'] = [dict(repository=REPO, number=n, day='2026-10-17') for n in range(1, 20)]
        self.assertEqual(len(self.run_queue()['selected']), 1)

    def test_malformed_history_and_future_charge_fail_closed(self):
        self.snapshot['reviews'] = [{}]
        self.assertTrue(self.run_queue()['blocked'])
        self.snapshot['reviews'] = []
        self.snapshot['daily_charges'] = [dict(repository=REPO, number=1, day='2026-10-19')]
        self.assertTrue(self.run_queue()['blocked'])

    def test_complete_validation_before_selection(self):
        self.snapshot['pr_pages'] = [[pr()], [dict(number=2, head='short')]]
        self.assertFalse(self.run_queue()['selected'])
        self.assertTrue(self.run_queue()['blocked'])

    def test_repository_case_cannot_bypass_dedup_or_daily_cap(self):
        self.config['repository'] = 'Example/Private-Project'
        self.snapshot['reviews'] = [dict(repository='EXAMPLE/private-project', number=1,
                                         head='a'*40, policy=queue.POLICY, completed=True, published=True)]
        self.assertFalse(self.run_queue()['selected'])
        self.snapshot['reviews'] = []
        self.snapshot['daily_charges'] = [dict(repository='EXAMPLE/private-project', number=n,
                                               day='2026-10-18') for n in range(2, 12)]
        self.assertFalse(self.run_queue()['selected'])
        self.assertTrue(self.run_queue()['blocked'])

    def test_cli_status_and_invalid_json(self):
        good = subprocess.run(['python3', str(SCRIPT)], input=json.dumps(dict(config=self.config, snapshot=self.snapshot)), text=True, capture_output=True)
        self.assertEqual(good.returncode, 0)
        bad = subprocess.run(['python3', str(SCRIPT)], input='{', text=True, capture_output=True)
        self.assertEqual(bad.returncode, 2)
        self.assertFalse(json.loads(bad.stdout)['selected'])

    def test_installed_resource_and_private_input_not_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'installed'
            subprocess.run(['bash', str(ROOT/'scripts/sync-project.sh'), '--project', 'router', '--tools', 'codex', '--target', str(target)], check=True, capture_output=True)
            installed = target/'skills/repository-review-source/scripts/select_private_queue.py'
            self.assertEqual(installed.read_bytes(), SCRIPT.read_bytes())
            self.assertTrue((installed.parent.parent/'references/private-queue.md').exists())
            before = sorted(str(p.relative_to(target)) for p in target.rglob('*'))
            result = subprocess.run(['python3', str(installed)], input=json.dumps(dict(config=self.config, snapshot=self.snapshot)), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(before, sorted(str(p.relative_to(target)) for p in target.rglob('*')))


if __name__ == '__main__':
    unittest.main()
