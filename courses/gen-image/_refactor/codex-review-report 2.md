# Codex Review Report

日期：2026-04-26
範圍：`CH*.html`、`PRAC*.html`、`_refactor/codex-image-requests.md`、`img/`

## 內容問題

### BLOCKER

- `_refactor/codex-image-requests.md` 的補圖數量互相矛盾：總覽列 `v31-v42` 共 12 張，表格為 P0 3 + P0 4 + P1 2 + P2 3 = 12 張，但第 19 行寫「總計 9 張新圖（5 張 P0 + 2 張 P1 + 2 張 P2）」，第 270 行又寫「P0 5 張（v31-v37）」；實際 P0 是 7 張。這會直接造成補圖漏產或驗收口徑不一致。

### WARN

- `CH2-2.html`、`CH4-3.html`、`CH5-1.html` 的「弄一下咖啡工作室」一方面被描述為台北單店或台灣課程主線，另一方面商品價格使用 `¥680 / ¥580 / ¥620 / ¥730`，且品名混用日文。若品牌設定是台北店，價格與語言不可信；若是日系虛構品牌，需要在案例前明確說明「以日本市場為設定」。
- `CH1-2.html` 平台選擇段落含高度時效資訊，例如 Gemini / ChatGPT / Canva / Firefly 的免費配額、付費方案與「品質拿到 90%」等判斷。頁面雖有 2026-04 提醒，但教學現場若照念，仍容易把已變動資訊當成定論；建議改成「現場查價流程」與「比較欄位」，把數字移到講師備註或課前更新表。
- `CH5-1.html` 案例 B 保健品文案含「100 億活菌」「腸道健康」「醫師監修」「敏感腸友善」等健康訴求。作為生圖練習可用，但若定位成商業案例，需加註「避免療效保證、實際投放須符合法規」並把療效語改成更保守的產品資訊語。
- `PRAC3.html` 的時間盒設計要求每張 4 分鐘完成 L2 反推、自檢與筆記，但又允許驗收失敗後多花 1-2 分鐘迭代；若學員連續 2 張需要迭代，20 分鐘內完成 5 張會失真。建議把「5 張」改成 stretch goal，核心合格維持 3 張。
- `PRAC4.html` 結尾金句是「多看、多拆、多練、版型力自然提升」，和本頁主題「品牌小卡 + 系列一致性」相比偏回到版型訓練，收束焦點略散。建議改成品牌一致性相關句。
- 結構可讀性上，多頁 callout 過量：lint 顯示 `CH1-1` 10 個、`CH1-2` 7 個、`CH3-1` 10 個、`CH3-2` 8 個、`PRAC2` 6 個、`PRAC3` 6 個等，超過每頁最多 4 個的設計系統建議。會降低重點層級，尤其在練習頁容易把提示、規則、提醒混在一起。
- 多個頁面 `<details>` 很多，尤其 `CH2-2.html` 16 個、`CH5-1.html` 17 個。折疊能收斂資訊，但過多時學員會不知道哪些必開、哪些課後看；建議把講師備註、延伸表、卡關提示三類在視覺上分級。

### NIT

- `PRAC2.html`、`PRAC3.html` 混用 `Step 1-4` 與「步驟 N」。設計 lint 也抓到 `PRAC2` 1 處、`PRAC3` 7 處；建議全站統一為「步驟 N」。
- `CH2-1.html`、`CH2-2.html` 多處使用「3 秒決定」「等 30 秒」「5 分鐘出圖」這類節奏型說法，課堂上有動能，但容易被理解成保證產出；建議改成「約」或「目標時間」。
- `CH1-2.html` 的平台段落品牌名密度高，且列出 Midjourney / SD / Flux / Grok / 文心 / 通義萬相 / 可靈等排除名單。若目標是初學 PM，這段可再收斂成「本課只要求同對話延續編輯能力」，其餘工具放折疊。
- `CH5-1.html` 案例 A/C/D/E 的主題都設定在 2026 年或固定日期，作為教材可行；若課程會重複開班，日期應改成可替換欄位，避免明年內容看起來過期。

## 設計系統 lint

執行命令：

```bash
python3 ../../docs/lint-page.py courses/gen-image
```

結果摘要：

- 掃描：19 頁（包含 `module*.html`；本次內容審查只採 `CH*.html` 與 `PRAC*.html`）
- BLOCKER：0
- ERROR：0
- WARN：55

CH/PRAC 主要 WARN 類型：

- 多頁箭頭符號缺 `aria-hidden`
- 非 V4 15 階字型值，例如 `1rem`、`.78rem`、`.98rem`、`1.15rem`、`1.35rem`
- 多頁 callout 超過每頁最多 4 個
- 多頁 `--c-main` 使用次數超過 v3 建議
- `PRAC2.html`、`PRAC3.html` 含 `Step N`

## 補圖結果

因 `img/` 原本已有 `v01-v30`，本次依 brief 補齊 `v31-v42`。雖然 brief 寫「總計 9 張」，但已命名需求實際為 12 張，因此全部產出。

| Brief | 檔名 | 用途 |
|---|---|---|
| v31 | `img/v31-preset-jp.png` | CH2-2 Cycle 4 日系 preset |
| v32 | `img/v32-preset-kr.png` | CH2-2 Cycle 4 韓系 preset |
| v33 | `img/v33-preset-vintage.png` | CH2-2 Cycle 4 美式復古 preset |
| v34 | `img/v34-variant-LR.png` | CH4-2 左右對調 |
| v35 | `img/v35-variant-TB.png` | CH4-2 上下對調 |
| v36 | `img/v36-variant-symm.png` | CH4-2 中央對稱 |
| v37 | `img/v37-variant-asymm.png` | CH4-2 不對稱留白 |
| v38 | `img/v38-case-b-health.png` | CH5-1 案例 B 保健品 hero |
| v39 | `img/v39-case-e-app.png` | CH5-1 案例 E App / SaaS hero |
| v40 | `img/v40-case-a-coffee.png` | CH5-1 案例 A 咖啡 hero |
| v41 | `img/v41-case-c-course.png` | CH5-1 案例 C 課程 hero |
| v42 | `img/v42-case-d-travel.png` | CH5-1 案例 D 旅遊 hero |

檔案檢查：12 張皆為 PNG，尺寸皆為 `1254 x 1254`。

## 優先修正順序

1. 先修 `_refactor/codex-image-requests.md` 的數量與優先級矛盾，確定到底要交 9 張、12 張，或只交 P0/P1。
2. 再修案例真實性：統一「台北品牌 vs 日本市場」設定、平台價格配額改成可更新流程、保健品案例加法規保守語。
3. 最後做結構清理：callout 降到每頁 4 個內、`Step N` 改「步驟 N」、折疊區分成必看 / 卡關 / 課後延伸。
