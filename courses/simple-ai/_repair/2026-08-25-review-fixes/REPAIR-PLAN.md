# simple-ai 審核修正計畫

日期：2026-08-25

## Scope

- slug：`simple-ai`
- 說明：依課程審核結果修正素材可操作性、環境前置、上下游交接、資安示範與 PDF 連結。
- 會修改：`CH1-1.html`、`CH1-2.html`、`CH1-3.html`、`CH1-4.html`、`CH2-1.html`、`CH2-2.html`、`CH2-3.html`、`CH2-4.html`、`module1.html`、`module2.html`、`handbook.html`、`index.html`、`prompt-library.html`、`_outlines/simple-ai.md`。
- 會新增：`_outlines/simple-ai.environment.md`、三張合成文件照片、`assets/learner-workflow-path-template.txt`、本修復報告與還原腳本。
- 不修改：其他課程、既有 unrelated worktree changes、既有交付物來源內容。

## 修正項目與驗收

1. **核心照片素材**：CH1-3 直接提供可下載的虛構報價單、名片、菜單 JPG；每張有對應欄位與安全標示。
2. **環境契約**：說清楚免費/付費邊界、登入、起始狀態、路徑、配額漂移與 fallback。
3. **學員產物**：CH2-4 先完成可保存的「一條工作流路徑」再選延伸作業。
4. **上下游交接**：CH2-2、CH2-3、CH2-4 明確指定輸入檔名、完成證據與 fallback 只作示範。
5. **資安與示範**：修正半透明塗抹示範、標示未查證行銷數字，移除未納入工具契約的 Perplexity 必修暗示。
6. **課程負荷**：模組頁標註課堂核心與課後延伸，避免把全部段落誤當必做。
7. **PDF 連結**：handbook 的素材連結改為可攜 HTTPS 目標，重新輸出後驗證 annotations。

## Stop conditions

- 新增素材無法被頁面連結或內容無法核對：停止，不以文字敘事補洞。
- lint 出現 BLOCKER/ERROR：停止發布並回到修正。
- PDF 連結仍指向本機 `file://`：標記 BLOCKED，不宣稱已完成。
