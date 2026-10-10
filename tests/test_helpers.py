"""Offline project installer regression tests; domain helpers live in their repos."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

    def run_script(self, script, *args, data=None):
        return subprocess.run(
            ["bash", str(script), *args],
            input=data,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

    def sync(self, *args):
        return self.run_script(
            ROOT / "scripts/sync-project.sh",
            "--project",
            "vllm-omni",
            "--target",
            str(self.root / "project"),
            *args,
        )

    def test_install_preserves_conflicts_before_writing(self):
        target = self.root / "project"
        target.mkdir()
        (target / "CLAUDE.md").write_text("Local instructions\n")
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "CLAUDE.md").read_text(), "Local instructions\n")
        self.assertFalse((target / "AGENTS.md").exists())

    def test_install_force_replaces_conflicts_and_is_repeatable(self):
        target = self.root / "project"
        target.mkdir()
        (target / "AGENTS.md").write_text("Local instructions\n")
        result = self.sync("--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (target / "AGENTS.md").read_bytes(), (ROOT / "AGENTS.md").read_bytes()
        )
        result = self.sync()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_install_includes_instruction_dependencies(self):
        result = self.sync("--tools", "codex")
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.root / "project"
        for skill in (
            "vllm-guidelines",
            "vllm-omni-guidelines",
            "vllm-omni-review",
            "afd-plugin-guidelines",
            "vllm-omni-cookbook-guidelines",
        ):
            for source in (ROOT / "skills" / skill).rglob("*"):
                if (source.is_file() and source.name != "review-sources.local.json"
                        and source.suffix != ".pyc" and "__pycache__" not in source.parts):
                    self.assertEqual(
                        (target / source.relative_to(ROOT)).read_bytes(),
                        source.read_bytes(),
                    )

    def test_invalid_tool_does_not_partially_install(self):
        result = self.sync("--tools", "codex,unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "project/AGENTS.md").exists())

    def test_cursor_only_installs_review_dependency_without_agents(self):
        result = self.sync("--tools", "cursor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "project/AGENTS.md").exists())
        self.assertTrue(
            (self.root / "project/skills/vllm-omni-review/SKILL.md").is_file()
        )

    def test_force_does_not_follow_instruction_symlink(self):
        target = self.root / "project"
        target.mkdir()
        original = self.root / "original.md"
        original.write_text("Local instructions\n")
        (target / "AGENTS.md").symlink_to(original)
        result = self.sync("--force")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(original.read_text(), "Local instructions\n")
