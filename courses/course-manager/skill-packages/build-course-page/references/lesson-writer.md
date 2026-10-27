# 講義製作者共用指示

將正式教案轉為學員 HTML；不發明上游缺漏。必要輸入為教案路徑，Style Guide 可由 frontmatter 取得，輸出沿用本課命名與導覽。

1. 讀 `$SKILLS_ROOT/build-course-page/SKILL.md` 的頁面類型 D，從 anchor:step-d0.5 依序執行至 step-d5；未設定 `SKILLS_ROOT` 時停止，相對路徑依該 skill 的 `COURSE_WEB_ROOT`。
2. 確認正式正文範圍、本版本 content 審查及核心素材。缺件交還指定製作者，不能用摘要或標籤補洞。
3. 依模板及 design-tokens 保留教學原文中的完整表格、推理、輸入、完成例子與互動。教師筆記不進學員頁。
4. 跑逐頁 lint 與素材檢查，交 reviewer 做正文到 HTML 的 fidelity 審查；未做不勾成通過。
5. 批次只由指定整合者重建搜尋索引與 sitemap；隔離試作不改正式索引。只回報本頁建置、已驗證項目及待驗證部分。

角色可由主執行者依序承擔。代理派遣與模型切換遵循當次授權，不能再派遣。若既有 batch-progress 協議啟用，按已提供 job_id/task_id 記錄，不自行宣稱教學放行。
