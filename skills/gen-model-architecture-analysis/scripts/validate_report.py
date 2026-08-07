#!/usr/bin/env python3
"""Validate the structure and evidence hygiene of a model analysis report."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


BASE_SECTIONS = (
    "executive summary",
    "scope and revisions",
    "model architecture",
    "recommended next actions",
    "risks and unknowns",
    "evidence index",
)

VLLM_OMNI_SECTIONS = (
    "vllm omni support status",
    "vllm omni optimization direction",
)

SUPPORT_STATUSES = (
    "Supported",
    "Partial",
    "Unsupported",
    "Unverified",
    "N/A",
)

IMPLEMENTATION_STATES = (
    "Unknown",
    "Absent",
    "Proposed",
    "PR open",
    "Merged/present",
    "Superseded",
    "Reverted",
)

VALIDATION_GATES = (
    "Unknown",
    "No evidence found",
    "Unit",
    "Contract",
    "Smoke",
    "Recipe-validated",
    "Accuracy/quality",
    "Benchmark",
    "Recurring CI",
    "Production exercise",
)

HARDWARE_CLASSES = (
    "Measured configuration",
    "Official validated configuration",
    "Capacity proxy",
    "Derived capacity estimate",
    "Recommended configuration",
    "Not validated",
)

SUPPORT_COLUMNS = (
    "capability",
    "task api platform scope",
    "implementation",
    "validation",
    "support",
    "effective revision",
    "evidence",
    "gap or limitation",
)

HARDWARE_COLUMNS = (
    "platform",
    "device topology",
    "software stack",
    "workload",
    "precision placement",
    "device memory",
    "host ram storage",
    "configuration class",
    "support status",
    "evidence",
)

OPTIMIZATION_COLUMNS = (
    "priority status",
    "current gap and evidence",
    "bottleneck",
    "proposed change touchpoint",
    "nvidia direction",
    "ascend direction",
    "expected result",
    "risks dependencies",
    "verification",
)

EVIDENCE_COLUMNS = (
    "id",
    "claim use",
    "source",
    "revision date",
    "class",
    "confidence",
    "notes",
)

EVIDENCE_CLASSES = (
    "Observed",
    "Measured",
    "Reported",
    "Community-reported",
    "Derived",
    "Estimated",
    "Proposed",
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\bFIXME\b", re.IGNORECASE),
    re.compile(r"\?\?\?"),
)

ALLOWED_HTML_TAGS = {
    "a",
    "br",
    "code",
    "details",
    "div",
    "em",
    "img",
    "kbd",
    "p",
    "span",
    "strong",
    "sub",
    "summary",
    "sup",
}


@dataclass(frozen=True)
class Finding:
    level: str
    message: str


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    start: int
    end: int


def normalize_heading(value: str) -> str:
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s+", "", value)
    value = value.replace("vLLM-Omni", "vllm omni")
    value = re.sub(r"[^a-zA-Z0-9]+", " ", value).strip().casefold()
    return value


def fence_opening(line: str) -> tuple[str, int, str] | None:
    match = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})[ \t]*([^ \t`]*)", line)
    if not match:
        return None
    marker = match.group(1)
    return marker[0], len(marker), match.group(2).casefold()


def fence_closes(line: str, marker: tuple[str, int, str]) -> bool:
    char, count, _language = marker
    return bool(re.match(rf"^[ \t]{{0,3}}{re.escape(char)}{{{count},}}[ \t]*$", line))


def mask_html_comments(text: str) -> str:
    """Mask HTML comments while preserving character offsets and newlines."""
    characters = list(text)
    for match in re.finditer(r"<!--.*?(?:-->|\Z)", text, flags=re.DOTALL):
        for index in range(match.start(), match.end()):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters)


def mask_comment_line(line: str, in_comment: bool) -> tuple[str, bool]:
    """Mask comments on one non-fenced line and carry multiline state."""
    characters = list(line)
    position = 0
    while position < len(line):
        if in_comment:
            end = line.find("-->", position)
            stop = len(line) if end < 0 else end + 3
            for index in range(position, stop):
                characters[index] = " "
            if end < 0:
                return "".join(characters), True
            in_comment = False
            position = stop
            continue

        start = line.find("<!--", position)
        if start < 0:
            break
        end = line.find("-->", start + 4)
        stop = len(line) if end < 0 else end + 3
        for index in range(start, stop):
            characters[index] = " "
        in_comment = end < 0
        position = stop
    return "".join(characters), in_comment


def scan_headings(text: str) -> list[Heading]:
    headings: list[Heading] = []
    active_fence: tuple[str, int, str] | None = None
    in_comment = False
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        if active_fence is not None:
            if fence_closes(line, active_fence):
                active_fence = None
            offset += len(raw_line)
            continue

        visible_line, in_comment = mask_comment_line(line, in_comment)
        opening = fence_opening(visible_line)
        if opening is not None:
            active_fence = opening
            offset += len(raw_line)
            continue

        match = re.match(r"^[ \t]{0,3}(#{2,6})\s+(.+?)\s*#*\s*$", visible_line)
        if match:
            headings.append(
                Heading(
                    level=len(match.group(1)),
                    title=match.group(2),
                    start=offset + match.start(),
                    end=offset + match.end(),
                )
            )
        offset += len(raw_line)
    return headings


def strip_fenced_blocks(text: str) -> str:
    kept: list[str] = []
    active_fence: tuple[str, int, str] | None = None
    in_comment = False
    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        if active_fence is not None:
            if fence_closes(line, active_fence):
                active_fence = None
            continue
        visible_line, in_comment = mask_comment_line(line, in_comment)
        opening = fence_opening(visible_line)
        if opening is not None:
            active_fence = opening
            continue
        kept.append(raw_line)
    return "".join(kept)


def parse_sections(text: str) -> dict[str, str]:
    headings = scan_headings(text)
    sections: dict[str, str] = {}
    for index, heading in enumerate(headings):
        start = heading.end
        end = len(text)
        for following in headings[index + 1 :]:
            if following.level <= heading.level:
                end = following.start
                break
        sections[normalize_heading(heading.title)] = text[start:end].strip()
    return sections


def text_before_section(text: str, section_name: str) -> str:
    for heading in scan_headings(text):
        if normalize_heading(heading.title) == section_name:
            return text[: heading.start]
    return text


def visible_text(value: str) -> str:
    value = strip_fenced_blocks(value)
    value = mask_html_comments(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def split_markdown_row(line: str) -> list[str]:
    """Split a Markdown table row without treating escaped pipes as separators."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith(r"\|"):
        body = body[:-1]

    cells: list[str] = []
    current: list[str] = []
    index = 0
    in_code = False
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            current.extend((char, body[index + 1]))
            index += 2
            continue
        if char == "`":
            in_code = not in_code
            current.append(char)
        elif char == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def markdown_tables(section: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return Markdown tables that have a header and separator row."""
    section = strip_fenced_blocks(section)
    section = mask_html_comments(section)
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in section.splitlines() + [""]:
        if line.strip().startswith("|"):
            current.append(line)
            continue
        if current:
            blocks.append(current)
            current = []

    tables: list[tuple[list[str], list[list[str]]]] = []
    for block in blocks:
        if len(block) < 2:
            continue
        header = split_markdown_row(block[0])
        separator = split_markdown_row(block[1])
        if len(header) != len(separator):
            continue
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
            continue
        rows = [split_markdown_row(line) for line in block[2:]]
        tables.append((header, rows))
    return tables


def placeholder_tokens(text: str) -> list[str]:
    """Find unresolved template markers while allowing links and common HTML."""
    searchable = strip_fenced_blocks(text)
    searchable = mask_html_comments(searchable)
    searchable = re.sub(r"`[^`\n]+`", "", searchable)

    tokens: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        tokens.extend(match.group(0) for match in pattern.finditer(searchable))

    for match in re.finditer(r"<([A-Za-z][^>\n]*)>", searchable):
        value = match.group(1).strip()
        if re.match(r"^(?:https?://|mailto:)", value, re.IGNORECASE):
            continue
        tag = re.match(r"^/?([a-z][a-z0-9-]*)\b", value, re.IGNORECASE)
        if tag and tag.group(1).casefold() in ALLOWED_HTML_TAGS:
            continue
        tokens.append(match.group(0))
    return tokens


def state_is_valid(value: str, states: tuple[str, ...]) -> bool:
    normalized = normalize_heading(value)
    allowed = {normalize_heading(state) for state in states}
    if normalized in allowed:
        return True
    return normalize_heading("Unknown") in allowed and bool(
        re.fullmatch(
            r"\s*Unknown\s*(?:—|–|-|:)\s*[^;+\n]+\s*",
            value,
            re.IGNORECASE,
        )
    )


def validation_cell_is_valid(value: str) -> bool:
    parts = [part.strip() for part in value.strip("{} ").split(";")]
    if not parts or not all(state_is_valid(part, VALIDATION_GATES) for part in parts):
        return False
    normalized = [normalize_heading(part) for part in parts]
    unknown = any(item == "no evidence found" or item.startswith("unknown") for item in normalized)
    return not (unknown and len(parts) > 1)


def validate(text: str, profile: str, required_platforms: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    sections = parse_sections(text)
    required_sections = list(BASE_SECTIONS)
    if profile == "vllm-omni":
        required_sections.extend(VLLM_OMNI_SECTIONS)
    if required_platforms:
        required_sections.append("hardware requirements")

    for section_name in required_sections:
        if section_name not in sections:
            findings.append(Finding("ERROR", f"Missing required section: {section_name!r}"))
            continue
        if len(visible_text(sections[section_name])) < 40:
            findings.append(
                Finding("ERROR", f"Required section is empty or too thin: {section_name!r}")
            )

    for token in placeholder_tokens(text):
        findings.append(Finding("ERROR", f"Unresolved placeholder: {token!r}"))

    scope = sections.get("scope and revisions", "")
    if not re.search(r"\b(?:commit|revision|tag|version|sha)\b", scope, re.IGNORECASE):
        findings.append(Finding("WARNING", "Scope does not appear to record a pinned revision or version."))
    if not re.search(r"\b20\d{2}-\d{2}-\d{2}\b", scope):
        findings.append(Finding("WARNING", "Scope does not contain an ISO evidence-cutoff date."))

    hardware_tables = markdown_tables(sections.get("hardware requirements", ""))
    platform_tables: list[list[list[str]]] = []
    for header, rows in hardware_tables:
        normalized = [normalize_heading(cell) for cell in header]
        if tuple(normalized) == HARDWARE_COLUMNS:
            platform_tables.append(rows)

    if required_platforms and not platform_tables:
        findings.append(
            Finding(
                "ERROR",
                "Hardware section has no table with the canonical platform-matrix columns.",
            )
        )

    for platform in required_platforms:
        found_platform_row = False
        for rows in platform_tables:
            for row in rows:
                if not row:
                    continue
                words = normalize_heading(row[0]).split()
                if words and words[0] == platform:
                    found_platform_row = True
                    if len(row) != len(HARDWARE_COLUMNS):
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Hardware row for {platform} has {len(row)} cells; "
                                f"expected {len(HARDWARE_COLUMNS)}.",
                            )
                        )
                        continue
                    if any(not cell.strip() for cell in row):
                        findings.append(
                            Finding("ERROR", f"Hardware row for {platform} has an empty cell.")
                        )
                    hardware_class = normalize_heading(row[7])
                    allowed_classes = {normalize_heading(item) for item in HARDWARE_CLASSES}
                    if hardware_class not in allowed_classes:
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Hardware row for {platform} has invalid configuration class: {row[7]!r}",
                            )
                        )
                    status_cell = normalize_heading(row[8])
                    allowed_statuses = {normalize_heading(item) for item in SUPPORT_STATUSES}
                    if status_cell not in allowed_statuses:
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Hardware row for {platform} has invalid support status: {row[8]!r}",
                            )
                        )
                    if not re.search(r"\[E\d+\]", row[9], re.IGNORECASE):
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Hardware row for {platform} has no evidence ID.",
                            )
                        )
        if not found_platform_row:
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware section has no dedicated platform-matrix row for: {platform}",
                )
            )

    evidence_section = sections.get("evidence index", "")
    evidence_tables: list[list[list[str]]] = []
    for header, table_rows in markdown_tables(evidence_section):
        normalized = [normalize_heading(cell) for cell in header]
        if tuple(normalized) == EVIDENCE_COLUMNS:
            evidence_tables.append(table_rows)
    rows = [row for table_rows in evidence_tables for row in table_rows]
    if not rows:
        findings.append(
            Finding(
                "ERROR",
                "Evidence Index has no data table with the canonical columns.",
            )
        )
    else:
        defined_ids: set[str] = set()
        for row in rows:
            if len(row) != len(EVIDENCE_COLUMNS):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Evidence row has {len(row)} cells; expected {len(EVIDENCE_COLUMNS)}.",
                    )
                )
                continue
            if any(not cell.strip() for cell in row):
                findings.append(Finding("ERROR", "Evidence row has an empty required cell."))
            evidence_id = row[0].upper()
            if not re.fullmatch(r"E\d+", evidence_id):
                findings.append(Finding("ERROR", f"Invalid evidence ID: {row[0]!r}"))
                continue
            if evidence_id in defined_ids:
                findings.append(Finding("ERROR", f"Duplicate evidence ID: {evidence_id}"))
            defined_ids.add(evidence_id)
            if row[4] not in EVIDENCE_CLASSES:
                findings.append(
                    Finding("ERROR", f"Evidence row {evidence_id} has invalid class: {row[4]!r}")
                )
            if row[5] not in {"High", "Medium", "Low"}:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Evidence row {evidence_id} has invalid confidence: {row[5]!r}",
                    )
                )
            if row[2] in {"", "-", "N/A"}:
                findings.append(Finding("ERROR", f"Evidence row {evidence_id} has no source."))
            if row[3] in {"", "-", "N/A"}:
                findings.append(Finding("WARNING", f"Evidence row {evidence_id} has no revision/date."))
            if row[5] in {"Medium", "Low"} and len(row[6].strip()) < 12:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Evidence row {evidence_id} requires explanatory notes for {row[5]} confidence.",
                    )
                )

        report_body = strip_fenced_blocks(text_before_section(text, "evidence index"))
        report_body = mask_html_comments(report_body)
        report_body = re.sub(r"`[^`\n]+`", "", report_body)
        used_ids = re.findall(r"\[(E\d+)\]", report_body, re.IGNORECASE)
        referenced_ids = {item.upper() for item in used_ids}
        missing_ids = sorted(referenced_ids - defined_ids)
        for evidence_id in missing_ids:
            findings.append(Finding("ERROR", f"Claim references undefined evidence ID: {evidence_id}"))
        unused_ids = sorted(defined_ids - referenced_ids)
        for evidence_id in unused_ids:
            findings.append(Finding("WARNING", f"Evidence ID is not cited before the index: {evidence_id}"))

    if profile == "vllm-omni":
        support = sections.get("vllm omni support status", "")
        allowed_statuses = {normalize_heading(status) for status in SUPPORT_STATUSES}
        status_tables: list[list[list[str]]] = []
        for header, rows in markdown_tables(support):
            normalized = [normalize_heading(cell) for cell in header]
            if tuple(normalized) == SUPPORT_COLUMNS:
                status_tables.append(rows)
        if not status_tables or not any(status_tables):
            findings.append(
                Finding(
                    "ERROR",
                    "vLLM-Omni support section has no data table with the canonical columns.",
                )
            )
        for rows in status_tables:
            for row_number, row in enumerate(rows, start=1):
                if len(row) != len(SUPPORT_COLUMNS):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has {len(row)} cells; "
                            f"expected {len(SUPPORT_COLUMNS)}.",
                        )
                    )
                    continue
                if any(not cell.strip() for cell in row):
                    findings.append(
                        Finding("ERROR", f"Support row {row_number} has an empty cell.")
                    )
                if not state_is_valid(row[2], IMPLEMENTATION_STATES):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has invalid implementation state: {row[2]!r}",
                        )
                    )
                if not validation_cell_is_valid(row[3]):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has invalid validation gates: {row[3]!r}",
                        )
                    )
                value = normalize_heading(row[4])
                if value not in allowed_statuses:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has invalid status: {row[4]!r}",
                        )
                    )
                if not re.search(r"\[E\d+\]", row[6], re.IGNORECASE):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has no evidence ID.",
                        )
                    )

        optimization = sections.get("vllm omni optimization direction", "")
        optimization_tables: list[list[list[str]]] = []
        for header, rows in markdown_tables(optimization):
            normalized = [normalize_heading(cell) for cell in header]
            if tuple(normalized) == OPTIMIZATION_COLUMNS:
                optimization_tables.append(rows)
        if not optimization_tables or not any(optimization_tables):
            findings.append(
                Finding(
                    "ERROR",
                    "vLLM-Omni optimization section has no data table with the canonical columns.",
                )
            )
        for rows in optimization_tables:
            for row_number, row in enumerate(rows, start=1):
                if len(row) != len(OPTIMIZATION_COLUMNS):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has {len(row)} cells; "
                            f"expected {len(OPTIMIZATION_COLUMNS)}.",
                        )
                    )
                    continue
                if any(not cell.strip() for cell in row):
                    findings.append(
                        Finding("ERROR", f"Optimization row {row_number} has an empty cell.")
                    )
                priority = re.match(
                    r"^\s*P[0-3]\s*(?:—|–|-|:)\s*(.+?)\s*$",
                    row[0],
                    re.IGNORECASE,
                )
                if not priority:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has no P0-P3 priority.",
                        )
                    )
                elif not state_is_valid(priority.group(1), IMPLEMENTATION_STATES):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has invalid implementation state: "
                            f"{priority.group(1)!r}",
                        )
                    )
                if not re.search(r"\[E\d+\]", row[1], re.IGNORECASE):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has no gap evidence ID.",
                        )
                    )
                if not re.search(
                    r"\b(?:verification|validate|benchmark|A/B|quality|test|compare)\b",
                    row[8],
                    re.IGNORECASE,
                ):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has no concrete verification plan.",
                        )
                    )

    active_fence: tuple[str, int, str] | None = None
    for line in text.splitlines():
        if active_fence is not None:
            if fence_closes(line, active_fence):
                active_fence = None
            continue
        active_fence = fence_opening(line)
    if active_fence is not None and active_fence[2] == "mermaid":
        findings.append(Finding("ERROR", "A Mermaid code fence is not closed."))

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Markdown report path, or '-' to read standard input")
    parser.add_argument("--profile", choices=("base", "vllm-omni"), default="base")
    parser.add_argument(
        "--require-platform",
        action="append",
        choices=("nvidia", "ascend"),
        default=[],
        help="Require explicit coverage of a hardware platform (repeatable)",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    report_label = args.report
    if args.report == "-":
        text = sys.stdin.read()
        report_label = "<stdin>"
    else:
        report_path = Path(args.report)
        try:
            text = report_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: cannot read {report_path}: {exc}", file=sys.stderr)
            return 2

    findings = validate(text, args.profile, args.require_platform)
    for finding in findings:
        print(f"{finding.level}: {finding.message}")

    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    print(f"Validated {report_label}: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
