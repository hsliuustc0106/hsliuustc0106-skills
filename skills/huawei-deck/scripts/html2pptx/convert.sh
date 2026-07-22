#!/usr/bin/env bash
# convert.sh — 一键把 DC 独立版 HTML 课件转成 PPTX
# 用法:
#   ./convert.sh "课件.html"                 # 输出同名 .pptx
#   ./convert.sh "课件.html" "输出.pptx"      # 指定输出
#   SCALE=2 QUALITY=92 ./convert.sh ...      # 调清晰度/压缩
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IN="${1:?用法: ./convert.sh <input.html> [output.pptx]}"
OUT="${2:-${IN%.html}.pptx}"
SCALE="${SCALE:-2}"
QUALITY="${QUALITY:-92}"

[ -f "$IN" ] || { echo "找不到输入文件: $IN" >&2; exit 1; }

TMP="$(mktemp -d -t html2pptx.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

echo "▶ 截图: $IN"
node "$HERE/shoot.mjs" "$IN" "$TMP" "$SCALE" "$QUALITY"

echo "▶ 组装 PPTX"
# 默认不嵌入原始 HTML（省 ~34MB）；需要时 EMBED_HTML=1 ./convert.sh ... 开启
if [ "${EMBED_HTML:-0}" = "1" ]; then
  python3 "$HERE/build_pptx.py" "$TMP" "$OUT" "$IN"
else
  python3 "$HERE/build_pptx.py" "$TMP" "$OUT"
fi

echo "✅ 完成: $OUT"
ls -lh "$OUT"
