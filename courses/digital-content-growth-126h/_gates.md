# _gates.md — digital-content-growth-126h 品質檢核存證

> 一門課一份、append-only。此紀錄只保存已確認的設計決策與實際檢核結果。正式資產尚未建立時維持 BLOCK 或 Soft-fail，不以文字敘述代替試跑證據。

**課程 slug**：digital-content-growth-126h  
**負責人**：白辰幃／課程製作協作  
**建立**：2026-09-16

---

## G1 大綱定位（PM → 設計師放行）

**日期**：2026-09-16  
**來源**：使用者在本課程設計對話中確認；細節以 `_outlines/digital-content-growth-126h.md` 為準。

- Q1：受眾是誰、他們此刻的痛點？
  A：20–35 歲無職、計畫轉職，或想把專長轉成可展示工作成果的人。主要痛點是有零散專長與想法，卻缺少能說明問題、成果、證據與工作流程的作品；同時擔心工具訂閱、廣告預算與技術門檻。

- Q2：完課後學員能做出什麼？
  A：能建立服務／品牌 Brief；完成影像與平面內容、社群經營方案、SEO／追蹤判讀、國際廣告模擬與整合企劃；每一項成果都附可說明的判斷、來源與驗收證據。

- Q3：若只教 1 件事，是哪件？
  A：把問題、受眾、內容、渠道、證據與行動連成可重做的工作成果。創業、求職、企業專案與自由工作都是應用情境，課程保留學員選擇，不把單一出口列為必達。

- Q4：Brand Brief 四點（色系、語氣、對比、禁忌）？
  A：以可行、清楚、可帶走為核心調性；語氣直接、技術友善；差異在於把數位行銷技能放進多元工作情境並留下能力證據；避免產業黑話、空泛承諾、工具功能堆疊與「不是 X，而是 Y」式慣用對比句。

**結論**：☑ 放行（大綱狀態：`approved-for-production`）

---

## G2 教案審核

### G2-part1

**日期**：2026-09-16  
**結果**：Soft-fail（教案內容已存在；正式工作表、案例卡與完整參考完成品仍待建立）

- ☑ `CH1-1.md`、`CH1-2.md`、`CH1-3.md`、`PRAC1.md` 存在。
- ☑ 9 frontmatter 欄位齊全。
- ☑ 教學流程、講師筆記、試跑包、案例、動手題、常見錯誤與檢核題齊全。
- ☑ 前段 4 小時與大綱一致。
- △ 正式學員資產仍標記 BLOCK，未宣稱可直接試教。

### G2-part2

**日期**：2026-09-16  
**結果**：Soft-fail（內容教案完成；正式試跑包與 Windows 工具前測尚未完成）

- ☑ `CH2-1.md` 至 `CH2-7.md`、`PRAC2.md` 存在。
- ☑ 9 frontmatter 欄位齊全。
- ☑ 每份含 skill-operation 流程、操作示範、10–12 步操作、檢核點、恢復路徑與變體／版本判斷。
- ☑ Part 2 交付鏈與大綱依賴一致，總時數為 30 小時。
- ☑ 每份含 AI 使用時機、限制與紀錄要求；未使用 AI 仍可完成核心成果。
- ☑ 已完成用詞風險掃描與修正，未發現本課規則列出的不良修辭。
- △ Affinity／OpenShot 安裝與版本、starter file、示範素材、授權範例、輸出檢核與參考完成品尚未全部建立，維持 BLOCK。

### G2-part3 / G2-part4 / G2-part5 / G2-part6

G2-part3 已開始但尚未放行：

- ☑ `CH3-1.md`、`CH3-2.md` 已建立，依賴 PRAC2 與 PRAC1 的上游成果。
- ☑ 兩份教案均含平台角色／內容支柱的實作成果、接手驗證、AI 使用限制與恢復路徑。
- △ Part 3 的 `CH3-3` 至 `CH3-7`、`PRAC3` 尚未完成，因此本 Part 不標記完整 Pass。
- △ 平台角色卡、社群格式卡、LINE 延伸情境卡與參考完成品尚未建立，維持 Soft-fail／BLOCK。

G2-part4、G2-part5、G2-part6 尚未開始。依賴鏈要求先完成上游 Part 的交付成果，再生產下一 Part 教案。

---

## G3 講義驗收

**日期**：2026-09-16
**結果**：Soft-fail／BLOCK（HTML 與本機 fallback 已完成；尚待人工學員試跑與正式外部資產驗證）

