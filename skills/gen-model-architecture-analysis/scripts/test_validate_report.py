#!/usr/bin/env python3
"""Unit tests for validate_report.py."""

from __future__ import annotations

import io
import re
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_report import main, validate  # noqa: E402


VALID_REPORT = """\
# Example Analysis

## Executive Summary

The model and runtime have a deliberately narrow, evidence-backed conclusion for this validation fixture.

## Scope and Revisions

Model revision: commit 0123456789abcdef. Evidence cutoff: 2026-08-07. Workload and assumptions are recorded here.

## Model Architecture

The representative path includes an input processor, a core network, and an output decoder with traced shapes [E1].

## vLLM-Omni Support Status

| Capability | Task/API/platform scope | Implementation | Validation | Support | Effective revision | Evidence | Gap or limitation |
|---|---|---|---|---|---|---|---|
| Loading | Offline fixture | Merged/present | Smoke | Supported | commit 0123456789abcdef | [E1] | Fixture-only scope |

## Hardware Requirements

The NVIDIA and Ascend configurations are independently scoped and are not generalized beyond the cited evidence [E1].

| Platform | Device/topology | Software stack | Workload | Precision/placement | Device memory | Host RAM/storage | Configuration class | Support status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NVIDIA | Example GPU | Example stack | Batch 1 | BF16 resident | 16 GiB | 32 GiB / 8 GiB | Recommended configuration | Supported | [E1] |
| Ascend | Example NPU | Example stack | Batch 1 | BF16 resident | Unknown | Unknown | Not validated | Unverified | [E1] |

## vLLM-Omni Optimization Direction

| Priority/status | Current gap and evidence | Bottleneck | Proposed change/touchpoint | NVIDIA direction | Ascend direction | Expected result | Risks/dependencies | Verification |
|---|---|---|---|---|---|---|---|---|
| P2 — Proposed | Repeated operation [E1] | Profile hypothesis | Optimize the core path | Qualify CUDA | Qualify NPU | Lower latency | Quality risk | A/B benchmark with an accuracy quality gate |

## Recommended Next Actions

Profile the representative workload, preserve the quality baseline, and resolve the highest-evidence support gap first.

## Risks and Unknowns

The fixture intentionally records that untested workloads remain unknown and require a target-hardware run.

## Evidence Index

| ID | Claim/use | Source | Revision/date | Class | Confidence | Notes |
|---|---|---|---|---|---|---|
| E1 | Fixture evidence | tests/local | 2026-08-07 | Observed | High | Local deterministic fixture |
"""


def remove_section(report: str, title: str) -> str:
    pattern = rf"(?ms)^## {re.escape(title)}\s*\n.*?(?=^## |\Z)"
    return re.sub(pattern, "", report)


