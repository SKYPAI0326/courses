# Starter Kit／Lite Pack 安裝修復報告

日期：2026-09-15

## 判定

安裝警示的根因在 Lite Pack 的 Mac／Windows setup wizard，不在目前 Starter Kit 的四條環境設定。Starter Kit `n8n-compose.yml` 已含正確契約；舊 wizard 的 regex 只接受 `environment:` 後連續的 YAML list，遇到合法註解或空白行便回報 patch 失敗。

## 已修正

- Mac `setup-wizard.command` 與 Windows `setup-wizard.ps1` 改為依 `n8n` service 行掃描 `environment:`，允許註解／空白行，並只在該 service 內判斷缺漏。
- `N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES` 統一為 `true`，與 Starter Kit v1.1.0 一致。
- 錯誤提示統一指向實際檔名 `n8n-compose.yml`。
- Lite Pack wizard 升為 v1.3.6；Mac／Windows 安裝頁下載連結改用 `?v=1.3.6`。
- Starter Kit 下載連結的 cache-buster 從 `?v=1.0.2` 更新為 `?v=1.1.0`，避免瀏覽器沿用舊快取。
- 更新目前 learner-facing 頁面的版本頁尾；保留既有 Gmail OAuth 選修文案。

## 驗證證據

- 回歸測試先以原始 wizard 執行為 RED，再以修正版執行為 GREEN：`python3 n8n/_repair/2026-09-15-starter-compose-patch/tests/test_compose_patch.py` → `PASS`。
- Mac 腳本語法檢查：`bash -n .../setup-wizard.command` → 通過。
- Lite Pack zip：`unzip -t` → `No errors detected in compressed data`；`setup-wizard.command` 保留 `0755`。
- 下載包 SHA-256：`7ff7c4960489e47d6b398fdbfd3f8e0969c4d0c25635886964f4a737a13a8bde`。
- 14 個 workflow 與 Starter Kit archive 契約檢查通過；檢查器另外報告本機 Downloads 的舊 `09-gmail-categorize.json` 與下載包不一致，這是本機殘留檔案 drift，未納入本次修復。

## 尚待人工驗收

此主機沒有 PowerShell，因此 Windows wizard 尚未做實機執行；需在 Windows 下載新包後，確認含註解／空白行的 `n8n-compose.yml` 能完成 patch、重啟並匯入 14 個 workflow。
