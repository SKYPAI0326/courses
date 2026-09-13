# n8n 講義修正報告（2026-09-13）

## 本次已完成

- `lessons/m0-install-mac.html`
  - Phase B 改為 Gemini 必填、Telegram 選配。
  - 對齊 wizard 的 14 workflow、1／2 credentials 與兩種 smoke test 判準。
  - Step 0 的空 container 結果會顯示明確的成功訊息。
  - Gatekeeper 改成「若被擋才處理」；footer 加入 n8n 2.37.7、Starter Kit v1.1.0、Lite Pack v1.3.2 與建置日期。
  - Phase C 的 Telegram／Webhook 案例標示選配條件；Gemini-only 路徑明確改走 C3～C5。
- `lessons/m0-install-win.html`
  - 同步 Phase B 分支、數量、credential 與 Windows PowerShell 驗證輸出。
  - Phase C 的 Telegram／Webhook 案例標示選配條件，避免無 credential 時照做而失敗。
  - 保留 Windows 尚待實機驗證的狀態。
- `lessons/m1-1-launch.html`
  - 統一 Starter Kit 以 Downloads 為示例路徑，列出四個 `.command` 腳本。
  - 命令列備援改為兩行，排錯段落同時提供 macOS／Windows 路徑。
- `assets/n8n-starter-kit/README.md`
  - 同步跨平台路徑契約、版本與安全界線。
- `assets/n8n-lite-pack.zip`
  - 重寫內附 README，對齊 wizard v1.3.2、14 workflow、Gemini 必填／Telegram 選配、cloudflared 僅 workflow 07。
  - 同步 wizard Step 9 顯示實際 JSON 數量。
- `_backup/2026-09-13-pre-repair/` 與 `_tools/restore-2026-09-13-pre-repair.sh`
  - 保留修正前頁面、README 與兩個 ZIP，可一鍵回復。

## 靜態驗證證據

- `python3 ../docs/lint-page.py courses/n8n/lessons/m0-install-mac.html`：0 BLOCKER、0 ERROR、2 WARN。
- `python3 ../docs/lint-page.py courses/n8n/lessons/m0-install-win.html`：0 BLOCKER、0 ERROR、2 WARN。
- `python3 ../docs/lint-page.py courses/n8n/lessons/m1-1-launch.html`：0 BLOCKER、0 ERROR、2 WARN。
- `python3 ../docs/lint-page.py courses/n8n/lessons/m1-1-install.html`：0 BLOCKER、0 ERROR、1 WARN。
- 三個修正頁面的相對連結：0 個失效連結。
- Lite Pack ZIP：14 個 workflow JSON，全部可解析；`setup-wizard.command` 與 `.bat` 均存在，macOS 腳本保留 executable mode。
- `git diff --check`：通過。

`python3 ../docs/check-integrity.py` 的全站檢查仍列出其他課程／工具目錄既有的登錄錯誤（20 ERROR、17 WARN）；本次未修改那些範圍，故不把全站結果誤標為 n8n 修正失敗。

## 尚待人工驗證

- Docker Desktop 啟動、Owner Account、Gemini key 與 Lite Pack wizard 的完整實跑。
- Windows Docker Desktop／PowerShell 的實機流程。
- Telegram 選配分支與 workflow 05／06／07／09／10／11／13／14 的實際 credential 執行。
- Gmail 與其他外部服務 workflow 的帳號授權與平台行為。

這些項目在人工驗證前維持「待實機驗證」，不視為目前版本已通過。

## 回復

```bash
bash n8n/_tools/restore-2026-09-13-pre-repair.sh
```
