# 課程設計系統可使用性驗證

**驗證日期**：2026-10-18

**驗證範圍**：新課程 G0–G6 母系統、16 個安裝套件、端到端示範課與獨立 AI 試走

**結論**：系統已達 `INDEPENDENT_AI_VERIFIED`，可用於受控的新課程產製。尚未進行真人學員試走，因此不宣稱 `HUMAN_READY`。本輪未發布、未部署、未改變外部存取權，也未 push。

## 設計要求與實證

| 要求 | 系統實作 | 驗證證據 | 結果 |
| --- | --- | --- | --- |
| 先確認學員、情境、成果與限制 | `course-run` 以適應式 G0 訪談建立單一課程契約；重要未知仍會阻擋 Gate | `skill-packages/course-run/SKILL.md`、`course-contract.json` | PASS |
| 研究必須貼近當前現實 | G1 負責外部來源、真實工作、工具與風險驗證，研究證據需可追溯 | `evidence/research-record.json`、G1 Gate event | PASS |
| 只提出一個有完整理由的主方案 | G2 產出一份藍圖，包含成果、評量、進程、單元依賴、時數與取捨 | `evidence/blueprint.json`、G2 Gate event | PASS |
| 課程正文必須能讀、能跟做 | G3 要求情境、完整說明、示範、引導練習、獨立操作、檢查與修復，不接受名詞或待辦清單代替正文 | `evidence/lesson-unit-1.json` 至 `lesson-unit-3.json`、學員頁 | PASS |
| 依主題自行決定呈現方式 | 版型依學員、任務、內容密度、裝置與教學風險決定，不以主題標籤套固定模板 | `build-course-page` 的 visual decision 與 `evidence/visual-decision.json` | PASS |
| 素材要找得到且可使用 | 每項必要素材都有入口、用途、雜湊與可用性證據；需帳號、付費或權利判斷時才詢問 | `evidence/asset-manifest.json`、首頁下載入口 | PASS |
| 代表單元先行 | G4 只完成一個代表單元；通過保真、結構、瀏覽器與獨立試走後才准許全課製作 | `evidence/pilot-record.json`、`trials/g4-representative-unit.json` | PASS |
| 由未參與製作的 AI 完整操作 | G4 與 G5 使用不同的全新隔離情境，只提供學員可見頁面與素材，記錄輸入、動作、阻礙、完成品與雜湊 | `g4-cold-ai-context-20261018-c`、`g5-cold-ai-context-20261018-d` | PASS |
| 全課要有實際交接與最終成果 | G5 核對每單元不同成果、頁面與素材、前後產物交接、導覽及最終驗收 | `evidence/production-record.json`、完整試走成品 | PASS |
| 對外動作必須再次授權 | G6 只能先建立精確 action manifest；發布、部署、註冊、權限與外部訊息皆須在執行前取得明確授權並重驗雜湊 | `evidence/release-proposal.json`、`evidence/release-record.json` 的 `published: false` | PASS |
| 新課與舊課修復分流 | `course-run` 只處理新課；`course-repair` 採可回復的既有課掃描、修復與驗證；維護掃描保持唯讀 | `course-run`、`course-repair`、`course-refresh` | PASS |
| 本機安裝可稽核與回復 | 16 個套件均可獨立驗證；安裝 manifest 記錄來源、目的、雜湊、備份與 rollback | 安裝作業 `20261018T065615.753017Z-7refb3_3` | PASS |

## 端到端證明

示範課「活動成效摘要」從 G0 需求契約一路走到 G6 發行準備，共三個單元。未參與製作的 AI 已從學員入口取得 CSV、範本與 rubric，重算三個活動的五項指標，完成判讀、資料界線與下一步，最後交付可核對的 Markdown 摘要。

- G0–G6 Gate：全部 `PASS`。
- G4 代表單元試走：`INDEPENDENT_AI_VERIFIED`，沒有阻礙，沒有存取禁止輸入。
- G5 全課試走：`INDEPENDENT_AI_VERIFIED`，沒有阻礙，沒有存取禁止輸入。
- 發行狀態：`published: false`；只有本機 release proposal 與 staging 證據。

## 深入驗證發現與修正

初版證明課可閱讀，但缺少 `main#main`、可辨識的 learner content root、鍵盤 skip link 與完整 SEO／社群中繼資料。這表示流程測試通過仍不足以證明學員頁完全符合 HTML 契約。

本輪已補上上述結構，並完成下列重新驗證：

1. 新增四頁共同的 HTML 契約回歸測試。
2. `course-html-contract` 結構檢查四頁全部通過。
3. 以 390×844、820×1180、1440×900 三種 viewport 實際渲染；無頁面水平溢出，鍵盤第一個焦點可進入 skip link，啟用後抵達唯一的 `main#main`。
4. 舊試走證據移至 `trials/archive/pre-html-contract-fix/`，保留歷史而不冒充現況。
5. 重新計算頁面與素材雜湊，再以全新 G4、G5 隔離情境完整試走。

## 驗證邊界

- 尚無真人學員試走，證據成熟度停在 `INDEPENDENT_AI_VERIFIED`；不能宣稱 `HUMAN_READY`。
- 本輪刻意沒有測試真實公開發布，因為外部變更必須等最終明確授權。
- 示範課使用無登入、無付費的本機素材，因此沒有證明特定第三方平台的帳號、權限或 UI 流程。未來遇到這類課程，G1、G4 或 G5 必須取得對應平台證據，否則維持 `BLOCKED`。
- 這份證明確認母系統能執行並阻擋缺證課程；每一門新課仍須以自己的研究、素材、平台與學員試走證據逐 Gate 驗收。
