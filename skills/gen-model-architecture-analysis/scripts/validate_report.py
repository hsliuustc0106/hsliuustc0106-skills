#!/usr/bin/env python3
"""Validate the structure and evidence hygiene of a model analysis report."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

try:
    from markdown_it import MarkdownIt
except ImportError as exc:  # pragma: no cover - exercised only in an incomplete environment
    raise SystemExit(
        "validate_report.py requires markdown-it-py; install scripts/requirements.txt "
        "in the selected local environment."
    ) from exc


MARKDOWN = MarkdownIt("commonmark", {"html": True}).enable("table")


BASE_SECTIONS = (
    "executive summary",
    "scope and revisions",
    "model architecture",
    "inference performance analysis",
    "recommended next actions",
    "risks and unknowns",
    "evidence index",
)

PERFORMANCE_SUBSECTIONS = (
    "evidence level and profiling decision",
    "workload and execution count",
    "compute cost and arithmetic intensity",
    "parallelism and communication",
    "precision quantization and memory",
    "attention steps caching and fusion",
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

PERFORMANCE_COLUMNS = (
    "evidence mode",
    "scope workload",
    "environment",
    "method artifact",
    "result",
    "limitation reason",
    "evidence",
)

PERFORMANCE_DIMENSION_COLUMNS = (
    "dimension",
    "workload shape",
    "analysis result",
    "evidence class",
    "limitation next validation",
    "evidence",
)

PERFORMANCE_DIMENSIONS = (
    "Workload/execution count",
    "Compute/arithmetic intensity",
    "Parallelism/communication",
    "Precision/quantization/memory",
    "Attention/steps/caching/fusion",
)

PERFORMANCE_MODES = (
    "Static analysis",
    "Local test",
    "Local profile",
    "Source measurement",
    "Community measurement",
    "Not run",
)

BOTTLENECK_KINDS = (
    "Observed",
    "Measured",
    "Reported",
    "Community-reported",
    "Derived",
    "Estimated",
    "Hypothesis",
)

COMMAND_NAMES = {
    "bash",
    "cargo",
    "cmake",
    "curl",
    "go",
    "make",
    "msprof",
    "ninja",
    "npu-smi",
    "nsys",
    "nvidia-smi",
    "pytest",
    "python",
    "python3",
    "sh",
    "torchrun",
    "uv",
    "vllm",
}

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


class _HTMLVisibilityParser(HTMLParser):
    """Update a persistent visibility stack with quote-aware HTML parsing."""

    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(
        self,
        stack: list[tuple[str, bool]],
        *,
        hide_code: bool,
        hide_all: bool,
    ) -> None:
        super().__init__(convert_charrefs=True)
        self.stack = stack
        self.hide_code = hide_code
        self.hide_all = hide_all
        self.mismatched_close = False

    def hidden_state(self, tag: str, attributes: list[tuple[str, str | None]]) -> bool:
        attribute_map: dict[str, str | None] = {}
        for name, value in attributes:
            attribute_map.setdefault(name.casefold(), value)
        style = attribute_map.get("style") or ""
        style = re.sub(r"/\*.*?\*/", "", style, flags=re.DOTALL)
        explicitly_hidden = bool(
            "hidden" in attribute_map
            or (attribute_map.get("aria-hidden") or "").strip().casefold() == "true"
            or re.search(
                r"(?:display\s*:\s*none|visibility\s*:\s*hidden)"
                r"(?:\s*!\s*important)?(?:\s*;|\s*$)",
                style,
                re.IGNORECASE,
            )
            or tag in {"script", "style", "template"}
            or (tag == "dialog" and "open" not in attribute_map)
        )
        parent_hidden = self.stack[-1][1] if self.stack else False
        return bool(
            parent_hidden
            or explicitly_hidden
            or self.hide_all
            or (self.hide_code and tag in {"code", "pre"})
        )

    def handle_starttag(
        self,
        tag: str,
        attributes: list[tuple[str, str | None]],
    ) -> None:
        normalized_tag = tag.casefold()
        hidden = self.hidden_state(normalized_tag, attributes)
        if normalized_tag not in self.VOID_TAGS:
            self.stack.append((normalized_tag, hidden))

    def handle_startendtag(
        self,
        tag: str,
        attributes: list[tuple[str, str | None]],
    ) -> None:
        # In HTML (unlike XML), a trailing slash does not close non-void elements.
        self.handle_starttag(tag, attributes)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.casefold()
        if not self.stack or self.stack[-1][0] != normalized_tag:
            self.mismatched_close = True
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == normalized_tag:
                del self.stack[index:]
                break


def update_html_visibility_stack(
    html: str,
    stack: list[tuple[str, bool]],
    *,
    hide_code: bool,
    hide_all: bool = False,
) -> None:
    parser = _HTMLVisibilityParser(
        stack,
        hide_code=hide_code,
        hide_all=hide_all,
    )
    parser.feed(html)
    parser.close()


def update_html_block_visibility_stack(
    html: str,
    stack: list[tuple[str, bool]],
) -> None:
    """Conservatively exclude Markdown nested in cross-token raw HTML blocks."""
    update_html_visibility_stack(
        html,
        stack,
        hide_code=True,
        hide_all=True,
    )


def inline_plain_text(token: object, *, include_code: bool) -> str:
    """Extract visible text from one markdown-it inline token."""
    fragments: list[str] = []
    visibility_stack: list[tuple[str, bool]] = []
    children = getattr(token, "children", None) or []
    for child in children:
        if child.type == "html_inline":
            update_html_visibility_stack(
                child.content,
                visibility_stack,
                hide_code=not include_code,
            )
            continue
        if visibility_stack and visibility_stack[-1][1]:
            continue
        if child.type == "text":
            fragments.append(child.content)
        elif include_code and child.type == "code_inline":
            fragments.append(child.content)
        elif child.type in {"softbreak", "hardbreak"}:
            fragments.append(" ")
    return "".join(fragments)


def normalize_heading(value: str) -> str:
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s+", "", value)
    value = value.replace("vLLM-Omni", "vllm omni")
    return re.sub(r"[^a-zA-Z0-9]+", " ", value).strip().casefold()


def scan_headings(text: str) -> list[Heading]:
    """Return rendered, top-level H2-H6 headings with source offsets."""
    line_offsets = [0]
    for raw_line in text.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(raw_line))

    headings: list[Heading] = []
    html_block_stack: list[tuple[str, bool]] = []
    container_depth = 0
    container_tokens = {
        "blockquote_open",
        "bullet_list_open",
        "ordered_list_open",
        "list_item_open",
    }
    container_closes = {token.replace("_open", "_close") for token in container_tokens}
    tokens = MARKDOWN.parse(text)
    for index, token in enumerate(tokens):
        if token.type == "html_block":
            update_html_block_visibility_stack(token.content, html_block_stack)
            continue
        if token.type in container_closes:
            container_depth = max(0, container_depth - 1)
        if (
            token.type == "heading_open"
            and token.tag in {"h2", "h3", "h4", "h5", "h6"}
            and container_depth == 0
            and not (html_block_stack and html_block_stack[-1][1])
            and token.map is not None
        ):
            inline = tokens[index + 1] if index + 1 < len(tokens) else None
            title = (
                inline_plain_text(inline, include_code=True)
                if inline is not None and inline.type == "inline"
                else ""
            )
            start_line, end_line = token.map
            headings.append(
                Heading(
                    level=int(token.tag[1:]),
                    title=title,
                    start=line_offsets[start_line],
                    end=line_offsets[end_line],
                )
            )
        if token.type in container_tokens:
            container_depth += 1
    return headings


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


def text_outside_section(text: str, section_name: str) -> str:
    headings = scan_headings(text)
    for index, heading in enumerate(headings):
        if normalize_heading(heading.title) != section_name:
            continue
        end = len(text)
        for following in headings[index + 1 :]:
            if following.level <= heading.level:
                end = following.start
                break
        return text[: heading.start] + text[end:]
    return text


def rendered_claim_text(
    value: str,
    reference_env: dict[str, object] | None = None,
    *,
    include_code: bool = False,
) -> str:
    """Extract rendered text, excluding images, quotations, and code by default."""
    fragments: list[str] = []
    blockquote_depth = 0
    html_block_stack: list[tuple[str, bool]] = []
    parse_env: dict[str, object] = {}
    if reference_env and isinstance(reference_env.get("references"), dict):
        parse_env["references"] = dict(reference_env["references"])
    for token in MARKDOWN.parse(value, parse_env):
        if token.type == "html_block":
            update_html_block_visibility_stack(token.content, html_block_stack)
            continue
        if token.type == "blockquote_close":
            blockquote_depth = max(0, blockquote_depth - 1)
            continue
        if token.type == "blockquote_open":
            blockquote_depth += 1
            continue
        if (
            blockquote_depth
            or (html_block_stack and html_block_stack[-1][1])
            or token.type != "inline"
            or not token.children
        ):
            continue

        visibility_stack: list[tuple[str, bool]] = []
        link_label: list[str] | None = None
        for child in token.children:
            if child.type == "html_inline":
                update_html_visibility_stack(
                    child.content,
                    visibility_stack,
                    hide_code=True,
                )
                continue
            if child.type == "link_open":
                link_label = []
                continue
            if child.type == "link_close":
                label = "".join(link_label or [])
                if re.fullmatch(r"E\d+", label, re.IGNORECASE):
                    fragments.append(f"[{label}]")
                else:
                    fragments.append(label)
                link_label = None
                continue
            if visibility_stack and visibility_stack[-1][1]:
                continue
            if child.type == "text":
                if link_label is not None:
                    link_label.append(child.content)
                else:
                    fragments.append(child.content)
            elif child.type in {"softbreak", "hardbreak"}:
                if link_label is not None:
                    link_label.append(" ")
                else:
                    fragments.append("\n")
            elif child.type == "code_inline":
                if link_label is not None:
                    link_label.append(
                        child.content
                        if include_code
                        else "\N{OBJECT REPLACEMENT CHARACTER}"
                    )
                elif include_code:
                    fragments.append(child.content)
            elif link_label is not None and child.type == "image":
                link_label.append("\N{OBJECT REPLACEMENT CHARACTER}")
        if link_label is not None:
            fragments.append("".join(link_label))
        fragments.append("\n")
    return "".join(fragments)


def visible_text(value: str) -> str:
    """Return rendered text for semantic fields, including visible inline code."""
    return re.sub(
        r"\s+",
        " ",
        rendered_claim_text(value, include_code=True),
    ).strip()


def visible_evidence_ids(
    value: str,
    reference_env: dict[str, object] | None = None,
) -> set[str]:
    searchable = rendered_claim_text(value, reference_env)
    return {
        evidence_id.upper()
        for evidence_id in re.findall(r"\[(E\d+)\]", searchable, re.IGNORECASE)
    }


def visible_inline_code(value: str) -> list[str]:
    """Return only inline-code spans that are visibly rendered outside quotations."""
    commands: list[str] = []
    blockquote_depth = 0
    html_block_stack: list[tuple[str, bool]] = []
    for token in MARKDOWN.parse(value):
        if token.type == "html_block":
            update_html_block_visibility_stack(token.content, html_block_stack)
            continue
        if token.type == "blockquote_close":
            blockquote_depth = max(0, blockquote_depth - 1)
            continue
        if token.type == "blockquote_open":
            blockquote_depth += 1
            continue
        if (
            blockquote_depth
            or (html_block_stack and html_block_stack[-1][1])
            or token.type != "inline"
            or not token.children
        ):
            continue
        visibility_stack: list[tuple[str, bool]] = []
        for child in token.children:
            if child.type == "html_inline":
                update_html_visibility_stack(
                    child.content,
                    visibility_stack,
                    hide_code=True,
                )
                continue
            if visibility_stack and visibility_stack[-1][1]:
                continue
            if child.type == "code_inline":
                commands.append(child.content)
    return commands


def has_cross_token_inline_html_container(tokens: list[object]) -> bool:
    """Detect an inline HTML opener that remains active beyond its inline block."""
    for token in tokens:
        if getattr(token, "type", None) != "inline" or not getattr(token, "children", None):
            continue
        stack: list[tuple[str, bool]] = []
        parser = _HTMLVisibilityParser(
            stack,
            hide_code=False,
            hide_all=False,
        )
        for child in token.children:
            if child.type == "html_inline":
                parser.feed(child.content)
        parser.close()
        if stack or parser.mismatched_close:
            return True
    return False


def markdown_tables(section: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return top-level GFM tables from the CommonMark token stream."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    current_rows: list[list[str]] | None = None
    current_row: list[str] | None = None
    container_depth = 0
    html_block_stack: list[tuple[str, bool]] = []
    container_tokens = {
        "blockquote_open",
        "bullet_list_open",
        "ordered_list_open",
        "list_item_open",
    }
    container_closes = {token.replace("_open", "_close") for token in container_tokens}

    for token in MARKDOWN.parse(section):
        if token.type == "html_block":
            update_html_block_visibility_stack(token.content, html_block_stack)
            continue
        if token.type in container_closes:
            container_depth = max(0, container_depth - 1)
        hidden_by_html = bool(html_block_stack and html_block_stack[-1][1])
        if token.type == "table_open" and container_depth == 0 and not hidden_by_html:
            current_rows = []
        elif token.type == "tr_open" and current_rows is not None:
            current_row = []
        elif token.type in {"th_open", "td_open"} and current_row is not None:
            continue
        elif token.type == "inline" and current_row is not None:
            current_row.append(token.content.strip())
        elif token.type == "tr_close" and current_rows is not None and current_row is not None:
            current_rows.append(current_row)
            current_row = None
        elif token.type == "table_close" and current_rows is not None:
            if current_rows:
                tables.append((current_rows[0], current_rows[1:]))
            current_rows = None
            current_row = None
        if token.type in container_tokens:
            container_depth += 1
    return tables


def placeholder_tokens(text: str) -> list[str]:
    """Find unresolved template markers while allowing links and common HTML."""
    searchable = rendered_claim_text(text)
    html_fragments: list[str] = []
    blockquote_depth = 0
    for token in MARKDOWN.parse(text):
        if token.type == "blockquote_close":
            blockquote_depth = max(0, blockquote_depth - 1)
            continue
        if token.type == "blockquote_open":
            blockquote_depth += 1
            continue
        if blockquote_depth or token.type != "inline" or not token.children:
            continue
        html_code_depth = 0
        for child in token.children:
            if child.type != "html_inline":
                continue
            closing = re.match(r"\s*</\s*(code|pre)\s*>", child.content, re.IGNORECASE)
            opening = re.match(r"\s*<\s*(code|pre)\b", child.content, re.IGNORECASE)
            if closing:
                html_code_depth = max(0, html_code_depth - 1)
                continue
            if opening:
                if not re.search(r"/\s*>\s*$", child.content):
                    html_code_depth += 1
                continue
            if not html_code_depth and not child.content.lstrip().startswith("<!--"):
                html_fragments.append(child.content)
    angle_searchable = searchable + "\n" + "\n".join(html_fragments)

    tokens: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        tokens.extend(match.group(0) for match in pattern.finditer(searchable))

    for match in re.finditer(r"<([A-Za-z][^>\n]*)>", angle_searchable):
        value = match.group(1).strip()
        if re.match(r"^(?:https?://|mailto:)", value, re.IGNORECASE):
            continue
        tag = re.match(r"^/?([a-z][a-z0-9-]*)\b", value, re.IGNORECASE)
        if tag and tag.group(1).casefold() in ALLOWED_HTML_TAGS:
            continue
        tokens.append(match.group(0))
    return tokens


def state_is_valid(value: str, states: tuple[str, ...]) -> bool:
    value = visible_text(value)
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
    value = visible_text(value)
    parts = [part.strip() for part in value.strip("{} ").split(";")]
    if not parts or not all(state_is_valid(part, VALIDATION_GATES) for part in parts):
        return False
    normalized = [normalize_heading(part) for part in parts]
    unknown = any(item == "no evidence found" or item.startswith("unknown") for item in normalized)
    return not (unknown and len(parts) > 1)


def has_bounded_inline_command(value: str) -> bool:
    for command in visible_inline_code(value):
        tokens = command.strip().split()
        while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=\S+", tokens[0]):
            tokens.pop(0)
        if not tokens:
            continue
        executable = tokens[0].rsplit("/", maxsplit=1)[-1].casefold()
        executable_like = (
            executable in COMMAND_NAMES
            or re.fullmatch(r"python\d+(?:\.\d+)?", executable) is not None
            or "/" in tokens[0]
            or executable.endswith((".py", ".sh"))
        )
        if executable_like and (len(tokens) > 1 or "/" in tokens[0]):
            return True
    return False


def has_unnegated_measure(value: str, pattern: str) -> bool:
    """Return whether a measurement term is asserted rather than explicitly absent."""
    for match in re.finditer(pattern, value, re.IGNORECASE):
        prefix = value[max(0, match.start() - 48) : match.start()]
        suffix = value[match.end() : match.end() + 32]
        negated_before = re.search(
            r"\b(?:no|not|without)(?:\s+[A-Za-z]+){0,3}\s*$",
            prefix,
            re.IGNORECASE,
        )
        negated_after = re.match(
            r"\s+(?:(?:is|was|were|will|shall|would|should|can|could|may|might)\s+)?"
            r"(?:not|never)\s+(?:actually\s+)?(?:be\s+)?"
            r"(?:measured|recorded|reported|captured|available)\b",
            suffix,
            re.IGNORECASE,
        )
        if negated_before is None and negated_after is None:
            return True
    return False


def optimization_verification_issues(value: str) -> list[str]:
    """Validate the structured baseline/candidate A/B contract."""
    value = visible_text(value)
    aliases = {
        "workload": "workload",
        "metric": "metrics",
        "metrics": "metrics",
        "repetition": "repetitions",
        "repetitions": "repetitions",
        "quality gate": "quality gate",
        "quality gates": "quality gate",
    }
    fields: dict[str, str] = {}
    issues: list[str] = []
    for segment in value.split(";"):
        match = re.match(r"^\s*([^:=]+?)\s*[:=]\s*(.*?)\s*$", segment)
        if match is None:
            if segment.strip():
                issues.append("unlabeled trailing text")
            continue
        label = aliases.get(normalize_heading(match.group(1)))
        if label is None:
            issues.append(f"unknown field {match.group(1).strip()!r}")
            continue
        if label in fields:
            issues.append(f"duplicate {label}")
            continue
        fields[label] = match.group(2).strip()

    required = ("workload", "metrics", "repetitions", "quality gate")
    for field in required:
        if field not in fields:
            issues.append(f"missing {field}")

    placeholders = {
        "-",
        "n a",
        "na",
        "none",
        "not applicable",
        "tbd",
        "todo",
        "unknown",
        "x",
    }
    minimum_lengths = {"workload": 12, "metrics": 12, "quality gate": 12}
    for field, minimum in minimum_lengths.items():
        field_value = fields.get(field, "")
        if (
            len(visible_text(field_value)) < minimum
            or normalize_heading(field_value) in placeholders
        ):
            issues.append(f"non-concrete {field}")

    workload = fields.get("workload", "")
    workload_arms = re.fullmatch(
        r"\s*baseline\s*=\s*(.+?)\s+vs\.?\s+candidate\s*=\s*(.+?)\s*",
        workload,
        re.IGNORECASE,
    )
    if workload and workload_arms is None:
        issues.append("workload must use baseline=<...> vs candidate=<...>")
    elif workload_arms is not None:
        baseline = visible_text(workload_arms.group(1))
        candidate = visible_text(workload_arms.group(2))
        if (
            len(baseline) < 8
            or len(candidate) < 8
            or normalize_heading(baseline) in placeholders
            or normalize_heading(candidate) in placeholders
        ):
            issues.append("workload arms must be concrete")
        elif normalize_heading(baseline) == normalize_heading(candidate):
            issues.append("baseline and candidate workload arms must differ")

    metrics = fields.get("metrics", "")
    metric_arms = re.fullmatch(
        r"\s*performance\s*=\s*(.+?)\s*,\s*resource\s*=\s*(.+?)\s*",
        metrics,
        re.IGNORECASE,
    )
    if metrics and metric_arms is None:
        issues.append("metrics must use performance=<...>, resource=<...>")
    performance_metrics = metric_arms.group(1) if metric_arms is not None else ""
    resource_metrics = metric_arms.group(2) if metric_arms is not None else ""
    performance_pattern = (
        r"\b(?:latency|throughput|duration|time|requests?/s|tokens?/s|frames?/s|"
        r"(?:execution|wall|kernel|stage|step|startup|compile|load|denoise)\s+time|"
        r"time\s+(?:per|to))\b"
    )
    resource_pattern = (
        r"\b(?:memory|hbm|ram|bytes|allocation|workspace|storage|bandwidth|"
        r"utilization|payload|transfer\s+(?:bytes|volume)|"
        r"(?:peak|allocated|reserved|resident|host|device)\s+"
        r"(?:memory|hbm|ram|bytes))\b"
    )
    absent_measure = re.compile(
        r"\b(?:unmeasured|unrecorded|unreported|uncaptured|unavailable|unknown|"
        r"not\s+available|not\s+collected)\b",
        re.IGNORECASE,
    )
    if performance_metrics and (
        absent_measure.search(performance_metrics)
        or not has_unnegated_measure(performance_metrics, performance_pattern)
    ):
        issues.append("metrics need a performance measure")
    if resource_metrics and (
        absent_measure.search(resource_metrics)
        or not has_unnegated_measure(resource_metrics, resource_pattern)
    ):
        issues.append("metrics need a resource measure")

    repetitions = fields.get("repetitions", "")
    repetitions_match = re.fullmatch(
        r"\s*(?:warmups?\s*=\s*\d+|mode\s*=\s*"
        r"(?:cold|deterministic|not applicable|n/?a))\s*,\s*"
        r"measured\s*=\s*[1-9]\d*(?:\s+per\s+arm)?\s*",
        repetitions,
        re.IGNORECASE,
    )
    if normalize_heading(repetitions) in placeholders or repetitions_match is None:
        issues.append("repetitions need a positive measured count")
    if repetitions and not re.match(
        r"\s*(?:warmups?\s*=|mode\s*=\s*(?:cold|deterministic|not applicable|n/?a))",
        repetitions,
        re.IGNORECASE,
    ):
        issues.append("repetitions need warmups=<count> or mode=<cold/deterministic/N/A>")

    quality_gate = fields.get("quality gate", "")
    quality_syntax = re.fullmatch(
        r"\s*(?:pass|accept)\s+if\s+(.+?)\s*",
        quality_gate,
        re.IGNORECASE,
    ) if quality_gate else None
    if quality_gate and quality_syntax is None:
        issues.append("quality gate must use pass if <criterion>")
    quality_criterion = re.sub(
        r"^\s*(?:pass|accept)\s+if\s+",
        "",
        quality_gate,
        flags=re.IGNORECASE,
    )
    parity_entity = re.search(
        r"\b(?:outputs?|results?|tensors?|logits?|hashes?)\b",
        quality_criterion,
        re.IGNORECASE,
    )
    parity_relation = re.search(
        r"\b(?:match(?:es)?|equals?|identical|parity)\b",
        quality_criterion,
        re.IGNORECASE,
    )
    parity_target = re.search(
        r"\b(?:baseline|reference|golden|tolerances?|thresholds?|hashes?|"
        r"numerical|media)\b",
        quality_criterion,
        re.IGNORECASE,
    )
    output_relation = bool(parity_entity and parity_relation and parity_target)
    baseline_unchanged = re.search(
        r"\bbaseline\b.{0,50}\b(?:loads?\s+)?unchanged\b",
        quality_criterion,
        re.IGNORECASE,
    )
    named_quality_metric = re.search(
        r"\b(?:correctness|accuracy|ssim|psnr|lpips|wer|cer|fidelity|"
        r"spectral|rms|perceptual|semantic)\b",
        quality_criterion,
        re.IGNORECASE,
    )
    named_threshold = re.search(
        r"\b(?:thresholds?|tolerances?|at\s+(?:least|most)|within\s+\d|"
        r"no\s+quality\s+regression)\b|(?:<=|>=|<|>)\s*\d",
        quality_criterion,
        re.IGNORECASE,
    )
    numeric_metric_pattern = re.compile(
        r"\b(?P<metric>[A-Za-z][A-Za-z0-9 _/-]{0,60}?)\s*"
        r"(?:<=|>=|==|=|<|>)\s*\d+(?:\.\d+)?(?:e[+-]?\d+)?\b",
        re.IGNORECASE,
    )
    non_quality_metric_pattern = re.compile(
        performance_pattern
        + "|"
        + resource_pattern
        + r"|\b(?:cost|power|energy|joules?|watts?|queue|startup|compile|load)\b",
        re.IGNORECASE,
    )
    numeric_quality_matches = [
        match
        for match in numeric_metric_pattern.finditer(quality_criterion)
        if non_quality_metric_pattern.search(match.group("metric")) is None
    ]
    zero_failure_pattern = re.compile(
        r"\b(?:no|zero)\s+(?:(?:output|candidate|validation|correctness)\s+){0,3}"
        r"(?:errors?|failures?)\b",
        re.IGNORECASE,
    )
    zero_failure_contract = zero_failure_pattern.search(quality_criterion)
    explicit_media_contract = re.search(
        r"\bvalid\b.{0,60}\b(?:video|audio|image)\b.{0,60}"
        r"\b\d+(?:\.\d+)?\s*(?:fps|hz|khz|frames?|seconds?|s)\b|"
        r"\bvalid\b.{0,60}\b\d+(?:\.\d+)?\s*"
        r"(?:fps|hz|khz|frames?|seconds?|s)\b.{0,30}\b(?:video|audio|image)\b",
        quality_criterion,
        re.IGNORECASE,
    )
    quality_contract = bool(
        output_relation
        or baseline_unchanged
        or (named_quality_metric and named_threshold)
        or numeric_quality_matches
        or zero_failure_contract
        or explicit_media_contract
    )
    if (
        quality_gate
        and quality_syntax is not None
        and len(quality_criterion) < 12
        and not numeric_quality_matches
    ):
        issues.append("quality gate criterion is too short to be concrete")
    if quality_gate and not quality_contract:
        issues.append(
            "quality gate needs explicit baseline parity, a named quality metric threshold, "
            "or a concrete media-output contract"
        )

    negative_searchable = re.sub(
        zero_failure_pattern.pattern
        + r"|\b(?:injected[- ]?)?failure[- ]recovery\b",
        "",
        quality_criterion,
        flags=re.IGNORECASE,
    )
    negative_searchable = numeric_metric_pattern.sub("", negative_searchable)
    negative_acceptance = re.search(
        r"\b(?:fail(?:s|ure)?|errors?|invalid|incorrect|wrong|bad|corrupt|"
        r"nonfinite|non-finite)\b|\bdoes\s+not\s+need\s+to\b",
        negative_searchable,
        re.IGNORECASE,
    )
    deliberate_negative_test = bool(
        baseline_unchanged
        and re.search(
            r"\b(?:candidate|missing|corrupt|invalid)\b.{0,40}\bfails?\b",
            quality_criterion,
            re.IGNORECASE,
        )
    )
    if quality_gate and re.search(
        r"\b(?:output|result|candidate|quality)\b.{0,30}"
        r"\b(?:does|do|must|should|will)\s+not\s+(?:match|pass|meet|satisfy|equal)\b",
        quality_criterion,
        re.IGNORECASE,
    ):
        issues.append("quality gate describes failure rather than acceptance")
    if quality_gate and re.search(
        r"\b(?:may|can|could)\s+fail\b",
        quality_criterion,
        re.IGNORECASE,
    ):
        issues.append("quality gate permits failure")
    if quality_gate and negative_acceptance and not deliberate_negative_test:
        issues.append("quality gate accepts an invalid or failing result")

    decline = re.search(
        r"\b(?:test|benchmark|profile|experiment|comparison|validation|a/b)\b"
        r".{0,60}\b(?:will|shall|is|are)?\s*(?:not|never)\s+(?:be\s+)?"
        r"(?:run|performed|executed|conducted|provided|planned)\b",
        value,
        re.IGNORECASE,
    ) or re.search(
        r"\b(?:no|not|never|without)\b.{0,80}"
        r"\b(?:verification|validation|test|benchmark|profile|experiment|compare|comparison|quality)\b"
        r".{0,50}\b(?:performed|run|planned|provided|conducted|executed)\b",
        value,
        re.IGNORECASE,
    ) or re.search(
        r"\b(?:test|benchmark|profile|experiment|comparison|validation|a/b)\b"
        r".{0,30}\b(?:skipped|omitted|deferred|not\s+required)\b|"
        r"\b(?:skip|omit|defer)\b.{0,30}"
        r"\b(?:test|benchmark|profile|experiment|comparison|validation|a/b)\b",
        value,
        re.IGNORECASE,
    )
    if decline is not None:
        issues.append("verification is explicitly declined")

    return issues


def validate(text: str, profile: str, required_platforms: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    markdown_env: dict[str, object] = {}
    document_tokens = MARKDOWN.parse(text, markdown_env)
    raw_html_blocks = [
        token
        for token in document_tokens
        if token.type == "html_block"
        and re.fullmatch(r"\s*<!--.*?-->\s*", token.content, re.DOTALL) is None
    ]
    if raw_html_blocks:
        findings.append(
            Finding(
                "ERROR",
                "Raw HTML blocks cannot carry report claims or structure; use Markdown "
                "or permitted inline HTML.",
            )
        )
    if has_cross_token_inline_html_container(document_tokens):
        findings.append(
            Finding(
                "ERROR",
                "Inline HTML containers must open and close within one rendered inline block; "
                "use Markdown for cross-block structure.",
            )
        )

    def evidence_ids(value: str) -> set[str]:
        return visible_evidence_ids(value, markdown_env)

    headings = scan_headings(text)
    heading_levels: dict[str, set[int]] = {}
    for heading in headings:
        heading_levels.setdefault(normalize_heading(heading.title), set()).add(heading.level)
    sections = parse_sections(text)
    required_sections = list(BASE_SECTIONS)
    validate_vllm = profile == "vllm-omni" or any(
        section_name in sections for section_name in VLLM_OMNI_SECTIONS
    )
    if validate_vllm:
        required_sections.extend(VLLM_OMNI_SECTIONS)
    if required_platforms:
        required_sections.append("hardware requirements")

    top_level_sections = set(BASE_SECTIONS) | set(VLLM_OMNI_SECTIONS) | {
        "hardware requirements"
    }
    canonical_headings = top_level_sections | set(PERFORMANCE_SUBSECTIONS)
    for section_name in sorted(canonical_headings):
        occurrences = sum(
            normalize_heading(heading.title) == section_name for heading in headings
        )
        if occurrences > 1:
            findings.append(
                Finding("ERROR", f"Duplicate canonical heading: {section_name!r}")
            )
    for section_name in sorted(top_level_sections.intersection(sections)):
        if 2 not in heading_levels.get(section_name, set()):
            findings.append(
                Finding("ERROR", f"Top-level section must use an H2 heading: {section_name!r}")
            )
    for section_name in PERFORMANCE_SUBSECTIONS:
        if section_name in sections and 3 not in heading_levels.get(section_name, set()):
            findings.append(
                Finding(
                    "ERROR",
                    f"Inference-performance subsection must use an H3 heading: {section_name!r}",
                )
            )

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

    performance = sections.get("inference performance analysis", "")
    performance_sections = parse_sections(performance)
    for section_name in PERFORMANCE_SUBSECTIONS:
        if section_name not in performance_sections:
            findings.append(
                Finding(
                    "ERROR",
                    f"Missing required inference-performance subsection: {section_name!r}",
                )
            )
            continue
        if len(visible_text(performance_sections[section_name])) < 40:
            findings.append(
                Finding(
                    "ERROR",
                    f"Inference-performance subsection is empty or too thin: {section_name!r}",
                )
            )
        if not evidence_ids(performance_sections[section_name]):
            findings.append(
                Finding(
                    "ERROR",
                    f"Inference-performance subsection has no evidence ID: {section_name!r}",
                )
            )
    performance_tables: list[list[list[str]]] = []
    for header, rows in markdown_tables(performance):
        normalized = [normalize_heading(visible_text(cell)) for cell in header]
        if tuple(normalized) == PERFORMANCE_COLUMNS:
            performance_tables.append(rows)
    if not performance_tables or not any(performance_tables):
        findings.append(
            Finding(
                "ERROR",
                "Inference performance section has no data table with the canonical columns.",
            )
        )
    local_decision_recorded = False
    allowed_performance_modes = {
        normalize_heading(mode): mode for mode in PERFORMANCE_MODES
    }
    for rows in performance_tables:
        for row_number, row in enumerate(rows, start=1):
            if len(row) != len(PERFORMANCE_COLUMNS):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Performance-evidence row {row_number} has {len(row)} cells; "
                        f"expected {len(PERFORMANCE_COLUMNS)}.",
                    )
                )
                continue
            if any(not visible_text(cell) for cell in row):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Performance-evidence row {row_number} has an empty cell.",
                    )
                )
            mode = normalize_heading(visible_text(row[0]))
            if mode not in allowed_performance_modes:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Performance-evidence row {row_number} has invalid evidence mode: {row[0]!r}",
                    )
                )
            if mode in {
                normalize_heading("Local test"),
                normalize_heading("Local profile"),
                normalize_heading("Not run"),
            }:
                local_decision_recorded = True
            if mode in {
                normalize_heading("Local test"),
                normalize_heading("Local profile"),
            } and not has_bounded_inline_command(row[3]):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Performance-evidence row {row_number} must record the executed "
                        "test/profile command as visible inline code in Method/artifact.",
                    )
                )
            if not evidence_ids(row[6]):
                findings.append(
                    Finding(
                        "ERROR",
                        f"Performance-evidence row {row_number} has no evidence ID.",
                    )
                )
            if mode == normalize_heading("Not run"):
                if len(visible_text(row[5])) < 20:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Performance-evidence row {row_number} does not give a concrete "
                            "reason why the local run was skipped.",
                        )
                    )
                if not has_bounded_inline_command(row[3]):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Performance-evidence row {row_number} must give the bounded next "
                            "test/profile command as inline code in Method/artifact.",
                        )
                    )
    if performance_tables and any(performance_tables) and not local_decision_recorded:
        findings.append(
            Finding(
                "ERROR",
                "Performance evidence must record a Local test, Local profile, or Not run decision.",
            )
        )

    performance_rows = [row for table_rows in performance_tables for row in table_rows]

    performance_dimension_tables: list[list[list[str]]] = []
    for header, rows in markdown_tables(performance):
        normalized = [normalize_heading(visible_text(cell)) for cell in header]
        if tuple(normalized) == PERFORMANCE_DIMENSION_COLUMNS:
            performance_dimension_tables.append(rows)
    if not performance_dimension_tables or not any(performance_dimension_tables):
        findings.append(
            Finding(
                "ERROR",
                "Inference performance section has no dimension matrix with the canonical columns.",
            )
        )
    performance_dimension_rows = [
        row for table_rows in performance_dimension_tables for row in table_rows
    ]
    found_dimensions: set[str] = set()
    allowed_evidence_classes = set(EVIDENCE_CLASSES) - {"Proposed"}
    for row_number, row in enumerate(performance_dimension_rows, start=1):
        if len(row) != len(PERFORMANCE_DIMENSION_COLUMNS):
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} has {len(row)} cells; "
                    f"expected {len(PERFORMANCE_DIMENSION_COLUMNS)}.",
                )
            )
            continue
        if any(not visible_text(cell) for cell in row):
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} has an empty cell.",
                )
            )
        dimension = normalize_heading(visible_text(row[0]))
        allowed_dimensions = {
            normalize_heading(item): item for item in PERFORMANCE_DIMENSIONS
        }
        if dimension not in allowed_dimensions:
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} has invalid dimension: {row[0]!r}",
                )
            )
        elif dimension in found_dimensions:
            findings.append(
                Finding(
                    "ERROR",
                    f"Duplicate performance dimension: {row[0]!r}",
                )
            )
        else:
            found_dimensions.add(dimension)
        evidence_class = visible_text(row[3])
        if evidence_class not in allowed_evidence_classes:
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} has invalid evidence class: {row[3]!r}",
                )
            )
        if not evidence_ids(row[5]):
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} has no evidence ID.",
                )
            )
    for dimension in PERFORMANCE_DIMENSIONS:
        if normalize_heading(dimension) not in found_dimensions:
            findings.append(
                Finding(
                    "ERROR",
                    f"Missing required performance dimension: {dimension!r}",
                )
            )

    scope = visible_text(sections.get("scope and revisions", ""))
    if not re.search(r"\b(?:commit|revision|tag|version|sha)\b", scope, re.IGNORECASE):
        findings.append(Finding("WARNING", "Scope does not appear to record a pinned revision or version."))
    if not re.search(r"\b20\d{2}-\d{2}-\d{2}\b", scope):
        findings.append(Finding("WARNING", "Scope does not contain an ISO evidence-cutoff date."))

    hardware_tables = markdown_tables(sections.get("hardware requirements", ""))
    platform_tables: list[list[list[str]]] = []
    for header, rows in hardware_tables:
        normalized = [normalize_heading(visible_text(cell)) for cell in header]
        if tuple(normalized) == HARDWARE_COLUMNS:
            platform_tables.append(rows)

    hardware_present = "hardware requirements" in sections
    if (required_platforms or hardware_present) and not platform_tables:
        findings.append(
            Finding(
                "ERROR",
                "Hardware section has no table with the canonical platform-matrix columns.",
            )
        )

    allowed_hardware_classes = {normalize_heading(item) for item in HARDWARE_CLASSES}
    allowed_hardware_statuses = {normalize_heading(item) for item in SUPPORT_STATUSES}
    hardware_rows = [row for rows in platform_tables for row in rows]
    for row_number, row in enumerate(hardware_rows, start=1):
        if len(row) != len(HARDWARE_COLUMNS):
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware row {row_number} has {len(row)} cells; "
                    f"expected {len(HARDWARE_COLUMNS)}.",
                )
            )
            continue
        platform_label = visible_text(row[0]) or f"row {row_number}"
        if any(not visible_text(cell) for cell in row):
            findings.append(
                Finding("ERROR", f"Hardware row for {platform_label} has an empty cell.")
            )
        if normalize_heading(visible_text(row[7])) not in allowed_hardware_classes:
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware row for {platform_label} has invalid configuration class: {row[7]!r}",
                )
            )
        if normalize_heading(visible_text(row[8])) not in allowed_hardware_statuses:
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware row for {platform_label} has invalid support status: {row[8]!r}",
                )
            )
        if not evidence_ids(row[9]):
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware row for {platform_label} has no evidence ID.",
                )
            )

    for platform in required_platforms:
        found_platform_row = any(
            len(row) == len(HARDWARE_COLUMNS)
            and normalize_heading(visible_text(row[0])) == platform
            for row in hardware_rows
        )
        if not found_platform_row:
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware section has no dedicated platform-matrix row for: {platform}",
                )
            )

    evidence_section = sections.get("evidence index", "")
    evidence_classes_by_id: dict[str, str] = {}
    evidence_tables: list[list[list[str]]] = []
    for header, table_rows in markdown_tables(evidence_section):
        normalized = [normalize_heading(visible_text(cell)) for cell in header]
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
            if any(not visible_text(cell) for cell in row):
                findings.append(Finding("ERROR", "Evidence row has an empty required cell."))
            evidence_id = visible_text(row[0]).upper()
            if not re.fullmatch(r"E\d+", evidence_id):
                findings.append(Finding("ERROR", f"Invalid evidence ID: {row[0]!r}"))
                continue
            if evidence_id in defined_ids:
                findings.append(Finding("ERROR", f"Duplicate evidence ID: {evidence_id}"))
            defined_ids.add(evidence_id)
            evidence_class = visible_text(row[4])
            confidence = visible_text(row[5])
            source = visible_text(row[2])
            revision = visible_text(row[3])
            notes = visible_text(row[6])
            evidence_classes_by_id[evidence_id] = evidence_class
            if evidence_class not in EVIDENCE_CLASSES:
                findings.append(
                    Finding("ERROR", f"Evidence row {evidence_id} has invalid class: {row[4]!r}")
                )
            if confidence not in {"High", "Medium", "Low"}:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Evidence row {evidence_id} has invalid confidence: {row[5]!r}",
                    )
                )
            if source in {"", "-", "N/A"}:
                findings.append(Finding("ERROR", f"Evidence row {evidence_id} has no source."))
            if revision in {"", "-", "N/A"}:
                findings.append(Finding("WARNING", f"Evidence row {evidence_id} has no revision/date."))
            if confidence in {"Medium", "Low"} and len(notes) < 12:
                findings.append(
                    Finding(
                        "ERROR",
                        f"Evidence row {evidence_id} requires explanatory notes for {row[5]} confidence.",
                    )
                )

        report_body = text_outside_section(text, "evidence index")
        referenced_ids = evidence_ids(report_body)
        missing_ids = sorted(referenced_ids - defined_ids)
        for evidence_id in missing_ids:
            findings.append(Finding("ERROR", f"Claim references undefined evidence ID: {evidence_id}"))
        unused_ids = sorted(defined_ids - referenced_ids)
        for evidence_id in unused_ids:
            findings.append(Finding("WARNING", f"Evidence ID is not cited before the index: {evidence_id}"))

    expected_classes_by_performance_mode = {
        normalize_heading("Static analysis"): {"Derived"},
        normalize_heading("Local test"): {"Measured"},
        normalize_heading("Local profile"): {"Measured"},
        normalize_heading("Source measurement"): {"Reported"},
        normalize_heading("Community measurement"): {"Community-reported"},
    }
    for row_number, row in enumerate(performance_rows, start=1):
        if len(row) != len(PERFORMANCE_COLUMNS):
            continue
        mode = normalize_heading(visible_text(row[0]))
        expected_classes = expected_classes_by_performance_mode.get(mode)
        if expected_classes is None:
            continue
        cited_ids = evidence_ids(row[6])
        actual_classes = {
            evidence_classes_by_id[evidence_id]
            for evidence_id in cited_ids
            if evidence_id in evidence_classes_by_id
        }
        if not actual_classes.intersection(expected_classes):
            expected = " or ".join(sorted(expected_classes))
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-evidence row {row_number} with mode {row[0]!r} must cite "
                    f"at least one {expected} evidence item.",
                )
            )

    for row_number, row in enumerate(performance_dimension_rows, start=1):
        if len(row) != len(PERFORMANCE_DIMENSION_COLUMNS):
            continue
        cited_ids = evidence_ids(row[5])
        if not any(
            evidence_classes_by_id.get(evidence_id) == visible_text(row[3])
            for evidence_id in cited_ids
        ):
            findings.append(
                Finding(
                    "ERROR",
                    f"Performance-dimension row {row_number} labeled {row[3]!r} must cite "
                    "an evidence item with the same class.",
                )
            )

    expected_classes_by_hardware_class = {
        normalize_heading("Measured configuration"): {"Measured"},
        normalize_heading("Official validated configuration"): {"Reported"},
        normalize_heading("Capacity proxy"): {
            "Measured",
            "Reported",
            "Community-reported",
        },
        normalize_heading("Derived capacity estimate"): {"Derived", "Estimated"},
        normalize_heading("Recommended configuration"): {
            "Measured",
            "Reported",
            "Derived",
            "Estimated",
        },
    }
    for row_number, row in enumerate(hardware_rows, start=1):
        if len(row) != len(HARDWARE_COLUMNS):
            continue
        expected_classes = expected_classes_by_hardware_class.get(
            normalize_heading(visible_text(row[7]))
        )
        if expected_classes is None:
            continue
        cited_ids = evidence_ids(row[9])
        actual_classes = {
            evidence_classes_by_id[evidence_id]
            for evidence_id in cited_ids
            if evidence_id in evidence_classes_by_id
        }
        if not actual_classes.intersection(expected_classes):
            expected = " or ".join(sorted(expected_classes))
            findings.append(
                Finding(
                    "ERROR",
                    f"Hardware row {row_number} with configuration class {row[7]!r} must "
                    f"cite at least one {expected} evidence item.",
                )
            )

    if validate_vllm:
        support = sections.get("vllm omni support status", "")
        allowed_statuses = {normalize_heading(status) for status in SUPPORT_STATUSES}
        status_tables: list[list[list[str]]] = []
        for header, rows in markdown_tables(support):
            normalized = [normalize_heading(visible_text(cell)) for cell in header]
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
                if any(not visible_text(cell) for cell in row):
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
                value = normalize_heading(visible_text(row[4]))
                if value not in allowed_statuses:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has invalid status: {row[4]!r}",
                        )
                    )
                positive_status = value in {
                    normalize_heading("Supported"),
                    normalize_heading("Partial"),
                }
                implementation_value = normalize_heading(visible_text(row[2]))
                validation_cell = visible_text(row[3])
                validation_values = {
                    normalize_heading(part)
                    for part in validation_cell.strip("{} ").split(";")
                }
                if positive_status and implementation_value != normalize_heading("Merged/present"):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} cannot claim {row[4]!r} with "
                            f"implementation state {row[2]!r}.",
                        )
                    )
                if positive_status and any(
                    item == normalize_heading("No evidence found") or item.startswith("unknown")
                    for item in validation_values
                ):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} cannot claim {row[4]!r} without a "
                            "positive validation gate.",
                        )
                    )
                if not evidence_ids(row[6]):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Support row {row_number} has no evidence ID.",
                        )
                    )
                positive_validation = not any(
                    item == normalize_heading("No evidence found") or item.startswith("unknown")
                    for item in validation_values
                )
                if positive_validation:
                    cited_validation_ids = evidence_ids(row[6])
                    validation_classes = {
                        evidence_classes_by_id[evidence_id]
                        for evidence_id in cited_validation_ids
                        if evidence_id in evidence_classes_by_id
                    }
                    if not validation_classes.intersection(
                        {"Measured", "Reported", "Community-reported"}
                    ):
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Support row {row_number} claims validation gates without "
                                "Measured, Reported, or Community-reported run evidence.",
                            )
                        )

        optimization = sections.get("vllm omni optimization direction", "")
        optimization_tables: list[list[list[str]]] = []
        for header, rows in markdown_tables(optimization):
            normalized = [normalize_heading(visible_text(cell)) for cell in header]
            if tuple(normalized) == OPTIMIZATION_COLUMNS:
                optimization_tables.append(rows)
        if not optimization_tables or not any(optimization_tables):
            findings.append(
                Finding(
                    "ERROR",
                    "vLLM-Omni optimization section has no data table with the canonical columns.",
                )
            )
        platform_direction_columns = {"nvidia": 4, "ascend": 5}
        platform_direction_coverage = {
            platform: False
            for platform in required_platforms
            if platform in platform_direction_columns
        }
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
                if any(not visible_text(cell) for cell in row):
                    findings.append(
                        Finding("ERROR", f"Optimization row {row_number} has an empty cell.")
                    )
                for platform in platform_direction_coverage:
                    direction = visible_text(row[platform_direction_columns[platform]])
                    normalized_direction = normalize_heading(direction)
                    if normalized_direction in {"n a", "na", "not applicable"}:
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Optimization row {row_number} uses bare N/A for requested "
                                f"platform {platform}; give 'N/A — <specific reason>'.",
                            )
                        )
                    elif re.fullmatch(
                        r"\s*(?:N/?A|Not applicable)\s*(?:—|–|-|:)\s*.{8,}\s*",
                        direction,
                        re.IGNORECASE,
                    ):
                        continue
                    elif len(direction) >= 8:
                        platform_direction_coverage[platform] = True
                priority_value = visible_text(row[0])
                priority = re.match(
                    r"^\s*P[0-3]\s*(?:—|–|-|:)\s*(.+?)\s*$",
                    priority_value,
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
                bottleneck_value = visible_text(row[2])
                bottleneck = re.match(
                    r"^\s*(Observed|Measured|Reported|Community-reported|Derived|Estimated|Hypothesis)\s*"
                    r"(?:—|–|-|:)\s*(.+?)\s*$",
                    bottleneck_value,
                    re.IGNORECASE,
                )
                if not bottleneck:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} must label its bottleneck as "
                            f"one of {', '.join(BOTTLENECK_KINDS)}.",
                        )
                    )
                else:
                    priority_level = re.match(r"^\s*(P[0-3])", priority_value, re.IGNORECASE)
                    bottleneck_kind = normalize_heading(bottleneck.group(1))
                    if (
                        priority_level
                        and priority_level.group(1).casefold() == "p2"
                        and bottleneck_kind != "measured"
                    ):
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Optimization row {row_number} uses P2 for an unmeasured bottleneck; "
                                "use locally Measured evidence or rank the direction P3.",
                            )
                        )
                    cited_bottleneck_ids = evidence_ids(row[2])
                    bottleneck_classes = {
                        evidence_classes_by_id[evidence_id]
                        for evidence_id in cited_bottleneck_ids
                        if evidence_id in evidence_classes_by_id
                    }
                    expected_bottleneck_classes = {
                        "observed": {"Observed"},
                        "measured": {"Measured"},
                        "reported": {"Reported"},
                        "community reported": {"Community-reported"},
                        "derived": {"Derived"},
                        "estimated": {"Estimated"},
                        "hypothesis": {"Observed", "Derived", "Estimated"},
                    }[bottleneck_kind]
                    if not bottleneck_classes.intersection(expected_bottleneck_classes):
                        expected = " or ".join(sorted(expected_bottleneck_classes))
                        findings.append(
                            Finding(
                                "ERROR",
                                f"Optimization row {row_number} bottleneck label "
                                f"{bottleneck.group(1)!r} must cite {expected} evidence.",
                            )
                        )
                if not evidence_ids(row[2]):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has no bottleneck evidence ID.",
                        )
                    )
                if not evidence_ids(row[1]):
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} has no gap evidence ID.",
                        )
                    )
                verification_issues = optimization_verification_issues(row[8])
                declined = "verification is explicitly declined" in verification_issues
                verification_issues = [
                    issue
                    for issue in verification_issues
                    if issue != "verification is explicitly declined"
                ]
                if verification_issues:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} verification must define a concrete "
                            f"A/B contract: {', '.join(verification_issues)}.",
                        )
                    )
                if declined:
                    findings.append(
                        Finding(
                            "ERROR",
                            f"Optimization row {row_number} explicitly declines verification.",
                        )
                    )
        for platform, covered in platform_direction_coverage.items():
            if not covered:
                findings.append(
                    Finding(
                        "ERROR",
                        "vLLM-Omni optimization section has no substantive optimization or "
                        f"qualification direction for requested platform: {platform}.",
                    )
                )

    for token in MARKDOWN.parse(text):
        if (
            token.type == "fence"
            and (token.info.strip().split(maxsplit=1) or [""])[0].casefold() == "mermaid"
            and token.map is not None
        ):
            span_lines = token.map[1] - token.map[0]
            content_lines = len(token.content.splitlines())
            if span_lines < content_lines + 2:
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
