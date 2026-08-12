# Vercel／Render 部署角色一致化 Repair Report

## 結論

`gen-ai-140h` 的部署教學已統一為三條路徑：

- 純靜態且沒有私密 API key：GitHub Pages。
- 個人作品集、課堂練習、非商業 Demo：Vercel Hobby，並明示不可用於公司、客戶、受薪或收費情境。
- Node.js／Express 後端、公司／客戶原型或可能商用：Render 為本課主路徑；正式 production SLA 需另評估付費方案。

Railway 已退出免費主路徑，學員不再被引導建立 Railway 專案、產生 Railway 網域或把它當成可長期免費方案。

## 修正範圍

- 核心操作：CH5-4、PRAC5-4 改為可從零跟做的 Render Web Service 流程。
- 平台判斷：CH4-3、PRAC5-2 與跨頁導覽補上 GitHub Pages／Vercel Hobby／Render 的用途邊界。
- 專題與職涯：Part 6、Part 7 的公司、團隊與商業案例不再推薦 Vercel Hobby。
- 規格同步：`_outlines/gen-ai-140h.md` 加入 Render，並同步 PRAC5-2、PRAC5-4、PRAC5-17 名稱與定位。
- 回復能力：20 個來源檔已備份，restore script 有 20 條明確映射。

`fun-apps.html` 經檢查只含第三方工具網址與技術標籤，沒有部署建議，因此保留原文，避免無關改動。

## 教學驗收

- CH5-4 與 PRAC5-4 包含 `New + → Web Service`、Build Command、Start Command、Environment、Logs、`.onrender.com` 與常見錯誤排查。
- Render Free 限制在第一次操作前說明：閒置 15 分鐘休眠、冷啟動約一分鐘、未綁付款方式超額會暫停，以及不適合正式 production SLA。
- Vercel 實作頁與作品案例均標示 Hobby 的個人、非商業邊界；公司／客戶案例改走 Render 或 Vercel Pro。
- Shared Copy Audit：導覽、預期輸出、案例素材、作業、測驗與職涯工具棧已同步，不只修改標題。
- Activity Identity 未改：本次只更換部署平台角色與操作介面，不改學習產物、學員決策或原有活動流程。

## 驗證證據

- `python3 docs/lint-page.py courses/gen-ai-140h/ --summary`
  - 掃描 78 頁
  - BLOCKER 0
  - ERROR 0
  - WARN 233（既有設計系統／metadata 類警告，本次不擴張範圍修正）
- Railway 舊操作錨點：0 命中。
- `bash -n courses/gen-ai-140h/_tools/restore-2026-08-12-pre-vercel-render.sh`：通過。
- restore 映射：20；備份檔：20。
- `git diff --check`：通過。
- `docs/build-search-index.py`：成功產生 648 筆。
- `docs/build-sitemap.py`：成功產生 648 筆 URL。

搜尋索引與 sitemap 的重建結果包含工作區其他課程的既有變化，為維持本次 scoped staging 邊界，未納入本次修正提交。

## 提交紀錄

- `0261997`：備份、scan 與 restore gate。
- `19b39b5`：後端部署主線改為 Render。
- `3982e53`：Vercel 限定為個人作品展示補充方案。
- `1c6e7da`：Part 6／7 專題與職涯部署建議一致化。

