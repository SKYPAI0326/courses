# career-guidance 建課 Pipeline 計畫（_plan.md）

> course-run 救生索。每完成一項打勾。狀態強制檢核以 `_gates.md` 為準，本檔為自述進度。
> 內容依據：`courses/career-guidance/_local/proposal.md`（定稿，5 項決策已鎖定）。

## 課程定錨（來自 proposal 裁決紀錄）

- slug：`career-guidance`
- 課名：留任、內轉、轉職：8 小時職涯定位實戰
- fork 來源：`career-pivot-mid`（原課保留不動）
- 受眾 persona：工作 3-10 年、非新人未成核心、對現職失成長感、猶豫深耕/內轉/轉職
- 時數：8h 一日（上午 判斷方向 255 分 / 下午 驗證下一步 225 分）
- 主題色：`#8a7a9e` 霧紫
- 核心心法：通用版為主（方向越清楚越好、年資是經歷不是答案、適性是線索不是命運）+ 資深 callout
- Part 1：適性+趨勢+引導（CH1-1~1-6，CH1-5 需重寫為通用就業趨勢）
- Part 2：抽象為 4 工具 × 三 lane（深耕/內轉/轉職）共用
  - 能力證據包（←履歷 STAR）
  - 關鍵對話腳本（←面試 5 題+模擬，三版本：績效面談/內部訪談/外部面試）
  - 條件談判（←薪資談判，含現職議價）
  - 30 天行動實驗（←入職計畫+過渡策略，定位為低風險驗證）

## Gate 進度

### G1 大綱（/course-pm）✅ PASS 2026-05-31
- [x] 產出 `_outlines/career-guidance.md`（frontmatter 9 欄 + 受眾 + outcomes + 單元矩陣 + 依賴鏈 + 試跑包規格 + 風險表）
- [x] outcomes 改寫為對探索型可驗證的產物（方向地圖 + 適性結論 + 30 天行動實驗計畫）；#3 依 Q3 精修為三條篩選
- [x] 單元矩陣反映上午判斷方向 / 下午四工具×三 lane
- [x] 答完 G1 Q1-Q4 寫入 `_gates.md`（Q1=CH1-5最沒把握 / Q2=受眾符合 / Q3=#3精修 / Q4=探索vs衝刺）

### G2-part1 教案（/course-designer ×7）✅ PASS 2026-05-31
- [x] 前置：_outlines/career-guidance.style-guide.md（fork 改寫）
- [x] CH1-1 開場+現況診斷  [x] CH1-2 雙測適性  [x] CH1-3 價值觀+Ikigai
- [x] CH1-4 可遷移技能  [x] CH1-5 就業趨勢（實查 4 來源）  [x] CH1-6 三路徑決策
- [x] PRAC1 職涯方向地圖
- [x] 每單元 9 frontmatter + concept 4 段齊
- [x] 跨單元數據對齊（CH1-1/CH1-6 ← CH1-5）；大綱 PRAC1 typo 修正
- [ ] Soft-fail 待講師驗證：CH1-5 推估項（×14換算/50-64薪資/5職位分類框架）

### G3 講義（course-lesson-writer ×12）✅ PASS 2026-05-31
- [x] CH1-1~1-6 + PRAC1 HTML（Part 1）
- [x] CH2-1~2-4 + PRAC2 HTML（Part 2）
- [x] lint 全 0 BLOCKER / 0 ERROR（17 WARN 為 .78rem serif 例外等 migration-debt）

### 補充頁 ✅ 2026-05-31
- [x] index.html（總覽，霧紫，決策痛點招生文案，lint 0）
- [x] module1.html / module2.html（含三 lane 說明卡，lint 0 BLOCKER）
- [x] personality-test.html（複製姊妹課 + 去轉職特化，PDP30+MBTI16 計分完整，lint 全綠）

### G2-part2 教案（下午四工具）✅ PASS 2026-05-31
- [x] CH2-1 能力證據包  [x] CH2-2 關鍵對話腳本  [x] CH2-3 條件談判  [x] CH2-4 30 天行動實驗
- [x] PRAC2 行動工具產出
- [x] 每工具備齊三 lane（深耕/內轉/轉職）範例，留任 lane 獨立有料

### G3-part2 講義
- [ ] 下午單元 HTML  [ ] lint 0 BLOCKER

### 補充頁
- [ ] index.html（總覽，霧紫，決策痛點招生文案）
- [ ] module1.html / module2.html 導覽
- [ ] personality-test.html（雙測獨立頁，去轉職特化判讀）

### G4 收尾（/course-ops + /course-register）✅ 2026-05-31
- [x] lint --all 0 new BLOCKER  [x] check-integrity（本課乾淨，2 ERROR 屬他課）  [x] build-all 全綠
- [x] /course-register career-guidance（密碼 careerguidance2026 + 登錄 + COURSES.md + 入口卡片 + 16 頁注入）

## 資產複用決策（proposal §6 風險）
- [ ] 決定：雙測 JS 腳本 / .handout-card / personality-test 是複製獨立維護或共用一份（建議複製獨立，去轉職特化）

## 當前狀態
**G1→G4 全 PASS + 已部署（2026-05-31，commit 9ecad35，push origin/main）**。16 HTML + 12 教案 + 大綱 + style-guide，密碼 careerguidance2026 註冊注入，GH Pages 上線。
**唯一待辦**：講師備課驗證 CH1-5 Soft-fail 推估項（×14換算/50-64薪資/AI職位5分類框架）。
