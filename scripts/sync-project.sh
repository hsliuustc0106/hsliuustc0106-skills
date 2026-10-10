#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync-project.sh --project <name> [--tools codex,claude,cursor] [--target /path/to/project] [--force]

Projects:
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
  vllm|vllm-omni|afd-plugin|vllm-omni-cookbook|nanodot|router|sciencediscovery|system1-omni)
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
COPY_SKILLS=false
IFS=',' read -ra TOOL_LIST <<< "$TOOLS"
for tool in "${TOOL_LIST[@]}"; do
  case "$tool" in
    codex)
      FILES+=(AGENTS.md)
      COPY_SKILLS=true
      ;;
    claude)
      FILES+=(AGENTS.md CLAUDE.md)
      COPY_SKILLS=true
      ;;
    cursor)
      FILES+=(.cursor/rules/agentic-coding-guidelines.mdc)
      if [ -f "$ROOT/.cursor/rules/$PROJECT.mdc" ]; then
        FILES+=(".cursor/rules/$PROJECT.mdc")
      fi
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
  # Copy every skill referenced by AGENTS.md, including review resources.
  for skill in repository-review-source router-review sciencediscovery-review system1-omni-review afd-plugin-review personal-skills-review nanodot-review vllm-guidelines vllm-omni-guidelines vllm-omni-review afd-plugin-guidelines vllm-omni-cookbook-guidelines; do
    # Runtime-local source mappings are private inputs, not installable resources.
    while IFS= read -r -d '' source; do
      FILES+=("${source#"$ROOT/"}")
    done < <(find "$ROOT/skills/$skill" -type f ! -name 'review-sources.local.json' ! -name '*.pyc' ! -path '*/__pycache__/*' -print0)
  done
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
for file in "${FILES[@]}"; do
  destination="$TARGET/$file"
  if [ -L "$destination" ] || [ -d "$destination" ]; then
    echo "Refusing to replace a symlink or directory: $destination" >&2
    exit 1
  fi
  if [ -e "$destination" ] && ! cmp -s "$ROOT/$file" "$destination" && [ "$FORCE" = false ]; then
    echo "Refusing to overwrite $destination; merge your rules or pass --force to replace it" >&2
    exit 1
  fi
done

for file in "${FILES[@]}"; do
  destination="$TARGET/$file"
  if ! cmp -s "$ROOT/$file" "$destination"; then
    mkdir -p "$(dirname "$destination")"
    cp "$ROOT/$file" "$destination"
  fi
done

echo "Synced $PROJECT rules to $TARGET for tools: $TOOLS"
