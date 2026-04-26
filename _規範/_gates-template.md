# _gates.md — {slug} 品質檢核存證

> **一門課一份、append-only。** 每個 G 檢核點結束時把問答記在下面。
> 禁止刪除舊條目，要改就另開新條目並註明「修正前述 X」。
>
> 用途：留下**決策軌跡**（為什麼某 Part 設計這樣？為什麼 Hard-fail 退回？），
> 未來做 refresh / 仿課 / 檢討時有完整脈絡。

**課程 slug**：{slug}
**負責人**：{name}
**建立**：{YYYY-MM-DD}

---

## G1 大綱定位（PM → 設計師放行）

**日期**：
**問答**：

- Q1：受眾是誰、他們此刻的痛點？
  A：

- Q2：完課後學員能做出什麼（3–5 條）？
  A：

- Q3：若只教 1 件事，是哪件？為什麼其他砍掉？
  A：

- Q4：Brand Brief 四點（色系、語氣、對比、禁忌）？
  A：

**結論**：□ 放行 / □ 退回（附原因與修改項）

---

## G2 教案審核（每 Part 一次，共 4 次）

### G2-part1（Part 1 教案 3–5 單元）

**日期**：
**審核項**：

- □ 每單元 9 frontmatter 完整
- □ 6 正文區塊齊
- □ 試跑包規格符合 course_type
- □ 商業情境案例具體、可驗證
- □ 常見錯誤 3 條真實（非湊數）
- □ 檢核題 2 條有標準答案

**Hard-fail 項**：（若退回設計師重跑，列在這）

**放行決定**：□ Pass / □ Soft-fail（條件：）/ □ Hard-fail（回 designer）

### G2-part2 / G2-part3 / G2-part4
（同 part1 格式，按 Part 複製。）

---

## G3 講義驗收（每 Part 結束後一次）

用 `_規範/G3-人眼驗收清單.md` 逐條打勾，把結果記下：

### G3-part1

**日期**：
**排版視覺**：Pass / Soft-fail / Hard-fail（原因：）
**敘事連貫**：Pass / Soft-fail / Hard-fail（原因：）
**AI 味偵測**：Pass / Soft-fail / Hard-fail（原因：）
**試跑包驗證**：Pass / Soft-fail / Hard-fail（原因：）
**SEO / 連結 / 行為**：Pass / Soft-fail / Hard-fail（原因：）

**飛輪**：本 Part 發現新模式、要不要轉 lint 規則？
- [ ] 寫進 `docs/lint-page.py`：（規則描述）
- [ ] 留在人眼清單第三層：（原因）

### G3-part2 / G3-part3 / G3-part4
（同上格式。）

---

## G4 收尾（課程整體上線前）

**日期**：
**項目**：

- □ 全站 `python3 docs/lint-page.py --baseline` 無 new BLOCKER
- □ `python3 docs/check-integrity.py` 無 ERROR
- □ `python3 docs/build-all.py` 全綠
- □ inject_gate.py 已登錄、密碼發給學員
- □ COURSES.md 已加入本課表列
- □ _outlines/{slug}.md 仍與最終章節對齊

**檢討**：
- 本課哪一步最耗時？
- 下一課想改什麼流程？

---

## 備忘（非 Gate 但值得留存）

（重大決策、學員反饋、平台變動等，隨時追加）
