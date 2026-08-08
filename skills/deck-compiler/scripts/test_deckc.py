#!/usr/bin/env python3
"""Focused regression tests for the minimal deck compiler."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURE_DIR = SCRIPT_DIR / "fixtures"
MODULE_PATH = SCRIPT_DIR / "deckc.py"
MODULE_SPEC = importlib.util.spec_from_file_location("deckc", MODULE_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
deckc = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = deckc
MODULE_SPEC.loader.exec_module(deckc)


def load_fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def codes(diagnostics) -> set[str]:
    return {item.code for item in diagnostics}


def spec_for_profile(profile_name: str, profile: dict) -> dict:
    groups = profile["required_role_groups"]
    order = [group["id"] for group in groups]
    return {
        "schema_version": 1,
        "deck": {
            "id": f"{profile_name}-example",
            "title": f"{profile_name} example",
            "audience": "Reviewers",
            "objective": "Exercise the narrative profile",
            "language": "en",
        },
        "narrative": {
            "profile": profile_name,
            "thesis": "The narrative is complete and ordered.",
        },
        "slides": {
            "order": order,
            "items": {
                group["id"]: {
                    "title": group["id"].replace("-", " ").title(),
                    "purpose": "Fill the required narrative role.",
                    "takeaway": "Each slide has one explicit job.",
                    "narrative_roles": [group["any_of"][0]],
                }
                for group in groups
            },
        },
    }


class DeckCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = deckc.load_json(deckc.DEFAULT_SCHEMA)
        cls.profiles = deckc.load_yaml(deckc.DEFAULT_PROFILES)

    def lint(self, spec: dict):
        return deckc.lint_spec(spec, self.schema, self.profiles)

    def test_three_cross_domain_language_fixtures_pass(self) -> None:
        fixtures = [
            "valid-executive-strategy.yaml",
            "valid-technical-deep-dive.yaml",
            "valid-product-update-zh.yaml",
        ]
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                self.assertFalse(codes(self.lint(load_fixture(fixture))))

    def test_every_builtin_profile_has_a_valid_minimal_shape(self) -> None:
        for name, profile in self.profiles["profiles"].items():
            with self.subTest(profile=name):
                spec = spec_for_profile(name, profile)
                self.assertFalse(codes(self.lint(spec)))

    def test_narrative_missing_order_custom_and_unknown_profiles(self) -> None:
        base = load_fixture("valid-executive-strategy.yaml")
        missing = copy.deepcopy(base)
        missing["slides"]["items"]["how-to-win"]["narrative_roles"] = ["support"]
        self.assertIn("missing-narrative-role", codes(self.lint(missing)))

        misordered = copy.deepcopy(base)
        misordered["slides"]["order"] = [
            "decision",
            *[item for item in base["slides"]["order"] if item != "decision"],
        ]
        self.assertIn("narrative-order", codes(self.lint(misordered)))

        custom = copy.deepcopy(base)
        custom["narrative"] = {
            "profile": "custom",
            "thesis": "Only two roles are required.",
            "required_roles": ["why-now", "decision"],
        }
        self.assertFalse(codes(self.lint(custom)))

        unknown = copy.deepcopy(base)
        unknown["narrative"]["profile"] = "unknown-profile"
        self.assertIn("unknown-narrative-profile", codes(self.lint(unknown)))

    def test_structure_references_and_dependency_cycles_are_checked(self) -> None:
        base = load_fixture("valid-executive-strategy.yaml")
        mismatch = copy.deepcopy(base)
        mismatch["slides"]["order"].remove("decision")
        self.assertIn("slide-order-mismatch", codes(self.lint(mismatch)))

        unknown = copy.deepcopy(base)
        unknown["slides"]["items"]["decision"]["dependencies"] = [
            {"target": "missing-slide"}
        ]
        self.assertIn("unknown-dependency", codes(self.lint(unknown)))

        cycle = copy.deepcopy(base)
        cycle["slides"]["items"]["why-now"]["dependencies"] = [{"target": "decision"}]
        self.assertIn("dependency-cycle", codes(self.lint(cycle)))

    def test_impact_is_transitive_and_respects_propagation(self) -> None:
        spec = load_fixture("valid-executive-strategy.yaml")
        report = deckc.impact_report(spec, ["why-now"])
        self.assertEqual(report["affected"], spec["slides"]["order"])
        self.assertEqual(
            report["dependent"],
            spec["slides"]["order"][1:],
        )

        local = copy.deepcopy(spec)
        local["slides"]["items"]["what-changes"]["dependencies"][0]["propagates"] = (
            False
        )
        report = deckc.impact_report(local, ["why-now"])
        self.assertEqual(report["affected"], ["why-now"])
        with self.assertRaises(ValueError):
            deckc.impact_report(spec, ["missing-slide"])

    def test_compile_is_deterministic_and_derives_page_numbers(self) -> None:
        spec = load_fixture("valid-product-update-zh.yaml")
        first = deckc.compile_deck(spec)
        second = deckc.compile_deck(copy.deepcopy(spec))
        self.assertEqual(first, second)
        self.assertEqual(
            [slide["page_number"] for slide in first["slides"]],
            [1, 2, 3, 4, 5],
        )
        self.assertEqual(
            [slide["id"] for slide in first["slides"]],
            spec["slides"]["order"],
        )

    def test_non_json_values_are_rejected_and_unicode_is_preserved(self) -> None:
        valid = load_fixture("valid-product-update-zh.yaml")
        valid["extensions"] = {"emoji": "有效 ✅"}
        self.assertFalse(codes(self.lint(valid)))

        invalid_values = [
            {1: "one"},
            float("nan"),
            "\ud800",
            ("tuple",),
        ]
        for invalid in invalid_values:
            with self.subTest(value_type=type(invalid).__name__):
                spec = copy.deepcopy(valid)
                spec["extensions"] = {"invalid": invalid}
                self.assertIn("non-json-value", codes(self.lint(spec)))

    def test_cli_lint_impact_and_compile(self) -> None:
        valid = FIXTURE_DIR / "valid-executive-strategy.yaml"
        lint = subprocess.run(
            [sys.executable, MODULE_PATH, "lint", valid],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(lint.returncode, 0, lint.stderr)

        impact = subprocess.run(
            [
                sys.executable,
                MODULE_PATH,
                "impact",
                valid,
                "--changed",
                "why-now",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(impact.returncode, 0, impact.stderr)
        self.assertEqual(
            json.loads(impact.stdout)["affected"],
            load_fixture("valid-executive-strategy.yaml")["slides"]["order"],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "compiled.json"
            compiled = subprocess.run(
                [
                    sys.executable,
                    MODULE_PATH,
                    "compile",
                    valid,
                    "--output",
                    output,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            self.assertEqual(
                json.loads(output.read_text())["slides"][0]["id"], "why-now"
            )


if __name__ == "__main__":
    unittest.main()
