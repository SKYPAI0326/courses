# Scan：gen-image 2026-10-16 趨勢與規範修正基線

## Scope

- 課程：`gen-image`
- 掃描日期：2026-10-16（Asia/Taipei）
- HTML：41 頁（`index.html`、6 個 module、13 個核心 CH／PRAC、21 個 CH6／附錄頁）
- 教案：`_lessons/gen-image/*.md` 共 13 份
- 上游：`_outlines/gen-image.md`、`_outlines/gen-image.style-guide.md`
- 視覺資產：`img/*.png` 共 62 張
- 本輪範圍：只盤點與規劃；未修改正式教案、HTML 或資產

## Machine Baseline

| 檢查 | 結果 | 判讀 |
|---|---:|---|
| `python3 docs/lint-page.py courses/gen-image --summary --v3-soft` | 41 頁；BLOCKER 0、ERROR 0、WARN 26 | 結構基線可用，不代表內容可發布 |
| `python3 docs/audit-course-substance.py gen-image` | 34 頁 MACHINE_CHECKED；semantic review PENDING；missing_assets 0 | 掃描器未辨識正文提到但不存在的 Markdown 教材，不能採其 missing_assets=0 作放行證據 |
| Footer metadata | 41/41 有 `data-platform-version` 與 `data-built-at` | 版本字串全面落後 |
| 製作日期 | 2026-04-24～2026-05-01，距掃描日 168～175 天 | 依 course-refresh 屬 REVIEW；已確認實質漂移者升為 REFRESH |
| `_sources/gen-image/` | 不存在 | 核心練習依賴缺檔，BLOCKER |
| 工作區 `git status --short -- .` | 無輸出 | 本課目錄掃描前無既有修改 |

## Reviewer Issues

| ID | 嚴重度 | 類別 | 主要位置 | 問題摘要 |
|---|---|---|---|---|
| B1 | BLOCKER | ASSET_DISCOVERABILITY | `PRAC2`、`CH2-1`、`CH2-2` 及多份教案 | `10-industries-brief-library.md`、`prompt-templates.md` 等必備教材不存在 |
| B2 | BLOCKER | VALIDATION | `CH1-1`、`CH3-1`、`CH4-1`、`CH4-3`、`PRAC4`、`CH5-1` | 生成模型自評被設為主要驗收，缺人類與可觀測工具證據 |
| B3 | BLOCKER | RIGHTS | `CH1-2`、`CH2-2`、`PRAC3`、`CH5-1`、outline／style guide | 「版權保險／乾淨／無負擔」及下載第三方廣告再上傳模型會誤導學員 |
| M1 | MAJOR | STALE_UI | 全課 metadata；`CH1-2`、`CH2-2`、PRAC | 模型名、方案、額度、價格與生成秒數停留在 2026-04 |
| M2 | MAJOR | CONTENT_THIN | `CH4-1`、`CH4-3`、`PRAC4`、`CH5-1` | 缺多 reference、角色分工、選區／局部編修與 reference fidelity 驗收 |
| M3 | MAJOR | RIGHTS／PRIVACY | `PRAC3`、`CH6-C4` | 缺肖像同意、未成年人、公共人物、深偽、資料控制與刪除路徑 |
| M4 | MAJOR | PROVENANCE | `module5`、`CH5-1`、交付流程 | 缺 C2PA／Content Credentials／SynthID、來源與人工修改紀錄 |
| M5 | MAJOR | LEARNER_PATH | `module5` 對照 `CH5-1` | module 承諾的商用五問沒有可執行表格、失敗案例或修復路徑 |
| M6 | MAJOR | ACCESSIBILITY | `CH6-B5`、`CH6-C1`～`C3`、`CH5-1` | 學員交付規格缺 alt、純文字稿、文字校稿、對比與純圖備援 |
| M7 | MAJOR | BIAS | `CH6-C4`、人物驗收流程 | 缺表示偏誤、文化刻板印象與成對提示測試 |
| m1 | MINOR | STALE_CLAIM | `CH6-1`、`CH6-supplement-typography` | 把三次 pilot 推論成中文字生成的固定限制 |
| m2 | MINOR | RIGHTS | `CH4-3`、`CH6-A2`、`CH6-B5` | 以 MUJI／Apple／Nike 等品牌名作風格捷徑，邊界說明不足 |
| m3 | MINOR | STALE_UI | `CH6-supplement-typography` | Adobe／字型服務價格與方案已漂移 |

## Root Cause and Responsibility

| 問題群 | 唯一責任層 | 原因 | 不採用的補法 |
|---|---|---|---|
| 缺教材資產 | 課程資產 + outline handoff | 上游已宣告必備，但從未交付實檔 | 不在 HTML 臨時補幾個片段冒充完整資料庫 |
| AI 自我驗收 | outline outcome + style guide + lessons | 課程核心框架把「AI 回答清單」誤當客觀證據 | 不只換掉一頁的「不用眼睛」句子 |
| 權利／商用說法 | outline + style guide + lessons | 上游規則本身含「版權保險」與第三方素材捷徑 | 不只在頁尾加免責聲明 |
| 平台漂移 | outline metadata + lessons + HTML | 方案名稱、價格、額度與秒數寫進長效正文 | 不只 bump `data-built-at` |
| reference-first 缺口 | lessons／活動設計 | 現有流程偏文字 DNA 與同對話延續，未形成可驗收的 reference workflow | 不新增孤立名詞卡片 |
| consent／provenance／a11y／bias | release gate + 受影響單元 | module 有承諾，正文無可執行 gate | 不把規範集中成學員看不到的教師備註 |

