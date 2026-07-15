#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
BACKUP="$ROOT/courses/office-ai/_backup/2026-07-15-pre-taiwan-locale/ch1/CH1-3.html"
TARGET="$ROOT/courses/office-ai/ch1/CH1-3.html"

cp "$BACKUP" "$TARGET"
echo "已還原台灣用語修正前的 CH1-3.html。請重新執行 lint 與搜尋索引產生器。"
