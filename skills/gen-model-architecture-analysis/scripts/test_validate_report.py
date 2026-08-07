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

## Inference Performance Analysis

### Evidence Level and Profiling Decision

| Evidence mode | Scope/workload | Environment | Method/artifact | Result | Limitation/reason | Evidence |
|---|---|---|---|---|---|---|
| Static analysis | Batch-one fixture | Pinned source fixture | FLOP and byte formulas in the report | Derived operation cost | Formula inputs and assumptions | [E2] |
| Local test | Batch-one fixture | Python test environment | `python -m unittest fixture` log | Contract passed locally | Deterministic local execution only | [E3] |

#### Required Dimension Matrix

| Dimension | Workload/shape | Analysis/result | Evidence class | Limitation/next validation | Evidence |
|---|---|---|---|---|---|
| Workload/execution count | Batch-one fixture | One forward and one decode | Derived | Other batches remain untested | [E2] |
| Compute/arithmetic intensity | Fixture operation shapes | FLOPs and bytes are derived | Derived | Achieved utilization is unprofiled | [E2] |
| Parallelism/communication | One rank | No distributed collectives apply | Derived | Multi-rank topology remains untested | [E2] |
| Precision/quantization/memory | Fixture component dtypes | Stored and compute precision are separated | Observed | Allocator peak is unmeasured | [E1] |
| Attention/steps/caching/fusion | Fixture execution path | Current mechanisms are recorded | Observed | Optimization A/B remains unmeasured | [E1] |

### Workload and Execution Count

The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].

### Compute Cost and Arithmetic Intensity

The fixture records operation-level FLOPs and bytes as derived values; it does not relabel those values as achieved throughput [E2].

### Parallelism and Communication

The single-rank fixture has no distributed collectives; multi-rank payload and topology therefore remain outside this result [E2].

### Precision, Quantization, and Memory

The fixture distinguishes stored precision, compute precision, derived weight bytes, and unmeasured allocator or device peaks [E2].

### Attention, Steps, Caching, and Fusion

The fixture records attention, execution-count, cache-eligibility, and fusion questions without claiming an unmeasured speedup [E2].

## vLLM-Omni Support Status

| Capability | Task/API/platform scope | Implementation | Validation | Support | Effective revision | Evidence | Gap or limitation |
|---|---|---|---|---|---|---|---|
| Loading | Offline fixture | Merged/present | Smoke | Supported | commit 0123456789abcdef | [E3] | Fixture-only scope |

## Hardware Requirements

The NVIDIA and Ascend configurations are independently scoped and are not generalized beyond the cited evidence [E1].

| Platform | Device/topology | Software stack | Workload | Precision/placement | Device memory | Host RAM/storage | Configuration class | Support status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NVIDIA | Example GPU | Example stack | Batch 1 | BF16 resident | 16 GiB | 32 GiB / 8 GiB | Recommended configuration | Supported | [E2] |
| Ascend | Example NPU | Example stack | Batch 1 | BF16 resident | Unknown | Unknown | Not validated | Unverified | [E1] |

## vLLM-Omni Optimization Direction

| Priority/status | Current gap and evidence | Bottleneck | Proposed change/touchpoint | NVIDIA direction | Ascend direction | Expected result | Risks/dependencies | Verification |
|---|---|---|---|---|---|---|---|---|
| P3 — Proposed | Repeated operation [E1] | Hypothesis — core path dominance [E2] | Optimize the core path | Qualify CUDA | Qualify NPU | Lower latency | Quality risk | Workload: baseline=batch-one fixture vs candidate=core-path change; metrics: performance=latency, resource=peak memory; repetitions: warmups=2, measured=5; quality gate: pass if output matches baseline tolerance |

## Recommended Next Actions

Profile the representative workload, preserve the quality baseline, and resolve the highest-evidence support gap first.

## Risks and Unknowns

The fixture intentionally records that untested workloads remain unknown and require a target-hardware run.

## Evidence Index

