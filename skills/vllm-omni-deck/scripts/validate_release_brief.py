#!/usr/bin/env python3
"""Validate the evidence and change contract for a stable-release deck update."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ACTIONS = {"preserve", "update", "remove", "add"}
DECISIONS = {"main", "appendix", "exclude"}
RELATIONS = {"in_tag", "post_tag", "roadmap", "unverified"}
SOURCE_KINDS = {
    "release",
    "tag",
    "commit",
    "pull_request",
    "documentation",
    "test",
    "blog",
    "paper",
    "model_card",
    "issue",
    "discussion",
    "attachment",
}
SHIPPED_SOURCE_KINDS = {
    "release",
    "tag",
    "commit",
    "pull_request",
    "documentation",
    "test",
}
BENCHMARK_FIELDS = {
    "model",
    "hardware",
    "software",
    "workload",
    "metric",
    "units",
    "baseline",
    "conditions",
}
HEX_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")


def non_empty_string(value: Any) -> bool:
    """Return whether value is a non-empty string."""

    return isinstance(value, str) and bool(value.strip())


def require_strings(
    mapping: dict[str, Any], fields: set[str], path: str, errors: list[str]
) -> None:
    """Require non-empty string fields in a mapping."""

    for field in sorted(fields):
        if not non_empty_string(mapping.get(field)):
            errors.append(f"{path}.{field} must be a non-empty string")


def validate_targets(
    value: Any,
    known_slides: set[str],
    path: str,
    errors: list[str],
    *,
    required: bool,
) -> None:
    """Validate a list of slide-key references without trusting input types."""

    if not isinstance(value, list) or (required and not value):
        requirement = "a non-empty array" if required else "an array"
        errors.append(f"{path} must be {requirement}")
        return
    invalid = [target for target in value if not non_empty_string(target)]
    if invalid:
        errors.append(f"{path} must contain only non-empty strings")
    unknown = sorted(
        {target for target in value if non_empty_string(target)} - known_slides
    )
    if unknown:
        errors.append(f"{path} contains unknown slides: {unknown}")


def validate_source(source: Any, path: str, errors: list[str]) -> bool:
    """Validate one source and return whether it proves tagged shipment."""

    if not isinstance(source, dict):
        errors.append(f"{path} must be an object")
        return False
    require_strings(source, {"url", "kind", "revision"}, path, errors)
    kind = source.get("kind")
    if not isinstance(kind, str) or kind not in SOURCE_KINDS:
        errors.append(f"{path}.kind must be one of {sorted(SOURCE_KINDS)}")
    if not isinstance(source.get("primary"), bool):
        errors.append(f"{path}.primary must be a boolean")
    if source.get("included_in_target_tag") is not None and not isinstance(
        source.get("included_in_target_tag"), bool
    ):
        errors.append(f"{path}.included_in_target_tag must be a boolean")
    return (
        bool(source.get("primary"))
        and isinstance(kind, str)
        and kind in SHIPPED_SOURCE_KINDS
        and non_empty_string(source.get("revision"))
        and source.get("included_in_target_tag") is True
    )


def validate_figure(figure: Any, path: str, errors: list[str]) -> None:
    """Validate source-asset provenance and proportional fallback metadata."""

    if not isinstance(figure, dict):
        errors.append(f"{path} must be an object")
        return
    require_strings(
        figure,
        {"canonical_url", "source_revision", "original_format", "original_sha256", "usage_basis"},
        path,
        errors,
    )
    if not HEX_SHA256.fullmatch(str(figure.get("original_sha256", ""))):
        errors.append(f"{path}.original_sha256 must be a 64-character hex digest")
    ratio = figure.get("aspect_ratio")
    if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or ratio <= 0:
        errors.append(f"{path}.aspect_ratio must be a positive number")
        ratio = None
    derivative = figure.get("derivative")
    if derivative is None:
        return
    if not isinstance(derivative, dict):
        errors.append(f"{path}.derivative must be an object")
        return
    require_strings(derivative, {"format", "sha256"}, f"{path}.derivative", errors)
    if not HEX_SHA256.fullmatch(str(derivative.get("sha256", ""))):
        errors.append(f"{path}.derivative.sha256 must be a 64-character hex digest")
    derived_ratio = derivative.get("aspect_ratio")
    if (
        not isinstance(derived_ratio, (int, float))
        or isinstance(derived_ratio, bool)
        or derived_ratio <= 0
    ):
        errors.append(f"{path}.derivative.aspect_ratio must be a positive number")
    elif ratio is not None and abs(derived_ratio / ratio - 1) > 0.005:
        errors.append(f"{path}.derivative must preserve aspect ratio within 0.5%")


def validate_release_brief(document: Any) -> tuple[list[str], list[str]]:
    """Return validation errors and non-blocking warnings."""

    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(document, dict):
        return ["release brief must be a JSON object"], warnings
    if document.get("schema_version") != 1:
        errors.append("schema_version must equal 1")

    release = document.get("release")
    if not isinstance(release, dict):
        errors.append("release must be an object")
        release = {}
    require_strings(
        release,
        {"previous_tag", "current_tag", "target_commit", "cutoff_date"},
        "release",
        errors,
    )
    if release.get("previous_tag") == release.get("current_tag"):
        errors.append("release.previous_tag and release.current_tag must differ")
    if non_empty_string(release.get("cutoff_date")):
        try:
            date.fromisoformat(release["cutoff_date"])
        except ValueError:
            errors.append("release.cutoff_date must use YYYY-MM-DD")

    deck = document.get("deck")
    if not isinstance(deck, dict):
        errors.append("deck must be an object")
    else:
        require_strings(deck, {"baseline", "audience"}, "deck", errors)
        budget = deck.get("slide_budget")
        if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
            errors.append("deck.slide_budget must be a positive integer")

    slides = document.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append("slides must be a non-empty array")
        slides = []
    slide_keys: list[str] = []
    for index, slide in enumerate(slides):
        path = f"slides[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{path} must be an object")
            continue
        require_strings(slide, {"key", "role", "action"}, path, errors)
        key = slide.get("key")
        if non_empty_string(key):
            slide_keys.append(key)
        action = slide.get("action")
        if not isinstance(action, str) or action not in ACTIONS:
            errors.append(f"{path}.action must be one of {sorted(ACTIONS)}")
        if slide.get("locked") is not None and not isinstance(slide.get("locked"), bool):
            errors.append(f"{path}.locked must be a boolean")
        if slide.get("locked") and action != "preserve":
            errors.append(f"{path} is locked and must use action 'preserve'")
        if action in ("add", "update"):
            layout = slide.get("layout")
            if not isinstance(layout, dict):
                errors.append(f"{path}.layout must be an object for {action} actions")
                continue
            require_strings(
                layout,
                {"exemplar_slide_id", "placement_notes", "source_position"},
                f"{path}.layout",
                errors,
            )
            for field in ("title_max_lines", "subtitle_max_lines"):
                if layout.get(field) not in (1, 2):
                    errors.append(f"{path}.layout.{field} must equal 1 or 2")
            if layout.get("protected_footer") is not True:
                errors.append(f"{path}.layout.protected_footer must be true")
    duplicates = sorted(key for key, count in Counter(slide_keys).items() if count > 1)
    if duplicates:
        errors.append(f"slide keys must be unique; duplicates: {duplicates}")
    known_slides = set(slide_keys)

    instructions = document.get("instructions", [])
    if not isinstance(instructions, list):
        errors.append("instructions must be an array")
        instructions = []
    for index, instruction in enumerate(instructions):
        path = f"instructions[{index}]"
        if not isinstance(instruction, dict):
            errors.append(f"{path} must be an object")
            continue
        require_strings(instruction, {"text"}, path, errors)
        validate_targets(
            instruction.get("slide_keys"),
            known_slides,
            f"{path}.slide_keys",
            errors,
            required=True,
        )

    highlights = document.get("highlights")
    if not isinstance(highlights, list) or not highlights:
        errors.append("highlights must be a non-empty array")
        highlights = []
    highlight_ids: list[str] = []
    main_categories: list[str] = []
    main_count = 0
    for index, highlight in enumerate(highlights):
        path = f"highlights[{index}]"
        if not isinstance(highlight, dict):
            errors.append(f"{path} must be an object")
            continue
        require_strings(
            highlight,
            {
                "id",
                "claim",
                "category",
                "user_impact",
                "decision",
                "decision_reason",
                "release_relation",
            },
            path,
            errors,
        )
        if non_empty_string(highlight.get("id")):
            highlight_ids.append(highlight["id"])
        decision = highlight.get("decision")
        relation = highlight.get("release_relation")
        if not isinstance(decision, str) or decision not in DECISIONS:
            errors.append(f"{path}.decision must be one of {sorted(DECISIONS)}")
        if not isinstance(relation, str) or relation not in RELATIONS:
            errors.append(f"{path}.release_relation must be one of {sorted(RELATIONS)}")
        selected = decision in ("main", "appendix")
        if decision == "main":
            main_count += 1
            if non_empty_string(highlight.get("category")):
                main_categories.append(highlight["category"])
        targets = highlight.get("slide_keys", [])
        validate_targets(
            targets,
            known_slides,
            f"{path}.slide_keys",
            errors,
            required=selected,
        )
        if selected and relation == "unverified":
            errors.append(f"{path} cannot select unverified evidence")
        if selected and relation in ("post_tag", "roadmap"):
            label = str(highlight.get("presentation_label", "")).casefold()
            if relation == "roadmap" and "roadmap" not in label:
                errors.append(f"{path}.presentation_label must visibly say roadmap")
            if relation == "post_tag" and not any(
                marker in label for marker in ("post-tag", "post-release")
            ):
                errors.append(
                    f"{path}.presentation_label must visibly say post-tag or post-release"
                )

        sources = highlight.get("sources", [])
        if not isinstance(sources, list) or (selected and not sources):
            errors.append(f"{path}.sources must be a non-empty array for selected highlights")
            sources = []
        source_checks = [
            validate_source(source, f"{path}.sources[{source_index}]", errors)
            for source_index, source in enumerate(sources)
        ]
        proves_shipment = any(source_checks)
        if selected and relation == "in_tag" and not proves_shipment:
            errors.append(f"{path} needs a primary tag-pinned source that proves shipment")

        quantitative = highlight.get("quantitative", False)
        if not isinstance(quantitative, bool):
            errors.append(f"{path}.quantitative must be a boolean")
        if quantitative:
            if not isinstance(highlight.get("carried_forward"), bool):
                errors.append(f"{path}.carried_forward must be a boolean")
            benchmark = highlight.get("benchmark")
            if not isinstance(benchmark, dict):
                errors.append(f"{path}.benchmark must be an object for quantitative claims")
            else:
                require_strings(benchmark, BENCHMARK_FIELDS, f"{path}.benchmark", errors)
            if (
                highlight.get("carried_forward")
                and highlight.get("revalidated_for_release") is not True
            ):
                errors.append(
                    f"{path} carries quantitative evidence without release revalidation"
                )

        figures = highlight.get("figures", [])
        if not isinstance(figures, list):
            errors.append(f"{path}.figures must be an array")
        else:
            for figure_index, figure in enumerate(figures):
                validate_figure(figure, f"{path}.figures[{figure_index}]", errors)
        results = highlight.get("results", [])
        if (
            selected
            and non_empty_string(highlight.get("mechanism_summary"))
            and isinstance(results, list)
            and len(results) >= 2
            and highlight.get("presentation_pattern") != "mechanism_then_results"
        ):
            warnings.append(
                f"{path} should split mechanism and extensive results across two slides"
            )

    duplicate_highlights = sorted(
        key for key, count in Counter(highlight_ids).items() if count > 1
    )
    if duplicate_highlights:
        errors.append(f"highlight ids must be unique; duplicates: {duplicate_highlights}")
    if main_count > 5:
        warnings.append("more than five main highlights may weaken the release narrative")
    if main_count > 1 and len(set(main_categories)) == 1:
        warnings.append("all main highlights use one category; review narrative balance")
    return errors, warnings


def main() -> int:
    """Validate a JSON release brief from the command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()
    try:
        document = json.loads(args.brief.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    errors, warnings = validate_release_brief(document)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors or (warnings and args.warnings_as_errors):
        return 1
    print("release brief is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
