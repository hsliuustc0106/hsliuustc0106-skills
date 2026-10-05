"""Offline packaging checks; scenarios are separate behavioral forward tests."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "tech-blog-post"


class TechBlogPackageTests(unittest.TestCase):
    def test_discovered_by_existing_plugin(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        roots = [(ROOT / path).resolve() for path in manifest["skills"]]
        self.assertTrue(any(root in SKILL.resolve().parents for root in roots))

    def test_frontmatter_identity(self):
        text = (SKILL / "SKILL.md").read_text()
        frontmatter = text.split("---", 2)[1]
        fields = dict(line.split(":", 1) for line in frontmatter.strip().splitlines())
        self.assertEqual(fields["name"].strip(), SKILL.name)
        self.assertTrue(fields["description"].strip())

    def test_local_reference_graph_is_complete_and_reachable(self):
        pending = [SKILL / "SKILL.md"]
        visited = set()
        while pending:
            source = pending.pop()
            if source in visited:
                continue
            visited.add(source)
            for target in re.findall(r"\]\(([^)]+)\)", source.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                path = (source.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(path.is_file(), f"Missing reference: {source}: {target}")
                self.assertIn(SKILL.resolve(), path.parents)
                if path.suffix == ".md":
                    pending.append(path)
        self.assertTrue(set((SKILL / "references").glob("*.md")) <= visited)

    def test_legacy_profiles_remain_packaged(self):
        for profile in ("markdown", "nextjs-site", "zhihu"):
            self.assertTrue((SKILL / "references" / (profile + ".md")).is_file())


if __name__ == "__main__":
    unittest.main()
