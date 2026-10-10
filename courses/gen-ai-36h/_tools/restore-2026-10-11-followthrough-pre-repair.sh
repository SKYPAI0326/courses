#!/bin/bash
set -eu
course_root="$(cd "$(dirname "$0")/.." && pwd)"
cp -R "$course_root/_backup/2026-10-11-followthrough-pre-repair/files/." "$course_root/"
printf '%s\n' '已還原本輪既有課程檔案；新增指南保留。全站鏡像備份位於 backup/site，需依目前其他課程狀態選擇還原。'
