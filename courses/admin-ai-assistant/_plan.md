# 行政 AI 虛擬助理實戰（admin-ai-assistant）製作 Plan

> **For agentic workers:** REQUIRED SUB-SKILL：本 plan 是課程製作 pipeline（`course-run` skill）的 Gate checklist，非程式 TDD plan。依 Gate 順序執行，每個 Gate 完成後在 `courses/admin-ai-assistant/_gates.md` 記錄放行結果，才能勾選對應項目。

**Goal:** 把來源文件《行政AI虛擬助理_2小時課程介紹.docx》轉為可上線的 2 小時課程網頁（slug: `admin-ai-assistant`）。

**Architecture:** 扁平 CH 結構（無 module），index + CH1~CH6 共 7 頁，參考 office-ai-cases（案例式、無行銷、不繳交）與 gemini-notebooklm-workshop（雙工具寫法基調）定位，但內容獨立撰寫、不引用其他課程頁面。主題色灰藍綠 `#7a9ea3`。

**Tech Stack:** 純 HTML/CSS/JS，`_規範/lesson-template-v3.html` 骨架，`docs/lint-page.py` 驗收。

---

## Gate 0：來源與規格（已完成）

- [x] 讀取來源 docx 全文
- [x] 使用者確認：slug=admin-ai-assistant、主題色=#7a9ea3、機構=公開通用版、CH6=獨立精簡改寫

## Gate 1：大綱（course-pm）✅ 已放行 2026-07-08

**產出：** `_outlines/admin-ai-assistant.md`

- [x] 呼叫 `course-pm` 產出大綱（受眾、學習成果、單元矩陣、前置知識鏈、試跑包規格）
- [x] 使用者答完 G1 Q1-Q4（受眾、產出、砍什麼、Brand Brief）
- [x] 問答寫入 `courses/admin-ai-assistant/_gates.md`
- [x] 依 Q1/Q3 回饋補「教學設計風險與對策」段落（CH2 時間風險 + 裸問 vs 結構化提示詞對照設計原則）

## Gate 2：教案（course-designer）✅ 已放行 2026-07-08

**產出：** `_lessons/admin-ai-assistant/*.md`（CH1~CH6 共 6 份）

- [x] CH1｜從 AI 工具到行政虛擬助理方案
- [x] CH2｜用 Gemini 處理會議紀錄（並行 agent 產出）
- [x] CH3｜Email、公文與行政通知撰寫（並行 agent 產出）
- [x] CH4｜資料彙整與主管摘要（並行 agent 產出）
- [x] CH5｜簡報製作：產出乾淨內容包（並行 agent 產出）
- [x] CH6｜完整方案：NotebookLM×Gemini 串聯助理（獨立改寫版，並行 agent 產出）
- [x] 每份教案 9 frontmatter + 6 區塊齊全，grep 抽驗禁用詞/主角/依賴鏈過

## Gate 3：講義 HTML（course-lesson-writer + course-web-builder）✅ 已放行 2026-07-08

**產出：** `courses/admin-ai-assistant/index.html` + `CH1.html`~`CH6.html`

- [x] index.html（course-web-builder，Editorial-strict 家族）
- [x] CH1.html ~ CH6.html（course-lesson-writer ×6，並行派遣）
- [x] `python3 docs/lint-page.py courses/admin-ai-assistant/` → 0 BLOCKER / 0 ERROR / 2 WARN（皆既有允許例外）
- [x] G3 人眼清單過（連結、導覽、色彩配額、禁用組件、AI 味偵測）

## Gate 4：收尾（course-ops + course-register）✅ 已完成 2026-07-08

- [x] 補件：`prompt-library.html`（Gem 系統提示詞 + NotebookLM 素材 + 檢核清單 + 流程卡），index.html 已加連結
- [x] `python3 docs/lint-page.py courses/admin-ai-assistant/` → 8 頁 0 BLOCKER / 0 ERROR / 2 WARN（既有允許例外）
- [x] `python3 docs/build-search-index.py` + `python3 docs/build-sitemap.py`（645 筆 / 51 URL）
- [x] `python3 docs/check-integrity.py` admin-ai-assistant 相關 0 ERROR
- [x] `/course-register admin-ai-assistant` 完成（2026-07-08）：密碼（見本地密碼對照表，不進 repo）/ key adminai_auth / 8 頁 gate 注入 / COURSES.md + 入口頁卡片 + COURSE_LABEL 登錄 / build-all 全綠

---

## 執行紀錄

| 日期 | Gate | 動作 |
|------|------|------|
| 2026-07-08 | Gate 0 | 讀 docx、AskUserQuestion 定案規格 |
