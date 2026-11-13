#!/bin/bash
# Restore files changed by the 2026-11-13 Part 1 repetition repair.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
SRC="$REPO/courses/acp-ae/_backup/2026-11-13-pre-repair"
cd "$SRC"
find . -type f | while read -r f; do mkdir -p "$REPO/$(dirname "$f")"; cp -p "$f" "$REPO/$f"; done
echo "restored from $SRC"
