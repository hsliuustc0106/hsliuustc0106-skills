"""Validate the bundled NCU skill without importing helpers or needing a GPU."""

import ast
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ncu-report-skill"


class NcuSkillPackagingTests(unittest.TestCase):
    def test_plugin_discovers_ncu_entrypoint(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        entrypoints = {
            path.resolve()
            for directory in manifest["skills"]
            for path in (ROOT / directory).rglob("SKILL.md")
        }
        self.assertIn((SKILL / "SKILL.md").resolve(), entrypoints)

    def test_local_markdown_links_resolve_inside_bundle(self):
        checked = 0
        for document in SKILL.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                path = (document.parent / unquote(url.path)).resolve()
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(
                        path == SKILL.resolve() or SKILL.resolve() in path.parents
                    )
                    self.assertTrue(path.exists())
                checked += 1
        self.assertGreater(checked, 0)

    def test_python_helpers_parse_without_execution(self):
        helpers = list((SKILL / "helpers").glob("*.py"))
        self.assertTrue(helpers)
        for helper in helpers:
            with self.subTest(helper=helper.name):
                ast.parse(helper.read_text(), filename=str(helper))

    def test_license_and_non_python_assets_are_present(self):
        license_text = (SKILL / "LICENSE").read_text()
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 hanlab", license_text)
        for relative in (
            "helpers/harness_template.cu",
            "helpers/safetensors_loader.h",
            "blackwell-cuda-programming.md",
        ):
            with self.subTest(asset=relative):
                self.assertGreater((SKILL / relative).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
