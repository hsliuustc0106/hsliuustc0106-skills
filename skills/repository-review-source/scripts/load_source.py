#!/usr/bin/env python3
"""Resolve canonical review instructions without network access or execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def load(alias, checkout, config=None):
    manifest = Path(config) if config else Path(__file__).resolve().parents[1] / "sources.json"
    item = json.loads(manifest.read_text())[alias]
    repo = item["repository"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("Invalid repository identity")
    root = Path(git(Path(checkout).resolve(), "rev-parse", "--show-toplevel")).resolve()
    origin = git(root, "remote", "get-url", "origin")
    allowed = {"https://github.com/" + repo, "https://github.com/" + repo + ".git", "git@github.com:" + repo, "git@github.com:" + repo + ".git", "ssh://git@github.com/" + repo, "ssh://git@github.com/" + repo + ".git"}
    if origin not in allowed:
        raise ValueError("Checkout origin does not match configured repository")
    relative = Path(item["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Source path must stay inside repository")
    source = (root / relative).resolve()
    source.relative_to(root)
    data = source.read_bytes()
    text = data.decode("utf-8")
    if not text.startswith("---\n"):
        raise ValueError("Canonical source is not a skill")
    try:
        head_data = subprocess.check_output(["git", "-C", str(root), "show", "HEAD:" + relative.as_posix()], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        head_data = None
    dirty = head_data != data or bool(git(root, "status", "--porcelain", "--ignored=matching", "--untracked-files=all", "--", relative.parent.as_posix()))
    return {"alias": alias, "repository": repo, "commit": git(root, "rev-parse", "HEAD"), "path": relative.as_posix(), "source_directory": str(source.parent), "sha256": hashlib.sha256(data).hexdigest(), "source_tracked_at_head": head_data is not None, "working_tree_dirty": dirty, "skill": text}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("alias")
    parser.add_argument("--checkout", required=True)
    parser.add_argument("--config")
    args = parser.parse_args()
    try:
        result = load(args.alias, args.checkout, args.config)
    except (OSError, ValueError, TypeError, KeyError, subprocess.CalledProcessError) as exc:
        print("Cannot load canonical review skill: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
