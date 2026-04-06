#!/usr/bin/env bash
# 在仓库根目录 linscio-portal/ 的**上一级**生成 linscio-portal.zip（顶层目录名为 linscio-portal/）
# 用法：cd /path/to/parent-of-linscio-portal && bash linscio-portal/deploy/package-source-zip.sh
# 或：cd /path/to/linscio-portal && bash deploy/package-source-zip.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORTAL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PARENT="$(dirname "$PORTAL_DIR")"
OUT="$PARENT/linscio-portal.zip"

if [[ ! -f "$PORTAL_DIR/api/requirements.txt" ]]; then
  echo "ERROR: 未找到 $PORTAL_DIR/api/requirements.txt" >&2
  exit 1
fi

cd "$PARENT"
rm -f "$OUT"
zip -r -q "$OUT" "$(basename "$PORTAL_DIR")" \
  -x "*/node_modules/*" -x "*node_modules/*" \
  -x "*/venv/*" -x "*/.venv/*" \
  -x "*/__pycache__/*" -x "*.pyc" \
  -x "*/.git/*" -x "*/dist/*" \
  -x "*.DS_Store" -x "*/.env" \
  -x "*/api/dev.db*" -x "*/api/*.db-shm" -x "*/api/*.db-wal"

echo "已生成: $OUT ($(du -h "$OUT" | cut -f1))"
unzip -l "$OUT" | head -5
