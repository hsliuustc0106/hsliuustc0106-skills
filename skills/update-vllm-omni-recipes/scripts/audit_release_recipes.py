#!/usr/bin/env python3
"""Generate a read-only stable-release audit for vLLM-Omni recipes."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


STABLE_TAG_RE = re.compile(
    r"^v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:\.post(?P<post>\d+))?$"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
INDEX_LINK_RE = re.compile(r"\]\(\./([^)#?]+\.md)(?:#[^)]*)?\)")
CODE_REPO_PATH_RE = re.compile(
    r"(?P<path>(?:(?:\.\./)+|\./)?(?:examples|docs|tests|vllm_omni|recipes)/"
    r"[A-Za-z0-9_./-]+\.(?:py|sh|md|ya?ml))"
)
PRERELEASE_RE = re.compile(
    r"(?i)\b\d+\.\d+(?:\.\d+)?(?:rc\d+|[.-]?dev\d*)"
)
COMMIT_RE = re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])")
NON_RELEASE_EVIDENCE_RE = re.compile(
    r"(?i)\b(?:current (?:checkout|main)|source checkout|"
    r"commit you are deploying from|match the repository requirements|"
    r"branch\s+[`'\"]?[^\s,;)`'\"]+|PR\s*#?\d+)"
)


class AuditError(RuntimeError):
    """Report an invalid invocation or repository state."""


@dataclasses.dataclass(frozen=True, order=True)
class StableTag:
    major: int
    minor: int
    patch: int
    post: int
    name: str = dataclasses.field(compare=False)


@dataclasses.dataclass(frozen=True)
class Finding:
    path: str
    line: int
    detail: str


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        command = "git " + " ".join(args)
        message = result.stderr.strip() or result.stdout.strip()
        raise AuditError(f"{command} failed: {message}")
    return result.stdout.rstrip("\n")


def parse_stable_tag(tag: str) -> StableTag | None:
    match = STABLE_TAG_RE.fullmatch(tag)
    if not match:
        return None
    return StableTag(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        post=int(match.group("post") or 0),
        name=tag,
    )


def resolve_tag_commit(repo: Path, tag: str) -> str:
    return run_git(repo, "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}")


def resolve_remote_tag_commit(repo: Path, remote: str, tag: str) -> str:
    tag_ref = f"refs/tags/{tag}"
    peeled_ref = f"{tag_ref}^{{}}"
    output = run_git(repo, "ls-remote", "--tags", remote, tag_ref, peeled_ref)
    refs = {}
    for line in output.splitlines():
        fields = line.split("\t", 1)
        if len(fields) == 2:
            refs[fields[1]] = fields[0]
    commit = refs.get(peeled_ref) or refs.get(tag_ref)
    if commit is None:
        raise AuditError(f"{remote} does not publish final tag {tag}")
    return commit


def commit_exists(repo: Path, commit: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{commit}^{{commit}}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def select_previous_tag(repo: Path, target: StableTag) -> StableTag:
    candidates = []
    for name in run_git(repo, "tag", "--list").splitlines():
        parsed = parse_stable_tag(name.strip())
        if parsed is not None and parsed < target:
            candidates.append(parsed)
    if not candidates:
        raise AuditError(
            f"no final stable tag precedes {target.name}; pass --previous explicitly"
        )
    return max(candidates)


def recipe_files(repo: Path) -> list[Path]:
    recipes_dir = repo / "recipes"
    if not recipes_dir.is_dir():
        raise AuditError(f"missing recipes directory: {recipes_dir}")
    return sorted(
        path
        for path in recipes_dir.rglob("*.md")
        if path.name not in {"README.md", "TEMPLATE.md"}
    )


def repo_relative(repo: Path, path: Path) -> str:
    return path.relative_to(repo).as_posix()


def parse_index(repo: Path) -> tuple[list[str], list[str]]:
    index_path = repo / "recipes" / "README.md"
    if not index_path.is_file():
        raise AuditError(f"missing recipe index: {index_path}")

    entries = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        match = INDEX_LINK_RE.search(line)
        if match:
            entries.append(match.group(1))

    counts = collections.Counter(entries)
    duplicates = sorted(path for path, count in counts.items() if count > 1)
    return sorted(counts), duplicates


def split_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(None, 1)[0]
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


def local_links(repo: Path, markdown_path: Path) -> list[tuple[int, str, Path]]:
    links = []
    text = markdown_path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for raw_target in MARKDOWN_LINK_RE.findall(line):
            target = split_link_target(raw_target)
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            if "://" in target:
                continue
            if target.startswith("/"):
                resolved = repo / target.lstrip("/")
            else:
                resolved = markdown_path.parent / target
            links.append((line_number, target, resolved.resolve(strict=False)))
    return links


def broken_local_links(repo: Path, markdown_paths: list[Path]) -> list[Finding]:
    findings = []
    for markdown_path in markdown_paths:
        for line_number, target, resolved in local_links(repo, markdown_path):
            try:
                resolved.relative_to(repo)
            except ValueError:
                findings.append(
                    Finding(
                        repo_relative(repo, markdown_path),
                        line_number,
                        f"local target escapes the repository: {target}",
                    )
                )
                continue
            if not resolved.exists():
                findings.append(
                    Finding(
                        repo_relative(repo, markdown_path),
                        line_number,
                        f"missing local target: {target}",
                    )
                )
    return findings


def broken_fenced_code_paths(repo: Path, markdown_paths: list[Path]) -> list[Finding]:
    findings = []
    for markdown_path in markdown_paths:
        in_fence = False
        fence_marker = ""
        for line_number, line in enumerate(
            markdown_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                elif marker == fence_marker:
                    in_fence = False
                    fence_marker = ""
                continue
            if not in_fence:
                continue
            for match in CODE_REPO_PATH_RE.finditer(line):
                target = match.group("path").rstrip("./")
                if target.startswith("../"):
                    resolved = markdown_path.parent / target
                else:
                    resolved = repo / target
                resolved = resolved.resolve(strict=False)
                try:
                    resolved.relative_to(repo)
                except ValueError:
                    continue
                if not resolved.exists():
                    findings.append(
                        Finding(
                            repo_relative(repo, markdown_path),
                            line_number,
                            f"missing repository path in fenced code: {target}",
                        )
                    )
    return findings


def version_review_findings(repo: Path, paths: list[Path]) -> list[Finding]:
    findings = []
    for path in paths:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            lower_line = line.lower()
            if "vllm" not in lower_line:
                continue
            has_version_context = (
                line.lstrip().lower().startswith(("- vllm", "* vllm"))
                or any(
                    marker in lower_line
                    for marker in (
                        "version",
                        "commit",
                        "checkout",
                        "branch",
                        "pr #",
                        "minimum",
                        "current main",
                        "current `main`",
                        "editable install",
                    )
                )
            )
            if not has_version_context:
                continue
            reasons = []
            if PRERELEASE_RE.search(line):
                reasons.append("pre-release/development version")
            if NON_RELEASE_EVIDENCE_RE.search(line):
                reasons.append("floating branch, PR, or checkout reference")
            if COMMIT_RE.search(line):
                reasons.append("exact commit reference (usually preserve)")
            if reasons:
                findings.append(
                    Finding(
                        repo_relative(repo, path),
                        line_number,
                        f"{', '.join(sorted(set(reasons)))} — {line.strip()}",
                    )
                )
    return findings


def changed_paths(repo: Path, previous: str, target: str) -> set[str]:
    output = run_git(repo, "diff", "--name-only", f"{previous}..{target}")
    return {line for line in output.splitlines() if line}


def changed_recipe_status(repo: Path, previous: str, target: str) -> list[str]:
    output = run_git(
        repo,
        "diff",
        "--name-status",
        "--find-renames",
        f"{previous}..{target}",
        "--",
        "recipes",
    )
    return [line for line in output.splitlines() if line]


def current_recipe_status(repo: Path, target: str) -> list[str]:
    output = run_git(
        repo,
        "diff",
        "--name-status",
        "--find-renames",
        target,
        "--",
        "recipes",
    )
    status = [line for line in output.splitlines() if line]
    untracked = run_git(
        repo, "ls-files", "--others", "--exclude-standard", "--", "recipes"
    )
    status.extend(f"??\t{line}" for line in untracked.splitlines() if line)
    return status


def paths_at_revision(repo: Path, revision: str, prefix: str) -> set[str]:
    output = run_git(
        repo, "ls-tree", "-r", "--name-only", revision, "--", prefix
    )
    return {line for line in output.splitlines() if line}


def linked_release_changes(
    repo: Path,
    markdown_paths: list[Path],
    release_changes: set[str],
    target_recipe_paths: set[str],
) -> dict[str, set[str]]:
    impacted: dict[str, set[str]] = collections.defaultdict(set)
    for markdown_path in markdown_paths:
        recipe = repo_relative(repo, markdown_path)
        if recipe not in target_recipe_paths:
            continue
        for _, _, resolved in local_links(repo, markdown_path):
            try:
                target = repo_relative(repo, resolved)
            except ValueError:
                continue
            if target in release_changes:
                impacted[recipe].add(target)
    return dict(sorted(impacted.items()))


def release_hotspots(release_changes: set[str]) -> dict[str, int]:
    prefixes = ("recipes/", "examples/", "docs/", "vllm_omni/", "tests/")
    counts = {prefix: 0 for prefix in prefixes}
    counts["other"] = 0
    for path in release_changes:
        matched = False
        for prefix in prefixes:
            if path.startswith(prefix):
                counts[prefix] += 1
                matched = True
                break
        if not matched:
            counts["other"] += 1
    return counts


def markdown_list(items: list[str], empty: str = "None.") -> list[str]:
    if not items:
        return [empty]
    return [f"- `{item}`" for item in items]


def render_report(
    *,
    repo: Path,
    target: str,
    target_commit: str,
    previous: str,
    previous_commit: str,
    remote_verification: str,
    recipes: list[Path],
    indexed: list[str],
    duplicate_index: list[str],
    missing_from_index: list[str],
    missing_on_disk: list[str],
    broken_links: list[Finding],
    version_findings: list[Finding],
    recipe_changes: list[str],
    current_recipe_changes: list[str],
    linked_changes: dict[str, set[str]],
    hotspots: dict[str, int],
) -> str:
    branch = run_git(repo, "branch", "--show-current") or "(detached HEAD)"
    head_commit = run_git(repo, "rev-parse", "HEAD")
    dirty = bool(run_git(repo, "status", "--porcelain"))
    lines = [
        "# vLLM-Omni stable-release recipe audit",
        "",
        f"- Repository: `{repo}`",
        f"- Working branch: `{branch}`",
        f"- Working HEAD: `{head_commit[:12]}`",
        f"- Working tree dirty: `{'yes' if dirty else 'no'}`",
        f"- Target: `{target}` (`{target_commit[:12]}`)",
        f"- Previous final tag: `{previous}` (`{previous_commit[:12]}`)",
        f"- Remote tag verification: {remote_verification}",
        "",
        "> This report is a triage aid. Version markers and static checks are not hardware validation.",
        "",
        "## Inventory",
        "",
        f"- Recipe Markdown files: `{len(recipes)}`",
        f"- Indexed recipe paths: `{len(indexed)}`",
        "",
        "### Recipe files not listed in recipes/README.md",
        "",
        *markdown_list(missing_from_index),
        "",
        "### Indexed paths missing on disk",
        "",
        *markdown_list(missing_on_disk),
        "",
        "### Duplicate index entries",
        "",
        *markdown_list(duplicate_index),
        "",
        "## Release delta",
        "",
        f"Changed-path counts for `{previous}..{target}`:",
        "",
    ]
    lines.extend(f"- `{prefix}`: `{count}`" for prefix, count in hotspots.items())
    lines.extend(["", "### Recipe changes in the release range", ""])
    lines.extend(markdown_list(recipe_changes))
    lines.extend(
        [
            "",
            "### Current checkout recipe delta from the target tag",
            "",
            "Treat these changes as post-target until release evidence proves otherwise.",
            "",
        ]
    )
    lines.extend(markdown_list(current_recipe_changes))
    lines.extend(["", "### Recipes whose local links changed in the release range", ""])
    if linked_changes:
        for recipe, changed in linked_changes.items():
            lines.append(f"- `{recipe}`")
            lines.extend(f"  - `{path}`" for path in sorted(changed))
    else:
        lines.append("None.")

    lines.extend(
        [
            "",
            "## Version evidence requiring human classification",
            "",
            "These are not automatic update candidates; exact historical evidence is usually preserved.",
            "",
        ]
    )
    if version_findings:
        for finding in version_findings:
            lines.append(
                f"- `{finding.path}:{finding.line}` — {finding.detail}"
            )
    else:
        lines.append("None.")

    lines.extend(["", "## Broken local links or fenced-command paths", ""])
    if broken_links:
        for finding in broken_links:
            lines.append(
                f"- `{finding.path}:{finding.line}` — {finding.detail}"
            )
    else:
        lines.append("None.")

    lines.extend(
        [
            "",
            "## Required interpretation",
            "",
            "- Preserve exact historical test versions unless replacement evidence exists.",
            "- Review changed commands and linked examples against the target tag.",
            "- Map unlinked runtime/API changes to recipes semantically; the script cannot infer them.",
            "- Label each edited recipe as hardware verified, CI verified, static only, or needs revalidation.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit vLLM-Omni recipes for a final stable release."
    )
    parser.add_argument(
        "--repo", type=Path, default=Path.cwd(), help="vLLM-Omni repository"
    )
    parser.add_argument(
        "--target", required=True, help="final stable tag, for example v0.26.0"
    )
    parser.add_argument(
        "--previous", help="preceding final tag; inferred by semantic version by default"
    )
    parser.add_argument(
        "--remote", default="origin", help="remote used to verify published tags"
    )
    verification = parser.add_mutually_exclusive_group()
    verification.add_argument(
        "--offline",
        action="store_true",
        help="skip remote tag verification for a deliberate local-only audit",
    )
    verification.add_argument(
        "--use-remote-tags",
        action="store_true",
        help="use mismatched remote tag commits when those objects exist locally",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 for inventory mismatches, duplicate index entries, or broken paths",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo.resolve()

    try:
        repo_root = Path(run_git(repo, "rev-parse", "--show-toplevel")).resolve()
        target_tag = parse_stable_tag(args.target)
        if target_tag is None:
            raise AuditError(
                f"target {args.target!r} is not a final tag like v0.26.0"
            )
        local_target_commit = resolve_tag_commit(repo_root, target_tag.name)

        if args.previous:
            previous_tag = parse_stable_tag(args.previous)
            if previous_tag is None:
                raise AuditError(
                    f"previous tag {args.previous!r} is not a final stable tag"
                )
        else:
            previous_tag = select_previous_tag(repo_root, target_tag)
        local_previous_commit = resolve_tag_commit(repo_root, previous_tag.name)

        if previous_tag >= target_tag:
            raise AuditError(
                f"previous tag {previous_tag.name} must precede {target_tag.name}"
            )

        target_commit = local_target_commit
        previous_commit = local_previous_commit
        target_revision = target_tag.name
        previous_revision = previous_tag.name
        if args.offline:
            remote_verification = "`skipped (--offline)`"
        else:
            remote_target_commit = resolve_remote_tag_commit(
                repo_root, args.remote, target_tag.name
            )
            remote_previous_commit = resolve_remote_tag_commit(
                repo_root, args.remote, previous_tag.name
            )
            mismatches = []
            if remote_target_commit != local_target_commit:
                mismatches.append(
                    f"{target_tag.name}: local {local_target_commit[:12]}, "
                    f"{args.remote} {remote_target_commit[:12]}"
                )
            if remote_previous_commit != local_previous_commit:
                mismatches.append(
                    f"{previous_tag.name}: local {local_previous_commit[:12]}, "
                    f"{args.remote} {remote_previous_commit[:12]}"
                )
            if mismatches and not args.use_remote_tags:
                raise AuditError(
                    "local and published tag commits differ ("
                    + "; ".join(mismatches)
                    + "). Stop and inspect the moved tag; rerun with "
                    "--use-remote-tags only after choosing the published remote refs."
                )
            if args.use_remote_tags:
                for tag, commit in (
                    (target_tag.name, remote_target_commit),
                    (previous_tag.name, remote_previous_commit),
                ):
                    if not commit_exists(repo_root, commit):
                        raise AuditError(
                            f"published {tag} commit {commit} is not available locally; "
                            "fetch it into an isolated ref or use a temporary clone"
                        )
                target_commit = remote_target_commit
                previous_commit = remote_previous_commit
                target_revision = remote_target_commit
                previous_revision = remote_previous_commit
            if mismatches:
                remote_verification = (
                    f"`{args.remote}` selected explicitly; local mismatch: "
                    + "; ".join(mismatches)
                )
            else:
                remote_verification = f"`{args.remote}` matches local final tags"

        recipes = recipe_files(repo_root)
        recipe_paths = [
            path.relative_to(repo_root / "recipes").as_posix() for path in recipes
        ]
        indexed, duplicate_index = parse_index(repo_root)
        missing_from_index = sorted(set(recipe_paths) - set(indexed))
        missing_on_disk = sorted(set(indexed) - set(recipe_paths))

        markdown_paths = recipes + [
            repo_root / "recipes" / "README.md",
            repo_root / "recipes" / "TEMPLATE.md",
        ]
        broken_links = broken_local_links(repo_root, markdown_paths)
        broken_links.extend(broken_fenced_code_paths(repo_root, markdown_paths))
        broken_links = sorted(
            set(broken_links), key=lambda item: (item.path, item.line, item.detail)
        )
        version_findings = version_review_findings(repo_root, recipes)
        release_changes = changed_paths(repo_root, previous_revision, target_revision)
        recipe_changes = changed_recipe_status(
            repo_root, previous_revision, target_revision
        )
        current_recipe_changes = current_recipe_status(repo_root, target_revision)
        target_recipe_paths = paths_at_revision(repo_root, target_revision, "recipes")
        linked_changes = linked_release_changes(
            repo_root, recipes, release_changes, target_recipe_paths
        )
        hotspots = release_hotspots(release_changes)

        print(
            render_report(
                repo=repo_root,
                target=target_tag.name,
                target_commit=target_commit,
                previous=previous_tag.name,
                previous_commit=previous_commit,
                remote_verification=remote_verification,
                recipes=recipes,
                indexed=indexed,
                duplicate_index=duplicate_index,
                missing_from_index=missing_from_index,
                missing_on_disk=missing_on_disk,
                broken_links=broken_links,
                version_findings=version_findings,
                recipe_changes=recipe_changes,
                current_recipe_changes=current_recipe_changes,
                linked_changes=linked_changes,
                hotspots=hotspots,
            )
        )

        structural_findings = (
            missing_from_index or missing_on_disk or duplicate_index or broken_links
        )
        return 1 if args.strict and structural_findings else 0
    except (AuditError, FileNotFoundError, NotADirectoryError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
