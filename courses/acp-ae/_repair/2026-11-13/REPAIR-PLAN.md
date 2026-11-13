# REPAIR-PLAN：Part 1 改為四個反覆使用專案

日期：2026-11-13　模式：治理修復（含刪除、單元結構改變）

## 使用者決定

- Part 1 原本 6 頁（CH1-1～CH1-5、PRAC1）換成 4 個專案頁。
- Part 2、Part 3 只改引用舊 Part 1 成品的名稱（工程檔與 Composition），其他不動。
- 只改主版，不動 `易讀版/`；改完不 commit、不推上線。

## Finding

| 代碼 | 位置 | 內容 | owner Gate |
|---|---|---|---|
| F1 | Part 1 六頁 | 每頁名詞卡、任務契約表、預列修復、同一格式；基礎操作各教一次，到題庫時學員對功能定位不熟 | G2（單元架構）／G3（正文） |
| F2 | CH2-1、CH3-1、CH3-2、CH3-3 教案 | 引用 `ACP-AE-Lab-PRAC1.aep`、`PRAC1_Title_6s`，新 Part 1 不再產生 | G5（跨單元產物鏈） |

## 內容來源

`01-PROJECTS/講義研究/實驗/ae-反覆使用/` 四份講義（已經兩輪官方說明核對與使用者回饋修正：開頭鋪陳、改用點選路徑）。

## 變更清單

| 檔案 | 動作 |
|---|---|
| `_lessons/acp-ae/CH1-1.md`～`CH1-4.md` | 以四個專案正文取代 |
| `_lessons/acp-ae/CH1-5.md`、`PRAC1.md` | 移除（備份保留） |
| `part1/CH1-1.html`～`CH1-4.html` | 依新教案重建，沿用既有 head、topbar、`.lesson-body`、footer、script |
| `part1/CH1-5.html`、`PRAC1.html` | 移除（備份保留） |
| `module1.html`、`index.html` | Part 1 單元清單、單元數、成果描述 |
| `ae-interface-function-guide.html` | 指向 `part1/PRAC1.html` 的連結改指 Part 1 新頁 |
| `part2/CH2-1.html`、`part3/CH3-1.html`、`part3/CH3-2.html`，與 `_lessons/acp-ae/CH2-1.md`、`CH3-1.md`、`CH3-2.md`、`CH3-3.md` | 只換工程檔與 Composition 名稱 |
| `assets/handout.css` | 新增 `.body-list` 一條規則（清單縮排），不改既有規則 |
| `README.md`、`assets/downloads/README.md`、`assets/downloads/acp-ae-evidence-checklist.md` | 舊工程名稱與 PRAC1 說法 |
| `_tools/validate-handout.py` | 單元清單改為 8 個；「第一個動作／成功訊號」等模板錨點只檢查 Part 2、3（Part 1 新寫法不使用任務契約表，這是使用者要求的寫法改變） |

## 驗證

- `_tools/validate-handout.py`
- `validate-course-structure.py`、`docs/lint-page.py`、`docs/audit-course-substance.py` 對受影響頁
- 內建瀏覽器 1440／820／390px 代表頁抽查
- `git diff --check`

## 回復

`_backup/2026-11-13-pre-repair/`（27 個檔案，原始雜湊在 `original-sha256.txt`），`_tools/restore-2026-11-13-pre-repair.sh`，隔離還原驗證通過。

## 已知未實機確認

Composition Marker 選單路徑、Interpret Footage 後圖層色條是否自動變長、Lock Aspect Ratio 與 Pre-compose 勾選框預設、Shift 拖曳吸附 CTI、Typewriter Keyframe 所在屬性。
