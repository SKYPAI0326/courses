# _gates.md — ict-ai-digital-workflow 品質檢核存證

> 一門課一份、append-only。後續修訂新增條目，不覆蓋既有決策。

**課程 slug**：ict-ai-digital-workflow
**負責人**：弄一下工作室
**建立**：2026-08-04

---

## G1 大綱定位（PM → 設計師放行）

**日期**：2026-08-04

- Q1：主要風險？
  A：使用者指出付費工具門檻；全課改為免費帳號基準，付費功能不得成為完成條件。
- Q2：受眾是否正確？
  A：使用者確認一般職場工作者、具基本電腦操作能力的設定正確。
- Q3：哪項成果需要具體化？
  A：使用者指定學習成果 1；已改為可實作、可檢查的 6 列數位任務拆解表。
- Q4：Brand Brief？
  A：使用者確認「務實、可信賴、有秩序」符合定位。

**結論**：Pass。

---

## G2 教案審核（五章整批）

**日期**：2026-08-04
**授權狀態**：使用者指示「先全部執行」，授權連續製作；以下是依現有教案證據完成的內部審查，不冒稱為使用者逐題回答。

- [x] 每單元 9 frontmatter 完整。
- [x] 每單元 7 個主要正文區塊齊全。
- [x] 每單元 7–9 個操作步驟與 2 個 Checkpoint。
- [x] 每單元試跑包規格符合 skill-operation。
- [x] 商業情境沿用阿凱與弄一下行銷工作室，任務可驗證。
- [x] 每單元 3 個具體常見錯誤與 2 題有答案的檢核題。
- [x] 五章時數合計 300 分鐘。
- [x] 免費工具、無帳號、固定輸出或離線備援均已寫入。

**風險排序（內部審查）**：CH5 40 分鐘端到端實作風險最高，其次 CH3 資料型態與公式、CH2 來源查證、CH4 權限驗證、CH1 任務拆解。

**Hard-fail 項**：無結構性 Hard-fail；CH5 必須用固定短素材包試跑，不能把下載、登入或等待算進 40 分鐘。

**放行決定**：Pass to G3，附條件為所有頁面與素材保留免費／離線備援。

---

## G3 HTML 與試跑包審查

**日期**：2026-08-04

- [x] 完成總覽頁與 CH1–CH5，共 6 頁。
- [x] 完成 23 份試跑素材；HTML 共 24 個素材連結均指向實際檔案。
- [x] 修正全課品牌主色為 `#6b7fa3`，並修正頂端品牌連結層級。
- [x] 手機 375px 與桌面版皆無水平溢位；頁面標題、步驟與下載入口可見。
- [x] 每章均保留學員動作、預期結果、Checkpoint、卡關修復與免費／離線備援。
- [x] `lint-page.py`：6 頁 BLOCKER 0、ERROR 0、WARN 0。
- [x] 本地連結檢查：missing local links 0。

**結論**：Pass to G4。

---

## G4 營運與全站建置檢查

**日期**：2026-08-04

- [x] 搜尋索引標籤已加入 `docs/build-search-index.py`。
- [x] `search-index.json` 已由官方腳本重建，共 676 筆。
- [x] `sitemap.xml` 已由官方腳本重建，共 69 筆 URL。
- [x] 全站完整性檢查已執行。
- [ ] `COURSES.md` 與 `inject_gate.py` 登錄：Deferred，依計畫不執行 course-register、密碼生成或公開部署。

**完整性檢查說明**：共 11 項 ERROR；本課占 2 項，均為尚未正式登錄；其餘 9 項為既有目錄／登錄差異，不屬本課修改範圍。

**結論**：教材建置 Pass；正式上線登錄 Deferred。

---

## G5 七層驗證

**日期**：2026-08-04
**Run ID**：`r-20260804-195648`

- [x] Preflight：OK（23 pass、1 warn；素材位於章節目錄而非 `datasets/`）。
- [x] L0：OK。CH3＝12 筆／40,000 元／3 筆待確認；CH5＝6 筆／19,600 元／1 筆待確認。
- [x] L1–L3：OK；6 頁 lint 全綠。本課提示詞置於章節素材，驗證腳本未偵測到 `prompts-*.md`，已另備 L4a prompt。
- [ ] L4a：DEGRADED_MANUAL。外部 Codex 審核未獲未公開課程內容的明確外傳授權。
- [ ] L4b：DEGRADED_MANUAL。同上。
- [ ] L5：DEGRADED_MANUAL。同上。
- [x] 已產生三份待審 prompt 與 `FINAL-REPORT-DRAFT.md`；Report Gate 正確拒絕產出 FINAL。

**結論**：G5 尚未放行；目前唯一剩餘條件為取得外部第二意見授權、完成 verdict 並重跑 report。不得標示為可交付 FINAL。

---

## G5 後續放行紀錄

**日期**：2026-08-04

- [x] 使用者已明確授權外部 Codex 審查。
- [x] L4a：7.8/10，Call ID `64c52a66`；由 6.5 經三輪修補後放行。
- [x] L4b：8.4/10，Call ID `39c09d12`；免費平台中立成立。
- [x] L5：7.7/10，Call ID `b2a3004e`；已補 START HERE 與欄位轉譯表。
- [x] 所有 Codex Call 已 mark verdict 為 actionable。
- [x] Report Gate：PASS；已產生 `FINAL-REPORT.md`。

**結論**：G5 Pass。教材可交付；正式註冊、密碼、Git 發布與公開部署仍為 Deferred。

---

## 正式課程註冊（公開例外）

**日期**：2026-08-04
**使用者授權**：本案為特殊公開課程，不需要密碼加密。

- [x] `COURSES.md` 已登錄為完成、已註冊、公開。
- [x] 全站 `index.html` 已加入「AI 入門與工作應用」課程卡片。
- [x] 大綱 metadata 已標記 `status: REGISTERED_PUBLIC`、`public: true`、`password_gate: false`。
- [x] `docs/check-integrity.py` 已將本課列入公開課程例外。
- [x] `inject_gate.py` 不新增本課、密碼對照表不新增條目、6 頁 HTML 不注入 `_gate`。

**結論**：正式註冊完成，採公開無密碼模式。

### 註冊後驗證

- [x] 根入口 `index.html`：BLOCKER 0、ERROR 0、WARN 0。
- [x] 本課 6 頁：BLOCKER 0、ERROR 0、WARN 0。
- [x] sitemap：6 個本課 URL。
- [x] search-index：已登錄 1 個課程 slug、全站共 676 筆。
- [x] 根入口卡片：1 張。
- [x] 本課密碼 gate：0 頁。
- [x] `build-all.py --skip-lint`：PASS。

**全站既有債**：完整 `build-all.py` 的 lint 階段被其他課程 `tmp/pdfs/` 內 19 個既有 `box-shadow` BLOCKER 擋住；`check-integrity.py` 另有 8 個既有暫存／未登錄目錄 ERROR。本課與公開例外均未出現在錯誤清單，未越權修正其他課程。
