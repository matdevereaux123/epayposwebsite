#!/bin/bash
# Builds the local preview and serves it at http://localhost:4321
#
# The build runs from a copy at ~/epay-site-preview, not from the Desktop:
# the Desktop syncs to iCloud, and builds reading from it can hang.
# BLOG_SHOW_DRAFTS=1 makes blog drafts visible at /blog/drafts in this preview
# only. The real site (Netlify) never sets it, so drafts are never public.
set -euo pipefail
export PATH="$HOME/.local/node/bin:$PATH"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/epay-site-preview"

mkdir -p "$DEST"
rsync -a --delete --exclude node_modules --exclude dist --exclude .astro --exclude tools "$SRC/" "$DEST/"
cd "$DEST"
if [ ! -d node_modules ] || [ package-lock.json -nt node_modules/.package-lock.json ]; then
  npm ci --no-audit --no-fund
fi
BLOG_SHOW_DRAFTS=1 npm run build

if ! curl -s -o /dev/null --max-time 3 http://localhost:4321/; then
  rm -f .astro/preview.json
  nohup npx astro preview --port 4321 > "$DEST/preview.log" 2>&1 &
  sleep 3
fi
echo "Preview ready: http://localhost:4321  (drafts: http://localhost:4321/blog/drafts)"