## Refresh Report

| 範圍 | 日期老化 | 實質漂移 | 建議 |
|---|---:|---|---|
| 13 個核心 CH／PRAC | 173～175 天 | 模型、方案、生成時間、工作流均有漂移 | REFRESH：先改教案，再同步 HTML |
| `index.html`、`module1`～`module5` | 175 天 | 導覽文字與承諾含舊平台及未實作商用 gate | REFRESH |
| `module6`、21 個 CH6／附錄 | 168 天 | 全面含舊模型 metadata；部分 JSON／價格／人物與品牌說法需改 | REVIEW 全頁；指定頁 REFRESH |

正式內容完成並重驗前，不得單獨更新 metadata 日期。

## Activity Identity Audit

| page | role | material | artifact | learner decision | repair effect | overlap verdict |
|---|---|---|---|---|---|---|
| `CH2-2` | Demo／Together | brief 六件套 + 版型資料 | 1 份 prompt + 1 張初稿 | 把需求轉為可執行欄位 | 連到真實下載資產；加入輸入權利 gate | 保留，首次完整方法 |
| `PRAC2` | Solo | 10 業種庫 + preset | 2 張不同風格作品 | 選業種、骨架與主要風格變因 | 使用完整實檔並加入人類 QA | 保留，條件與獨立性皆不同 |
| `CH3-1` | Demo／Together | 自產 L4 | L2 線稿 + 驗收記錄 | 判斷骨架是否可繼承 | AI 自檢降為線索；人類／工具證據主判 | 保留，新增結構抽取能力 |
| `PRAC3` | Solo | 授權 reference pack + 自產圖 | 5 張 L2 + 結構筆記 | 選擇合法輸入並處理失敗 | 移除 IG／Pinterest 下載上傳路徑 | 保留，來源與獨立性明確 |
| `CH4-1` | Demo／Together | 多張已授權 reference + L2 | 跨產業完稿 | 分配參考圖角色並保留／替換元素 | 補多 reference、選區與 fidelity | 保留，成為 reference-first 核心案例 |
| `CH4-3` | Demo／Together | brand DNA + reference | 系列稿 + 跨張檢核 | 判斷品牌一致性與可接受偏差 | 改為可觀測證據 + 第三方辨識 | 保留，系列責任不同 |
| `PRAC4` | Solo | 自家／假想品牌素材 | 3 張系列 + DNA | 獨立維持角色／商品／品牌一致性 | 加 rights／a11y／provenance 最小 gate | 保留，獨立遷移 |
| `CH5-1` | Capstone | 上游全部產物 | 可交付包 | 判斷是否可發布、商用或停止 | 實作 release gate 與修訂路徑 | 保留，整合與交付責任不可被前課取代 |

## Shared Copy Audit

| repeated copy | pages | allowed reason | action |
|---|---|---|---|
| 「卡關就換另一家」 | 多個核心單元 | 平台 fallback 必要 | 集中成 platform check card；各頁只留與本階段相符的觸發條件 |
| 「預期差異」 | 多個 CH／PRAC | AI 輸出變異屬必要提醒 | 保留，但改成該頁的可觀測完成標準，不用同一句複製 |
| AI 自檢 A／B／C | `CH1-1`、`CH3-1`、`CH4-1`、`CH4-3`、`PRAC4`、`CH5-1` | 跨課沿用同一檢查架構 | 改為「AI 提示 + 人類與工具證據」同一框架；各頁只新增該階段證據 |
| Canva／Firefly 商用提醒 | `CH1-2`、`CH2-2`、`CH5-1` | 商用風險提醒必要 | 由 release gate 定義；各頁連回對應關卡，移除保證語 |

## Current-Evidence Anchors

- OpenAI Images：<https://help.openai.com/en/articles/11084440-images-in-chatgpt>
- Google Gemini image generation：<https://ai.google.dev/gemini-api/docs/image-generation>
- C2PA 2.4：<https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html>
- 台灣智慧財產局 1150522：<https://www.tipo.gov.tw/tw/copyright/692-86904.html>
- Canva AI Product Terms：<https://www.canva.com/policies/ai-product-terms/>
- Adobe Firefly Product Description：<https://helpx.adobe.com/legal/product-descriptions/adobe-firefly.html>
- W3C Images Tutorial：<https://www.w3.org/WAI/tutorials/images/>
- NIST AI 600-1：<https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf>

## Scan Verdict

`BLOCK`。結構 lint 可通過，但核心教材缺檔、驗收方法與權利說法仍阻斷發布。修正必須走 source-first，且在正文完成後重新建立 evidence；現有 MACHINE_CHECKED 不得沿用為語意 PASS。
