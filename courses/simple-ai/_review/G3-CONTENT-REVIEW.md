# G3 Content Substance Review：simple-ai

**reviewed_at**：2026-08-25

**reviewed_by**：codex

**status**：BLOCKED

**three_minute_follow_test**：PENDING_USER
**release_verdict**：CONDITIONAL；完成使用者跟讀簽核前不得宣告上線完成

## 審核範圍

- `courses/simple-ai/index.html`
- `courses/simple-ai/module1.html`、`module2.html`
- `courses/simple-ai/CH1-1.html` 至 `CH2-4.html`
- `courses/simple-ai/prompt-library.html`
- `courses/simple-ai/handbook.html`、`quick-reference.html`
- `_outlines/simple-ai.md`、`_outlines/simple-ai.environment.md`

## Content Substance Verdict

| 檢核項 | 結果 | 證據 |
|---|---|---|
| 首次概念有白話定義、理由、正例／非例與判斷 | PASS（靜態檢查） | 八個 CH 頁的概念、情境與判斷區塊；`docs/audit-course-substance.py simple-ai` 未發現 DEMO_FIDELITY_LOSS |
| 核心操作有完整 worked example | PASS（靜態檢查） | CH1-1～CH2-4 含輸入、Prompt、預期輸出、檢查與卡關修復；下載素材位於 `courses/simple-ai/assets/` |
| 教案表格／Prompt／正反例保留資訊等價內容 | PASS（靜態檢查） | `docs/audit-course-substance.py simple-ai` 通過頁面內容對照；`docs/lint-page.py courses/simple-ai/` 無 BLOCKER／ERROR |
| Environment Contract | PASS（檔案存在） | `_outlines/simple-ai.environment.md`，含免費界線、登入起始狀態、文字備援與課前檢查 |
| Demo／Together／Solo 可跟做 | PENDING_USER | 需使用者依下面三分鐘跟讀流程實際完成一次，不能由 Codex 代簽 |
| 學員教材下載與圖片素材 | PASS（本機瀏覽器） | 首頁 PDF 下載可觸發；CH1-3 三張照片實際載入並可下載 |

## 使用者三分鐘跟讀簽核

請使用沒有既有課程狀態的瀏覽器視窗，依序完成：

1. 開啟 `index.html`，確認密碼關卡後可進入首頁，點「第一堂」進入 `module1.html`。
2. 開啟 `CH1-1.html`，用頁面提供的 EF-08 素材完成一次五零件 Prompt，確認結果含格式、限制與退路。
3. 開啟 `CH1-3.html`，使用報價單照片完成一次結構化欄位萃取，並確認模糊欄位標為「無法辨識」；再下載一張 JPG 備援素材。
4. 回到首頁下載完整版 PDF，確認瀏覽器能另開或下載，且 PDF 內的素材連結可開啟。

完成後，使用者需將本檔案的三個欄位改為通過值（以下僅為欄位格式，不是目前狀態）：

```text
reviewed_by: <user>
status: <PASS after actual test>
three_minute_follow_test: <PASS after actual test>
```

若任何一步卡住，請在本檔案下方追加現象、頁面、步驟與修復結果，不得直接改成 PASS。

## Online Black-box Verification

**verified_at**：2026-08-25

**deployed_commit**：`48ce176`

**technical_online_verdict**：PASS

- GitHub Pages 的 simple-ai 站內 HTML、環境契約、文字素材、照片與兩份 PDF 均回應 HTTP 200。
- 線上 CH1-3 的三張照片實際載入為 1600×1200；首頁完整版 PDF 下載按鈕可觸發下載。
- 線上手冊下載後為 65 頁，SHA-256 與本機產物一致；18 個 PDF URI 全為 HTTPS，無 `file://` 或舊版 `/courses/simple-ai/` 路徑。
- 環境契約線上回應 `text/markdown`；若瀏覽器阻擋直接預覽 `.md`，可用下載或另存方式取得，不影響檔案可達性。

## 已知尚未放行項目

1. GitHub Pages 目前仍是舊版；修正版 commit `4bc8f89` 尚未部署，因此新 PDF／照片／環境契約的線上 404 需在正式部署後重測。
2. `handbook.html` 與 `quick-reference.html` 是公開素材頁；GitHub Pages 靜態檔案無法阻止知道網址的人直接取得 PDF。若要求嚴格學員限定，需改用具存取控制的主機。