class ValidateReportTests(unittest.TestCase):
    def test_valid_vllm_omni_report(self) -> None:
        findings = validate(VALID_REPORT, "vllm-omni", ["nvidia", "ascend"])
        self.assertEqual([], findings)

    def test_cli_reads_standard_input(self) -> None:
        output = io.StringIO()
        with patch("sys.stdin", io.StringIO(VALID_REPORT)), redirect_stdout(output):
            result = main(
                [
                    "-",
                    "--profile",
                    "vllm-omni",
                    "--require-platform",
                    "nvidia",
                    "--require-platform",
                    "ascend",
                    "--strict",
                ]
            )
        self.assertEqual(0, result)
        self.assertIn("Validated <stdin>", output.getvalue())

    def test_missing_required_section_is_error(self) -> None:
        report = VALID_REPORT.replace("## Model Architecture", "## Architecture Notes")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "model architecture" in item.message for item in findings))

    def test_required_heading_inside_fence_does_not_satisfy_schema(self) -> None:
        report = VALID_REPORT.replace("## Model Architecture", "## Architecture Notes")
        report += (
            "\n```markdown\n## Model Architecture\n"
            "This fenced example is long enough to defeat a naive heading parser.\n```\n"
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "model architecture" in item.message for item in findings))

    def test_required_heading_inside_html_comment_does_not_satisfy_schema(self) -> None:
        report = VALID_REPORT.replace("## Model Architecture", "## Architecture Notes")
        report += (
            "\nVisible text <!--\n## Model Architecture\n"
            "This commented example is long enough to defeat a naive parser.\n-->\n"
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "model architecture" in item.message for item in findings))

    def test_fence_inside_comment_does_not_expose_hidden_heading(self) -> None:
        report = VALID_REPORT.replace("## Model Architecture", "## Architecture Notes")
        report += (
            "\nVisible text <!--\n```markdown\n## Model Architecture\n"
            "Hidden by both a comment and fence.\n```\n-->\n"
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "model architecture" in item.message for item in findings))

    def test_parent_section_can_start_with_subheading(self) -> None:
        report = VALID_REPORT.replace(
            "The representative path includes an input processor, a core network, "
            "and an output decoder with traced shapes [E1].",
            "### Components\n\nThe representative path includes an input processor, "
            "a core network, and an output decoder with traced shapes [E1].",
        )
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertEqual([], findings)

    def test_placeholder_is_error(self) -> None:
        findings = validate(VALID_REPORT + "\n[TODO]\n", "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "placeholder" in item.message for item in findings))

    def test_bare_fixme_is_error(self) -> None:
        findings = validate(VALID_REPORT + "\nFIXME\n", "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "placeholder" in item.message for item in findings))

    def test_angle_bracket_placeholder_is_error(self) -> None:
        findings = validate(
            VALID_REPORT + "\n<repository and commit/tag>\n", "vllm-omni", []
        )
        self.assertTrue(any(item.level == "ERROR" and "placeholder" in item.message for item in findings))

    def test_autolink_and_html_are_not_placeholders(self) -> None:
        report = VALID_REPORT + "\n<https://example.com> <br> latency < 100 ms\n"
        findings = validate(report, "vllm-omni", [])
        self.assertFalse(any("placeholder" in item.message for item in findings))

    def test_undefined_evidence_is_error(self) -> None:
        report = VALID_REPORT.replace("traced shapes [E1]", "traced shapes [E2]")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "E2" in item.message for item in findings))

    def test_numbered_evidence_heading_does_not_count_index_rows_as_citations(self) -> None:
        report = VALID_REPORT.replace("## Evidence Index", "## 7. Evidence Index")
        body, evidence_index = report.split("## 7. Evidence Index", maxsplit=1)
        report = body.replace("[E1]", "") + "## 7. Evidence Index" + evidence_index
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "WARNING" and "not cited" in item.message for item in findings))

    def test_fenced_evidence_id_does_not_count_as_citation(self) -> None:
        body, evidence_index = VALID_REPORT.split("## Evidence Index", maxsplit=1)
        body = body.replace("[E1]", "") + "\n```text\n[E1]\n```\n"
        report = body + "## Evidence Index" + evidence_index
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "WARNING" and "not cited" in item.message for item in findings))

    def test_inline_code_evidence_id_does_not_count_as_citation(self) -> None:
        body, evidence_index = VALID_REPORT.split("## Evidence Index", maxsplit=1)
        body = body.replace("[E1]", "") + "\n`[E1]`\n"
        report = body + "## Evidence Index" + evidence_index
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "WARNING" and "not cited" in item.message for item in findings))

    def test_platform_requirement_is_enforced(self) -> None:
        report = VALID_REPORT.replace(
            "| Ascend | Example NPU | Example stack | Batch 1 | BF16 resident | "
            "Unknown | Unknown | Not validated | Unverified | [E1] |\n",
            "",
        )
        findings = validate(report, "vllm-omni", ["ascend"])
        self.assertTrue(any(item.level == "ERROR" and "ascend" in item.message for item in findings))

    def test_combined_platform_row_does_not_satisfy_ascend(self) -> None:
        report = VALID_REPORT.replace(
            "| Ascend | Example NPU | Example stack | Batch 1 | BF16 resident | "
            "Unknown | Unknown | Not validated | Unverified | [E1] |\n",
            "",
        ).replace("| NVIDIA |", "| NVIDIA and Ascend |")
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertTrue(any(item.level == "ERROR" and "ascend" in item.message for item in findings))

    def test_invalid_support_row_is_error_even_with_legend(self) -> None:
        report = VALID_REPORT.replace(
            "| Smoke | Supported |", "| Smoke | Ready |"
        )
        report = report.replace(
            "## vLLM-Omni Support Status\n",
            "## vLLM-Omni Support Status\n\nAllowed: Supported or Partial.\n",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "invalid status" in item.message for item in findings))

    def test_unknown_implementation_with_reason_is_valid(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke |", "| Unknown — repository unavailable | Smoke |"
        )
        findings = validate(report, "vllm-omni", [])
        self.assertFalse(any("implementation state" in item.message for item in findings))

    def test_unknown_cannot_hide_another_implementation_state(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke |", "| Unknown; Merged/present | Smoke |"
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "implementation state" in item.message for item in findings))

    def test_unknown_reason_cannot_append_another_state(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke |",
            "| Unknown — repository unavailable; Merged/present | Smoke |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "implementation state" in item.message for item in findings))

    def test_invalid_validation_gate_is_error(self) -> None:
        report = VALID_REPORT.replace("| Merged/present | Smoke |", "| Merged/present | Banana |")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "validation gates" in item.message for item in findings))

    def test_unknown_cannot_be_combined_with_positive_validation(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke |",
            "| Merged/present | Unknown — tests unavailable; Smoke |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "validation gates" in item.message for item in findings))

    def test_optimization_row_requires_gap_evidence(self) -> None:
        report = VALID_REPORT.replace("Repeated operation [E1]", "Repeated operation")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "gap evidence" in item.message for item in findings))

    def test_optimization_row_requires_implementation_state(self) -> None:
        report = VALID_REPORT.replace("P2 — Proposed", "P2 — Banana")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "implementation state" in item.message for item in findings))

    def test_escaped_pipe_does_not_shift_evidence_columns(self) -> None:
        report = VALID_REPORT.replace("tests/local", r"tests/local\|fixture")
        findings = validate(report, "vllm-omni", [])
        self.assertFalse(any("invalid class" in item.message for item in findings))

    def test_noncanonical_evidence_table_is_error(self) -> None:
        report = VALID_REPORT.replace("| Claim/use |", "| Claim |")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "Evidence Index" in item.message for item in findings))

    def test_blank_evidence_claim_and_notes_are_errors(self) -> None:
        report = VALID_REPORT.replace(
            "| E1 | Fixture evidence | tests/local | 2026-08-07 | Observed | High | Local deterministic fixture |",
            "| E1 | | tests/local | 2026-08-07 | Observed | High | |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "empty required cell" in item.message for item in findings))

    def test_hardware_row_with_empty_cells_is_error(self) -> None:
        report = VALID_REPORT.replace(
            "| Ascend | Example NPU | Example stack | Batch 1 | BF16 resident | "
            "Unknown | Unknown | Not validated | Unverified | [E1] |",
            "| Ascend | | | | | | | Not validated | Unverified | [E1] |",
        )
        findings = validate(report, "vllm-omni", ["ascend"])
        self.assertTrue(any(item.level == "ERROR" and "empty cell" in item.message for item in findings))

    def test_hardware_row_requires_exact_support_status(self) -> None:
        report = VALID_REPORT.replace(
            "| Supported | [E1] |", "| Supported and Unsupported | [E1] |"
        )
        findings = validate(report, "vllm-omni", ["nvidia"])
        self.assertTrue(any(item.level == "ERROR" and "support status" in item.message for item in findings))

    def test_unclosed_mermaid_fence_is_error(self) -> None:
        report = VALID_REPORT + "\n```mermaid\ngraph TD\n  A --> B\n"
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "Mermaid" in item.message for item in findings))

    def test_unclosed_tilde_mermaid_fence_is_error(self) -> None:
        report = VALID_REPORT + "\n~~~mermaid\ngraph TD\n  A --> B\n"
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "Mermaid" in item.message for item in findings))

    def test_longer_mermaid_closing_fence_is_valid(self) -> None:
        report = VALID_REPORT + "\n```mermaid\ngraph TD\n  A --> B\n````\n"
        findings = validate(report, "vllm-omni", [])
        self.assertFalse(any("Mermaid" in item.message for item in findings))

    def test_html_comment_inside_fence_does_not_hide_following_sections(self) -> None:
        report = VALID_REPORT.replace(
            "# Example Analysis\n",
            "# Example Analysis\n\n```text\n<!-- literal, intentionally unclosed\n```\n",
        )
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertEqual([], findings)

    def test_fence_inside_comment_does_not_hide_following_table(self) -> None:
        report = VALID_REPORT.replace(
            "## vLLM-Omni Support Status\n",
            "## vLLM-Omni Support Status\n\n<!--\n```markdown\n-->\n",
        )
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertEqual([], findings)

    def test_base_profile_allows_architecture_only(self) -> None:
        report = remove_section(VALID_REPORT, "Hardware Requirements")
        report = remove_section(report, "vLLM-Omni Support Status")
        report = remove_section(report, "vLLM-Omni Optimization Direction")
        self.assertNotIn("## Hardware Requirements", report)
        findings = validate(report, "base", [])
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
