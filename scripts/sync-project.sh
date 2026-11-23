#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync-project.sh --project <name> [--tools codex,claude,cursor,skills] [--target /path/to/project] [--force]

Projects:
  generic
  vllm
  vllm-omni
  afd-plugin
  vllm-omni-cookbook
  nanodot
  router
  sciencediscovery
  system1-omni

Tools:
  codex   Copy AGENTS.md and its referenced skills
  claude  Copy AGENTS.md, CLAUDE.md, and their referenced skills
  cursor  Copy Cursor .mdc project rules and referenced skills
  skills  Copy only the selected profile's skills, without project rules

Existing identical files are left alone. Conflicting files require --force.
EOF
}

PROJECT=""
TOOLS="codex,claude,cursor"
FORCE=false
TARGET="$(pwd)"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      PROJECT="${2:-}"
      shift 2
      ;;
    --tools)
      TOOLS="${2:-}"
      shift 2
      ;;
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

case "$PROJECT" in
  generic|vllm|vllm-omni|afd-plugin|vllm-omni-cookbook|nanodot|router|sciencediscovery|system1-omni)
    ;;
  "")
    echo "--project is required" >&2
    usage
    exit 1
    ;;
  *)
    echo "Unsupported project: $PROJECT" >&2
    usage
    exit 1
    ;;
esac

FILES=()
SOURCES=()
COPY_SKILLS=false
add_file() {
  SOURCES+=("$1")
  FILES+=("${2:-$1}")
}

IFS=',' read -ra TOOL_LIST <<< "$TOOLS"
for tool in "${TOOL_LIST[@]}"; do
  case "$tool" in
    codex)
      if [ "$PROJECT" = generic ]; then
        add_file templates/generic/AGENTS.md AGENTS.md
      else
        add_file AGENTS.md
      fi
      COPY_SKILLS=true
      ;;
    claude)
      if [ "$PROJECT" = generic ]; then
        add_file templates/generic/AGENTS.md AGENTS.md
        add_file templates/generic/CLAUDE.md CLAUDE.md
      else
        add_file AGENTS.md
        add_file CLAUDE.md
      fi
      COPY_SKILLS=true
      ;;
    cursor)
      add_file .cursor/rules/agentic-coding-guidelines.mdc
      if [ -f "$ROOT/.cursor/rules/$PROJECT.mdc" ]; then
        add_file ".cursor/rules/$PROJECT.mdc"
      fi
      COPY_SKILLS=true
      ;;
    skills)
      COPY_SKILLS=true
      ;;
    "")
      ;;
    *)
      echo "Unsupported tool: $tool" >&2
      usage
      exit 1
      ;;
  esac
done

if [ "$COPY_SKILLS" = true ]; then
  # Project review overlays and selectors are resources of repository-maintenance.
  SKILLS=(agentic-coding-guidelines repository-maintenance repository-review-source)
  SKILL_FILE_LIST="$(mktemp)"
  trap 'rm -f "$SKILL_FILE_LIST"' EXIT
  for skill in "${SKILLS[@]}"; do
    if [ ! -f "$ROOT/skills/$skill/SKILL.md" ] || [ -L "$ROOT/skills/$skill" ] || [ -L "$ROOT/skills/$skill/SKILL.md" ]; then
      echo "Missing required skill entrypoint or unsupported symlink: $ROOT/skills/$skill/SKILL.md" >&2
      exit 1
    fi
    # Runtime-local source mappings are private inputs, not installable resources.
    if ! find "$ROOT/skills/$skill" -type f ! -name 'review-sources.local.json' ! -name '*.pyc' ! -path '*/__pycache__/*' -print0 > "$SKILL_FILE_LIST"; then
      echo "Cannot enumerate skill resources: $ROOT/skills/$skill" >&2
      exit 1
    fi
    while IFS= read -r -d '' source; do
      add_file "${source#"$ROOT/"}"
    done < "$SKILL_FILE_LIST"
  done
  rm -f "$SKILL_FILE_LIST"
  trap - EXIT
fi

# Reject ancestor collisions too; otherwise mkdir/cp can follow a directory
# symlink or partially install before encountering a regular-file parent.
python3 - "$TARGET" "${FILES[@]}" <<'PY_PREFLIGHT'
import os
from pathlib import Path
import sys
root = Path(os.path.abspath(sys.argv[1]))
for relative in sys.argv[2:]:
    parent = (root / relative).parent
    while True:
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise SystemExit("Refusing non-directory or symlink ancestor: " + str(parent))
        if parent == root or parent == parent.parent:
            break
        parent = parent.parent
PY_PREFLIGHT

# Preflight the complete install before changing any target files.
for index in "${!FILES[@]}"; do
  file="${FILES[$index]}"
  source="${SOURCES[$index]}"
  destination="$TARGET/$file"
  if [ ! -f "$ROOT/$source" ] || [ ! -r "$ROOT/$source" ]; then
    echo "Missing or unreadable install source: $ROOT/$source" >&2
    exit 1
  fi
  if [ -L "$destination" ] || { [ -e "$destination" ] && [ ! -f "$destination" ]; }; then
    echo "Refusing to replace a symlink or non-regular file: $destination" >&2
    exit 1
  fi
  if [ -e "$destination" ] && ! cmp -s "$ROOT/$source" "$destination" && [ "$FORCE" = false ]; then
    echo "Refusing to overwrite $destination; merge your rules or pass --force to replace it" >&2
    exit 1
  fi
done

for index in "${!FILES[@]}"; do
  file="${FILES[$index]}"
  source="${SOURCES[$index]}"
  destination="$TARGET/$file"
  if ! cmp -s "$ROOT/$source" "$destination"; then
    mkdir -p "$(dirname "$destination")"
    cp "$ROOT/$source" "$destination"
  fi
done

echo "Synced $PROJECT rules to $TARGET for tools: $TOOLS"
