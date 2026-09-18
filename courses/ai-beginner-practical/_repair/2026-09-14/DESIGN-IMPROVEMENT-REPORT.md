# AI 入門即戰力：版面改善報告

日期：2026-09-14

## 結果

已完成入口頁與 CH1–CH4 內容頁的版面一致性改善，未刪除課程內容，也未改變四個單元的教學流程。

## 已完成

- 統一 `--c-muted` 為 `#8c8880`，入口頁同步更新。
- 將內容頁重複的主色引用收斂為既有 `--c-a4` 語意色；每頁 `var(--c-main)` 引用由 10–11 次降為 2 次。
- 移除 CH2、CH3 主要按鈕的 `filter:brightness`，並為四頁統一明確的 hover 背景與邊框色。
- 統一 hero 返回連結與底部前後頁文字；修正 CH1 下一單元名稱、CH2 footer 舊文案與 CH4 返回位置。
- 入口頁三個內容頁 CTA 改為獨立行、品牌色連結與 hover 狀態，避免瀏覽器預設藍色底線及 CH3 CTA 擁擠斷行。
- 重新建立搜尋索引：`666` 筆。

## 驗收證據

- `python3 docs/lint-page.py courses/ai-beginner-practical/ --summary`：5 頁，0 BLOCKER、0 ERROR、0 WARN。
- 本地連結檢查：55 條，PASS。
- 結構／token 掃描：入口頁與 4 個內容頁 PASS；內容頁均為 1 main、1 skip link、8 lesson sections、1 progress strip、1 footer、統一 muted 色、主色引用 ≤4。
- 平台政策掃描：CH2／CH4 未指定平台；CH3 僅固定 NotebookLM；未引入資安單元文案，PASS。
- 教學互動數量與改善前備份一致：CH1 11 steps、CH2 10 steps、CH3 5 steps、CH4 10 steps；各頁 2 個 quiz；CH4 32 個 details。
- `git diff --check`：PASS。
- 以本機預覽實際冷讀 `module1.html`、CH2、CH3、CH4：入口 CTA 已獨立成行，CH2／CH3／CH4 hero 導覽與標籤可見，標題與學習成果在桌面視窗正常折行。

## 回復

本次修改前檔案位於 `_backup/2026-09-14-pre-design-improvement/`，可執行：

```bash
bash ai-beginner-practical/_tools/restore-2026-09-14-pre-design-improvement.sh
```

## 尚待人工確認

- `topbar` 的 blur 與膠囊標籤圓角仍由共用 lesson template v3 提供，本次未在單頁覆寫；若要完全符合設計規格，應另開共用模板改善。
- CH2 在入口頁的代表卡與詳細單元區仍保留雙重曝光，避免未經內容審議刪除課程入口；可在下一輪資訊架構改善時決定合併方式。
- 瀏覽器請重新整理 `module1.html`，再沿 CH1 → CH2 → CH3 → CH4 冷讀一次，確認實際視窗中的 CTA、導覽與手機版折行。
