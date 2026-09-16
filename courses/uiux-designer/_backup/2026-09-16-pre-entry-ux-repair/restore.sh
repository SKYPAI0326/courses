#!/bin/zsh
set -euo pipefail
BACKUP_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_DIR="$(cd "$BACKUP_DIR/../../.." && pwd)"
cp "$BACKUP_DIR/index.html" "$COURSE_DIR/index.html"
print "Restored uiux-designer/index.html"
