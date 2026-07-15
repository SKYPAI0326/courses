#!/bin/sh
set -eu

BASE=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
BACKUP="$BASE/courses/office-ai/_backup/2026-07-15-pre-full-copy-sync"
COURSE="$BASE/courses/office-ai"

cp "$BACKUP/ch1/CH1-4.html" "$COURSE/ch1/CH1-4.html"
cp "$BACKUP/ch2/CH2-1.html" "$COURSE/ch2/CH2-1.html"
cp "$BACKUP/ch3/CH3-1.html" "$COURSE/ch3/CH3-1.html"
cp "$BACKUP/ch5/CH5-3.html" "$COURSE/ch5/CH5-3.html"
cp "$BACKUP/ch6/CH6-2.html" "$COURSE/ch6/CH6-2.html"
