# B4 Overlay 單一互動冷啟動審查

> 審查時間：2026-09-16 18:20（Asia/Taipei）
> 審查者：Codex machine pass
> 狀態：`MACHINE_PASS_PENDING_HUMAN`

## 審查範圍

- 教案：`../_lessons/uiux-designer/B4-overlay-single-action.md`
- HTML：`../uiux-designer/part2/CH4-overlay-single-action.html`
- 實測依據：`../uiux-designer/_validation/figma-starter-browser/PROBE-B.md`
- 素材包：`../uiux-designer/assets/B4-overlay-single-action/`

## 機器冷啟動結果

| Gate | 結果 | 證據 |
|---|---|---|
| 讀者能找到起始狀態 | PASS | START-HERE、FIGMA-FILE-URL、尺寸參考圖與檢查表皆存在 |
| 內容能從零執行 | PASS | 教案含 Hook、Concepts、Demo、Together、Solo、Checkpoint、修復、驗收與 Quiz |
| Figma Starter 邊界誠實 | PASS | 明寫同檔一核心 action 與拆檔備援；不要求升級、分享或付款 |
| 產出能被觀察 | PASS | Host／Overlay 名稱、尺寸、Prototype action、Chrome Preview 結果都有固定判準 |
| HTML 結構 | PASS | 8 個 lesson section，符合 v3 版面；`lint-page.py` 0 BLOCKER／0 ERROR／0 WARN |
| Chrome 版面與可及性樹 | PASS | 本地 `http://127.0.0.1:8766/.../CH4-overlay-single-action.html` 可開啟；標題、8 段、表格、清單、素材連結均可見 |
| 素材連結 | PASS | Overlay PNG 連結可開啟並顯示 320×200 圖；其餘路徑由伺服器回應檢查 |
| 實際 Figma 互動 | MACHINE_PASS | Probe B 在 Chrome Preview 點擊 Host 後顯示「確認完成」 |

## 已知未完成項

1. 尚未由外部學員完成真人跟做，因此不能標 `HUMAN_PASS`。
2. 本單元只驗證一條 action；登入→清單→Dialog 的完整三段流程仍須拆檔或另行升級方案。
3. Photoshop 開檔、色彩管理、匯入後修復與公開部署尚未實測，不能從本頁推論已通過。
4. 目前只做本地瀏覽器預覽；GitHub push、Figma Share 權限與公開站點仍保持未執行。

## 人工驗證交接

- 用自己的 Figma Starter 帳號從空白 Draft 重建兩個 Frame。
- 嚴格只建立一條 `On click → Open overlay → Dialog / Overlay`。
- 在 Chrome Preview 點擊並截圖，將結果附在 `EXPECTED-CHECK.md`。
- 若與機器證據不同，保留原檔、記錄瀏覽器／方案／日期，再回寫 `PROBE-B.md` 與 Run Log。