| ID | Claim/use | Source | Revision/date | Class | Confidence | Notes |
|---|---|---|---|---|---|---|
| E1 | Fixture evidence | tests/local | 2026-08-07 | Observed | High | Local deterministic fixture |
| E2 | Fixture performance arithmetic | tests/local | 2026-08-07 | Derived | High | Transparent fixture calculation |
| E3 | Fixture local contract run | tests/local | 2026-08-07 | Measured | High | Command and environment are recorded above |
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

    def test_missing_performance_section_is_error_for_base_profile(self) -> None:
        report = remove_section(VALID_REPORT, "Inference Performance Analysis")
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "inference performance analysis" in item.message
                for item in findings
            )
        )

    def test_missing_performance_subsection_is_error(self) -> None:
        report = VALID_REPORT.replace(
            "### Compute Cost and Arithmetic Intensity",
            "### Compute Notes",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "compute cost and arithmetic intensity" in item.message
                for item in findings
            )
        )

    def test_performance_subsection_requires_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This unrelated filler is deliberately long enough to satisfy a superficial section-length check without supporting evidence.",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "workload and execution count" in item.message
                and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_indented_code_does_not_supply_subsection_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This prose is long enough to pass the content-length gate but has no visible evidence citation.\n\n    [E2]",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "workload and execution count" in item.message
                and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_visible_indented_paragraph_continuation_supplies_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "The fixture derives one request and one output decode from the pinned contract.\n    Supporting derivation [E2] remains visible in the same paragraph.",
        )
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_visible_list_continuation_supplies_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "- The fixture derives one request and one output decode.\n\n    Supporting derivation [E2] is a visible list continuation.",
        )
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_nested_list_indented_code_does_not_supply_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "- This visible list claim deliberately has no evidence.\n\n      [E2]",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_top_level_indented_list_marker_is_still_code(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This visible filler is deliberately long enough for the section content gate.\n\n    - hidden code citation [E2]",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_blockquoted_fence_does_not_supply_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This unrelated filler is long enough for the section content gate but has no citation.\n\n> ```text\n> [E2]\n> ```",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_lazy_blockquote_continuation_does_not_supply_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "> quoted paragraph\nThis lazy continuation is long enough for the section content gate [E2]",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_link_reference_definition_does_not_supply_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This unrelated filler is long enough for the section content gate but has no citation.\n\n[E2]: https://example.com",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_multiline_link_reference_definition_does_not_supply_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This unrelated filler is long enough for the section content gate but has no citation.\n\n[E2]:\n  https://example.com",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_list_and_escaped_link_definitions_do_not_supply_evidence(self) -> None:
        replacements = (
            "This unrelated filler is long enough for the section content gate.\n\n- [foo]: /path/[E2]",
            "This unrelated filler is long enough for the section content gate.\n\n[foo\\]]: /path/[E2]",
        )
        for replacement in replacements:
            with self.subTest(replacement=replacement):
                report = VALID_REPORT.replace(
                    "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
                    replacement,
                )
                findings = validate(report, "base", [])
                self.assertTrue(
                    any(
                        "workload and execution count" in item.message
                        and "no evidence ID" in item.message
                        for item in findings
                    )
                )

    def test_reference_like_text_inside_paragraph_remains_visible(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This visible paragraph is deliberately long enough for the content gate.\n[E2]: https://example.com",
        )
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_nonvisible_inline_constructs_do_not_supply_evidence(self) -> None:
        replacements = (
            "This unrelated filler is long enough for the section content gate. ``hidden\n[E2]``",
            "This unrelated filler is long enough for the section content gate. <code>[E2]</code>",
            "This unrelated filler is long enough for the section content gate. [source](<https://example.invalid/[E2]>)",
        )
        for replacement in replacements:
            with self.subTest(replacement=replacement):
                report = VALID_REPORT.replace(
                    "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
                    replacement,
                )
                findings = validate(report, "base", [])
                self.assertTrue(
                    any(
                        "workload and execution count" in item.message
                        and "no evidence ID" in item.message
                        for item in findings
                    )
                )

    def test_hidden_inline_html_cannot_supply_evidence(self) -> None:
        hidden_fragments = (
            "<span hidden>[E2]</span>",
            '<span style="display:none">[E2]</span>',
            '<span style="visibility:hidden">[E2]</span>',
            "<span style=display:none>[E2]</span>",
            "<span style=visibility:hidden>[E2]</span>",
            "<span style=display:none!important>[E2]</span>",
            '<span style="display:/**/none">[E2]</span>',
            '<span style="visibility:hidden /**/">[E2]</span>',
            '<span aria-hidden="true">[E2]</span>',
            "<span aria-hidden=true>[E2]</span>",
            '<span data-x=">" hidden>[E2]</span>',
            '<span data-x=">" style="display:none">[E2]</span>',
            '<span title="1 > 0" aria-hidden=true>[E2]</span>',
            '<span style="display:none" style="display:block">[E2]</span>',
            '<span aria-hidden=true aria-hidden=false>[E2]</span>',
            "<span hidden/>[E2]",
        )
        for hidden in hidden_fragments:
            with self.subTest(hidden=hidden):
                report = VALID_REPORT.replace(
                    "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
                    f"This visible filler is deliberately long enough for the content gate. {hidden}",
                )
                findings = validate(report, "base", [])
                self.assertTrue(
                    any(
                        "workload and execution count" in item.message
                        and "no evidence ID" in item.message
                        for item in findings
                    )
                )

    def test_raw_html_wrapper_cannot_supply_report_structure(self) -> None:
        wrappers = (
            ("<div hidden>", "</div>"),
            ("<div style=display:none>", "</div>"),
            ("<section aria-hidden=true>", "</section>"),
            ("<template>", "</template>"),
            ("<dialog>", "</dialog>"),
            ("<div>", "</div>"),
        )
        for opening, closing in wrappers:
            with self.subTest(opening=opening):
                report = f"{opening}\n\n{VALID_REPORT}\n\n{closing}\n"
                findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
                self.assertTrue(
                    any(
                        item.level == "ERROR"
                        and "Missing required section: 'executive summary'" in item.message
                        for item in findings
                    )
                )

    def test_raw_html_wrapper_cannot_supply_subsection_evidence(self) -> None:
        cited_claim = (
            "The fixture derives one request, one core-network forward, and one output "
            "decode from the pinned execution contract [E2]."
        )
        report = VALID_REPORT.replace(
            cited_claim,
            "<div>\n\n"
            + cited_claim
            + "\n\n</div>\n\n"
            + "This visible filler is deliberately long enough for the content gate.",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "workload and execution count" in item.message
                and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_visible_raw_html_claim_block_is_rejected(self) -> None:
        report = VALID_REPORT + "\n<div>Visible unsupported claim [E999] and TODO</div>\n"
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(item.level == "ERROR" and "Raw HTML blocks" in item.message for item in findings)
        )

    def test_reference_link_label_cannot_supply_evidence(self) -> None:
        labels = ("[source][E2]", "[source [nested]][E2]", "[so\\]urce][E2]")
        for label in labels:
            with self.subTest(label=label):
                report = VALID_REPORT.replace(
                    "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
                    f"This visible filler is deliberately long enough for the content gate {label}.",
                )
                report += "\n[E2]: https://example.com/source\n"
                findings = validate(report, "base", [])
                self.assertTrue(
                    any(
                        "workload and execution count" in item.message
                        and "no evidence ID" in item.message
                        for item in findings
                    )
                )

    def test_evidence_id_as_visible_link_text_counts(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "This visible fixture derivation is deliberately long enough [E2][source].",
        )
        report += "\n[source]: https://example.com/source\n"
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_only_complete_visible_link_label_can_be_evidence_id(self) -> None:
        invalid_labels = (
            "[E2*notcitation*](https://example.com)",
            "[*notcitation*E2](https://example.com)",
            "[E2<span>junk</span>](https://example.com)",
            "[E2`junk`](https://example.com)",
            "[`E2`](https://example.com)",
        )
        claim = (
            "The fixture derives one request, one core-network forward, and one output "
            "decode from the pinned execution contract [E2]."
        )
        for label in invalid_labels:
            with self.subTest(label=label):
                report = VALID_REPORT.replace(
                    claim,
                    "This visible filler is deliberately long enough for the content gate "
                    + label,
                )
                findings = validate(report, "base", [])
                self.assertTrue(
                    any(
                        "workload and execution count" in item.message
                        and "no evidence ID" in item.message
                        for item in findings
                    )
                )

        report = VALID_REPORT.replace(claim, claim.replace("[E2]", "[**E2**](https://example.com)"))
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_reference_link_label_cannot_supply_table_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "| Local test | Batch-one fixture | Python test environment | `python -m unittest fixture` log | Contract passed locally | Deterministic local execution only | [E3] |",
            "| Local test | Batch-one fixture | Python test environment | `python -m unittest fixture` log | Contract passed locally | Deterministic local execution only | [run log][E3] |",
        )
        report += "\n[E3]: https://example.com/run\n"
        findings = validate(report, "base", [])
        self.assertTrue(
            any("Performance-evidence row" in item.message and "no evidence ID" in item.message for item in findings)
        )

    def test_entire_report_in_list_fence_has_no_visible_structure(self) -> None:
        nested = "- ```markdown\n" + "".join(
            "  " + line for line in VALID_REPORT.splitlines(keepends=True)
        ) + "  ```\n"
        findings = validate(nested, "vllm-omni", ["nvidia", "ascend"])
        self.assertTrue(any("Missing required section" in item.message for item in findings))

    def test_entire_report_in_raw_html_control_block_has_no_visible_structure(self) -> None:
        wrappers = (("<?opaque\n", "?>\n"), ("<![CDATA[\n", "]]>\n"))
        for opening, closing in wrappers:
            with self.subTest(opening=opening):
                hidden = opening + VALID_REPORT + closing
                findings = validate(hidden, "vllm-omni", ["nvidia", "ascend"])
                self.assertTrue(any("Missing required section" in item.message for item in findings))

    def test_html_div_block_cannot_supply_hidden_section(self) -> None:
        report = VALID_REPORT.replace(
            "## Inference Performance Analysis\n\n",
            "<div>\n## Inference Performance Analysis\n",
            1,
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                "Missing required section" in item.message
                and "inference performance analysis" in item.message
                for item in findings
            )
        )

    def test_cross_inline_html_container_is_rejected(self) -> None:
        prefixes = (
            "prefix <div hidden>\n\n",
            "prefix <span><div hidden></span>\n\n",
        )
        for prefix in prefixes:
            with self.subTest(prefix=prefix):
                report = prefix + VALID_REPORT + "\n\nsuffix </div>\n"
                findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
                self.assertTrue(
                    any(
                        item.level == "ERROR" and "Inline HTML containers" in item.message
                        for item in findings
                    )
                )

    def test_indented_backticks_do_not_close_top_level_fence(self) -> None:
        hidden = "```markdown\n    ```\n" + VALID_REPORT + "```\n"
        findings = validate(hidden, "vllm-omni", ["nvidia", "ascend"])
        self.assertTrue(any("Missing required section" in item.message for item in findings))

    def test_commonmark_indented_top_level_headings_are_accepted(self) -> None:
        report = re.sub(r"^(##+ )", r"  \1", VALID_REPORT, flags=re.MULTILINE)
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertEqual([], findings)

    def test_rendered_heading_text_drives_section_matching(self) -> None:
        variants = (
            "## Executive&#32;Summary",
            "Executive&#32;Summary\n---",
            "## <span>Executive Summary</span>",
        )
        for variant in variants:
            with self.subTest(variant=variant):
                report = VALID_REPORT.replace("## Executive Summary", variant, 1)
                findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
                self.assertEqual([], findings)

    def test_top_level_sections_require_h2(self) -> None:
        report = VALID_REPORT.replace("## Executive Summary", "###### Executive Summary", 1)
        findings = validate(report, "base", [])
        self.assertTrue(any("Top-level section must use an H2" in item.message for item in findings))

    def test_performance_subsections_require_h3(self) -> None:
        report = VALID_REPORT.replace(
            "### Workload and Execution Count",
            "#### Workload and Execution Count",
            1,
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any("Inference-performance subsection must use an H3" in item.message for item in findings)
        )

    def test_duplicate_canonical_heading_cannot_bypass_level_check(self) -> None:
        report = VALID_REPORT.replace(
            "## Executive Summary\n\n",
            "## Executive Summary\n\n###### Executive Summary\n\n",
            1,
        )
        findings = validate(report, "base", [])
        self.assertTrue(any("Duplicate canonical heading" in item.message for item in findings))

    def test_duplicate_performance_subsection_is_rejected(self) -> None:
        report = VALID_REPORT.replace(
            "### Workload and Execution Count\n\n",
            "### Workload and Execution Count\n\n###### Workload and Execution Count\n\n",
            1,
        )
        findings = validate(report, "base", [])
        self.assertTrue(any("Duplicate canonical heading" in item.message for item in findings))

    def test_backtick_in_fence_info_is_visible_paragraph_text(self) -> None:
        report = VALID_REPORT.replace(
            "The fixture derives one request, one core-network forward, and one output decode from the pinned execution contract [E2].",
            "```foo``` visible prelude\nSupporting derivation remains visible [E2].",
        )
        findings = validate(report, "base", [])
        self.assertFalse(
            any(
                "workload and execution count" in item.message and "no evidence ID" in item.message
                for item in findings
            )
        )

    def test_performance_section_requires_canonical_table(self) -> None:
        report = VALID_REPORT.replace("| Evidence mode |", "| Evidence kind |")
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "canonical columns" in item.message
                for item in findings
            )
        )

    def test_fenced_performance_table_does_not_satisfy_schema(self) -> None:
        report = VALID_REPORT.replace("| Evidence mode |", "| Evidence kind |")
        fenced_table = (
            "```markdown\n"
            "| Evidence mode | Scope/workload | Environment | Method/artifact | Result | Limitation/reason | Evidence |\n"
            "|---|---|---|---|---|---|---|\n"
            "| Local test | Hidden | Hidden | Hidden | Hidden | Hidden | [E3] |\n"
            "```\n\n"
        )
        report = report.replace(
            "### Workload and Execution Count\n",
            fenced_table + "### Workload and Execution Count\n",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "canonical columns" in item.message
                for item in findings
            )
        )

    def test_performance_row_with_wrong_width_is_error(self) -> None:
        report = VALID_REPORT.replace(
            "| Static analysis | Batch-one fixture | Pinned source fixture | "
            "FLOP and byte formulas in the report | Derived operation cost | "
            "Formula inputs and assumptions | [E2] |",
            "| Static analysis | Batch-one fixture | Pinned source fixture | "
            "FLOP and byte formulas in the report | Derived operation cost | "
            "Formula inputs and assumptions |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR"
                and ("expected 7" in item.message or "empty cell" in item.message)
                for item in findings
            )
        )

    def test_performance_dimension_matrix_requires_every_dimension(self) -> None:
        report = re.sub(
            r"^\| Attention/steps/caching/fusion \|.*\n",
            "",
            VALID_REPORT,
            flags=re.MULTILINE,
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "Attention/steps/caching/fusion" in item.message
                for item in findings
            )
        )

    def test_performance_dimension_rejects_proposed_as_present_state(self) -> None:
        report = VALID_REPORT.replace(
            "| Workload/execution count | Batch-one fixture | One forward and one decode | Derived |",
            "| Workload/execution count | Batch-one fixture | One forward and one decode | Proposed |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "invalid evidence class" in item.message
                for item in findings
            )
        )

    def test_invalid_performance_evidence_mode_is_error(self) -> None:
        report = VALID_REPORT.replace("| Static analysis |", "| Guessed |", 1)
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "invalid evidence mode" in item.message
                for item in findings
            )
        )

    def test_performance_mode_requires_matching_evidence_class(self) -> None:
        report = VALID_REPORT.replace(
            "| E3 | Fixture local contract run | tests/local | 2026-08-07 | Measured |",
            "| E3 | Fixture local contract run | tests/local | 2026-08-07 | Observed |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "at least one Measured evidence item" in item.message
                for item in findings
            )
        )

    def test_performance_evidence_requires_local_run_decision(self) -> None:
        report = re.sub(
            r"^\| Local test \|.*\n",
            "",
            VALID_REPORT,
            flags=re.MULTILINE,
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "Local test, Local profile, or Not run" in item.message
                for item in findings
            )
        )

    def test_performed_local_run_requires_visible_inline_command(self) -> None:
        report = VALID_REPORT.replace(
            "`python -m unittest fixture` log",
            "Executed local checks and retained the resulting log artifact",
            1,
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "executed test/profile command" in item.message
                for item in findings
            )
        )

    def test_not_run_requires_reason_and_bounded_next_run(self) -> None:
        report = VALID_REPORT.replace(
            "| Local test | Batch-one fixture | Python test environment | "
            "`python -m unittest fixture` log | Contract passed locally | "
            "Deterministic local execution only | [E3] |",
            "| Not run | Batch-one fixture | Python test environment | N/A | "
            "Not measured | Missing | [E3] |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "reason why the local run was skipped" in item.message
                for item in findings
            )
        )

    def test_not_run_with_reason_and_bounded_next_run_is_valid(self) -> None:
        report = VALID_REPORT.replace(
            "| Local test | Batch-one fixture | Python test environment | "
            "`python -m unittest fixture` log | Contract passed locally | "
            "Deterministic local execution only | [E3] |",
            "| Not run | Batch-one fixture | Shared accelerator environment | "
            "Run `python profile_fixture.py --repetitions 5` after the device is free | "
            "Not measured | Existing jobs made a local profile unsafe during this analysis | [E1] |",
        )
        findings = validate(report, "base", [])
        self.assertFalse(any(item.level == "ERROR" for item in findings))

    def test_not_run_rejects_long_filler_without_inline_command(self) -> None:
        report = VALID_REPORT.replace(
            "| Local test | Batch-one fixture | Python test environment | "
            "`python -m unittest fixture` log | Contract passed locally | "
            "Deterministic local execution only | [E3] |",
            "| Not run | Batch-one fixture | Shared accelerator environment | "
            "A detailed follow-up `abcdefgh` will be selected and executed later | Not measured | "
            "Existing jobs made a local profile unsafe during this analysis | [E1] |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "bounded next test/profile command" in item.message
                for item in findings
            )
        )

    def test_not_run_rejects_hidden_inline_command(self) -> None:
        report = VALID_REPORT.replace(
            "| Local test | Batch-one fixture | Python test environment | "
            "`python -m unittest fixture` log | Contract passed locally | "
            "Deterministic local execution only | [E3] |",
            "| Not run | Batch-one fixture | Shared accelerator environment | "
            "<span hidden>Run `python profile_fixture.py --repetitions 5`</span> "
            "No executable command is visible | Not measured | Existing accelerator jobs made "
            "a local profile unsafe during this analysis | [E1] |",
        )
        findings = validate(report, "base", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "bounded next test/profile command" in item.message
                for item in findings
            )
        )

    def test_evidence_after_early_index_is_still_checked(self) -> None:
        body, evidence_index = VALID_REPORT.split("## Evidence Index", maxsplit=1)
        report = "## Evidence Index" + evidence_index + "\n" + body + "\nLate claim [E999].\n"
        findings = validate(report, "base", [])
        self.assertTrue(
            any(item.level == "ERROR" and "E999" in item.message for item in findings)
        )

    def test_four_space_indented_tables_do_not_satisfy_schema(self) -> None:
        report = re.sub(r"(?m)^\|", "    |", VALID_REPORT)
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertTrue(
            any(item.level == "ERROR" and "canonical columns" in item.message for item in findings)
        )

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
            "\n<!--\n## Model Architecture\n"
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
        report = VALID_REPORT.replace("traced shapes [E1]", "traced shapes [E99]")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "E99" in item.message for item in findings))

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

    def test_present_vllm_sections_are_validated_under_base_profile(self) -> None:
        report = VALID_REPORT.replace("| Smoke | Supported |", "| Smoke | Ready |")
        findings = validate(report, "base", [])
        self.assertTrue(any(item.level == "ERROR" and "invalid status" in item.message for item in findings))

    def test_supported_status_requires_present_code_and_positive_validation(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke | Supported |",
            "| Proposed | No evidence found | Supported |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(item.level == "ERROR" and "cannot claim 'Supported'" in item.message for item in findings)
        )

    def test_unknown_implementation_with_reason_is_valid(self) -> None:
        report = VALID_REPORT.replace(
            "| Merged/present | Smoke |", "| Unknown — repository unavailable | Smoke |"
        )
        report = report.replace(
            "| Smoke | Supported | commit 0123456789abcdef |",
            "| Smoke | Unverified | commit 0123456789abcdef |",
            1,
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
        report = VALID_REPORT.replace("P3 — Proposed", "P3 — Banana")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "implementation state" in item.message for item in findings))

    def test_p2_requires_measured_or_reported_bottleneck(self) -> None:
        report = VALID_REPORT.replace("P3 — Proposed", "P2 — Proposed")
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "P2 for an unmeasured bottleneck" in item.message
                for item in findings
            )
        )

    def test_community_report_cannot_promote_p2(self) -> None:
        report = VALID_REPORT.replace("P3 — Proposed", "P2 — Proposed")
        report = report.replace(
            "Hypothesis — core path dominance [E2]",
            "Community-reported — core path dominance [E4]",
        )
        report = report.replace(
            "| E3 | Fixture local contract run | tests/local | 2026-08-07 | Measured | High | Command and environment are recorded above |",
            "| E3 | Fixture local contract run | tests/local | 2026-08-07 | Measured | High | Command and environment are recorded above |\n"
            "| E4 | Third-party performance claim | community/post | 2026-08-07 | Community-reported | Medium | Exact target environment was not reproduced |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "P2 for an unmeasured bottleneck" in item.message
                for item in findings
            )
        )

    def test_optimization_row_requires_bottleneck_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "Hypothesis — core path dominance [E2]",
            "Hypothesis — core path dominance",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "bottleneck evidence ID" in item.message
                for item in findings
            )
        )

    def test_measured_bottleneck_requires_measured_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "Hypothesis — core path dominance [E2]",
            "Measured — core path dominance [E2]",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "must cite Measured evidence" in item.message
                for item in findings
            )
        )

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

    def test_hidden_markup_does_not_fill_required_table_cells(self) -> None:
        cases = (
            ("tests/local", "<span hidden>not visible</span>", "Evidence row has an empty"),
            (
                "`python -m unittest fixture` log",
                "<span hidden>not visible</span>",
                "Performance-evidence row 2 has an empty",
            ),
            (
                "Fixture-only scope",
                "<span hidden>not visible</span>",
                "Support row 1 has an empty",
            ),
            ("Example stack", "<span hidden>not visible</span>", "Hardware row"),
        )
        for original, replacement, message in cases:
            with self.subTest(original=original):
                report = VALID_REPORT.replace(original, replacement, 1)
                findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
                self.assertTrue(
                    any(item.level == "ERROR" and message in item.message for item in findings)
                )

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
            "| Supported | [E2] |", "| Supported and Unsupported | [E2] |"
        )
        findings = validate(report, "vllm-omni", ["nvidia"])
        self.assertTrue(any(item.level == "ERROR" and "support status" in item.message for item in findings))

    def test_reported_capacity_proxy_is_allowed(self) -> None:
        report = VALID_REPORT.replace(
            "Recommended configuration | Supported | [E2]",
            "Capacity proxy | Supported | [E4]",
        ).replace(
            "| E3 | Fixture local contract run",
            "| E4 | Exact topology reported on different devices | upstream/report | 2026-08-07 | Reported | High | Device difference is retained as a limitation |\n| E3 | Fixture local contract run",
        )
        findings = validate(report, "vllm-omni", ["nvidia"])
        self.assertFalse(any("Hardware row" in item.message for item in findings))

    def test_present_hardware_section_is_validated_without_platform_flags(self) -> None:
        report = VALID_REPORT.replace("Recommended configuration", "Imaginary class", 1)
        findings = validate(report, "base", [])
        self.assertTrue(
            any(item.level == "ERROR" and "configuration class" in item.message for item in findings)
        )

    def test_reciprocal_combined_platform_rows_are_not_dedicated_rows(self) -> None:
        report = VALID_REPORT.replace("| NVIDIA |", "| NVIDIA and Ascend |", 1)
        report = report.replace("| Ascend |", "| Ascend and NVIDIA |", 1)
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        self.assertTrue(
            any(item.level == "ERROR" and "dedicated platform-matrix row" in item.message for item in findings)
        )

    def test_negative_verification_language_is_rejected(self) -> None:
        report = VALID_REPORT.replace(
            "Workload: baseline=batch-one fixture vs candidate=core-path change; metrics: performance=latency, resource=peak memory; repetitions: warmups=2, measured=5; quality gate: pass if output matches baseline tolerance",
            "No test, benchmark, comparison, validation, or quality check will be performed",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(item.level == "ERROR" and "declines verification" in item.message for item in findings)
        )

    def test_generic_optimization_verification_is_rejected(self) -> None:
        report = VALID_REPORT.replace(
            "Workload: baseline=batch-one fixture vs candidate=core-path change; metrics: performance=latency, resource=peak memory; repetitions: warmups=2, measured=5; quality gate: pass if output matches baseline tolerance",
            "Run an A/B benchmark with a quality gate",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any(
                item.level == "ERROR" and "verification must define" in item.message
                for item in findings
            )
        )

    def test_placeholder_optimization_verification_values_are_rejected(self) -> None:
        report = VALID_REPORT.replace(
            "Workload: baseline=batch-one fixture vs candidate=core-path change; metrics: performance=latency, resource=peak memory; repetitions: warmups=2, measured=5; quality gate: pass if output matches baseline tolerance",
            "Workload: x; metrics: none; repetitions: 0; quality gate: x",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("concrete A/B contract" in item.message for item in findings))

    def test_optimization_verification_requires_baseline_candidate_and_resource_metric(self) -> None:
        report = VALID_REPORT.replace(
            "Workload: baseline=batch-one fixture vs candidate=core-path change; metrics: performance=latency, resource=peak memory; repetitions: warmups=2, measured=5; quality gate: pass if output matches baseline tolerance",
            "Workload: baseline=batch-one fixture vs candidate=batch-one fixture; metrics: performance=latency, resource=latency; repetitions: measured=5; quality gate: pass if output matches baseline tolerance",
        )
        findings = validate(report, "vllm-omni", [])
        messages = "\n".join(item.message for item in findings)
        self.assertIn("workload arms must differ", messages)
        self.assertIn("resource measure", messages)
        self.assertIn("warmups=<count>", messages)

    def test_optimization_verification_decline_suffix_is_rejected(self) -> None:
        report = VALID_REPORT.replace(
            "quality gate: pass if output matches baseline tolerance",
            "quality gate: pass if output matches baseline tolerance. The benchmark will not be run",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("declines verification" in item.message for item in findings))

    def test_optimization_verification_requires_positive_measured_runs(self) -> None:
        valid = "repetitions: warmups=2, measured=5"
        for invalid in (
            "repetitions: warmups=5, measured=0",
            "repetitions: warmups=5",
        ):
            with self.subTest(invalid=invalid):
                report = VALID_REPORT.replace(valid, invalid)
                findings = validate(report, "vllm-omni", [])
                self.assertTrue(any("positive measured count" in item.message for item in findings))

    def test_optimization_quality_gate_cannot_define_failure_as_acceptance(self) -> None:
        report = VALID_REPORT.replace(
            "quality gate: pass if output matches baseline tolerance",
            "quality gate: pass if output does not match baseline tolerance",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("failure rather than acceptance" in item.message for item in findings))

    def test_optimization_metrics_must_name_actual_measures(self) -> None:
        report = VALID_REPORT.replace(
            "metrics: performance=latency, resource=peak memory",
            "metrics: performance=step, resource=device",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        messages = "\n".join(item.message for item in findings)
        self.assertIn("performance measure", messages)
        self.assertIn("resource measure", messages)

    def test_optimization_metrics_and_counts_cannot_be_negated(self) -> None:
        replacements = (
            "metrics: performance=no latency measurement, resource=no memory measurement",
            "metrics: performance=latency will not be measured, resource=memory will not be measured",
            "metrics: performance=unmeasured latency, resource=unmeasured memory",
            "metrics: performance=latency unavailable, resource=memory unavailable",
            "repetitions: warmups=2, not measured=5",
            "repetitions: warmups=2, measured=5 will not be recorded",
            "repetitions: warmups=2, measured=5 is not actually recorded",
            "repetitions: warmups=2, measured=5 unavailable",
        )
        originals = (
            "metrics: performance=latency, resource=peak memory",
            "metrics: performance=latency, resource=peak memory",
            "metrics: performance=latency, resource=peak memory",
            "metrics: performance=latency, resource=peak memory",
            "repetitions: warmups=2, measured=5",
            "repetitions: warmups=2, measured=5",
            "repetitions: warmups=2, measured=5",
            "repetitions: warmups=2, measured=5",
        )
        for original, replacement in zip(originals, replacements, strict=True):
            with self.subTest(replacement=replacement):
                report = VALID_REPORT.replace(original, replacement, 1)
                findings = validate(report, "vllm-omni", [])
                self.assertTrue(any("concrete A/B contract" in item.message for item in findings))

    def test_optimization_quality_gate_requires_affirmative_output_quality(self) -> None:
        invalid_gates = (
            "quality gate: pass if latency is within target threshold",
            "quality gate: pass if peak memory is within target threshold",
            "quality gate: pass if benchmark succeeds",
            "quality gate: pass if at least 5 runs complete",
            "quality gate: pass if latency result is within target threshold",
            "quality gate: pass if output is invalid but latency remains within threshold",
            "quality gate: pass if output matches baseline tolerance or fails validation",
            "quality gate: pass if output fails validation but latency is within threshold",
            "quality gate: pass if output errors occur but latency is within threshold",
            "quality gate: pass if output does not need to match baseline tolerance",
            "quality gate: pass if invalid output matches the expected failure pattern",
            "quality gate: pass if output is valid somehow",
            "quality gate: pass if output validation succeeds",
            "quality gate: pass if output matches something",
            "quality gate: pass if quality meets requirements",
            "quality gate: pass if output is within any tolerance",
            "quality gate: pass if output failure is expected",
            "quality gate: pass if errors are acceptable",
            "quality gate: pass if output is bad",
        )
        for invalid_gate in invalid_gates:
            with self.subTest(invalid_gate=invalid_gate):
                report = VALID_REPORT.replace(
                    "quality gate: pass if output matches baseline tolerance",
                    invalid_gate,
                    1,
                )
                findings = validate(report, "vllm-omni", [])
                self.assertTrue(any("concrete A/B contract" in item.message for item in findings))

    def test_concrete_parity_and_numeric_quality_gates_are_accepted(self) -> None:
        valid_gates = (
            "quality gate: pass if baseline and candidate outputs are identical",
            "quality gate: pass if candidate results match baseline tolerance",
            "quality gate: pass if LPIPS < 0.2",
            "quality gate: pass if WER <= 0.1",
            "quality gate: pass if CER < 0.1",
            "quality gate: pass if PSNR > 20",
            "quality gate: pass if MSE <= 1e-4",
            "quality gate: pass if max absolute error < 1e-5",
            "quality gate: pass if cosine similarity >= 0.99",
            "quality gate: pass if FVD <= 100",
            "quality gate: pass if PESQ >= 3.0",
            "quality gate: pass if output errors = 0",
            "quality gate: pass if zero output errors",
            "quality gate: pass if no output errors and baseline unchanged",
            "quality gate: pass if failure count < 1",
        )
        for valid_gate in valid_gates:
            with self.subTest(valid_gate=valid_gate):
                report = VALID_REPORT.replace(
                    "quality gate: pass if output matches baseline tolerance",
                    valid_gate,
                    1,
                )
                findings = validate(report, "vllm-omni", [])
                self.assertFalse(any("concrete A/B contract" in item.message for item in findings))

    def test_optimization_contract_ignores_hidden_semantic_tokens(self) -> None:
        report = VALID_REPORT.replace(
            "Workload: baseline=batch-one fixture vs candidate=core-path change; "
            "metrics: performance=latency, resource=peak memory; repetitions: warmups=2, "
            "measured=5; quality gate: pass if output matches baseline tolerance",
            "Workload: baseline=standard path vs candidate=optimized path; metrics: "
            "performance=<span hidden>latency</span> irrelevant words, "
            "resource=<span hidden>memory</span> irrelevant words; repetitions: "
            "<span hidden>warmups=2, measured=5</span>; quality gate: pass if "
            "<span hidden>output matches baseline within tolerance</span> irrelevant visible words",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("concrete A/B contract" in item.message for item in findings))

    def test_optimization_quality_gate_cannot_permit_failure(self) -> None:
        report = VALID_REPORT.replace(
            "quality gate: pass if output matches baseline tolerance",
            "quality gate: pass if all outputs may fail validation",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("permits failure" in item.message for item in findings))

    def test_optimization_verification_cannot_be_marked_skipped(self) -> None:
        report = VALID_REPORT.replace(
            "quality gate: pass if output matches baseline tolerance",
            "quality gate: pass if output matches baseline tolerance. Benchmark is skipped",
            1,
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("declines verification" in item.message for item in findings))

    def test_requested_platform_needs_substantive_optimization_direction(self) -> None:
        report = VALID_REPORT.replace("Qualify CUDA", "N/A", 1).replace(
            "Qualify NPU", "N/A — this synthetic row is CUDA-only", 1
        )
        findings = validate(report, "vllm-omni", ["nvidia", "ascend"])
        messages = "\n".join(item.message for item in findings)
        self.assertIn("bare N/A for requested platform nvidia", messages)
        self.assertIn("no substantive optimization or qualification direction", messages)

    def test_inline_code_cannot_supply_support_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "| Supported | commit 0123456789abcdef | [E3] | Fixture-only scope |",
            "| Supported | commit 0123456789abcdef | `[E3]` | Fixture-only scope |",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any("Support row" in item.message and "no evidence ID" in item.message for item in findings))

    def test_inline_code_undefined_id_cannot_supply_optimization_gap_evidence(self) -> None:
        report = VALID_REPORT.replace(
            "Repeated operation [E1]",
            "Repeated operation `[E999]`",
        )
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(
            any("Optimization row" in item.message and "no gap evidence ID" in item.message for item in findings)
        )
        self.assertFalse(any("undefined evidence ID: E999" in item.message for item in findings))

    def test_unclosed_mermaid_fence_is_error(self) -> None:
        report = VALID_REPORT + "\n```mermaid\ngraph TD\n  A --> B\n"
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "Mermaid" in item.message for item in findings))

    def test_unclosed_tilde_mermaid_fence_is_error(self) -> None:
        report = VALID_REPORT + "\n~~~mermaid\ngraph TD\n  A --> B\n"
        findings = validate(report, "vllm-omni", [])
        self.assertTrue(any(item.level == "ERROR" and "Mermaid" in item.message for item in findings))

    def test_mermaid_text_inside_raw_html_is_not_a_fence(self) -> None:
        report = VALID_REPORT + "\n<div>\n```mermaid\ngraph TD\n</div>\n"
        findings = validate(report, "vllm-omni", [])
        self.assertFalse(any("Mermaid" in item.message for item in findings))

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

    def test_base_profile_requires_performance_but_allows_no_hardware_or_vllm(self) -> None:
        report = remove_section(VALID_REPORT, "Hardware Requirements")
        report = remove_section(report, "vLLM-Omni Support Status")
        report = remove_section(report, "vLLM-Omni Optimization Direction")
        self.assertNotIn("## Hardware Requirements", report)
        findings = validate(report, "base", [])
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
