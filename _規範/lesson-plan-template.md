---
slug: {slug}
unit_id: {CH1-1 / PRAC1 / pilot-a / ...}
title: {單元標題}
course_type: {skill-operation|concept|programming}
duration: {Xh 或 X min}
learning_objective: {1 行，動詞開頭，可驗證}
prerequisites: [{CH1-1}, {CH1-2}, ...]
style_guide: {Style Guide 檔案相對路徑}
platform_version: {繼承自大綱}
---

<!--
教案標準模板（course-designer 產出使用）
_規範/lesson-plan-template.md

更新日期：2026-04-19（從 course-designer/SKILL.md 抽出）

產出規則：
  1. 複製本檔 → 存至 _lessons/{slug}/{unit-id}.md
  2. 替換 frontmatter 全部欄位（9 keys 皆必填）
  3. 依 course_type 選填第 3/4/5 段
  4. 長度目標 300–600 行
-->

## 教學流程（Teaching Flow）

### 破題 / Hook

{1–2 段。用 Style Guide 主角的具體情境開場。不要「今天我們要學 X」——直接帶入「阿凱遇到 Y 問題...」}

### 概念 / Concepts

{每條關鍵概念用「名詞 — 一句話定義」格式列出。3–5 條為宜。}

- **{概念 A}** — {一句話定義}
- **{概念 B}** — {一句話定義}

### {第 3 段：依 course_type 選}

- skill-operation：**操作示範 / Demo**
- concept：**案例 / Case Study**
- programming：**設計 / Design**

{具體內容...}

### {第 4 段：依 course_type 選}

- skill-operation：**動手 / Hands-on**
- concept：**反思 / Reflection**
- programming：**實作 / Implementation**

{具體內容...}

### {第 5 段，僅 skill-operation 有}

**檢核 / Verification**

{學員如何自行驗證學會了。具體動作+可觀察成果。}

### {programming 專屬：驗證 / Testing}

{測試案例、預期輸入輸出。}

---

## 試跑包需求清單（Verification Asset Spec）

**課程類型**：{course_type}

{依類型填寫具體清單——這是使用者後續要產出/蒐集的}

### skill-operation 範本

- Credential 所需：
  - Gmail（OAuth）
  - Notion API token
- Node 組成：
  - Gmail Trigger → Filter → Notion Page Create
- 關鍵設定欄位：
  - Gmail Trigger: `labelIds`, `q`
  - Notion: `database_id`, `properties mapping`

### concept 範本

- 概念測驗題：5 題選擇題
- 分類練習：10 個真實案例（含預期分類答案）
- 常見誤判樣本：3 個

### programming 範本

- `requirements.txt`：`gspread==6.0`、`google-auth==2.29`
- 認證檔：`service-account.json`（範本與填寫說明）
- 範例資料：Google Sheet 連結 + 預期輸出

---

## 商業情境案例（Case）

**角色**：{阿凱 / 雯姊 / 老闆，選最適合的}
**公司**：弄一下行銷工作室
**任務**：{1 句話，具體到「X 做 Y 以達到 Z」}
**本單元要他學會**：{呼應 learning_objective}

---

## 動手練習題（Hands-on Exercise）

**題目**：{1–2 段，延續上面案例}

**預期成果**：{學員做完應該產出什麼——可檢查的具體物件}

**完成標準**（self-check）：
- [ ] {條件 1}
- [ ] {條件 2}
- [ ] {條件 3}

---

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：{具體樣貌，含錯誤訊息或畫面描述}
   **原因**：{為什麼會發生}
   **解法**：{怎麼修}

2. ...

3. ...

---

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：{問題}
- [ ] A
- [ ] B
- [ ] C ←（正確答案）
- [ ] D

**Q2（應用驗證）**：{情境題，問學員如何處理}
- 預期答案要點：{2–3 個關鍵點}
