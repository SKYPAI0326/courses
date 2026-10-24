# GA4 × GTM 共用量測練習包

> 版本：2026-10-24-v1
> 用途：讓沒有網站、GA4 歷史資料或 GTM 編輯權限的學員，也能完成分析與設定推理。
> 資料聲明：下列數據與除錯紀錄是課堂合成案例，不是真實客戶資料，也不是 GA4 匯出檔。離線完成不等於已在平台安裝或驗證。

## 先選你的練習軌

| 軌別 | 你需要的條件 | 能完成 | 不能宣稱 |
|---|---|---|---|
| A 真實環境 | 自有網站、GA4 資源權限、GTM 容器編輯權限、已確認的 Consent／CMP 政策 | 建立、Preview、DebugView／Realtime 驗證、核准後發布 | 未實測的瀏覽器、同意情境或轉換仍不能寫成通過 |
| B Google Demo | 可登入 Google 帳號 | 用 Google Analytics demo account 練習報告與探索、解讀真實商業資料 | 不能在示範資源安裝自己的 GTM 或改管理設定 |
| C 離線案例 | 本檔即可 | 算指標、找流失、設計事件、判讀 consent／tag firing trace、寫 QA 清單 | 不能寫「GA4／GTM 已安裝」「Tag Assistant／DebugView 已通過」 |

Google 官方 Demo Account：<https://support.google.com/analytics/answer/10993011>

## Part 1｜GA4 練習資料

案例：教學電商「日日沖煮」；期間 2026-09-01～2026-09-30；幣別 TWD。

### 1A. 流量來源

| Session default channel group | Sessions | Engaged sessions | Key events | Purchases | Revenue |
|---|---:|---:|---:|---:|---:|
| Organic Search | 6,200 | 3,720 | 620 | 186 | 372,000 |
| Paid Search | 3,100 | 1,860 | 465 | 155 | 341,000 |
| Paid Social | 4,400 | 1,980 | 352 | 88 | 167,200 |
| Email | 1,600 | 1,120 | 272 | 96 | 211,200 |
| Direct | 2,700 | 1,350 | 216 | 81 | 170,100 |

獨立任務：計算各渠道參與率、購買轉換率與平均訂單金額。只根據表中數字回答「保留、調查、降低」各一個渠道，並註明還缺什麼證據。

### 1B. 電商漏斗

| 步驟 | 事件 | 使用者數 |
|---|---|---:|
| 1 | session_start | 5,000 |
| 2 | view_item | 3,000 |
| 3 | add_to_cart | 900 |
| 4 | begin_checkout | 450 |
| 5 | purchase | 270 |

裝置細分：

| 裝置 | view_item | add_to_cart | begin_checkout | purchase |
|---|---:|---:|---:|---:|
| Mobile | 2,100 | 525 | 210 | 105 |
| Desktop | 900 | 375 | 240 | 165 |

獨立任務：計算每一步流失率，找出最大流失點；再比較 Mobile／Desktop。提出一個只改單一變因的測試，並寫出主要指標與停止條件。資料不足時寫「待驗證」，不要補數字。

## Part 2｜GTM 設定草案

案例需求：追蹤頁面瀏覽與「預約體驗」按鈕。組織採 Basic Consent Mode；未同意前不載入 Google tags。

| 元件 | 課堂草案 |
|---|---|
| Consent 預設 | `analytics_storage`、`ad_storage`、`ad_user_data`、`ad_personalization` 皆為 `denied` |
| Consent 更新 | 使用者按「全部接受」才把四項更新為 `granted`；拒絕則維持 `denied` |
| Google tag | Tag ID：`G-COURSE123`（課堂假 ID，不可發布） |
| Google tag trigger | `Initialization - All Pages`；仍須遵守 consent checks |
| CTA 事件 | event name：`generate_lead`；parameter：`cta_name=trial_booking`、`page_type=course_landing` |
| CTA trigger | Click Text equals `預約體驗`，且 Page Path equals `/course/` |

### 2A. 正常 Preview trace（Basic 模式）

| 順序 | Event／階段 | Consent 狀態 | Tag Assistant 可觀察結果 |
|---:|---|---|---|
| 1 | Consent Initialization | 四項 denied | Consent default tag fired |
| 2 | Initialization | 四項 denied | Google tag blocked；沒有 GA4 event tag fired |
| 3 | consent_accept | 四項 update 為 granted | Consent update 可見 |
| 4 | page_view | granted | Google tag 與 page_view 可見 |
| 5 | click「預約體驗」 | granted | `generate_lead` fired，兩個參數值正確 |

### 2B. 故障 trace

| 順序 | Event／階段 | Consent 狀態 | Tag Assistant 可觀察結果 |
|---:|---|---|---|
| 1 | Initialization | 尚未設定 | Google tag fired |
| 2 | DOM Ready | 四項 default 為 denied | Consent default 才出現 |
| 3 | click「預約體驗」 | denied | `generate_lead` 仍 fired |

獨立任務：指出至少兩個失敗證據、風險與修復位置。最低答案必須包含「default 太晚」與「denied 時事件仍觸發」。修正後重排正確順序；離線作答只標記為 `CONFIG REVIEW PASS`，不能標記為 `PLATFORM VERIFIED`。

## Part 3｜繳交與驗收

請交一份 `measurement-decision.md`。若你已完成 M6-1，先從 `ga4-setup-check.md` 帶入練習軌、GA4 可用條件與平台狀態；若直接從 M7 開始，就把 GA4 readiness 標成 `PENDING`，再使用本檔 Part 2 完成 GTM 設定審查。

```markdown
# Measurement Decision
- 版本／日期：
- 練習軌：A／B／C
- 使用資料來源與期間：
- GA4 readiness：已驗證／待處理／不適用（來源：ga4-setup-check.md／本練習包）
- 一個已確認發現：
- 一個仍待驗證假設：
- 決策：保留／調查／降低／修復
- 依據數字或 trace：
- 下一個驗證動作、負責人、日期：

## GTM 設定審查
- Consent 模式與政策來源：Basic／Advanced／待確認
- Tag／Trigger／Variable／Consent 配對：
- 正常 trace 的預期順序與依據：
- 失敗證據與修復：至少兩項

## 三種同意情境
| 情境 | 各 consent type 預期狀態 | 預期 tag 行為 | 證據層級 |
|---|---|---|---|
| 全部接受 |  |  | 課堂 trace／平台證據 |
| 全部拒絕 |  |  | 課堂 trace／平台證據 |
| 部分接受 |  |  | 課堂 trace／平台證據 |

## 收集與報表複核
- 當下用 Tag Assistant、Realtime 或 DebugView 檢查：
- 需要等待處理的標準報表／探索與複核條件：
- 停止發布條件：
- 設定審查狀態：CONFIG REVIEW PASS／需修訂
- 平台狀態：PLATFORM VERIFIED／PENDING（附證據連結或截圖編號）
```

互評者先檢查結論是否有來源、未知是否誠實標示、下一步是否能執行，再抽查 GTM 設定、三種同意情境、失敗修復與平台狀態是否使用同一證據層級。離線軌可以通過 `CONFIG REVIEW PASS`，但平台狀態必須是 `PENDING`；任一不合格就退回修訂。
