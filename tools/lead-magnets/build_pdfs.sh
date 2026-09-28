#!/bin/bash
# Renders each lead-magnet HTML page to PDF with headless Chrome.
#   bash tools/lead-magnets/build_pdfs.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../../public/downloads"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$OUT"
for src in "$HERE"/*.html; do
  name="$(basename "$src" .html)"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
    --print-to-pdf="$OUT/$name.pdf" "file://$src" >/dev/null 2>&1
  echo "built $name.pdf ($(du -h "$OUT/$name.pdf" | cut -f1))"
done
