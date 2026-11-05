# M2 生成式 AI 模組｜PM 檢查紀錄

日期：2026-11-05。素材：`素材規格-M2.md` → GPT-5.6 Sol 一次完成（commit `b30726e3`）。頁面：`派工單-M2.md`，批次 A（m2a、m2b）與批次 B（m2c、m2d）並行承作，承作每頁自跑檢查腳本。依 SOP，批量頁不跑試讀。

## 素材核對
- 練習資料不附答案（`ai-practice.md` Part A～E、`social-practice.md`、`competitor-posts-practice-b.csv`）。
- `social-practice.md` 的篇數占比與互動占比排序不同、有一類只有 1 則，符合設計卡。
- PM 直修：`social-practice.md` 小標題 `SOCIAL-PRACTICE-01` 代號改成內容名稱。

## 頁面檢查
- 腳本 12 頁通過。批次 A 字數貼近下限（2,303～2,580），PM 讀 m2a-1 全文：概念、例子、練習完整，沒有灌水。
- PM 讀 12 頁每節第一段：都先說要解決的問題或先給定義，沒有「沒引入就講步驟」。
- 需實跑的示範（m2c-2 候選圖、m2d-1 深度研究）都標「示意」，沒有編造外部數字或網址。
- PM 直修 m2d-3 模組作業：改成五段格式（個人準備、小組討論、上台分享、回饋、放進企劃書）；回饋補「請 AI 依判準給建議」的路與提示詞。

## 同步
- 改名同步：`lesson-meta.json`（標題、短名、完成物）、`module2.html`、`_outlines/digital-marketing-70h.md`、`prompts-all.md`；m2b-1 標題「指令五要素」改「提示詞五要素」，相鄰頁導覽一併更新。
- lint：全課 76 頁無 BLOCKER／ERROR。

## 未完成
- m2c-2、m2d-1 示範等使用者交回實跑結果（`實跑清單.md`）。
