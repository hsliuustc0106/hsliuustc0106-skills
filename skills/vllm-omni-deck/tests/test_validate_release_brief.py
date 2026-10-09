"""Regression tests for stable-release deck evidence validation."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from validate_release_brief import validate_release_brief

FIXTURE = Path(__file__).parent / "fixtures" / "release-brief-v026.json"


class ReleaseBriefTests(unittest.TestCase):
    """Exercise release evidence, scope, and layout guardrails."""

    def setUp(self) -> None:
        """Load a clean historical-release fixture for each test."""

        self.brief = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def validate(self) -> tuple[list[str], list[str]]:
        """Validate a defensive copy of the mutable test fixture."""

        return validate_release_brief(copy.deepcopy(self.brief))

    def test_v026_regression_fixture_is_valid(self) -> None:
        """The intended preserve, split, roadmap, and appendix decisions pass."""

        errors, warnings = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_rejects_stale_quantitative_carry_forward(self) -> None:
        """Old benchmark evidence must be explicitly revalidated."""

        qwen = self.brief["highlights"][2]
        qwen["revalidated_for_release"] = False
        errors, _ = self.validate()
        self.assertTrue(any("without release revalidation" in error for error in errors))

    def test_rejects_incomplete_benchmark_context(self) -> None:
        """A performance headline must retain its hardware and other conditions."""

        del self.brief["highlights"][2]["benchmark"]["hardware"]
        errors, _ = self.validate()
        self.assertTrue(any("benchmark.hardware" in error for error in errors))

    def test_issue_alone_does_not_prove_shipment(self) -> None:
        """An issue may support roadmap context, not a tagged release claim."""

        h3 = self.brief["highlights"][1]
        h3["release_relation"] = "in_tag"
        h3.pop("presentation_label")
        errors, _ = self.validate()
        self.assertTrue(any("proves shipment" in error for error in errors))

    def test_source_must_be_verified_in_target_tag(self) -> None:
        """A merged-looking source is insufficient without a tag audit result."""

        self.brief["highlights"][0]["sources"][0]["included_in_target_tag"] = False
        errors, _ = self.validate()
        self.assertTrue(any("proves shipment" in error for error in errors))

    def test_requires_visible_roadmap_label(self) -> None:
        """Selected post-tag work must be visibly distinguished on-slide."""

        self.brief["highlights"][1]["presentation_label"] = "Model optimization"
        errors, _ = self.validate()
        self.assertTrue(any("visibly say roadmap" in error for error in errors))

    def test_locked_slide_cannot_be_updated(self) -> None:
        """The release delta cannot silently mutate the general introduction."""

        self.brief["slides"][0]["action"] = "update"
        errors, _ = self.validate()
        self.assertTrue(any("locked and must use action 'preserve'" in error for error in errors))

    def test_requires_exemplar_driven_layout_contract(self) -> None:
        """Added or updated slides must record approved placement constraints."""

        del self.brief["slides"][1]["layout"]["exemplar_slide_id"]
        errors, _ = self.validate()
        self.assertTrue(any("exemplar_slide_id" in error for error in errors))

    def test_rejects_distorted_asset_fallback(self) -> None:
        """A target-compatible raster fallback must preserve source proportions."""

        figure = self.brief["highlights"][2]["figures"][0]
        figure["derivative"]["aspect_ratio"] = 1.2
        errors, _ = self.validate()
        self.assertTrue(any("preserve aspect ratio" in error for error in errors))

    def test_warns_when_mechanism_and_results_are_not_split(self) -> None:
        """Dense evidence should trigger the successful two-slide pattern."""

        self.brief["highlights"][0]["presentation_pattern"] = "single_slide"
        errors, warnings = self.validate()
        self.assertEqual(errors, [])
        self.assertTrue(any("split mechanism" in warning for warning in warnings))

    def test_malformed_nested_values_return_errors(self) -> None:
        """Untrusted JSON values must not crash the validator."""

        self.brief["slides"][1]["action"] = []
        self.brief["instructions"][0]["slide_keys"] = [{}]
        self.brief["highlights"][0]["decision"] = []
        self.brief["highlights"][0]["sources"][0]["kind"] = []
        errors, _ = self.validate()
        self.assertGreaterEqual(len(errors), 4)


if __name__ == "__main__":
    unittest.main()
