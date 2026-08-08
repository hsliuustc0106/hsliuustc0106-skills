#!/usr/bin/env python3
"""Lint semantic deck specifications and report dependency impact."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "deckc requires PyYAML and jsonschema. Run with "
        "`uv run --with pyyaml --with jsonschema python scripts/deckc.py ...`."
    ) from exc


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_DIR / "references" / "deck-spec.schema.json"
DEFAULT_PROFILES = SKILL_DIR / "references" / "narrative-profiles.yaml"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    path: str
    message: str


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if type(value) is not dict:
        raise TypeError(f"{path} must contain a mapping at the root.")
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if type(value) is not dict:
        raise TypeError(f"{path} must contain an object at the root.")
    return value


def json_value_error(
    value: Any,
    path: str = "$",
    active: set[int] | None = None,
) -> str | None:
    """Return the first reason a value cannot be emitted as canonical UTF-8 JSON."""
    containers = active if active is not None else set()
    if type(value) is dict:
        identity = id(value)
        if identity in containers:
            return f"{path} contains a circular object reference"
        containers.add(identity)
        try:
            for key, item in value.items():
                if type(key) is not str:
                    return f"{path} contains non-string key {key!r}"
                try:
                    key.encode("utf-8")
                except UnicodeEncodeError:
                    return f"{path} contains a key that is not valid UTF-8"
                error = json_value_error(item, f"{path}.{key}", containers)
                if error:
                    return error
        finally:
            containers.remove(identity)
        return None
    if type(value) is list:
        identity = id(value)
        if identity in containers:
            return f"{path} contains a circular array reference"
        containers.add(identity)
        try:
            for index, item in enumerate(value):
                error = json_value_error(item, f"{path}[{index}]", containers)
                if error:
                    return error
        finally:
            containers.remove(identity)
        return None
    if type(value) is str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            return f"{path} contains a string that is not valid UTF-8"
        return None
    if type(value) is float and not math.isfinite(value):
        return f"{path} contains a non-finite number"
    if value is None or type(value) in {bool, int, float}:
        return None
    return f"{path} contains unsupported type {type(value).__name__}"


def format_path(parts: Any) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def structural_diagnostics(
    spec: dict[str, Any],
    schema: dict[str, Any],
) -> list[Diagnostic]:
    serialization_error = json_value_error(spec)
    if serialization_error:
        return [Diagnostic("non-json-value", "$", serialization_error)]

    validator = Draft202012Validator(schema)
    diagnostics = [
        Diagnostic("schema", format_path(error.absolute_path), error.message)
        for error in sorted(
            validator.iter_errors(spec),
            key=lambda item: (format_path(item.absolute_path), item.message),
        )
    ]
    if diagnostics:
        return diagnostics

    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    if set(order) != set(items):
        missing = sorted(set(order) - set(items))
        unordered = sorted(set(items) - set(order))
        details = []
        if missing:
            details.append("missing blueprints: " + ", ".join(missing))
        if unordered:
            details.append("unordered blueprints: " + ", ".join(unordered))
        diagnostics.append(
            Diagnostic("slide-order-mismatch", "$.slides", "; ".join(details))
        )

    unknown_dependencies: list[tuple[str, int, str]] = []
    for slide_id, slide in items.items():
        for index, dependency in enumerate(slide.get("dependencies", [])):
            target = dependency["target"]
            if target not in items:
                unknown_dependencies.append((slide_id, index, target))
    for slide_id, index, target in unknown_dependencies:
        diagnostics.append(
            Diagnostic(
                "unknown-dependency",
                f"$.slides.items.{slide_id}.dependencies[{index}]",
                f"Dependency target {target!r} does not exist.",
            )
        )
    if unknown_dependencies:
        return diagnostics

    indegree = {slide_id: 0 for slide_id in items}
    reverse: dict[str, list[str]] = defaultdict(list)
    for slide_id, slide in items.items():
        for dependency in slide.get("dependencies", []):
            if dependency.get("propagates", True):
                target = dependency["target"]
                reverse[target].append(slide_id)
                indegree[slide_id] += 1
    queue = deque(slide_id for slide_id in order if indegree[slide_id] == 0)
    visited = 0
    while queue:
        target = queue.popleft()
        visited += 1
        for dependent in reverse[target]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)
    if visited != len(items):
        diagnostics.append(
            Diagnostic(
                "dependency-cycle",
                "$.slides.items",
                "Propagating slide dependencies must be acyclic.",
            )
        )
    return diagnostics


def required_role_groups(
    spec: dict[str, Any],
    profiles: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[Diagnostic]]:
    narrative = spec["narrative"]
    explicit = narrative.get("required_roles")
    if explicit:
        return [{"id": role, "any_of": [role]} for role in explicit], []
    profile_name = narrative["profile"]
    profile = profiles.get("profiles", {}).get(profile_name)
    if profile is None:
        return [], [
            Diagnostic(
                "unknown-narrative-profile",
                "$.narrative.profile",
                f"Unknown narrative profile {profile_name!r}; provide required_roles for a custom profile.",
            )
        ]
    return profile.get("required_role_groups", []), []


def narrative_diagnostics(
    spec: dict[str, Any],
    profiles: dict[str, Any],
) -> list[Diagnostic]:
    groups, diagnostics = required_role_groups(spec, profiles)
    if diagnostics:
        return diagnostics
    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    first_positions: list[int] = []
    for group in groups:
        accepted = set(group["any_of"])
        positions = [
            index
            for index, slide_id in enumerate(order)
            if accepted & set(items[slide_id]["narrative_roles"])
        ]
        if not positions:
            diagnostics.append(
                Diagnostic(
                    "missing-narrative-role",
                    "$.slides.items",
                    f"Missing narrative role group {group['id']!r}.",
                )
            )
        else:
            first_positions.append(positions[0])
    if not diagnostics and first_positions != sorted(first_positions):
        diagnostics.append(
            Diagnostic(
                "narrative-order",
                "$.slides.order",
                "Required narrative roles do not appear in profile order.",
            )
        )
    return diagnostics


def lint_spec(
    spec: dict[str, Any],
    schema: dict[str, Any],
    profiles: dict[str, Any],
) -> list[Diagnostic]:
    diagnostics = structural_diagnostics(spec, schema)
    if diagnostics:
        return diagnostics
    diagnostics.extend(narrative_diagnostics(spec, profiles))
    return diagnostics


def ordered(ids: set[str], order: list[str]) -> list[str]:
    rank = {slide_id: index for index, slide_id in enumerate(order)}
    return sorted(ids, key=lambda slide_id: (rank.get(slide_id, len(rank)), slide_id))


def impact_report(spec: dict[str, Any], changed: list[str]) -> dict[str, Any]:
    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    changed_set = set(changed)
    unknown = changed_set - set(items)
    if unknown:
        raise ValueError("Unknown changed slide IDs: " + ", ".join(sorted(unknown)))

    reverse: dict[str, set[str]] = defaultdict(set)
    for slide_id, slide in items.items():
        for dependency in slide.get("dependencies", []):
            if dependency.get("propagates", True):
                reverse[dependency["target"]].add(slide_id)
    affected = set(changed_set)
    queue = deque(ordered(changed_set, order))
    while queue:
        target = queue.popleft()
        for dependent in ordered(reverse[target], order):
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)
    return {
        "changed": ordered(changed_set, order),
        "affected": ordered(affected, order),
        "dependent": ordered(affected - changed_set, order),
    }


def compile_deck(spec: dict[str, Any]) -> dict[str, Any]:
    order = spec["slides"]["order"]
    items = spec["slides"]["items"]
    compiled = {
        "schema_version": spec["schema_version"],
        "deck": spec["deck"],
        "narrative": spec["narrative"],
        "slides": [
            {
                "page_number": page_number,
                "id": slide_id,
                "blueprint": items[slide_id],
            }
            for page_number, slide_id in enumerate(order, start=1)
        ],
    }
    if "extensions" in spec:
        compiled["extensions"] = spec["extensions"]
    return compiled


def print_diagnostics(diagnostics: list[Diagnostic]) -> None:
    for item in diagnostics:
        print(
            f"ERROR [{item.code}] {item.path}: {item.message}",
            file=sys.stderr,
        )


def write_json(value: Any, output: Path | None) -> None:
    text = (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    )
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
    lint_parser = subparsers.add_parser("lint")
    add_common_arguments(lint_parser)
    impact_parser = subparsers.add_parser("impact")
    add_common_arguments(impact_parser)
    impact_parser.add_argument("--changed", action="append", required=True)
    compile_parser = subparsers.add_parser("compile")
    add_common_arguments(compile_parser)
    compile_parser.add_argument("--output", type=Path)
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

    diagnostics = lint_spec(spec, schema, profiles)
    if diagnostics:
        print_diagnostics(diagnostics)
        return 1
    if args.command == "lint":
        print("OK: deck specification passed structural and narrative lint.")
        return 0
    if args.command == "impact":
        try:
            report = impact_report(spec, args.changed)
        except ValueError as exc:
            print(f"ERROR [unknown-changed-slide] $: {exc}", file=sys.stderr)
            return 1
        write_json(report, None)
        return 0
    write_json(compile_deck(spec), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
