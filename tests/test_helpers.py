"""Offline project installer regression tests; domain helpers live in their repos."""
import os
import re
import shutil
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

    def sync_generic(self, target, *args):
        return self.run_script(
            ROOT / "scripts/sync-project.sh",
            "--project", "generic", "--target", str(target), *args,
        )

    def test_generic_profile_installs_only_shared_skills_for_each_tool(self):
        for tool in ("codex", "claude", "cursor", "skills"):
            with self.subTest(tool=tool):
                target = self.root / tool
                result = self.sync_generic(target, "--tools", tool)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    {path.name for path in (target / "skills").iterdir()},
                    {"agentic-coding-guidelines", "repository-maintenance", "repository-review-source"},
                )
                self.assertTrue((target / "skills/repository-maintenance/SKILL.md").is_file())
                self.assertTrue((target / "skills/repository-review-source/scripts/load_source.py").is_file())
                self.assertEqual((target / "AGENTS.md").exists(), tool in ("codex", "claude"))
                self.assertEqual((target / "CLAUDE.md").exists(), tool == "claude")
                self.assertEqual((target / ".cursor/rules/agentic-coding-guidelines.mdc").exists(), tool == "cursor")
                if tool in ("codex", "claude"):
                    self.assertEqual((target / "AGENTS.md").read_bytes(),
                                     (ROOT / "templates/generic/AGENTS.md").read_bytes())
                result = self.sync_generic(target, "--tools", tool)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_skills_only_preserves_local_mapping_even_on_update(self):
        target = self.root / "user-home"
        mapping = target / "skills/repository-review-source/review-sources.local.json"
        mapping.parent.mkdir(parents=True)
        mapping.write_text("private local mapping\n")
        result = self.sync_generic(target, "--tools", "skills")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(mapping.read_text(), "private local mapping\n")
        (target / "skills/repository-maintenance/SKILL.md").write_text("outdated\n")
        result = self.sync_generic(target, "--tools", "skills")
        self.assertNotEqual(result.returncode, 0)
        result = self.sync_generic(target, "--tools", "skills", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(mapping.read_text(), "private local mapping\n")
        self.assertEqual((target / "skills/repository-maintenance/SKILL.md").read_bytes(),
                         (ROOT / "skills/repository-maintenance/SKILL.md").read_bytes())

    def test_generic_template_conflict_is_preflighted_and_force_uses_template(self):
        target = self.root / "generic-conflict"
        target.mkdir()
        (target / "AGENTS.md").write_text("Local instructions\n")
        result = self.sync_generic(target, "--tools", "claude")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "AGENTS.md").read_text(), "Local instructions\n")
        self.assertFalse((target / "CLAUDE.md").exists())
        self.assertFalse((target / "skills").exists())
        result = self.sync_generic(target, "--tools", "claude", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / "AGENTS.md").read_bytes(),
                         (ROOT / "templates/generic/AGENTS.md").read_bytes())
        self.assertEqual((target / "CLAUDE.md").read_bytes(),
                         (ROOT / "templates/generic/CLAUDE.md").read_bytes())

    def test_missing_required_skill_aborts_before_installation(self):
        for missing in ("directory", "entrypoint", "skill-symlink", "entrypoint-symlink"):
            with self.subTest(missing=missing):
                source = self.root / ("source-" + missing)
                target = self.root / ("target-" + missing)
                (source / "scripts").mkdir(parents=True)
                (source / "skills").mkdir()
                shutil.copy2(ROOT / "scripts/sync-project.sh", source / "scripts")
                shutil.copytree(ROOT / "templates", source / "templates")
                for skill in ("repository-review-source", "agentic-coding-guidelines"):
                    shutil.copytree(ROOT / "skills" / skill, source / "skills" / skill)
                skill = source / "skills/repository-maintenance"
                if missing == "entrypoint":
                    skill.mkdir()
                elif missing == "skill-symlink":
                    skill.symlink_to(ROOT / "skills/repository-maintenance", target_is_directory=True)
                elif missing == "entrypoint-symlink":
                    skill.mkdir()
                    (skill / "SKILL.md").symlink_to(ROOT / "skills/repository-maintenance/SKILL.md")
                result = self.run_script(source / "scripts/sync-project.sh",
                                         "--project", "generic", "--tools", "codex",
                                         "--target", str(target))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Missing required skill entrypoint", result.stderr)
                self.assertFalse((target / "AGENTS.md").exists())
                self.assertFalse((target / "skills").exists())

    def test_skill_enumeration_failure_aborts_before_installation(self):
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        find = fake_bin / "find"
        find.write_text("#!/bin/sh\nprintf 'simulated find failure\\n' >&2\nexit 2\n")
        find.chmod(0o755)
        env = dict(self.env, PATH=str(fake_bin) + os.pathsep + os.defpath)
        target = self.root / "failed-enumeration"
        result = subprocess.run(
            ["bash", str(ROOT / "scripts/sync-project.sh"), "--project", "generic",
             "--tools", "codex", "--target", str(target)],
            env=env, text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot enumerate skill resources", result.stderr)
        self.assertFalse((target / "AGENTS.md").exists())
        self.assertFalse((target / "skills").exists())

    def test_installed_skill_entrypoints_can_reach_shared_guidance(self):
        reviews = ("afd-plugin", "nanodot", "router", "sciencediscovery",
                   "system1-omni", "vllm-omni")
        for project in ("generic", "vllm-omni"):
            for tool in ("codex", "cursor"):
                with self.subTest(project=project, tool=tool):
                    target = self.root / (project + "-" + tool)
                    result = self.run_script(ROOT / "scripts/sync-project.sh",
                                             "--project", project, "--tools", tool,
                                             "--target", str(target))
                    self.assertEqual(result.returncode, 0, result.stderr)
                    skills = target / "skills"
                    documents = [skills / "repository-maintenance/SKILL.md",
                                 skills / "agentic-coding-guidelines/SKILL.md",
                                 skills / "repository-maintenance/references/project-reviews.md"]
                    projects = skills / "repository-maintenance/references/projects"
                    documents += [projects / name / "review.md" for name in reviews]
                    documents += [projects / name / "references/maintenance.md" for name in reviews]
                    documents.append(projects / "personal-skills/review.md")
                    for document in documents:
                        links = re.findall(r"\]\(([^)]+)\)", document.read_text())
                        if (document.name == "maintenance.md" and
                                document.parent.parent.name != "system1-omni"):
                            self.assertIn("../../../daily-label-queue.md", links)
                        for link in links:
                            if "://" in link or link.startswith("#"):
                                continue
                            relative, _, anchor = link.partition("#")
                            destination = document.parent / relative
                            self.assertTrue(destination.is_file(), (document, link))
                            if anchor:
                                headings = re.findall(r"^#+\s+(.+)$", destination.read_text(), re.M)
                                slugs = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                                         for heading in headings}
                                self.assertIn(anchor, slugs, (document, link))

    def test_cursor_project_rules_reach_shared_development_guidance(self):
        projects = {
            "vllm": "inference-engines-and-kernels",
            "vllm-omni": "multimodal-paths",
            "afd-plugin": "plugin-and-host-integration",
            "vllm-omni-cookbook": "tutorials-and-examples",
        }
        for project, section in projects.items():
            with self.subTest(project=project):
                target = self.root / ("cursor-" + project)
                result = self.run_script(ROOT / "scripts/sync-project.sh",
                                         "--project", project, "--tools", "cursor",
                                         "--target", str(target))
                self.assertEqual(result.returncode, 0, result.stderr)
                guidance = "skills/repository-maintenance/references/development.md"
                self.assertIn(guidance + "#" + section,
                              (target / ".cursor/rules" / (project + ".mdc")).read_text())
                self.assertTrue((target / guidance).is_file())

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
            "agentic-coding-guidelines",
            "repository-maintenance",
            "repository-review-source",
        ):
            self.assertTrue((ROOT / "skills" / skill / "SKILL.md").is_file())
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
            (self.root / "project/skills/repository-maintenance/references/projects/vllm-omni/review.md").is_file()
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
