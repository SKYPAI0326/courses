# REPAIR-REPORT：Part 1 改為四個反覆使用專案

日期：2026-11-13　計畫：`REPAIR-PLAN.md`　狀態：已修改，未 commit、未發布

## 變更檔案（新雜湊前 16 碼）

| 檔案 | 狀態 | SHA-256 |
|---|---|---|
| `_lessons/acp-ae/CH1-1.md` | M | 59b0b5e4c5310d71 |
| `_lessons/acp-ae/CH1-2.md` | M | 2da84afe332d9c4a |
| `_lessons/acp-ae/CH1-3.md` | M | 86f6e0c5e4e8047a |
| `_lessons/acp-ae/CH1-4.md` | M | 18cbbcb06b996acd |
| `_lessons/acp-ae/CH1-5.md` | D | （已移除） |
| `_lessons/acp-ae/CH2-1.md` | M | b52ee7a2fe48bbc7 |
| `_lessons/acp-ae/CH3-1.md` | M | 02a02cdd88eb9a8c |
| `_lessons/acp-ae/CH3-2.md` | M | 4a6702a7704c35f3 |
| `_lessons/acp-ae/CH3-3.md` | M | 5608fe80426d1d69 |
| `_lessons/acp-ae/PRAC1.md` | D | （已移除） |
| `courses/acp-ae/README.md` | M | 5613f930a4ddb138 |
| `courses/acp-ae/_tools/validate-handout.py` | M | e21e78ffe39e6d27 |
| `courses/acp-ae/ae-interface-function-guide.html` | M | 9985d5ad0c408551 |
| `courses/acp-ae/assets/downloads/README.md` | M | 66503b8816b61fab |
| `courses/acp-ae/assets/downloads/acp-ae-evidence-checklist.md` | M | e0c507b16b46c449 |
| `courses/acp-ae/assets/handout.css` | M | 2864216aecdd8780 |
| `courses/acp-ae/index.html` | M | 9f12d70381f24cee |
| `courses/acp-ae/module1.html` | M | c31bc1eff96a65ed |
| `courses/acp-ae/part1/CH1-1.html` | M | 603c77956a4bd0f8 |
| `courses/acp-ae/part1/CH1-2.html` | M | d8533f673782aa23 |
| `courses/acp-ae/part1/CH1-3.html` | M | e80ad2b2f1a2d8c7 |
| `courses/acp-ae/part1/CH1-4.html` | M | 71e6a1985979606f |
| `courses/acp-ae/part1/CH1-5.html` | D | （已移除） |
| `courses/acp-ae/part1/PRAC1.html` | D | （已移除） |
| `courses/acp-ae/part2/CH2-1.html` | M | 8ac01bd586a8bda0 |
| `courses/acp-ae/part3/CH3-1.html` | M | 92e15318dfe3d883 |
| `courses/acp-ae/part3/CH3-2.html` | M | 7297933a13942204 |
| `courses/acp-ae/_tools/restore-2026-11-13-pre-repair.sh` | ?? | 561bd00d6266219e |

`CH1-5`、`PRAC1` 的 HTML 與教案另移到 `~/.Trash/acp-ae-old-part1-2026-11-13/`，並在 `_backup/2026-11-13-pre-repair/` 保留。

## 驗證（Claude 執行）

| 項目 | 結果 |
|---|---|
| `_tools/validate-handout.py` | PASS：8 lessons、12 HTML、40 操作卡、13 概念題、9 代表實作 |
| `validate-course-structure.py`（Part 1 四頁、CH2-1、CH3-1、CH3-2、介面指南） | 8 頁 blocked=0 |
| `docs/lint-page.py`（10 頁） | 0 BLOCKER、0 ERROR、0 WARN |
| `docs/audit-course-substance.py`（Part 1 四頁） | block=0；semantic_review PENDING |
| `git diff --check` | clean |
| 殘留引用 | 課程頁、下載區、教案無 `CH1-5`、`PRAC1` |
| 內建瀏覽器 | CH1-2 @1440、CH1-4 @390（表格在 table-scroll 內橫捲，頁面無水平溢位）、module1 @820；無頁面水平捲軸 |

## 未解風險

- 未做學員試走；AE 2025 實機未確認：Composition Marker 選單路徑、Interpret Footage 後圖層色條、Lock Aspect Ratio 與 Pre-compose 預設、Shift 吸附 CTI、Typewriter Keyframe 屬性。
- `validate-handout.py` 的模板錨點（第一個動作、成功訊號等）改為只檢查 Part 2、3，因為 Part 1 依使用者要求不再使用任務契約表。
- 搜尋索引與 sitemap 未重建（commit 前執行 `docs/build-search-index.py`、`docs/build-sitemap.py`）。
- `易讀版/` 未同步，仍是舊 Part 1。

## 回復

`bash courses/acp-ae/_tools/restore-2026-11-13-pre-repair.sh`（還原 27 個檔案；移除的兩頁也在備份內）。
