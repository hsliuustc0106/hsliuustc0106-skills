#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync-project.sh --project <name> [--tools codex,claude,cursor] [--target /path/to/project]

Projects:
  vllm
  vllm-omni
  afd-plugin
  vllm-omni-cookbook

Tools:
  codex   Copy AGENTS.md
  claude  Copy AGENTS.md and CLAUDE.md
  cursor  Copy Cursor .mdc project rules
EOF
}

PROJECT=""
TOOLS="codex,claude,cursor"
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
  vllm|vllm-omni|afd-plugin|vllm-omni-cookbook)
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

mkdir -p "$TARGET"

IFS=',' read -ra TOOL_LIST <<< "$TOOLS"
for tool in "${TOOL_LIST[@]}"; do
  case "$tool" in
    codex)
      cp "$ROOT/AGENTS.md" "$TARGET/AGENTS.md"
      ;;
    claude)
      cp "$ROOT/AGENTS.md" "$TARGET/AGENTS.md"
      cp "$ROOT/CLAUDE.md" "$TARGET/CLAUDE.md"
      ;;
    cursor)
      mkdir -p "$TARGET/.cursor/rules"
      cp "$ROOT/.cursor/rules/agentic-coding-guidelines.mdc" "$TARGET/.cursor/rules/"
      cp "$ROOT/.cursor/rules/$PROJECT.mdc" "$TARGET/.cursor/rules/"
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

echo "Synced $PROJECT rules to $TARGET for tools: $TOOLS"

