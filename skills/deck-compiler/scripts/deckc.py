#!/usr/bin/env python3
"""Validate and analyze general-purpose deck specifications."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import defaultdict, deque
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised only in missing environments
    raise SystemExit(
        "deckc requires PyYAML and jsonschema. Run with "
        "`uv run --with pyyaml --with jsonschema python scripts/deckc.py ...`."
    ) from exc


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_DIR / "references" / "deck-spec.schema.json"
DEFAULT_PROFILES = SKILL_DIR / "references" / "narrative-profiles.yaml"


@dataclass(frozen=True)
class Diagnostic:
    level: str
    code: str
    path: str
    message: str


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a YAML mapping at the root.")
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object at the root.")
    return value


def assert_canonical_json_value(
    value: Any,
    *,
    path: str = "$",
    active_containers: set[int] | None = None,
) -> None:
    """Reject Python/YAML values without a one-to-one UTF-8 JSON encoding."""
    active = active_containers if active_containers is not None else set()
    if type(value) is dict:
        container_id = id(value)
        if container_id in active:
            raise ValueError(f"{path} contains a circular object reference")
        active.add(container_id)
        try:
            for key, item in value.items():
                if type(key) is not str:
                    raise TypeError(f"{path} contains non-string object key {key!r}")
                try:
                    key.encode("utf-8")
                except UnicodeEncodeError as exc:
                    raise ValueError(
                        f"{path} contains an object key that is not valid UTF-8"
                    ) from exc
                assert_canonical_json_value(
                    item,
                    path=f"{path}.{key}",
                    active_containers=active,
                )
        finally:
            active.remove(container_id)
        return
    if type(value) is list:
        container_id = id(value)
        if container_id in active:
            raise ValueError(f"{path} contains a circular array reference")
        active.add(container_id)
        try:
            for index, item in enumerate(value):
                assert_canonical_json_value(
                    item,
                    path=f"{path}[{index}]",
                    active_containers=active,
                )
        finally:
            active.remove(container_id)
        return
    if type(value) is str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError(
                f"{path} contains a string that is not valid UTF-8"
            ) from exc
        return
    if value is None or type(value) in {bool, int, float}:
        return
    raise TypeError(f"{path} contains unsupported value type {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    assert_canonical_json_value(value)
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return text.encode("utf-8")


def canonical_json(value: Any) -> str:
    return canonical_json_bytes(value).decode("utf-8")


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def release_deck(deck: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in deck.items() if key != "operation"}


def semantic_payload(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "deck": release_deck(spec["deck"]),
        "profiles": spec["profiles"],
        "narrative": spec["narrative"],
        "sources": spec.get("sources", {}),
        "claims": spec.get("claims", {}),
        "qa": spec.get("qa", {}),
    }


def release_payload(spec: dict[str, Any]) -> dict[str, Any]:
    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    payload = {
        "schema_version": spec["schema_version"],
        "slides": {
            "order": order,
            "items": {slide_id: items[slide_id] for slide_id in order},
        },
    }
    payload.update(semantic_payload(spec))
    return payload


def release_fingerprint(spec: dict[str, Any]) -> str:
    return fingerprint(release_payload(spec))


def manifest_root_fingerprint(
    schema_version: int,
    release_fingerprint_value: str,
    history_fingerprint_value: str,
) -> str:
    return fingerprint(
        {
            "schema_version": schema_version,
            "release_fingerprint": release_fingerprint_value,
            "history_fingerprint": history_fingerprint_value,
        }
    )


def format_path(parts: Iterable[Any]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def schema_diagnostics(
    spec: dict[str, Any], schema: dict[str, Any]
) -> list[Diagnostic]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    diagnostics = []
    for error in sorted(
        validator.iter_errors(spec),
        key=lambda item: (format_path(item.absolute_path), item.message),
    ):
        diagnostics.append(
            Diagnostic(
                "error",
                "schema",
                format_path(error.absolute_path),
                error.message,
            )
        )
    return diagnostics


def serialization_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    try:
        canonical_json_bytes(spec)
    except (TypeError, ValueError) as exc:
        return [
            Diagnostic(
                "error",
                "non-json-value",
                "$",
                "Deck specification must contain only finite, UTF-8 "
                f"JSON-compatible values with string object keys: {exc}",
            )
        ]
    return []


def ordered(values: Iterable[str], slide_order: list[str]) -> list[str]:
    rank = {slide_id: index for index, slide_id in enumerate(slide_order)}
    return sorted(set(values), key=lambda item: (rank.get(item, len(rank)), item))


def reference_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    slides = spec.get("slides", {})
    slide_order = slides.get("order", [])
    slide_items = slides.get("items", {})
    sources = spec.get("sources", {})
    claims = spec.get("claims", {})

    missing_items = [
        slide_id for slide_id in slide_order if slide_id not in slide_items
    ]
    for slide_id in missing_items:
        diagnostics.append(
            Diagnostic(
                "error",
                "unknown-slide",
                "$.slides.order",
                f"Slide {slide_id!r} is ordered but has no blueprint.",
            )
        )

    active_items = set(slide_items)
    for slide_id in sorted(active_items - set(slide_order)):
        diagnostics.append(
            Diagnostic(
                "error",
                "unordered-slide",
                f"$.slides.items.{slide_id}",
                "Active slide is missing from slides.order.",
            )
        )
    for slide_id in slide_order:
        if slide_items.get(slide_id, {}).get("status") == "superseded":
            diagnostics.append(
                Diagnostic(
                    "error",
                    "ordered-superseded-slide",
                    f"$.slides.items.{slide_id}.status",
                    "A superseded slide cannot remain in slides.order.",
                )
            )

    chapter_ids: set[str] = set()
    for index, chapter in enumerate(spec.get("narrative", {}).get("chapters", [])):
        chapter_id = chapter.get("id")
        if chapter_id in chapter_ids:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "duplicate-chapter",
                    f"$.narrative.chapters[{index}].id",
                    f"Duplicate chapter ID {chapter_id!r}.",
                )
            )
        chapter_ids.add(chapter_id)
        for slide_id in chapter.get("slide_ids", []):
            if slide_id not in slide_order:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "inactive-slide",
                        f"$.narrative.chapters[{index}].slide_ids",
                        f"Chapter references inactive slide {slide_id!r}.",
                    )
                )

    for claim_id, claim in claims.items():
        for source_id in claim.get("source_ids", []):
            if source_id not in sources:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unknown-source",
                        f"$.claims.{claim_id}.source_ids",
                        f"Unknown source {source_id!r}.",
                    )
                )
        for supporting_id in claim.get("supporting_claim_ids", []):
            if supporting_id not in claims:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unknown-claim",
                        f"$.claims.{claim_id}.supporting_claim_ids",
                        f"Unknown supporting claim {supporting_id!r}.",
                    )
                )

    diagnostics.extend(claim_support_diagnostics(claims))

    dependency_graph: dict[str, set[str]] = defaultdict(set)
    for slide_id, slide in slide_items.items():
        for claim_id in slide.get("claim_ids", []):
            if claim_id not in claims:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unknown-claim",
                        f"$.slides.items.{slide_id}.claim_ids",
                        f"Unknown claim {claim_id!r}.",
                    )
                )
        for source_id in slide.get("source_ids", []):
            if source_id not in sources:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unknown-source",
                        f"$.slides.items.{slide_id}.source_ids",
                        f"Unknown source {source_id!r}.",
                    )
                )
        for dependency in slide.get("dependencies", []):
            target = dependency.get("target")
            if target not in slide_order:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "inactive-dependency",
                        f"$.slides.items.{slide_id}.dependencies",
                        f"Dependency targets inactive slide {target!r}.",
                    )
                )
            elif dependency.get("propagates", True):
                dependency_graph[slide_id].add(target)

    diagnostics.extend(cycle_diagnostics(dependency_graph))
    diagnostics.extend(change_set_reference_diagnostics(spec))
    return diagnostics


def claim_support_diagnostics(claims: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    graph = {
        claim_id: set(claim.get("supporting_claim_ids", []))
        for claim_id, claim in claims.items()
    }
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(claim_id: str) -> None:
        if claim_id in visited:
            return
        if claim_id in visiting:
            start = stack.index(claim_id)
            cycle = tuple(stack[start:] + [claim_id])
            if cycle not in cycles:
                cycles.add(cycle)
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "claim-support-cycle",
                        f"$.claims.{claim_id}.supporting_claim_ids",
                        "Claim support cycle: " + " -> ".join(cycle),
                    )
                )
            return
        visiting.add(claim_id)
        stack.append(claim_id)
        for supporting_id in sorted(graph.get(claim_id, ())):
            if supporting_id in claims:
                visit(supporting_id)
        stack.pop()
        visiting.remove(claim_id)
        visited.add(claim_id)

    for claim_id in sorted(graph):
        visit(claim_id)

    def reaches_source(claim_id: str, seen: set[str]) -> bool:
        if claim_id in seen:
            return False
        claim = claims.get(claim_id, {})
        if claim.get("source_ids"):
            return True
        next_seen = seen | {claim_id}
        return any(
            reaches_source(supporting_id, next_seen)
            for supporting_id in claim.get("supporting_claim_ids", [])
        )

    for claim_id, claim in claims.items():
        if (
            "inference" in claim.get("classes", [])
            and not claim.get("source_ids")
            and claim.get("supporting_claim_ids")
            and not reaches_source(claim_id, set())
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "inference-support-not-grounded",
                    f"$.claims.{claim_id}.supporting_claim_ids",
                    "Inference support must reach a source-backed claim.",
                )
            )
    return diagnostics


def cycle_diagnostics(graph: dict[str, set[str]]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            start = stack.index(node)
            cycle = tuple(stack[start:] + [node])
            if cycle not in reported:
                reported.add(cycle)
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "dependency-cycle",
                        f"$.slides.items.{node}.dependencies",
                        "Propagating dependency cycle: " + " -> ".join(cycle),
                    )
                )
            return
        visiting.add(node)
        stack.append(node)
        for target in sorted(graph.get(node, ())):
            visit(target)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)
    return diagnostics


def change_set_reference_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    slide_items = spec.get("slides", {}).get("items", {})
    slide_order = spec.get("slides", {}).get("order", [])
    seen_ids: set[str] = set()
    for index, change_set in enumerate(spec.get("change_sets", [])):
        base_path = f"$.change_sets[{index}]"
        change_id = change_set.get("id")
        if change_id in seen_ids:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "duplicate-change-set",
                    f"{base_path}.id",
                    f"Duplicate change-set ID {change_id!r}.",
                )
            )
        seen_ids.add(change_id)
        modification_ids = [
            modification.get("slide") for modification in change_set.get("modify", [])
        ]
        insertion_ids = [
            insertion.get("slide") for insertion in change_set.get("insert", [])
        ]
        modify = set(modification_ids)
        remove = set(change_set.get("remove", []))
        inserted = set(insertion_ids)
        preserve = set(change_set.get("preserve", []))
        review = set(change_set.get("review", []))
        status = change_set.get("status")

        for action, identifiers in (
            ("modify", modification_ids),
            ("insert", insertion_ids),
        ):
            duplicates = sorted(
                {
                    slide_id
                    for slide_id in identifiers
                    if identifiers.count(slide_id) > 1
                }
            )
            if duplicates:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        f"duplicate-{action}",
                        f"{base_path}.{action}",
                        f"Slides appear more than once in {action}: "
                        + ", ".join(duplicates),
                    )
                )

        existing_references: set[str] = set()
        if status == "proposed":
            existing_references = modify | remove | preserve | review
        elif status == "approved":
            existing_references = modify | preserve | review
        for slide_id in sorted(existing_references):
            if slide_id not in slide_items:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unknown-slide",
                        base_path,
                        f"Change set references unknown slide {slide_id!r}.",
                    )
                )

        action_sets = {
            "modify": modify,
            "insert": inserted,
            "remove": remove,
            "preserve": preserve,
        }
        action_names = list(action_sets)
        for left_index, left_name in enumerate(action_names):
            for right_name in action_names[left_index + 1 :]:
                conflicts = action_sets[left_name] & action_sets[right_name]
                if conflicts:
                    diagnostics.append(
                        Diagnostic(
                            "error",
                            "change-action-conflict",
                            base_path,
                            f"Slides cannot appear in both {left_name} and "
                            f"{right_name}: " + ", ".join(sorted(conflicts)),
                        )
                    )

        target_order = change_set.get("target_order", [])
        if (
            status in {"proposed", "approved"}
            and set(target_order) != (set(slide_order) | inserted) - remove
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "target-order-mismatch",
                    f"{base_path}.target_order",
                    "Target order must contain the current active slides plus "
                    "insertions and minus removals.",
                )
            )
        if status == "approved":
            target_fingerprint = change_set.get("target_fingerprint")
            if not target_fingerprint:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "target-fingerprint-required",
                        f"{base_path}.target_fingerprint",
                        "Approved change set requires the projected release "
                        "fingerprint reported by impact analysis.",
                    )
                )
            elif target_fingerprint != release_fingerprint(spec):
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "target-fingerprint-mismatch",
                        f"{base_path}.target_fingerprint",
                        "Active semantic release payload does not match the "
                        "approved target fingerprint.",
                    )
                )
            if not change_set.get("target_manifest_fingerprint"):
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "target-manifest-fingerprint-required",
                        f"{base_path}.target_manifest_fingerprint",
                        "Approved change set requires the projected manifest "
                        "fingerprint reported by impact analysis.",
                    )
                )

        for modification_index, modification in enumerate(change_set.get("modify", [])):
            slide_id = modification.get("slide")
            if (
                status == "approved"
                and slide_id in slide_items
                and fingerprint(modification.get("blueprint"))
                != fingerprint(slide_items[slide_id])
            ):
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "unapplied-modification",
                        f"{base_path}.modify[{modification_index}]",
                        f"Approved blueprint for {slide_id!r} does not match "
                        "the active slide.",
                    )
                )

        for insertion_index, insertion in enumerate(change_set.get("insert", [])):
            slide_id = insertion.get("slide")
            if status == "proposed" and slide_id in slide_order:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "preapplied-insertion",
                        f"{base_path}.insert[{insertion_index}]",
                        f"Proposed insertion {slide_id!r} is already active.",
                    )
                )
            if status == "approved":
                if slide_id not in slide_order:
                    diagnostics.append(
                        Diagnostic(
                            "error",
                            "unapplied-insertion",
                            f"{base_path}.insert[{insertion_index}]",
                            f"Approved insertion {slide_id!r} is not active.",
                        )
                    )
                elif fingerprint(insertion.get("blueprint")) != fingerprint(
                    slide_items.get(slide_id)
                ):
                    diagnostics.append(
                        Diagnostic(
                            "error",
                            "insertion-blueprint-mismatch",
                            f"{base_path}.insert[{insertion_index}]",
                            f"Approved blueprint for {slide_id!r} does not "
                            "match the active slide.",
                        )
                    )
    return diagnostics


def narrative_diagnostics(
    spec: dict[str, Any], profiles: dict[str, Any]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    profile_id = spec.get("profiles", {}).get("narrative")
    profile = profiles.get("profiles", {}).get(profile_id)
    required_roles = spec.get("narrative", {}).get("required_roles", [])
    if profile is None and not required_roles:
        return [
            Diagnostic(
                "error",
                "unknown-narrative-profile",
                "$.profiles.narrative",
                f"Unknown narrative profile {profile_id!r}; declare narrative.required_roles for a custom profile.",
            )
        ]

    order = spec.get("slides", {}).get("order", [])
    items = spec.get("slides", {}).get("items", {})
    role_positions: dict[str, list[int]] = defaultdict(list)
    for index, slide_id in enumerate(order):
        for role in items.get(slide_id, {}).get("narrative_roles", []):
            role_positions[role].append(index)

    group_positions: list[tuple[str, int]] = []
    for group in (profile or {}).get("required_role_groups", []):
        candidates = [
            position
            for role in group.get("any_of", [])
            for position in role_positions.get(role, [])
        ]
        if not candidates:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "missing-narrative-role",
                    "$.slides.items",
                    f"Narrative profile {profile_id!r} is missing role group {group.get('id')!r}.",
                )
            )
        else:
            group_positions.append((group.get("id", ""), min(candidates)))

    if (profile or {}).get("ordered", True):
        for previous, current in pairwise(group_positions):
            if current[1] < previous[1]:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "narrative-order",
                        "$.slides.order",
                        f"Narrative role group {current[0]!r} appears before {previous[0]!r}.",
                    )
                )

    for role in required_roles:
        if not role_positions.get(role):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "missing-custom-role",
                    "$.narrative.required_roles",
                    f"Custom narrative role {role!r} is not assigned to any slide.",
                )
            )
    return diagnostics


def claim_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    claims = spec.get("claims", {})
    referenced_claims = {
        claim_id
        for slide in spec.get("slides", {}).get("items", {}).values()
        for claim_id in slide.get("claim_ids", [])
    }
    for claim_id, claim in claims.items():
        path = f"$.claims.{claim_id}"
        classes = set(claim.get("classes", []))
        sources = claim.get("source_ids", [])
        supporting = claim.get("supporting_claim_ids", [])
        confidence = claim.get("confidence")
        measurement = claim.get("measurement", {})
        acceptance = claim.get("acceptance", {})

        if "fact" in classes and not sources:
            diagnostics.append(
                Diagnostic(
                    "error", "fact-needs-source", path, "Fact requires a source."
                )
            )
        if "inference" in classes:
            if confidence is None:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "inference-needs-confidence",
                        path,
                        "Inference requires confidence.",
                    )
                )
            if not sources and not supporting:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "inference-needs-support",
                        path,
                        "Inference requires a source or supporting claim.",
                    )
                )
        if "target" in classes:
            missing = [
                field
                for field in ("owner", "timeline", "gates")
                if not acceptance.get(field)
            ]
            if missing:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "target-needs-acceptance",
                        path,
                        "Target requires acceptance fields: " + ", ".join(missing),
                    )
                )
        if "comparative" in classes:
            missing = [
                field
                for field in ("baseline", "conditions")
                if not acceptance.get(field)
            ]
            if missing:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "comparison-needs-envelope",
                        path,
                        "Comparative claim requires acceptance fields: "
                        + ", ".join(missing),
                    )
                )
        if "quantitative" in classes:
            missing = [
                field
                for field in ("metric", "unit", "conditions")
                if not measurement.get(field)
            ]
            if missing:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "quantitative-needs-measurement",
                        path,
                        "Quantitative claim requires measurement fields: "
                        + ", ".join(missing),
                    )
                )
        if "illustrative" in classes and not claim.get("display_label"):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "illustrative-needs-label",
                    path,
                    "Illustrative claim requires a visible display_label.",
                )
            )
        if claim_id not in referenced_claims:
            diagnostics.append(
                Diagnostic(
                    "warning",
                    "unreferenced-claim",
                    path,
                    "Claim is not referenced by an active slide.",
                )
            )
    return diagnostics


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def policy_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    qa = spec.get("qa", {})
    searchable = "\n".join(iter_strings(spec.get("slides", {})))
    searchable_folded = searchable.casefold()
    for term in qa.get("forbidden_terms", []):
        if term.casefold() in searchable_folded:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "forbidden-term",
                    "$.slides",
                    f"Forbidden term appears in slide content: {term!r}.",
                )
            )

    claims = spec.get("claims", {})
    items = spec.get("slides", {}).get("items", {})
    for rule_index, rule in enumerate(qa.get("claim_term_rules", [])):
        try:
            pattern = re.compile(rule["pattern"])
        except re.error as exc:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-claim-term-pattern",
                    f"$.qa.claim_term_rules[{rule_index}].pattern",
                    str(exc),
                )
            )
            continue
        required_class = rule["required_class"]
        for slide_id, slide in items.items():
            slide_text = "\n".join(iter_strings(slide))
            if not pattern.search(slide_text):
                continue
            referenced_classes = {
                claim_class
                for claim_id in slide.get("claim_ids", [])
                for claim_class in claims.get(claim_id, {}).get("classes", [])
            }
            if required_class not in referenced_classes:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "claim-term-needs-contract",
                        f"$.slides.items.{slide_id}",
                        f"Pattern {rule['pattern']!r} requires a referenced "
                        f"{required_class!r} claim.",
                    )
                )
    return diagnostics


def approval_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    items = spec.get("slides", {}).get("items", {})
    for slide_id, slide in items.items():
        if slide.get("locked") and slide.get("status") != "approved":
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-lock-state",
                    f"$.slides.items.{slide_id}",
                    "Only an approved slide may be locked.",
                )
            )
        if slide.get("status") == "approved" and not slide.get("locked"):
            diagnostics.append(
                Diagnostic(
                    "warning",
                    "approved-slide-unlocked",
                    f"$.slides.items.{slide_id}",
                    "Approved slide is not locked.",
                )
            )

    for index, change_set in enumerate(spec.get("change_sets", [])):
        if change_set.get("status") != "proposed":
            continue
        changed = {item.get("slide") for item in change_set.get("modify", [])} | set(
            change_set.get("remove", [])
        )
        locked = [
            slide_id for slide_id in changed if items.get(slide_id, {}).get("locked")
        ]
        if locked:
            diagnostics.append(
                Diagnostic(
                    "warning",
                    "authorization-required",
                    f"$.change_sets[{index}]",
                    "Locked slides require approved change-set authorization: "
                    + ", ".join(sorted(locked)),
                )
            )
    return diagnostics


def release_diagnostics(spec: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    items = spec.get("slides", {}).get("items", {})
    for slide_id in spec.get("slides", {}).get("order", []):
        slide = items.get(slide_id, {})
        if slide.get("status") != "approved" or not slide.get("locked"):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "slide-not-release-approved",
                    f"$.slides.items.{slide_id}",
                    "Manifest emission requires every active slide to be "
                    "approved and locked.",
                )
            )
    for index, change_set in enumerate(spec.get("change_sets", [])):
        if change_set.get("status") == "proposed":
            diagnostics.append(
                Diagnostic(
                    "error",
                    "pending-change-set",
                    f"$.change_sets[{index}]",
                    "Approve or supersede the proposed change set before "
                    "emitting a manifest.",
                )
            )
    return diagnostics


def validate_spec(spec: dict[str, Any], schema: dict[str, Any]) -> list[Diagnostic]:
    diagnostics = serialization_diagnostics(spec)
    if diagnostics:
        return diagnostics
    diagnostics.extend(schema_diagnostics(spec, schema))
    if any(item.level == "error" for item in diagnostics):
        return diagnostics
    diagnostics.extend(reference_diagnostics(spec))
    return diagnostics


def lint_spec(
    spec: dict[str, Any],
    schema: dict[str, Any],
    profiles: dict[str, Any],
) -> list[Diagnostic]:
    diagnostics = validate_spec(spec, schema)
    if any(item.level == "error" for item in diagnostics):
        return diagnostics
    diagnostics.extend(narrative_diagnostics(spec, profiles))
    diagnostics.extend(claim_diagnostics(spec))
    diagnostics.extend(policy_diagnostics(spec))
    diagnostics.extend(approval_diagnostics(spec))
    return diagnostics


def find_change_set(spec: dict[str, Any], change_id: str) -> dict[str, Any]:
    for change_set in spec.get("change_sets", []):
        if change_set.get("id") == change_id:
            return change_set
    raise KeyError(change_id)


def spec_from_manifest(
    baseline: dict[str, Any],
    operation: str,
    target_semantics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    semantics = target_semantics or {
        "deck": release_deck(baseline["deck"]),
        "profiles": baseline["profiles"],
        "narrative": baseline["narrative"],
        "sources": baseline["sources"],
        "claims": baseline["claims"],
        "qa": baseline["qa"],
    }
    deck = copy.deepcopy(semantics["deck"])
    deck["operation"] = operation
    return {
        "schema_version": baseline["schema_version"],
        "deck": deck,
        "profiles": copy.deepcopy(semantics["profiles"]),
        "narrative": copy.deepcopy(semantics["narrative"]),
        "sources": copy.deepcopy(semantics["sources"]),
        "claims": copy.deepcopy(semantics["claims"]),
        "slides": {
            "order": [slide["id"] for slide in baseline["slides"]],
            "items": {
                slide["id"]: copy.deepcopy(slide["blueprint"])
                for slide in baseline["slides"]
            },
        },
        "change_sets": [],
        "qa": copy.deepcopy(semantics["qa"]),
    }


def projected_spec(
    spec: dict[str, Any],
    change_set: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    projected = spec_from_manifest(
        baseline,
        spec["deck"]["operation"],
        change_set.get("target_semantics"),
    )
    items = projected["slides"]["items"]
    for modification in change_set.get("modify", []):
        items[modification["slide"]] = copy.deepcopy(modification["blueprint"])
    for insertion in change_set.get("insert", []):
        items[insertion["slide"]] = copy.deepcopy(insertion["blueprint"])
    for slide_id in change_set.get("remove", []):
        items.pop(slide_id, None)
    projected["slides"]["order"] = list(change_set["target_order"])
    return projected


def slide_diff(
    baseline: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, set[str]]:
    baseline_fingerprints = {
        slide["id"]: slide["fingerprint"] for slide in baseline["slides"]
    }
    target_order = target["slides"]["order"]
    target_items = target["slides"]["items"]
    target_fingerprints = {
        slide_id: fingerprint(target_items[slide_id]) for slide_id in target_order
    }
    baseline_ids = set(baseline_fingerprints)
    target_ids = set(target_fingerprints)
    return {
        "modify": {
            slide_id
            for slide_id in baseline_ids & target_ids
            if baseline_fingerprints[slide_id] != target_fingerprints[slide_id]
        },
        "insert": target_ids - baseline_ids,
        "remove": baseline_ids - target_ids,
    }


def semantic_impact(
    baseline: dict[str, Any],
    projected: dict[str, Any],
) -> dict[str, Any]:
    baseline_spec = spec_from_manifest(
        baseline,
        projected["deck"]["operation"],
    )
    baseline_semantics = semantic_payload(baseline_spec)
    target_semantics = semantic_payload(projected)
    changed_sections = {
        key
        for key in baseline_semantics
        if baseline_semantics[key] != target_semantics[key]
    }

    def changed_keys(left: dict[str, Any], right: dict[str, Any]) -> set[str]:
        return {
            key for key in set(left) | set(right) if left.get(key) != right.get(key)
        }

    baseline_sources = baseline_semantics["sources"]
    target_sources = target_semantics["sources"]
    changed_sources = changed_keys(baseline_sources, target_sources)
    baseline_claims = baseline_semantics["claims"]
    target_claims = target_semantics["claims"]
    changed_claims = changed_keys(baseline_claims, target_claims)

    affected_claims = set(changed_claims)
    combined_claims = {**baseline_claims, **target_claims}
    expanded = True
    while expanded:
        expanded = False
        for claim_id, claim in combined_claims.items():
            if claim_id in affected_claims:
                continue
            if (
                set(claim.get("source_ids", [])) & changed_sources
                or set(claim.get("supporting_claim_ids", [])) & affected_claims
            ):
                affected_claims.add(claim_id)
                expanded = True

    baseline_items = baseline_spec["slides"]["items"]
    target_items = projected["slides"]["items"]
    combined_items = {**baseline_items, **target_items}
    affected_slides = {
        slide_id
        for slide_id, slide in combined_items.items()
        if set(slide.get("source_ids", [])) & changed_sources
        or set(slide.get("claim_ids", [])) & affected_claims
    }
    global_sections = changed_sections & {"deck", "profiles", "narrative", "qa"}
    if global_sections:
        affected_slides.update(combined_items)

    return {
        "sections": changed_sections,
        "sources": changed_sources,
        "claims": changed_claims,
        "affected_claims": affected_claims,
        "affected_slides": affected_slides,
        "global_sections": global_sections,
    }


def declared_changed_slides(change_set: dict[str, Any]) -> set[str]:
    return (
        {modification["slide"] for modification in change_set.get("modify", [])}
        | {insertion["slide"] for insertion in change_set.get("insert", [])}
        | set(change_set.get("remove", []))
    )


def semantic_review_required(
    baseline: dict[str, Any],
    projected: dict[str, Any],
    change_set: dict[str, Any],
) -> set[str]:
    impact = semantic_impact(baseline, projected)
    baseline_items = {slide["id"]: slide["blueprint"] for slide in baseline["slides"]}
    combined_items = {**baseline_items, **projected["slides"]["items"]}
    return {
        slide_id
        for slide_id in impact["affected_slides"]
        if slide_id not in declared_changed_slides(change_set)
        and combined_items.get(slide_id, {}).get("locked")
    }


def impact_diagnostics(
    spec: dict[str, Any],
    baseline: dict[str, Any],
    change_id: str,
    schema: dict[str, Any],
    profiles: dict[str, Any],
) -> tuple[list[Diagnostic], dict[str, Any] | None]:
    diagnostics = baseline_manifest_diagnostics(baseline)
    if has_errors(diagnostics):
        return diagnostics, None
    try:
        change_set = find_change_set(spec, change_id)
    except KeyError:
        return [
            Diagnostic(
                "error",
                "unknown-change-set",
                "$.change_sets",
                f"No change set named {change_id!r}.",
            )
        ], None

    if spec.get("deck", {}).get("operation") == "create":
        diagnostics.append(
            Diagnostic(
                "error",
                "revision-operation-required",
                "$.deck.operation",
                "Change-set impact requires revise, restyle, or migrate operation.",
            )
        )
    if change_set.get("status") != "proposed":
        diagnostics.append(
            Diagnostic(
                "error",
                "change-set-not-proposed",
                "$.change_sets",
                "Impact analysis requires a proposed change set.",
            )
        )
    if change_id in {item.get("id") for item in baseline.get("applied_changes", [])}:
        diagnostics.append(
            Diagnostic(
                "error",
                "reused-change-id",
                "$.change_sets",
                f"Change-set ID {change_id!r} already exists in manifest history.",
            )
        )
    if change_set.get("baseline_fingerprint") != baseline.get("manifest_fingerprint"):
        diagnostics.append(
            Diagnostic(
                "error",
                "baseline-fingerprint-mismatch",
                "$.change_sets",
                "Proposed change set does not target this baseline manifest.",
            )
        )
    if spec.get("deck", {}).get("id") != baseline.get("deck", {}).get("id"):
        diagnostics.append(
            Diagnostic(
                "error",
                "baseline-deck-mismatch",
                "$.deck.id",
                "Baseline manifest belongs to a different deck.",
            )
        )
    if release_fingerprint(spec) != baseline.get("release_fingerprint"):
        diagnostics.append(
            Diagnostic(
                "error",
                "preapplied-drift",
                "$",
                "Active deck differs from the baseline. Keep all candidate "
                "changes inside the proposed change set.",
            )
        )

    retired = set(baseline.get("retired_slide_ids", []))
    reused = {
        insertion["slide"]
        for insertion in change_set.get("insert", [])
        if insertion["slide"] in retired
    }
    if reused:
        diagnostics.append(
            Diagnostic(
                "error",
                "retired-slide-id",
                "$.change_sets",
                "Retired slide IDs cannot be reused: " + ", ".join(sorted(reused)),
            )
        )
    if has_errors(diagnostics):
        return diagnostics, None

    projected = projected_spec(spec, change_set, baseline)
    if projected["deck"]["id"] != baseline["deck"]["id"]:
        diagnostics.append(
            Diagnostic(
                "error",
                "target-deck-id-mismatch",
                "$.change_sets",
                "Target semantics cannot change the stable deck ID.",
            )
        )
    projected_diagnostics = lint_spec(projected, schema, profiles)
    projected_diagnostics.extend(release_diagnostics(projected))
    diagnostics.extend(projected_diagnostics)

    actual = slide_diff(baseline, projected)
    expected = {
        "modify": {
            modification["slide"] for modification in change_set.get("modify", [])
        },
        "insert": {insertion["slide"] for insertion in change_set.get("insert", [])},
        "remove": set(change_set.get("remove", [])),
    }
    for action in ("modify", "insert", "remove"):
        if actual[action] != expected[action]:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "proposal-scope-mismatch",
                    "$.change_sets",
                    f"Projected {action} set {sorted(actual[action])} does not "
                    f"match declared set {sorted(expected[action])}.",
                )
            )
    if release_fingerprint(projected) == baseline.get("release_fingerprint"):
        diagnostics.append(
            Diagnostic(
                "error",
                "proposal-no-op",
                "$.change_sets",
                "Projected candidate is identical to the baseline release.",
            )
        )
    required_reviews = semantic_review_required(
        baseline,
        projected,
        change_set,
    )
    missing_reviews = required_reviews - set(change_set.get("review", []))
    if missing_reviews:
        diagnostics.append(
            Diagnostic(
                "error",
                "semantic-review-required",
                "$.change_sets",
                "Semantic changes require explicit locked-slide review "
                "acknowledgements: " + ", ".join(sorted(missing_reviews)),
            )
        )
    return diagnostics, projected


def impact_report(
    spec: dict[str, Any],
    change_id: str,
    baseline: dict[str, Any],
) -> dict[str, Any]:
    change_set = find_change_set(spec, change_id)
    items = spec["slides"]["items"]
    slide_order = spec["slides"]["order"]
    inserted = [item["slide"] for item in change_set.get("insert", [])]
    changed = {item["slide"] for item in change_set.get("modify", [])}
    changed.update(change_set.get("remove", []))
    changed.update(inserted)
    projected = projected_spec(spec, change_set, baseline)
    semantic = semantic_impact(baseline, projected)

    reverse_dependencies: dict[str, set[str]] = defaultdict(set)
    for slide_id, slide in items.items():
        for dependency in slide.get("dependencies", []):
            if dependency.get("propagates", True):
                reverse_dependencies[dependency["target"]].add(slide_id)

    visited = set(changed)
    queue = deque(ordered(changed, slide_order))
    while queue:
        target = queue.popleft()
        for dependent in ordered(reverse_dependencies.get(target, ()), slide_order):
            if dependent not in visited:
                visited.add(dependent)
                queue.append(dependent)

    dependent_reviews = (visited - changed) | (semantic["affected_slides"] - changed)
    preserve = set(change_set.get("preserve", []))
    authorization_required = {
        slide_id
        for slide_id in changed
        if items.get(slide_id, {}).get("locked")
        and change_set.get("status") == "proposed"
    }
    projected_release_fingerprint = release_fingerprint(projected)
    return {
        "change_set": change_id,
        "status": change_set.get("status"),
        "changed": ordered(changed, slide_order),
        "dependent_reviews": ordered(dependent_reviews, slide_order),
        "preserved_reviews": ordered(dependent_reviews & preserve, slide_order),
        "locked_dependent_reviews": ordered(
            {
                slide_id
                for slide_id in dependent_reviews
                if (
                    items.get(slide_id)
                    or projected["slides"]["items"].get(slide_id, {})
                ).get("locked")
            },
            slide_order,
        ),
        "review_required": ordered(
            semantic_review_required(baseline, projected, change_set),
            slide_order,
        ),
        "authorization_required": ordered(authorization_required, slide_order),
        "order_changed": change_set["target_order"]
        != [slide["id"] for slide in baseline["slides"]],
        "semantic_changes": sorted(semantic["sections"]),
        "semantic_entities": {
            "sources": sorted(semantic["sources"]),
            "claims": sorted(semantic["claims"]),
            "affected_claims": sorted(semantic["affected_claims"]),
            "affected_slides": ordered(
                semantic["affected_slides"],
                slide_order,
            ),
            "global_sections": sorted(semantic["global_sections"]),
        },
        "approval_metadata_bound": change_set.get("approval") is not None,
        "projected_release_fingerprint": projected_release_fingerprint,
        "projected_manifest_fingerprint": projected_manifest_fingerprint(
            baseline,
            change_set,
            projected_release_fingerprint,
        ),
    }


def applied_change_record(change_set: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": change_set["id"],
        "status": "applied",
        "rationale": change_set["rationale"],
        "baseline_fingerprint": change_set["baseline_fingerprint"],
        "target_fingerprint": change_set["target_fingerprint"],
        "target_order": copy.deepcopy(change_set["target_order"]),
        "modify": [
            {
                "slide": item["slide"],
                "blueprint_fingerprint": fingerprint(item["blueprint"]),
            }
            for item in change_set.get("modify", [])
        ],
        "insert": [
            {
                "slide": item["slide"],
                "blueprint_fingerprint": fingerprint(item["blueprint"]),
            }
            for item in change_set.get("insert", [])
        ],
        "remove": copy.deepcopy(change_set.get("remove", [])),
        "preserve": copy.deepcopy(change_set.get("preserve", [])),
        "review": copy.deepcopy(change_set.get("review", [])),
        "reorder": change_set.get("reorder", False),
    }
    if change_set.get("target_semantics") is not None:
        record["target_semantics_fingerprint"] = fingerprint(
            change_set["target_semantics"]
        )
    if change_set.get("approval") is not None:
        record["approval"] = copy.deepcopy(change_set["approval"])
    return record


def projected_history(
    baseline: dict[str, Any],
    change_set: dict[str, Any],
    target_release_fingerprint: str,
) -> dict[str, Any]:
    projected_change = copy.deepcopy(change_set)
    projected_change["target_fingerprint"] = target_release_fingerprint
    return {
        "retired_slide_ids": sorted(
            set(baseline.get("retired_slide_ids", []))
            | set(change_set.get("remove", []))
        ),
        "applied_changes": copy.deepcopy(baseline.get("applied_changes", []))
        + [applied_change_record(projected_change)],
    }


def projected_manifest_fingerprint(
    baseline: dict[str, Any],
    change_set: dict[str, Any],
    target_release_fingerprint: str,
) -> str:
    history_fingerprint_value = fingerprint(
        projected_history(
            baseline,
            change_set,
            target_release_fingerprint,
        )
    )
    return manifest_root_fingerprint(
        baseline["schema_version"],
        target_release_fingerprint,
        history_fingerprint_value,
    )


def build_manifest(
    spec: dict[str, Any],
    *,
    baseline: dict[str, Any] | None = None,
    change_id: str | None = None,
) -> dict[str, Any]:
    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    retired_slide_ids = set((baseline or {}).get("retired_slide_ids", []))
    applied_changes = copy.deepcopy((baseline or {}).get("applied_changes", []))
    if change_id is not None:
        change_set = find_change_set(spec, change_id)
        retired_slide_ids.update(change_set.get("remove", []))
        applied_changes.append(applied_change_record(change_set))
    history = {
        "retired_slide_ids": sorted(retired_slide_ids),
        "applied_changes": applied_changes,
    }
    release_fingerprint_value = release_fingerprint(spec)
    history_fingerprint_value = fingerprint(history)
    return {
        "schema_version": spec["schema_version"],
        "deck": copy.deepcopy(spec["deck"]),
        "profiles": copy.deepcopy(spec["profiles"]),
        "narrative": copy.deepcopy(spec["narrative"]),
        "sources": copy.deepcopy(spec.get("sources", {})),
        "claims": copy.deepcopy(spec.get("claims", {})),
        "qa": copy.deepcopy(spec.get("qa", {})),
        "spec_fingerprint": fingerprint(spec),
        "release_fingerprint": release_fingerprint_value,
        "history_fingerprint": history_fingerprint_value,
        "manifest_fingerprint": manifest_root_fingerprint(
            spec["schema_version"],
            release_fingerprint_value,
            history_fingerprint_value,
        ),
        "slides": [
            {
                "page_number": page_number,
                "id": slide_id,
                "fingerprint": fingerprint(items[slide_id]),
                "blueprint": copy.deepcopy(items[slide_id]),
            }
            for page_number, slide_id in enumerate(order, start=1)
        ],
        **history,
    }


STABLE_ID_PATTERN = r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
SHA256_PATTERN = r"^[a-f0-9]{64}$"
APPLIED_CHANGE_RECORD_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "id",
        "status",
        "rationale",
        "baseline_fingerprint",
        "target_fingerprint",
        "target_order",
        "modify",
        "insert",
        "remove",
        "preserve",
        "review",
        "reorder",
    ],
    "properties": {
        "id": {"$ref": "#/$defs/stableId"},
        "status": {"const": "applied"},
        "rationale": {"type": "string", "minLength": 1},
        "baseline_fingerprint": {"$ref": "#/$defs/fingerprint"},
        "target_fingerprint": {"$ref": "#/$defs/fingerprint"},
        "target_order": {
            "$ref": "#/$defs/stableIdArray",
            "minItems": 1,
        },
        "modify": {"$ref": "#/$defs/blueprintActions"},
        "insert": {"$ref": "#/$defs/blueprintActions"},
        "remove": {"$ref": "#/$defs/stableIdArray"},
        "preserve": {"$ref": "#/$defs/stableIdArray"},
        "review": {"$ref": "#/$defs/stableIdArray"},
        "reorder": {"type": "boolean"},
        "target_semantics_fingerprint": {"$ref": "#/$defs/fingerprint"},
        "approval": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "revision": {"type": "integer", "minimum": 1},
                "approved_by": {"type": "string", "minLength": 1},
                "approved_at": {"type": "string", "format": "date-time"},
            },
        },
    },
    "$defs": {
        "stableId": {"type": "string", "pattern": STABLE_ID_PATTERN},
        "fingerprint": {"type": "string", "pattern": SHA256_PATTERN},
        "stableIdArray": {
            "type": "array",
            "uniqueItems": True,
            "items": {"$ref": "#/$defs/stableId"},
        },
        "blueprintActions": {
            "type": "array",
            "uniqueItems": True,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["slide", "blueprint_fingerprint"],
                "properties": {
                    "slide": {"$ref": "#/$defs/stableId"},
                    "blueprint_fingerprint": {"$ref": "#/$defs/fingerprint"},
                },
            },
        },
    },
}


def applied_change_history_diagnostics(
    applied_changes: list[dict[str, Any]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    validator = Draft202012Validator(
        APPLIED_CHANGE_RECORD_SCHEMA,
        format_checker=FormatChecker(),
    )
    seen_ids: set[str] = set()

    for index, record in enumerate(applied_changes):
        base_path = f"$.applied_changes[{index}]"
        record_errors = sorted(
            validator.iter_errors(record),
            key=lambda item: (format_path(item.absolute_path), item.message),
        )
        for error in record_errors:
            relative_path = format_path(error.absolute_path)[1:]
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"{base_path}{relative_path}",
                    f"Invalid applied change record: {error.message}",
                )
            )

        change_id = record.get("id")
        if isinstance(change_id, str) and re.fullmatch(
            STABLE_ID_PATTERN,
            change_id,
        ):
            if change_id in seen_ids:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "invalid-baseline",
                        f"{base_path}.id",
                        f"Duplicate applied change ID {change_id!r}.",
                    )
                )
            seen_ids.add(change_id)
        if record_errors:
            continue

        action_slides = {
            action: (
                {item["slide"] for item in record[action]}
                if action in {"modify", "insert"}
                else set(record[action])
            )
            for action in ("modify", "insert", "remove", "preserve", "review")
        }
        for action in ("modify", "insert"):
            slide_ids = [item["slide"] for item in record[action]]
            if len(slide_ids) != len(set(slide_ids)):
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "invalid-baseline",
                        f"{base_path}.{action}",
                        f"Applied {action} slide IDs must be unique.",
                    )
                )
        for left, right in (
            ("modify", "insert"),
            ("modify", "remove"),
            ("modify", "preserve"),
            ("insert", "remove"),
            ("insert", "preserve"),
            ("remove", "preserve"),
        ):
            overlap = action_slides[left] & action_slides[right]
            if overlap:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        "invalid-baseline",
                        base_path,
                        f"Applied change has conflicting {left}/{right} slides: "
                        + ", ".join(sorted(overlap)),
                    )
                )

        target_order = set(record["target_order"])
        present_in_target = (
            action_slides["modify"]
            | action_slides["insert"]
            | action_slides["preserve"]
            | action_slides["review"]
        )
        if (
            not present_in_target <= target_order
            or action_slides["remove"] & target_order
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"{base_path}.target_order",
                    "Applied target order must contain retained action slides "
                    "and exclude removed slides.",
                )
            )

        material_actions = (
            action_slides["modify"] | action_slides["insert"] | action_slides["remove"]
        )
        if (
            not material_actions
            and not record["reorder"]
            and "target_semantics_fingerprint" not in record
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    base_path,
                    "Applied change must contain at least one material action.",
                )
            )

    return diagnostics


def baseline_manifest_diagnostics(baseline: dict[str, Any]) -> list[Diagnostic]:
    diagnostics = serialization_diagnostics(baseline)
    if diagnostics:
        return diagnostics
    for field in (
        "spec_fingerprint",
        "release_fingerprint",
        "history_fingerprint",
        "manifest_fingerprint",
    ):
        value = baseline.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.{field}",
                    f"Baseline manifest requires a SHA-256 {field}.",
                )
            )
    slides = baseline.get("slides")
    if not isinstance(slides, list):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.slides",
                "Baseline manifest requires an ordered slides array.",
            )
        )
        return diagnostics
    seen: set[str] = set()
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}]",
                    "Baseline slide must be an object.",
                )
            )
            continue
        slide_id = slide.get("id")
        slide_fingerprint = slide.get("fingerprint")
        blueprint = slide.get("blueprint")
        if slide.get("page_number") != index + 1:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}].page_number",
                    "Baseline page numbers must be sequential and one-based.",
                )
            )
        if not isinstance(slide_id, str) or not slide_id:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}].id",
                    "Baseline slide requires an ID.",
                )
            )
        elif slide_id in seen:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}].id",
                    f"Duplicate baseline slide ID {slide_id!r}.",
                )
            )
        else:
            seen.add(slide_id)
        if not isinstance(slide_fingerprint, str) or not re.fullmatch(
            r"[a-f0-9]{64}", slide_fingerprint
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}].fingerprint",
                    "Baseline slide requires a SHA-256 fingerprint.",
                )
            )
        elif not isinstance(blueprint, dict) or slide_fingerprint != fingerprint(
            blueprint
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    f"$.slides[{index}].blueprint",
                    "Baseline slide fingerprint does not match its blueprint.",
                )
            )

    retired_slide_ids = baseline.get("retired_slide_ids")
    applied_changes = baseline.get("applied_changes")
    if (
        not isinstance(retired_slide_ids, list)
        or any(not isinstance(item, str) for item in retired_slide_ids)
        or len(retired_slide_ids) != len(set(retired_slide_ids))
    ):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.retired_slide_ids",
                "Baseline retired_slide_ids must be a unique string array.",
            )
        )
    elif set(retired_slide_ids) & seen:
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.retired_slide_ids",
                "Retired slide IDs cannot also be active.",
            )
        )
    if not isinstance(applied_changes, list) or any(
        not isinstance(item, dict) for item in (applied_changes or [])
    ):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.applied_changes",
                "Baseline applied_changes must be an object array.",
            )
        )
    else:
        diagnostics.extend(applied_change_history_diagnostics(applied_changes))
    if isinstance(applied_changes, list) and isinstance(retired_slide_ids, list):
        history = {
            "retired_slide_ids": retired_slide_ids,
            "applied_changes": applied_changes,
        }
        if fingerprint(history) != baseline.get("history_fingerprint"):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    "$.history_fingerprint",
                    "Baseline history fingerprint does not match its history.",
                )
            )

    required_payload_fields = (
        "schema_version",
        "deck",
        "profiles",
        "narrative",
        "sources",
        "claims",
        "qa",
    )
    if not all(field in baseline for field in required_payload_fields):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$",
                "Baseline manifest is missing semantic release payload fields.",
            )
        )
    elif baseline.get("schema_version") != 1 or any(
        not isinstance(baseline.get(field), dict)
        for field in (
            "deck",
            "profiles",
            "narrative",
            "sources",
            "claims",
            "qa",
        )
    ):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$",
                "Baseline semantic release fields have invalid types.",
            )
        )
    elif not has_errors(diagnostics):
        payload = {field: baseline[field] for field in required_payload_fields}
        payload["deck"] = release_deck(payload["deck"])
        payload["slides"] = {
            "order": [slide["id"] for slide in slides],
            "items": {slide["id"]: slide["blueprint"] for slide in slides},
        }
        if fingerprint(payload) != baseline.get("release_fingerprint"):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "invalid-baseline",
                    "$.release_fingerprint",
                    "Baseline release fingerprint does not match its semantic payload.",
                )
            )
    if (
        not has_errors(diagnostics)
        and manifest_root_fingerprint(
            baseline["schema_version"],
            baseline["release_fingerprint"],
            baseline["history_fingerprint"],
        )
        != baseline["manifest_fingerprint"]
    ):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.manifest_fingerprint",
                "Baseline manifest fingerprint does not bind release and history.",
            )
        )
    return diagnostics


def revision_diagnostics(
    spec: dict[str, Any],
    baseline: dict[str, Any] | None,
    change_id: str | None,
    *,
    initial_release: bool = False,
) -> list[Diagnostic]:
    operation = spec.get("deck", {}).get("operation")
    if operation == "create":
        if not initial_release:
            return [
                Diagnostic(
                    "error",
                    "initial-release-flag-required",
                    "$.deck.operation",
                    "Create manifests require the explicit --initial-release flag.",
                )
            ]
        if baseline is not None or change_id is not None:
            return [
                Diagnostic(
                    "error",
                    "unexpected-baseline",
                    "$.deck.operation",
                    "Create operations do not accept a baseline or change set.",
                )
            ]
        if spec.get("change_sets"):
            return [
                Diagnostic(
                    "error",
                    "initial-release-change-set",
                    "$.change_sets",
                    "Initial releases cannot carry revision change sets.",
                )
            ]
        return []
    if initial_release:
        return [
            Diagnostic(
                "error",
                "unexpected-initial-release",
                "$.deck.operation",
                "Only create operations may use --initial-release.",
            )
        ]

    diagnostics: list[Diagnostic] = []
    if baseline is None:
        diagnostics.append(
            Diagnostic(
                "error",
                "baseline-required",
                "$.deck.operation",
                f"Operation {operation!r} requires --baseline.",
            )
        )
    if not change_id:
        diagnostics.append(
            Diagnostic(
                "error",
                "change-set-required",
                "$.deck.operation",
                f"Operation {operation!r} requires --change-set.",
            )
        )
    if diagnostics:
        return diagnostics

    assert baseline is not None
    diagnostics.extend(baseline_manifest_diagnostics(baseline))
    if has_errors(diagnostics):
        return diagnostics
    try:
        change_set = find_change_set(spec, change_id)
    except KeyError:
        diagnostics.append(
            Diagnostic(
                "error",
                "unknown-change-set",
                "$.change_sets",
                f"No change set named {change_id!r}.",
            )
        )
        return diagnostics
    if change_set.get("status") != "approved":
        diagnostics.append(
            Diagnostic(
                "error",
                "change-set-not-approved",
                "$.change_sets",
                "Revision manifest requires the selected change set to be approved.",
            )
        )
        return diagnostics
    if change_id in {item.get("id") for item in baseline.get("applied_changes", [])}:
        diagnostics.append(
            Diagnostic(
                "error",
                "reused-change-id",
                "$.change_sets",
                f"Change-set ID {change_id!r} already exists in manifest history.",
            )
        )
    if change_set.get("baseline_fingerprint") != baseline.get("manifest_fingerprint"):
        diagnostics.append(
            Diagnostic(
                "error",
                "baseline-fingerprint-mismatch",
                "$.change_sets",
                "Selected change set was not approved against this baseline manifest.",
            )
        )
    baseline_deck = baseline.get("deck")
    if not isinstance(baseline_deck, dict):
        diagnostics.append(
            Diagnostic(
                "error",
                "invalid-baseline",
                "$.deck",
                "Baseline manifest requires deck metadata.",
            )
        )
    elif baseline_deck.get("id") != spec.get("deck", {}).get("id"):
        diagnostics.append(
            Diagnostic(
                "error",
                "baseline-deck-mismatch",
                "$.deck.id",
                "Baseline manifest belongs to a different deck.",
            )
        )
    retired = set(baseline.get("retired_slide_ids", []))
    reused = {
        insertion["slide"]
        for insertion in change_set.get("insert", [])
        if insertion["slide"] in retired
    }
    if reused:
        diagnostics.append(
            Diagnostic(
                "error",
                "retired-slide-id",
                "$.change_sets",
                "Retired slide IDs cannot be reused: " + ", ".join(sorted(reused)),
            )
        )
    if has_errors(diagnostics):
        return diagnostics

    projected = projected_spec(spec, change_set, baseline)
    projected_fingerprint = release_fingerprint(projected)
    target_fingerprint = change_set.get("target_fingerprint")
    if not target_fingerprint:
        diagnostics.append(
            Diagnostic(
                "error",
                "target-fingerprint-required",
                "$.change_sets",
                "Approved change set requires the projected release fingerprint "
                "reported by impact analysis.",
            )
        )
    elif target_fingerprint != projected_fingerprint:
        diagnostics.append(
            Diagnostic(
                "error",
                "target-fingerprint-mismatch",
                "$.change_sets",
                "Approved target fingerprint does not match the declared "
                "candidate projection.",
            )
        )
    projected_manifest = projected_manifest_fingerprint(
        baseline,
        change_set,
        projected_fingerprint,
    )
    target_manifest = change_set.get("target_manifest_fingerprint")
    if not target_manifest:
        diagnostics.append(
            Diagnostic(
                "error",
                "target-manifest-fingerprint-required",
                "$.change_sets",
                "Approved change set requires the projected manifest fingerprint "
                "reported by impact analysis.",
            )
        )
    elif target_manifest != projected_manifest:
        without_approval = copy.deepcopy(change_set)
        without_approval.pop("approval", None)
        unbound_approval_projection = projected_manifest_fingerprint(
            baseline,
            without_approval,
            projected_fingerprint,
        )
        if (
            change_set.get("approval") is not None
            and target_manifest == unbound_approval_projection
        ):
            diagnostics.append(
                Diagnostic(
                    "error",
                    "approval-metadata-not-finalized",
                    "$.change_sets",
                    "Approval metadata was added after the projected manifest "
                    "fingerprint was recorded. Keep the change set proposed, "
                    "freeze the complete history-bound record, rerun impact, "
                    "and record the final fingerprints before approval.",
                )
            )
        else:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "target-manifest-fingerprint-mismatch",
                    "$.change_sets",
                    "Approved target manifest fingerprint does not match the "
                    "projected release and history.",
                )
            )
    if release_fingerprint(spec) != projected_fingerprint:
        diagnostics.append(
            Diagnostic(
                "error",
                "revision-target-mismatch",
                "$",
                "Active semantic release payload does not exactly match the "
                "approved candidate projection.",
            )
        )

    actual = slide_diff(baseline, spec)
    expected = {
        "modify": {
            modification["slide"] for modification in change_set.get("modify", [])
        },
        "insert": {insertion["slide"] for insertion in change_set.get("insert", [])},
        "remove": set(change_set.get("remove", [])),
    }
    for action in ("modify", "insert", "remove"):
        if actual[action] != expected[action]:
            diagnostics.append(
                Diagnostic(
                    "error",
                    "revision-scope-mismatch",
                    "$.change_sets",
                    f"Actual {action} set {sorted(actual[action])} does not match "
                    f"authorized set {sorted(expected[action])}.",
                )
            )
    required_reviews = semantic_review_required(
        baseline,
        projected,
        change_set,
    )
    missing_reviews = required_reviews - set(change_set.get("review", []))
    if missing_reviews:
        diagnostics.append(
            Diagnostic(
                "error",
                "semantic-review-required",
                "$.change_sets",
                "Approved semantic change is missing locked-slide review "
                "acknowledgements: " + ", ".join(sorted(missing_reviews)),
            )
        )
    return diagnostics


def print_diagnostics(diagnostics: list[Diagnostic]) -> None:
    for item in diagnostics:
        print(
            f"{item.level.upper()} [{item.code}] {item.path}: {item.message}",
            file=sys.stderr if item.level == "error" else sys.stdout,
        )


def has_errors(diagnostics: list[Diagnostic]) -> bool:
    return any(item.level == "error" for item in diagnostics)


def write_json(value: Any, output: Path | None) -> None:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if output is None:
        sys.stdout.write(text)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("spec", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "lint"):
        subparser = subparsers.add_parser(command)
        add_common_arguments(subparser)

    impact_parser = subparsers.add_parser("impact")
    add_common_arguments(impact_parser)
    impact_parser.add_argument("--change-set", required=True)
    impact_parser.add_argument("--baseline", type=Path, required=True)

    manifest_parser = subparsers.add_parser("manifest")
    add_common_arguments(manifest_parser)
    manifest_parser.add_argument("--output", type=Path)
    manifest_parser.add_argument("--baseline", type=Path)
    manifest_parser.add_argument("--change-set")
    manifest_parser.add_argument("--initial-release", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        spec = load_yaml(args.spec)
        schema = load_json(args.schema)
        profiles = load_yaml(args.profiles)
    except (OSError, TypeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"ERROR [input] $: {exc}", file=sys.stderr)
        return 2

    if args.command == "validate":
        diagnostics = validate_spec(spec, schema)
        print_diagnostics(diagnostics)
        if has_errors(diagnostics):
            return 1
        print("OK: deck specification is structurally valid.")
        return 0

    if args.command == "lint":
        diagnostics = lint_spec(spec, schema, profiles)
        print_diagnostics(diagnostics)
        if has_errors(diagnostics):
            return 1
        print("OK: deck specification passed narrative, claim, and approval lint.")
        return 0

    diagnostics = validate_spec(spec, schema)
    if has_errors(diagnostics):
        print_diagnostics(diagnostics)
        return 1

    baseline = None
    if args.baseline is not None:
        try:
            baseline = load_json(args.baseline)
        except (OSError, TypeError, json.JSONDecodeError) as exc:
            print(f"ERROR [input] $.baseline: {exc}", file=sys.stderr)
            return 2

    if args.command == "impact":
        assert baseline is not None
        diagnostics, _ = impact_diagnostics(
            spec,
            baseline,
            args.change_set,
            schema,
            profiles,
        )
        print_diagnostics(diagnostics)
        if has_errors(diagnostics):
            return 1
        write_json(impact_report(spec, args.change_set, baseline), None)
        return 0

    diagnostics = lint_spec(spec, schema, profiles)
    diagnostics.extend(release_diagnostics(spec))
    diagnostics.extend(
        revision_diagnostics(
            spec,
            baseline,
            args.change_set,
            initial_release=args.initial_release,
        )
    )
    if has_errors(diagnostics):
        print_diagnostics(diagnostics)
        return 1
    write_json(
        build_manifest(spec, baseline=baseline, change_id=args.change_set),
        args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
