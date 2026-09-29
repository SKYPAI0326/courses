#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/../../.." && pwd)"
COURSE="$BASE/courses/ccs-foundations"
BACKUP="$COURSE/_backup/2026-09-29-pre-ch1-1-syntax-fix/pages/CH1-1.html"

cp -p "$BACKUP" "$COURSE/CH1-1.html"
printf '%s\n' 'Restored CH1-1.html from the dated syntax-fix backup.'
