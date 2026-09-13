# Repair Report: n8n webhook Listening UI wording

日期：2026-09-13

## 修正內容

- `m0-workflow-01-webhook.html`：將藍色 Listening 從固定畫面改為版本差異提示，並把綠框、`1 item`、Output 與 404 修復寫成可觀察驗收。
- `m0-install-mac.html`、`m0-install-win.html`：#06 Webhook AI 的執行步驟改用執行／等待狀態描述，保留 Mac／Windows 終端機差異。
- `m1-1-launch.html`：空白 Webhook 練習改用畫布下方橘色 `Execute workflow`。
- `m1-2-tunnel.html`：Tunnel 測試與 404 修復改用執行／等待、Test path、綠框與 Output 作判斷。
- `assets/n8n-lite-pack.zip`：#01 sticky note 與變更紀錄同步修正；14 個 workflow JSON 邏輯未改動。

## 驗證證據

| 檢查 | 結果 |
|---|---|
| `bash -n n8n/_tools/restore-2026-09-13-pre-webhook-listening-ui.sh` | PASS |
| 5 個目標 HTML `lint-page.py --summary` | 全部 BLOCKER 0、ERROR 0 |
| 全站 `python3 docs/build-all.py --lint-only` | 1330 頁；BLOCKER 0、ERROR 0 |
| ZIP `unzip -t` | PASS |
| ZIP workflow JSON parse | 14 / 14 PASS |
| #01 sticky note 欄位與 URL 對齊 | PASS |
| 強制藍色 Listening 文字掃描 | PASS（僅保留版本差異提示） |
| `git diff --check` | PASS |
| 搜尋索引 | 660 筆已重建 |
| sitemap | 45 筆 URL 已重建 |

## 人工驗證基線

使用者提供的 Mac 實測截圖確認 #01：Webhook 與 Set 節點綠框、勾號、連線 `1 item`、成功通知與三欄位 Output 均出現。這次修正讓教材驗收條件與該實測畫面一致。

## 平台狀態

- macOS：已有人工作業證據。
- Windows：教材已同步修正；仍標記為待實機驗證，未以 Mac 結果代替 Windows 證據。

## 可回復

備份：`n8n/_backup/2026-09-13-pre-webhook-listening-ui/`

還原：`n8n/_tools/restore-2026-09-13-pre-webhook-listening-ui.sh`
