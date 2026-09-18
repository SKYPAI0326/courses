# AI 入門即戰力：版面重設計執行報告

日期：2026-09-14

## 執行結果

已完成入口頁與 4 個內容頁的可見版面重設計。這次調整直接改變頁面結構的閱讀節奏：

- 入口頁首屏改為「課程定位＋課程產出」雙欄 hero。
- 單元索引改為編號、標題、時數、任務描述與獨立入口的課程路徑。
- 內容頁 hero 改為「單元標題／實務成果」雙欄，學習成果可在標題旁快速掃讀。
- 內容區改為左側章節標記、右側教學內容，縮短段落間距並保留操作順序。
- 卡片、提示區、底部導覽統一線條、色彩與 hover 行為；手機版回到單欄。

## 修改檔案

- `module1.html`
- `CH1-1.html`
- `CH2-1.html`
- `CH3-1.html`
- `CH4-1.html`
- `assets/layout-redesign.css`

頁面文字、操作步驟、練習、測驗、細節展開區、本地連結與錨點均未刪減。

## 驗收證據

- `lint-page.py`：5 頁，BLOCKER 0、ERROR 0、WARN 0。
- 版面備份比對：5 頁的 section 數、`a` 連結數與 HTML id 數均與修改前一致。
- 本地目標檢查：CSS、教材、備援文件與頁面連結均可解析，未發現 BROKEN。
- 本機瀏覽器預覽：4 個內容頁均載入 `layout-redesign.css`，桌面版 hero 與內容區均呈現雙欄；第一內容區起點約落在 549–629px，內容頁由原先約 682px 提前到約 549px，首屏留白改為可掃讀的學習成果區。

## 回復方式

如需回到本次版面重設計前的狀態，在課程目錄執行：

```bash
bash ai-beginner-practical/_tools/restore-2026-09-14-pre-layout-redesign.sh
```

備份位置：`ai-beginner-practical/_backup/2026-09-14-pre-layout-redesign/`
