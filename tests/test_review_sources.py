"""Offline canonical-source and installed-loader behavior."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/repository-review-source'
spec = importlib.util.spec_from_file_location('source_loader', SOURCE / 'scripts/load_source.py')
loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loader)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'checkout'
        self.root.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Offline test')
        self.git('remote', 'add', 'origin', 'https://github.com/ThinkFlowLab/nanodot.git')
        self.file = self.root / '.agents/skills/nanodot-review/SKILL.md'
        self.file.parent.mkdir(parents=True)
        self.file.write_text('---\nname: nanodot-review\ndescription: Test fixture.\n---\nCanonical fixture\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()

    def test_exact_source_and_version(self):
        result = loader.load('nanodot', self.root)
        self.assertEqual(result['skill'], self.file.read_text())
        self.assertEqual(result['sha256'], hashlib.sha256(self.file.read_bytes()).hexdigest())
        self.assertEqual(result['commit'], self.git('rev-parse', 'HEAD'))
        self.assertFalse(result['working_tree_dirty'])
        self.file.write_text(self.file.read_text() + 'changed\n')
        changed = loader.load('nanodot', self.root)
        self.assertTrue(changed['working_tree_dirty'])
        self.assertNotEqual(changed['sha256'], result['sha256'])

    def test_missing_source_and_wrong_repository_fail(self):
        with self.assertRaises(ValueError):
            loader.load('vllm-omni', self.root)
        self.file.unlink()
        with self.assertRaises(FileNotFoundError):
            loader.load('nanodot', self.root)

    def test_unknown_alias_and_escape_fail(self):
        with self.assertRaises(KeyError):
            loader.load('unknown', self.root)
        config = Path(self.temp.name) / 'local.json'
        config.write_text(json.dumps({'local': {'repository': 'ThinkFlowLab/nanodot', 'path': '../outside'}}))
        with self.assertRaises(ValueError):
            loader.load('local', self.root, config)

    def test_private_config_and_symlink_escape(self):
        config = Path(self.temp.name) / 'local.json'
        config.write_text(json.dumps({'local': {'repository': 'ThinkFlowLab/nanodot', 'path': '.agents/skills/nanodot-review/SKILL.md'}}))
        self.assertEqual(loader.load('local', self.root, config)['skill'], self.file.read_text())
        outside = Path(self.temp.name) / 'outside.md'
        outside.write_text(self.file.read_text())
        self.file.unlink()
        self.file.symlink_to(outside)
        with self.assertRaises(ValueError):
            loader.load('local', self.root, config)

    def test_ignored_untracked_skill_is_not_attributed_to_head(self):
        self.git('rm', '--cached', str(self.file.relative_to(self.root)))
        (self.root / '.gitignore').write_text('.agents/\n')
        self.git('add', '.gitignore')
        self.git('commit', '-qm', 'ignore source fixture')
        result = loader.load('nanodot', self.root)
        self.assertTrue(result['working_tree_dirty'])
        self.assertFalse(result['source_tracked_at_head'])

    def test_installer_preflights_ancestor_collisions(self):
        for kind in ('symlink', 'regular-file'):
            target = Path(self.temp.name) / kind
            target.mkdir()
            outside = Path(self.temp.name) / ('outside-' + kind)
            outside.mkdir()
            if kind == 'symlink':
                (target / 'skills').symlink_to(outside, target_is_directory=True)
            else:
                (target / 'skills').write_text('local file')
            result = subprocess.run(['bash', str(ROOT / 'scripts/sync-project.sh'), '--project', 'router', '--tools', 'codex', '--target', str(target), '--force'], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((target / 'AGENTS.md').exists())
            self.assertEqual(list(outside.iterdir()), [])

    def test_cursor_discovery_points_to_project_loader(self):
        for project in ('router', 'sciencediscovery', 'system1-omni', 'afd-plugin', 'vllm-omni', 'nanodot'):
            target = Path(self.temp.name) / ('cursor-' + project)
            subprocess.run(['bash', str(ROOT / 'scripts/sync-project.sh'), '--project', project, '--tools', 'cursor', '--target', str(target)], check=True, capture_output=True)
            rule = (target / '.cursor/rules' / (project + '.mdc')).read_text()
            self.assertIn('skills/' + project + '-review/SKILL.md', rule)
            self.assertTrue((target / 'skills' / (project + '-review') / 'SKILL.md').is_file())

    def test_discovery_and_install_all_tools(self):
        manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        discovered = {p.parent.name for folder in manifest['skills'] for p in (ROOT / folder).glob('*/SKILL.md')}
        aliases = json.loads((SOURCE / 'sources.json').read_text())
        for alias in aliases:
            self.assertIn(alias + '-review', discovered)
        for tool in ('codex', 'claude', 'cursor'):
            target = Path(self.temp.name) / tool
            cmd = ['bash', str(ROOT / 'scripts/sync-project.sh'), '--project', 'router', '--tools', tool, '--target', str(target)]
            subprocess.run(cmd, check=True, capture_output=True)
            subprocess.run(cmd, check=True, capture_output=True)
            installed = target / 'skills/repository-review-source/scripts/load_source.py'
            result = subprocess.run(['python3', str(installed), 'nanodot', '--checkout', str(self.root)], check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(result.stdout)['skill'], self.file.read_text())
            (target / 'skills/router-review/SKILL.md').write_text('existing change')
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual((target / 'skills/router-review/SKILL.md').read_text(), 'existing change')


if __name__ == '__main__':
    unittest.main()
