#!/usr/bin/env python3
"""Regression tests for the deck compiler foundation."""

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


def error_codes(diagnostics) -> set[str]:
    return {item.code for item in diagnostics if item.level == "error"}


def add_operating_model_change(spec: dict) -> dict:
    baseline = deckc.build_manifest(spec)
    spec["deck"]["operation"] = "revise"
    blueprint = copy.deepcopy(spec["slides"]["items"]["operating-model"])
    blueprint["title"] = "Operate through ownership, co-design, and measurable gates"
    spec["change_sets"] = [
        {
            "id": "revise-operating-model",
            "status": "proposed",
            "rationale": "Clarify how the platform will be operated.",
            "baseline_fingerprint": baseline["manifest_fingerprint"],
            "target_order": spec["slides"]["order"],
            "modify": [
                {
                    "slide": "operating-model",
                    "blueprint": blueprint,
                }
            ],
            "preserve": ["context", "roadmap"],
        }
    ]
    return baseline


def set_target_fingerprints(
    spec: dict,
    baseline: dict,
    change_id: str,
) -> None:
    change_set = deckc.find_change_set(spec, change_id)
    projected = deckc.projected_spec(spec, change_set, baseline)
    target_release = deckc.release_fingerprint(projected)
    change_set["target_fingerprint"] = target_release
    change_set["target_manifest_fingerprint"] = deckc.projected_manifest_fingerprint(
        baseline,
        change_set,
        target_release,
    )


def rehash_manifest_history(manifest: dict) -> None:
    history = {
        "retired_slide_ids": manifest["retired_slide_ids"],
        "applied_changes": manifest["applied_changes"],
    }
    manifest["history_fingerprint"] = deckc.fingerprint(history)
    manifest["manifest_fingerprint"] = deckc.manifest_root_fingerprint(
        manifest["schema_version"],
        manifest["release_fingerprint"],
        manifest["history_fingerprint"],
    )


class DeckCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = deckc.load_json(deckc.DEFAULT_SCHEMA)
        cls.profiles = deckc.load_yaml(deckc.DEFAULT_PROFILES)

    def lint(self, spec: dict):
        return deckc.lint_spec(spec, self.schema, self.profiles)

    def validate(self, spec: dict):
        return deckc.validate_spec(spec, self.schema)

    def test_generalized_fixtures_pass(self) -> None:
        fixtures = [
            "valid-executive-strategy.yaml",
            "valid-technical-deep-dive.yaml",
            "valid-research-summary.yaml",
            "valid-product-update-zh.yaml",
            "valid-proposal.yaml",
        ]
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                diagnostics = self.lint(load_fixture(fixture))
                self.assertFalse(error_codes(diagnostics), diagnostics)

    def test_missing_strategy_stage_fails(self) -> None:
        diagnostics = self.lint(load_fixture("missing-how-to-win.yaml"))
        self.assertIn("missing-narrative-role", error_codes(diagnostics))
        self.assertTrue(
            any("how-to-win" in item.message for item in diagnostics),
            diagnostics,
        )

    def test_custom_profile_uses_declared_roles(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["profiles"]["narrative"] = "custom-review"
        spec["narrative"]["required_roles"] = ["problem", "ask"]
        diagnostics = self.lint(spec)
        self.assertFalse(error_codes(diagnostics), diagnostics)

    def test_narrative_order_is_checked(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["slides"]["order"] = [
            "solution",
            "problem",
            "value",
            "plan",
            "ask",
        ]
        diagnostics = self.lint(spec)
        self.assertIn("narrative-order", error_codes(diagnostics))

    def test_dependency_cycle_is_rejected(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["slides"]["items"]["problem"]["dependencies"] = [
            {"target": "ask", "relation": "depends-on"}
        ]
        spec["slides"]["items"]["ask"]["dependencies"] = [
            {"target": "problem", "relation": "depends-on"}
        ]
        diagnostics = self.validate(spec)
        self.assertIn("dependency-cycle", error_codes(diagnostics))

    def test_claim_contracts_are_enforced(self) -> None:
        cases = [
            (
                {"statement": "A fact.", "classes": ["fact"]},
                "fact-needs-source",
            ),
            (
                {"statement": "An inference.", "classes": ["inference"]},
                "inference-needs-confidence",
            ),
            (
                {"statement": "A target.", "classes": ["target"]},
                "target-needs-acceptance",
            ),
            (
                {"statement": "A comparison.", "classes": ["comparative"]},
                "comparison-needs-envelope",
            ),
            (
                {"statement": "A number.", "classes": ["quantitative"]},
                "quantitative-needs-measurement",
            ),
            (
                {"statement": "Sample data.", "classes": ["illustrative"]},
                "illustrative-needs-label",
            ),
        ]
        for claim, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                spec = load_fixture("valid-proposal.yaml")
                spec["claims"] = {"test-claim": claim}
                spec["slides"]["items"]["value"]["claim_ids"] = ["test-claim"]
                diagnostics = self.lint(spec)
                self.assertIn(expected_code, error_codes(diagnostics))

    def test_claim_term_rules_are_configurable(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["qa"] = {
            "claim_term_rules": [
                {
                    "pattern": "(?i)reusable",
                    "required_class": "comparative",
                }
            ]
        }
        diagnostics = self.lint(spec)
        self.assertIn("claim-term-needs-contract", error_codes(diagnostics))

    def test_impact_is_transitive_and_preserves_authorization_scope(self) -> None:
        spec = load_fixture("valid-executive-strategy.yaml")
        baseline = add_operating_model_change(spec)
        diagnostics, projected = deckc.impact_diagnostics(
            spec,
            baseline,
            "revise-operating-model",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        self.assertIsNotNone(projected)
        report = deckc.impact_report(
            spec,
            "revise-operating-model",
            baseline,
        )
        self.assertEqual(report["changed"], ["operating-model"])
        self.assertEqual(report["dependent_reviews"], ["roadmap", "decision"])
        self.assertEqual(report["preserved_reviews"], ["roadmap"])
        self.assertEqual(report["authorization_required"], ["operating-model"])
        self.assertEqual(
            report["locked_dependent_reviews"],
            ["roadmap", "decision"],
        )

        approved = copy.deepcopy(spec)
        approved["change_sets"][0]["status"] = "approved"
        approved_report = deckc.impact_report(
            approved,
            "revise-operating-model",
            baseline,
        )
        self.assertEqual(approved_report["authorization_required"], [])

    def test_impact_rejects_preapplied_slide_and_semantic_drift(self) -> None:
        for mutation in ("slide", "narrative"):
            with self.subTest(mutation=mutation):
                spec = load_fixture("valid-executive-strategy.yaml")
                baseline = add_operating_model_change(spec)
                if mutation == "slide":
                    spec["slides"]["items"]["operating-model"]["title"] = (
                        "Pre-applied candidate"
                    )
                else:
                    spec["narrative"]["thesis"] = "Pre-applied semantic drift."
                diagnostics, projected = deckc.impact_diagnostics(
                    spec,
                    baseline,
                    "revise-operating-model",
                    self.schema,
                    self.profiles,
                )
                self.assertIn("preapplied-drift", error_codes(diagnostics))
                self.assertIsNone(projected)

    def test_explicit_semantic_target_is_reported_and_authorized(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        proposed = copy.deepcopy(baseline_spec)
        proposed["deck"]["operation"] = "revise"
        target_semantics = deckc.semantic_payload(baseline_spec)
        target_semantics["narrative"]["thesis"] = (
            "A bounded automation stage can reduce repeated manual checks."
        )
        proposed["change_sets"] = [
            {
                "id": "revise-thesis",
                "status": "proposed",
                "rationale": "Clarify the strategic thesis.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": proposed["slides"]["order"],
                "target_semantics": target_semantics,
                "review": proposed["slides"]["order"],
            }
        ]
        diagnostics, projected = deckc.impact_diagnostics(
            proposed,
            baseline,
            "revise-thesis",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        self.assertIsNotNone(projected)
        report = deckc.impact_report(proposed, "revise-thesis", baseline)
        self.assertEqual(report["semantic_changes"], ["narrative"])
        self.assertEqual(
            report["review_required"],
            proposed["slides"]["order"],
        )
        self.assertEqual(
            report["locked_dependent_reviews"],
            proposed["slides"]["order"],
        )

        assert projected is not None
        applied = copy.deepcopy(projected)
        applied["change_sets"] = copy.deepcopy(proposed["change_sets"])
        applied["change_sets"][0]["status"] = "approved"
        applied["change_sets"][0]["target_fingerprint"] = report[
            "projected_release_fingerprint"
        ]
        applied["change_sets"][0]["target_manifest_fingerprint"] = report[
            "projected_manifest_fingerprint"
        ]
        diagnostics = self.lint(applied)
        diagnostics.extend(deckc.release_diagnostics(applied))
        diagnostics.extend(
            deckc.revision_diagnostics(applied, baseline, "revise-thesis")
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)

    def test_claim_change_propagates_to_referencing_locked_slide(self) -> None:
        baseline_spec = load_fixture("valid-research-summary.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        proposed = copy.deepcopy(baseline_spec)
        proposed["deck"]["operation"] = "revise"
        target_semantics = copy.deepcopy(deckc.semantic_payload(baseline_spec))
        target_semantics["claims"]["measured-quality"]["statement"] = (
            "Selective retrieval improves measured answer quality under the "
            "evaluated workload."
        )
        proposed["change_sets"] = [
            {
                "id": "revise-result-claim",
                "status": "proposed",
                "rationale": "Clarify the evaluated claim.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": proposed["slides"]["order"],
                "target_semantics": target_semantics,
            }
        ]
        diagnostics, _ = deckc.impact_diagnostics(
            proposed,
            baseline,
            "revise-result-claim",
            self.schema,
            self.profiles,
        )
        self.assertIn("semantic-review-required", error_codes(diagnostics))
        self.assertTrue(
            any("results" in item.message for item in diagnostics),
            diagnostics,
        )

        proposed["change_sets"][0]["review"] = ["results"]
        diagnostics, _ = deckc.impact_diagnostics(
            proposed,
            baseline,
            "revise-result-claim",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        report = deckc.impact_report(
            proposed,
            "revise-result-claim",
            baseline,
        )
        self.assertEqual(report["review_required"], ["results"])
        self.assertEqual(report["locked_dependent_reviews"], ["results"])
        self.assertEqual(
            report["semantic_entities"]["affected_claims"],
            ["measured-quality"],
        )

    def test_impact_lints_candidate_blueprints_and_rejects_no_ops(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)

        unknown_claim = copy.deepcopy(baseline_spec)
        unknown_claim["deck"]["operation"] = "revise"
        candidate = {
            "title": "Candidate detail",
            "purpose": "Exercise projected validation.",
            "takeaway": "Candidate references must resolve before approval.",
            "claim_ids": ["missing-claim"],
            "status": "approved",
            "locked": True,
        }
        unknown_claim["change_sets"] = [
            {
                "id": "insert-detail",
                "status": "proposed",
                "rationale": "Add supporting detail.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": baseline_spec["slides"]["order"] + ["detail"],
                "insert": [{"slide": "detail", "blueprint": candidate}],
            }
        ]
        diagnostics, _ = deckc.impact_diagnostics(
            unknown_claim,
            baseline,
            "insert-detail",
            self.schema,
            self.profiles,
        )
        self.assertIn("unknown-claim", error_codes(diagnostics))

        no_op = copy.deepcopy(baseline_spec)
        no_op["deck"]["operation"] = "revise"
        no_op["change_sets"] = [
            {
                "id": "noop",
                "status": "proposed",
                "rationale": "Exercise no-op detection.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": no_op["slides"]["order"],
                "modify": [
                    {
                        "slide": "ask",
                        "blueprint": copy.deepcopy(no_op["slides"]["items"]["ask"]),
                    }
                ],
            }
        ]
        diagnostics, _ = deckc.impact_diagnostics(
            no_op,
            baseline,
            "noop",
            self.schema,
            self.profiles,
        )
        self.assertIn("proposal-scope-mismatch", error_codes(diagnostics))

    def test_target_order_is_the_single_reorder_contract(self) -> None:
        baseline_spec = load_fixture("valid-executive-strategy.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        proposed = copy.deepcopy(baseline_spec)
        proposed["deck"]["operation"] = "revise"
        target_order = copy.deepcopy(proposed["slides"]["order"])
        target_order[0], target_order[1] = target_order[1], target_order[0]
        proposed["change_sets"] = [
            {
                "id": "reorder-cover",
                "status": "proposed",
                "rationale": "Open with context before the cover card.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": target_order,
                "reorder": True,
            }
        ]
        diagnostics, _ = deckc.impact_diagnostics(
            proposed,
            baseline,
            "reorder-cover",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        report = deckc.impact_report(proposed, "reorder-cover", baseline)
        self.assertTrue(report["order_changed"])
        self.assertEqual(report["changed"], [])

    def test_manifest_is_deterministic_and_derives_page_numbers(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        first = deckc.build_manifest(spec)
        second = deckc.build_manifest(copy.deepcopy(spec))
        self.assertEqual(first, second)
        self.assertEqual(
            [slide["page_number"] for slide in first["slides"]],
            list(range(1, 6)),
        )
        self.assertEqual(
            [slide["id"] for slide in first["slides"]],
            spec["slides"]["order"],
        )
        self.assertEqual(first["narrative"], spec["narrative"])
        self.assertEqual(first["deck"], spec["deck"])
        self.assertEqual(
            first["slides"][0]["blueprint"], spec["slides"]["items"]["problem"]
        )

    def test_release_rejects_pending_and_unapproved_slides(self) -> None:
        spec = load_fixture("valid-executive-strategy.yaml")
        add_operating_model_change(spec)
        diagnostics = deckc.release_diagnostics(spec)
        self.assertIn("pending-change-set", error_codes(diagnostics))

        draft = load_fixture("valid-proposal.yaml")
        draft["slides"]["items"]["ask"]["status"] = "draft"
        draft["slides"]["items"]["ask"]["locked"] = False
        diagnostics = deckc.release_diagnostics(draft)
        self.assertIn("slide-not-release-approved", error_codes(diagnostics))

    def test_revision_manifest_enforces_exact_approved_diff(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        revised = copy.deepcopy(baseline_spec)
        revised["deck"]["operation"] = "revise"
        blueprint = copy.deepcopy(revised["slides"]["items"]["ask"])
        blueprint["title"] = "Approve the bounded first workflow"
        revised["slides"]["items"]["ask"] = blueprint
        revised["change_sets"] = [
            {
                "id": "revise-ask",
                "status": "approved",
                "rationale": "Make the decision more precise.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": revised["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": copy.deepcopy(blueprint)}],
            }
        ]
        set_target_fingerprints(revised, baseline, "revise-ask")

        diagnostics = self.lint(revised)
        diagnostics.extend(deckc.release_diagnostics(revised))
        diagnostics.extend(deckc.revision_diagnostics(revised, baseline, "revise-ask"))
        self.assertFalse(error_codes(diagnostics), diagnostics)

        unauthorized = copy.deepcopy(revised)
        unauthorized["slides"]["items"]["plan"]["title"] = "Unauthorized edit"
        diagnostics = deckc.revision_diagnostics(unauthorized, baseline, "revise-ask")
        self.assertIn("revision-scope-mismatch", error_codes(diagnostics))

        after_approval = copy.deepcopy(revised)
        after_approval["slides"]["items"]["ask"]["title"] = "Changed after approval"
        diagnostics = self.validate(after_approval)
        self.assertIn("unapplied-modification", error_codes(diagnostics))

        tampered_baseline = copy.deepcopy(baseline)
        tampered_baseline["slides"][0]["blueprint"]["title"] = "Tampered baseline"
        diagnostics = deckc.revision_diagnostics(
            revised, tampered_baseline, "revise-ask"
        )
        self.assertIn("invalid-baseline", error_codes(diagnostics))

    def test_approval_metadata_is_finalized_before_manifest_projection(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        proposed = copy.deepcopy(baseline_spec)
        proposed["deck"]["operation"] = "revise"
        blueprint = copy.deepcopy(proposed["slides"]["items"]["ask"])
        blueprint["title"] = "Approve a finalized bounded workflow"
        proposed["change_sets"] = [
            {
                "id": "finalize-approval",
                "status": "proposed",
                "rationale": "Exercise the two-phase approval commit.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": proposed["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": blueprint}],
            }
        ]

        diagnostics, _ = deckc.impact_diagnostics(
            proposed,
            baseline,
            "finalize-approval",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        preview = deckc.impact_report(proposed, "finalize-approval", baseline)
        self.assertFalse(preview["approval_metadata_bound"])

        proposed["change_sets"][0]["approval"] = {
            "revision": 1,
            "approved_by": "deck-owner",
            "approved_at": "2026-07-29T06:00:00Z",
        }
        diagnostics, projected = deckc.impact_diagnostics(
            proposed,
            baseline,
            "finalize-approval",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        assert projected is not None
        final = deckc.impact_report(proposed, "finalize-approval", baseline)
        self.assertTrue(final["approval_metadata_bound"])
        self.assertNotEqual(
            preview["projected_manifest_fingerprint"],
            final["projected_manifest_fingerprint"],
        )

        stale = copy.deepcopy(proposed)
        stale["slides"] = copy.deepcopy(projected["slides"])
        stale["change_sets"][0]["status"] = "approved"
        stale["change_sets"][0]["target_fingerprint"] = final[
            "projected_release_fingerprint"
        ]
        stale["change_sets"][0]["target_manifest_fingerprint"] = preview[
            "projected_manifest_fingerprint"
        ]
        diagnostics = deckc.revision_diagnostics(
            stale,
            baseline,
            "finalize-approval",
        )
        self.assertIn(
            "approval-metadata-not-finalized",
            error_codes(diagnostics),
        )

        approved = copy.deepcopy(stale)
        approved["change_sets"][0]["target_manifest_fingerprint"] = final[
            "projected_manifest_fingerprint"
        ]
        diagnostics = deckc.revision_diagnostics(
            approved,
            baseline,
            "finalize-approval",
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        manifest = deckc.build_manifest(
            approved,
            baseline=baseline,
            change_id="finalize-approval",
        )
        self.assertEqual(
            manifest["manifest_fingerprint"],
            final["projected_manifest_fingerprint"],
        )

        tampered = copy.deepcopy(approved)
        tampered["change_sets"][0]["approval"]["approved_by"] = "other-owner"
        diagnostics = deckc.revision_diagnostics(
            tampered,
            baseline,
            "finalize-approval",
        )
        self.assertIn(
            "target-manifest-fingerprint-mismatch",
            error_codes(diagnostics),
        )

    def test_proposed_insertion_is_not_preapplied(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        proposed = copy.deepcopy(baseline_spec)
        proposed["deck"]["operation"] = "revise"
        blueprint = {
            "title": "Risks are bounded by the first-stage gates",
            "purpose": "Explain the principal execution risks.",
            "takeaway": "The staged plan limits exposure before wider rollout.",
            "status": "approved",
            "locked": True,
        }
        proposed["change_sets"] = [
            {
                "id": "insert-risks",
                "status": "proposed",
                "rationale": "Make risk explicit before the ask.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": [
                    "problem",
                    "solution",
                    "value",
                    "plan",
                    "risks",
                    "ask",
                ],
                "insert": [
                    {
                        "slide": "risks",
                        "blueprint": blueprint,
                    }
                ],
            }
        ]
        self.assertFalse(error_codes(self.validate(proposed)))

        preapplied = copy.deepcopy(proposed)
        preapplied["slides"]["order"].insert(-1, "risks")
        preapplied["slides"]["items"]["risks"] = blueprint
        diagnostics = self.validate(preapplied)
        self.assertIn("preapplied-insertion", error_codes(diagnostics))

        applied = copy.deepcopy(preapplied)
        applied["change_sets"][0]["status"] = "approved"
        set_target_fingerprints(applied, baseline, "insert-risks")
        diagnostics = self.lint(applied)
        diagnostics.extend(deckc.release_diagnostics(applied))
        diagnostics.extend(
            deckc.revision_diagnostics(applied, baseline, "insert-risks")
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)

    def test_approved_removal_is_preserved_in_manifest_history(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        revised = copy.deepcopy(baseline_spec)
        revised["deck"]["operation"] = "revise"
        revised["slides"]["order"].remove("value")
        del revised["slides"]["items"]["value"]
        revised["slides"]["items"]["solution"]["narrative_roles"] = [
            "solution",
            "value",
        ]
        solution_blueprint = copy.deepcopy(revised["slides"]["items"]["solution"])
        revised["change_sets"] = [
            {
                "id": "remove-value",
                "status": "approved",
                "rationale": "Consolidate value into the solution slide.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": revised["slides"]["order"],
                "modify": [
                    {
                        "slide": "solution",
                        "blueprint": solution_blueprint,
                    }
                ],
                "remove": ["value"],
            }
        ]
        set_target_fingerprints(revised, baseline, "remove-value")

        diagnostics = self.lint(revised)
        diagnostics.extend(deckc.release_diagnostics(revised))
        diagnostics.extend(
            deckc.revision_diagnostics(revised, baseline, "remove-value")
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        manifest = deckc.build_manifest(
            revised,
            baseline=baseline,
            change_id="remove-value",
        )
        self.assertEqual(
            manifest["manifest_fingerprint"],
            revised["change_sets"][0]["target_manifest_fingerprint"],
        )
        self.assertIn("value", manifest["retired_slide_ids"])
        self.assertEqual(manifest["applied_changes"][-1]["id"], "remove-value")

        reuse = copy.deepcopy(revised)
        reuse["change_sets"] = [
            {
                "id": "reuse-value",
                "status": "proposed",
                "rationale": "Exercise retired-ID protection.",
                "baseline_fingerprint": manifest["manifest_fingerprint"],
                "target_order": reuse["slides"]["order"] + ["value"],
                "insert": [
                    {
                        "slide": "value",
                        "blueprint": {
                            "title": "Reused value",
                            "purpose": "Exercise history protection.",
                            "takeaway": "Retired IDs cannot be reused.",
                            "status": "approved",
                            "locked": True,
                        },
                    }
                ],
            }
        ]
        diagnostics, _ = deckc.impact_diagnostics(
            reuse,
            manifest,
            "reuse-value",
            self.schema,
            self.profiles,
        )
        self.assertIn("retired-slide-id", error_codes(diagnostics))

        alternate_history = copy.deepcopy(manifest)
        alternate_history["retired_slide_ids"] = []
        alternate_history["applied_changes"] = []
        history = {"retired_slide_ids": [], "applied_changes": []}
        alternate_history["history_fingerprint"] = deckc.fingerprint(history)
        alternate_history["manifest_fingerprint"] = deckc.manifest_root_fingerprint(
            alternate_history["schema_version"],
            alternate_history["release_fingerprint"],
            alternate_history["history_fingerprint"],
        )
        self.assertEqual(
            alternate_history["release_fingerprint"],
            manifest["release_fingerprint"],
        )
        diagnostics, _ = deckc.impact_diagnostics(
            reuse,
            alternate_history,
            "reuse-value",
            self.schema,
            self.profiles,
        )
        self.assertIn(
            "baseline-fingerprint-mismatch",
            error_codes(diagnostics),
        )

    def test_two_revisions_preserve_applied_history(self) -> None:
        initial_spec = load_fixture("valid-proposal.yaml")
        initial_manifest = deckc.build_manifest(initial_spec)

        first = copy.deepcopy(initial_spec)
        first["deck"]["operation"] = "revise"
        first_blueprint = copy.deepcopy(first["slides"]["items"]["ask"])
        first_blueprint["title"] = "Approve one bounded workflow"
        first["slides"]["items"]["ask"] = copy.deepcopy(first_blueprint)
        first["change_sets"] = [
            {
                "id": "first-revision",
                "status": "approved",
                "rationale": "Clarify the initial ask.",
                "baseline_fingerprint": initial_manifest["manifest_fingerprint"],
                "target_order": first["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": first_blueprint}],
            }
        ]
        set_target_fingerprints(first, initial_manifest, "first-revision")
        self.assertFalse(
            error_codes(
                deckc.revision_diagnostics(
                    first,
                    initial_manifest,
                    "first-revision",
                )
            )
        )
        first_manifest = deckc.build_manifest(
            first,
            baseline=initial_manifest,
            change_id="first-revision",
        )

        second = copy.deepcopy(first)
        second["change_sets"] = []
        second_blueprint = copy.deepcopy(second["slides"]["items"]["ask"])
        second_blueprint["title"] = "Approve one workflow with explicit gates"
        second["change_sets"] = [
            {
                "id": "second-revision",
                "status": "proposed",
                "rationale": "Add the acceptance-gate qualifier.",
                "baseline_fingerprint": first_manifest["manifest_fingerprint"],
                "target_order": second["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": second_blueprint}],
            }
        ]
        diagnostics, projected = deckc.impact_diagnostics(
            second,
            first_manifest,
            "second-revision",
            self.schema,
            self.profiles,
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        assert projected is not None
        second["slides"] = projected["slides"]
        second["change_sets"][0]["status"] = "approved"
        set_target_fingerprints(second, first_manifest, "second-revision")
        diagnostics = deckc.revision_diagnostics(
            second,
            first_manifest,
            "second-revision",
        )
        self.assertFalse(error_codes(diagnostics), diagnostics)
        second_manifest = deckc.build_manifest(
            second,
            baseline=first_manifest,
            change_id="second-revision",
        )
        self.assertEqual(
            [item["id"] for item in second_manifest["applied_changes"]],
            ["first-revision", "second-revision"],
        )
        self.assertFalse(
            error_codes(deckc.baseline_manifest_diagnostics(second_manifest))
        )

    def test_baseline_applied_history_records_are_fully_validated(self) -> None:
        initial_spec = load_fixture("valid-proposal.yaml")
        initial_manifest = deckc.build_manifest(initial_spec)
        revised = copy.deepcopy(initial_spec)
        revised["deck"]["operation"] = "revise"
        blueprint = copy.deepcopy(revised["slides"]["items"]["ask"])
        blueprint["title"] = "Approve a history validation workflow"
        revised["slides"]["items"]["ask"] = copy.deepcopy(blueprint)
        revised["change_sets"] = [
            {
                "id": "history-validation",
                "status": "approved",
                "rationale": "Create a valid applied history record.",
                "baseline_fingerprint": initial_manifest["manifest_fingerprint"],
                "target_order": revised["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": blueprint}],
            }
        ]
        set_target_fingerprints(revised, initial_manifest, "history-validation")
        manifest = deckc.build_manifest(
            revised,
            baseline=initial_manifest,
            change_id="history-validation",
        )
        self.assertFalse(error_codes(deckc.baseline_manifest_diagnostics(manifest)))

        corruptions = {}
        invalid_id = copy.deepcopy(manifest)
        invalid_id["applied_changes"][0]["id"] = []
        corruptions["unhashable-id"] = invalid_id

        missing_field = copy.deepcopy(manifest)
        del missing_field["applied_changes"][0]["rationale"]
        corruptions["missing-field"] = missing_field

        malformed_fingerprint = copy.deepcopy(manifest)
        malformed_fingerprint["applied_changes"][0]["target_fingerprint"] = "bad"
        corruptions["malformed-fingerprint"] = malformed_fingerprint

        duplicate_id = copy.deepcopy(manifest)
        duplicate_id["applied_changes"].append(
            copy.deepcopy(duplicate_id["applied_changes"][0])
        )
        corruptions["duplicate-id"] = duplicate_id

        invalid_action = copy.deepcopy(manifest)
        invalid_action["applied_changes"][0]["modify"][0]["slide"] = []
        corruptions["invalid-action"] = invalid_action

        duplicate_action = copy.deepcopy(manifest)
        duplicate_entry = copy.deepcopy(
            duplicate_action["applied_changes"][0]["modify"][0]
        )
        duplicate_entry["blueprint_fingerprint"] = "0" * 64
        duplicate_action["applied_changes"][0]["modify"].append(duplicate_entry)
        corruptions["duplicate-action-slide"] = duplicate_action

        conflicting_action = copy.deepcopy(manifest)
        conflicting_action["applied_changes"][0]["preserve"] = ["ask"]
        corruptions["conflicting-action"] = conflicting_action

        invalid_target_order = copy.deepcopy(manifest)
        invalid_target_order["applied_changes"][0]["remove"] = ["problem"]
        corruptions["invalid-target-order"] = invalid_target_order

        no_material_action = copy.deepcopy(manifest)
        no_material_action["applied_changes"][0]["modify"] = []
        corruptions["no-material-action"] = no_material_action

        invalid_approval = copy.deepcopy(manifest)
        invalid_approval["applied_changes"][0]["approval"] = {
            "revision": 0,
            "approved_at": "not-a-date",
        }
        corruptions["invalid-approval"] = invalid_approval

        for name, corrupted in corruptions.items():
            with self.subTest(corruption=name):
                rehash_manifest_history(corrupted)
                diagnostics = deckc.baseline_manifest_diagnostics(corrupted)
                self.assertIn("invalid-baseline", error_codes(diagnostics))
                impact_diagnostics, projected = deckc.impact_diagnostics(
                    revised,
                    corrupted,
                    "history-validation",
                    self.schema,
                    self.profiles,
                )
                self.assertIn(
                    "invalid-baseline",
                    error_codes(impact_diagnostics),
                )
                self.assertIsNone(projected)

    def test_change_sets_reject_empty_conflicting_and_legacy_placement_fields(
        self,
    ) -> None:
        base = load_fixture("valid-executive-strategy.yaml")
        add_operating_model_change(base)

        empty = copy.deepcopy(base)
        empty["change_sets"][0]["modify"] = []
        self.assertIn("schema", error_codes(self.validate(empty)))

        conflict = copy.deepcopy(base)
        conflict["change_sets"][0]["remove"] = ["operating-model"]
        diagnostics = self.validate(conflict)
        self.assertIn("change-action-conflict", error_codes(diagnostics))

        legacy_placement = load_fixture("valid-proposal.yaml")
        legacy_placement["change_sets"] = [
            {
                "id": "bad-insert",
                "status": "proposed",
                "rationale": "Exercise anchor validation.",
                "baseline_fingerprint": "0" * 64,
                "target_order": legacy_placement["slides"]["order"] + ["new-slide"],
                "insert": [
                    {
                        "slide": "new-slide",
                        "position": "after",
                        "anchor": "plan",
                        "blueprint": {
                            "title": "New slide",
                            "purpose": "Test validation.",
                            "takeaway": "Self-anchors are invalid.",
                            "status": "approved",
                            "locked": True,
                        },
                    }
                ],
            }
        ]
        diagnostics = self.validate(legacy_placement)
        self.assertIn("schema", error_codes(diagnostics))

    def test_claim_support_must_terminate_in_evidence(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["claims"] = {
            "claim-a": {
                "statement": "Inference A.",
                "classes": ["inference"],
                "confidence": "medium",
                "supporting_claim_ids": ["claim-b"],
            },
            "claim-b": {
                "statement": "Inference B.",
                "classes": ["inference"],
                "confidence": "medium",
                "supporting_claim_ids": ["claim-a"],
            },
        }
        spec["slides"]["items"]["value"]["claim_ids"] = ["claim-a"]
        diagnostics = self.lint(spec)
        self.assertIn("claim-support-cycle", error_codes(diagnostics))
        self.assertIn("inference-support-not-grounded", error_codes(diagnostics))

    def test_active_semantics_cannot_reference_removed_slides(self) -> None:
        spec = load_fixture("valid-executive-strategy.yaml")
        spec["slides"]["order"].remove("context")
        del spec["slides"]["items"]["context"]
        diagnostics = self.validate(spec)
        self.assertIn("inactive-slide", error_codes(diagnostics))
        self.assertIn("inactive-dependency", error_codes(diagnostics))

    def test_non_json_yaml_values_are_rejected_without_crashing(self) -> None:
        spec = load_fixture("valid-proposal.yaml")
        spec["slides"]["items"]["value"]["content_blocks"] = [
            {
                "type": "label",
                "content": yaml.safe_load("value: 2026-07-29")["value"],
            }
        ]
        diagnostics = self.validate(spec)
        self.assertIn("non-json-value", error_codes(diagnostics))

        non_finite = load_fixture("valid-proposal.yaml")
        non_finite["slides"]["items"]["value"]["content_blocks"] = [
            {"type": "metric", "content": float("nan")}
        ]
        diagnostics = self.validate(non_finite)
        self.assertIn("non-json-value", error_codes(diagnostics))

        baseline = deckc.build_manifest(load_fixture("valid-proposal.yaml"))
        baseline["slides"][0]["blueprint"]["invalid"] = float("nan")
        diagnostics = deckc.baseline_manifest_diagnostics(baseline)
        self.assertIn("non-json-value", error_codes(diagnostics))

    def test_canonical_json_requires_string_keys_and_valid_utf8(self) -> None:
        valid = load_fixture("valid-proposal.yaml")
        valid["slides"]["items"]["value"]["content_blocks"] = [
            {"type": "label", "content": {"emoji": "有效 ✅"}}
        ]
        self.assertFalse(error_codes(self.validate(valid)))
        self.assertEqual(
            deckc.fingerprint({"emoji": "有效 ✅"}),
            deckc.fingerprint({"emoji": "有效 ✅"}),
        )

        invalid_values = [
            {1: "one"},
            {True: "true"},
            {1.5: "float"},
            {None: "null"},
            {"nested": {"value": "\ud800"}},
            {"nested": {"\ud800": "value"}},
            ("tuple",),
        ]
        for index, invalid_value in enumerate(invalid_values):
            with self.subTest(index=index, value_type=type(invalid_value).__name__):
                spec = load_fixture("valid-proposal.yaml")
                spec["slides"]["items"]["value"]["content_blocks"] = [
                    {"type": "label", "content": invalid_value}
                ]
                diagnostics = self.validate(spec)
                self.assertIn("non-json-value", error_codes(diagnostics))
                with self.assertRaises((TypeError, ValueError)):
                    deckc.fingerprint(invalid_value)

        self.assertEqual(
            deckc.canonical_json({"1": "one"}),
            '{"1":"one"}',
        )
        with self.assertRaises(TypeError):
            deckc.canonical_json({1: "one"})

        baseline = deckc.build_manifest(load_fixture("valid-proposal.yaml"))
        baseline["slides"][0]["blueprint"]["invalid"] = {1: "one"}
        diagnostics = deckc.baseline_manifest_diagnostics(baseline)
        self.assertIn("non-json-value", error_codes(diagnostics))

        surrogate_baseline = deckc.build_manifest(load_fixture("valid-proposal.yaml"))
        surrogate_baseline["slides"][0]["blueprint"]["invalid"] = "\ud800"
        diagnostics = deckc.baseline_manifest_diagnostics(surrogate_baseline)
        self.assertIn("non-json-value", error_codes(diagnostics))

    def test_cli_exit_codes(self) -> None:
        valid = FIXTURE_DIR / "valid-proposal.yaml"
        invalid = FIXTURE_DIR / "missing-how-to-win.yaml"
        validate = subprocess.run(
            [sys.executable, MODULE_PATH, "validate", valid],
            check=False,
            capture_output=True,
            text=True,
        )
        lint = subprocess.run(
            [sys.executable, MODULE_PATH, "lint", invalid],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(validate.returncode, 0, validate.stderr)
        self.assertEqual(lint.returncode, 1, lint.stdout + lint.stderr)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            baseline_path = temp_path / "baseline.json"
            baseline_path.write_text(
                json.dumps(
                    deckc.build_manifest(load_fixture("valid-proposal.yaml")),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            unknown_change = subprocess.run(
                [
                    sys.executable,
                    MODULE_PATH,
                    "impact",
                    valid,
                    "--change-set",
                    "missing-change",
                    "--baseline",
                    baseline_path,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                unknown_change.returncode,
                1,
                unknown_change.stdout + unknown_change.stderr,
            )

            manifest_path = temp_path / "manifest.json"
            missing_initial_flag = subprocess.run(
                [sys.executable, MODULE_PATH, "manifest", valid],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing_initial_flag.returncode, 1)
            self.assertIn(
                "initial-release-flag-required",
                missing_initial_flag.stderr,
            )
            manifest = subprocess.run(
                [
                    sys.executable,
                    MODULE_PATH,
                    "manifest",
                    valid,
                    "--initial-release",
                    "--output",
                    manifest_path,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(manifest.returncode, 0, manifest.stdout + manifest.stderr)
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertIn("blueprint", payload["slides"][0])

            draft = load_fixture("valid-proposal.yaml")
            draft["slides"]["items"]["ask"]["status"] = "draft"
            draft["slides"]["items"]["ask"]["locked"] = False
            draft_path = temp_path / "draft.yaml"
            draft_path.write_text(
                yaml.safe_dump(draft, sort_keys=False),
                encoding="utf-8",
            )
            rejected = subprocess.run(
                [
                    sys.executable,
                    MODULE_PATH,
                    "manifest",
                    draft_path,
                    "--initial-release",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("slide-not-release-approved", rejected.stderr)

    def test_revision_manifest_cli_checks_baseline_and_target(self) -> None:
        baseline_spec = load_fixture("valid-proposal.yaml")
        baseline = deckc.build_manifest(baseline_spec)
        revised = copy.deepcopy(baseline_spec)
        revised["deck"]["operation"] = "revise"
        blueprint = copy.deepcopy(revised["slides"]["items"]["ask"])
        blueprint["title"] = "Approve one bounded workflow"
        revised["slides"]["items"]["ask"] = copy.deepcopy(blueprint)
        revised["change_sets"] = [
            {
                "id": "revise-ask",
                "status": "approved",
                "rationale": "Clarify the decision scope.",
                "baseline_fingerprint": baseline["manifest_fingerprint"],
                "target_order": revised["slides"]["order"],
                "modify": [{"slide": "ask", "blueprint": blueprint}],
            }
        ]
        set_target_fingerprints(revised, baseline, "revise-ask")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            baseline_path = temp_path / "baseline.json"
            spec_path = temp_path / "revised.yaml"
            output_path = temp_path / "manifest.json"
            baseline_path.write_text(
                json.dumps(baseline, ensure_ascii=False),
                encoding="utf-8",
            )
            spec_path.write_text(
                yaml.safe_dump(revised, sort_keys=False),
                encoding="utf-8",
            )
            command = [
                sys.executable,
                MODULE_PATH,
                "manifest",
                spec_path,
                "--baseline",
                baseline_path,
                "--change-set",
                "revise-ask",
                "--output",
                output_path,
            ]
            accepted = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                accepted.returncode,
                0,
                accepted.stdout + accepted.stderr,
            )
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["manifest_fingerprint"],
                revised["change_sets"][0]["target_manifest_fingerprint"],
            )

            revised["slides"]["items"]["plan"]["title"] = "Unauthorized edit"
            revised["change_sets"][0]["target_fingerprint"] = deckc.release_fingerprint(
                revised
            )
            spec_path.write_text(
                yaml.safe_dump(revised, sort_keys=False),
                encoding="utf-8",
            )
            rejected = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("revision-scope-mismatch", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