- ☑ 40 份單元 HTML、6 份 Part 導覽頁、1 份課程入口，共 47 份 HTML。
- ☑ 課程範圍 47/47 通過 `lint-page.py`，沒有課程內 blocker 或 warning。
- ☑ 相對連結檢查：0 failures；`#`、`{PREV_FILE}`、`{NEXT_FILE}` 與 `{{...}}` 佔位連結：0。
- ☑ 40/40 單元均有對應 `assets/templates/<unit-id>.md` 連結。
- ☑ Part 3 原先缺少的完成驗證、案例、動手練習、常見錯誤與檢核題已補回；40/40 continuity heuristic 無警告。
- ☑ 已建立 `MANUAL-LEARNER-RUN.md`，提供從入口開始的人工 cold follow-along 記錄欄位。
- △ `audit-course-substance.py` 在本專案不存在，未以不存在的腳本宣稱 substance pass。
- △ LocalWP、GTM、GA4 Demo、Search Console、Google／Meta／LINE 權限、正式示範畫面與完整參考完成品仍維持 BLOCK。

**放行條件**：人工學員不依賴講師口頭補充即可開啟模板、產出成果、完成檢核並找到恢復路徑；正式平台段落仍需課前取得並填入 `assets/environment/permission-checklist.md`。

---

## G4 收尾

**日期**：2026-09-16
**結果**：Soft-fail／等待人工試跑

- ☑ `search-index.json` 已重建（719 筆）。
- ☑ `sitemap.xml` 已重建（94 個 URL）。
- ☑ 人工學員試跑清單已建立。
- △ 全域 `build-all.py` 仍被其他既有課程的 3 個舊 blocker 擋住；本課程已用 scoped lint、連結與 continuity 檢查獨立驗證。
- ☐ 尚未執行正式課程註冊、密碼關卡與人工學員實跑；完成後再更新本 Gate。

---

## 備忘

- 2026-09-16：Part 2 先完成教案，正式工具與素材資產刻意保留 BLOCK；這是可驗證性要求，不是內容完成宣告。
- 2026-09-16：CH3-1 需等待 PRAC2，已於本輪具備；CH4-1／CH5-1 需等待 CH3-2，已於本輪具備；CH6-1 需等待 PRAC3、PRAC4、PRAC5。後續生產依大綱依賴鏈推進。

---

## 2026-09-16 追加稽核：126 小時教案內容完成

檢查範圍：../_lessons/digital-content-growth-126h/*.md
檢查結果：

- ☑ 40 份教案檔案。
- ☑ frontmatter 9 欄位全部存在。
- ☑ 每份均有 Teaching Flow、講師筆記、Verification Asset Spec、Case、Hands-on Exercise、Common Pitfalls、Quiz。
- ☑ duration 加總為 126 小時。
- ☑ unit_id 覆蓋 CH1-1～CH6-3 與 PRAC1～PRAC6，依賴鏈已按大綱完成。
- ☑ 課程規則列出的 LLM 慣用不良修辭掃描無命中。

### G2-part3

內容狀態：完成。CH3-1 至 CH3-7、PRAC3 均已建立並納入 30 小時鏈。
Gate 狀態：Soft-fail／BLOCK。平台示範畫面、社群格式卡、LINE 延伸情境卡、參考完成品與正式權限仍待建立及試跑。

### G2-part4

內容狀態：完成。CH4-1 至 CH4-7、PRAC4 均已建立並納入 24 小時鏈。
Gate 狀態：Soft-fail／BLOCK。LocalWP 站點、GA4 Demo Account、GTM 測試容器、Search Console 去識別資料包、模板與參考完成品仍待建立及試跑。

### G2-part5

內容狀態：完成。CH5-1 至 CH5-7、PRAC5 均已建立並納入 30 小時鏈。
Gate 狀態：Soft-fail／BLOCK。Google／Meta／LINE 示範資產、模擬流量與投放結果、預算試算表、權限界線與參考完成品仍待建立及試跑。

### G2-part6

內容狀態：完成。CH6-1 至 CH6-3、PRAC6 均已建立並納入 8 小時鏈。
Gate 狀態：Soft-fail／BLOCK。提案模板、成果資料夾規範、同伴評分表、計時器試跑與參考完成品仍待建立及試跑。

G2 總結：教案內容與 126 小時結構完成；正式資產與 learner follow-along 尚未完成，因此 G2 維持 Soft-fail，不宣稱完整 Pass。
