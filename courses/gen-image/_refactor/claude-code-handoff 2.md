# Claude Code Handoff

日期：2026-04-26
專案：`courses/gen-image`
目的：交給原本設計此課程的 Claude Code，作為下一輪修正與插圖整合依據。

## 本輪 Codex 已完成

1. 已審查 `CH*.html` 與 `PRAC*.html` 的內容品質，面向包含教學邏輯、案例真實性、文案精準、結構可讀。
2. 已執行設計系統 lint：

```bash
python3 ../../docs/lint-page.py courses/gen-image
```

結果：BLOCKER 0、ERROR 0、WARN 55。

3. 已依 `_refactor/codex-image-requests.md` 補齊新圖，新增 `img/v31-v42` 共 12 張。
4. 已產出完整報告：

- `_refactor/codex-review-report.md`
- `_refactor/content-review.md`
- `_refactor/image-gen-log.md`

本輪沒有修改任何 HTML。

## 需要 Claude Code 優先處理的 BLOCKER

`_refactor/codex-image-requests.md` 的補圖數量互相矛盾：

- 總覽表列出 `v31-v42`，實際是 12 張。
- 第 19 行寫「總計 9 張新圖」。
- 同一行寫「5 張 P0 + 2 張 P1 + 2 張 P2」，但表格實際是 P0 7 張、P1 2 張、P2 3 張。
- 第 270 行又寫「P0 5 張（v31-v37）」，但 `v31-v37` 是 7 張。

建議先修 brief 的數量與優先級口徑，再進行 HTML 插圖與正式交付。

## 新圖清單與建議插入位置

### CH2-2 Cycle 4：同 brief × 3 preset

插入位置：`CH2-2.html` 的「風格 preset 不是寫『日系』就好」section。

建議做成 `<details>`：

```text
📷 同 brief × 3 preset 對照（看「結構不變、表象切換」）
```

檔案：

- `img/v31-preset-jp.png`
- `img/v32-preset-kr.png`
- `img/v33-preset-vintage.png`

### CH4-2 整合任務：同 brief × 4 變體

插入位置：`CH4-2.html` 的「整合任務 — 用 PM 決策三問挑 1 張」附近，或「PM 決策三問」後方。

建議做成 `<details>`：

```text
📷 4 變體並列範例（PM 決策三問參考）
```

檔案：

- `img/v34-variant-LR.png`
- `img/v35-variant-TB.png`
- `img/v36-variant-symm.png`
- `img/v37-variant-asymm.png`

### CH5-1 案例庫 hero

插入位置：`CH5-1.html` 的「5 案例庫」各案例 `<details class="case-fold">` 內，放在案例 meta 或情境說明後方。

檔案：

- 案例 A：`img/v40-case-a-coffee.png`
- 案例 B：`img/v38-case-b-health.png`
- 案例 C：`img/v41-case-c-course.png`
- 案例 D：`img/v42-case-d-travel.png`
- 案例 E：`img/v39-case-e-app.png`

## 內容修正建議

### 1. 統一案例真實性

目前「弄一下咖啡工作室」同時呈現台北單店、台灣課程語境、日文品名、日圓價格。建議二選一：

- 改成日本市場設定：在案例前明確說明這是「日本市場模擬品牌」。
- 改成台灣市場設定：價格改 NT$，品名與 CTA 改中文或台灣常見日系風格文案。

優先檔案：

- `CH2-2.html`
- `CH4-3.html`
- `CH5-1.html`

### 2. 降低平台資訊時效風險

`CH1-2.html` 的平台選擇段落含配額、付費方案、品質判斷。建議把固定數字改成「現場查價流程」與比較欄位，避免之後模型、方案或價格變動造成教材過期。

### 3. 保健品案例加法規保守語

`CH5-1.html` 案例 B 含「100 億活菌」「腸道健康」「醫師監修」「敏感腸友善」等健康訴求。建議加入：

```text
此案例為視覺生成練習，實際投放須符合法規，不做療效保證。
```

並把療效語改成更保守的產品資訊語。

### 4. 調整 PRAC3 時間盒

`PRAC3.html` 要求 20 分鐘內跑 5 張，但每張 4 分鐘又可能追加 1-2 分鐘迭代。建議：

- 合格目標：3 張完成 L2 + 自檢 + 筆記。
- 進階目標：5 張。
- 明確說「5 張是 stretch goal」。

### 5. 收斂 callout 與 details

lint 顯示多頁 callout 超過每頁最多 4 個。建議把提示分級：

- 必看規則：保留 callout。
- 卡關補救：放 details。
- 講師備註 / 延伸知識：放頁尾 instructor note。

特別需要收斂：

- `CH1-1.html`
- `CH1-2.html`
- `CH3-1.html`
- `CH3-2.html`
- `PRAC2.html`
- `PRAC3.html`

`CH2-2.html` 有 16 個 details、`CH5-1.html` 有 17 個 details，也建議標示「課堂必開 / 卡關再開 / 課後延伸」。

### 6. 文案一致性

`PRAC2.html`、`PRAC3.html` 混用 `Step N` 與「步驟 N」。請統一成「步驟 N」。

## 建議修正順序

1. 修 `_refactor/codex-image-requests.md` 的總數、P0/P1/P2 數量與交付口徑。
2. 把 `v31-v42` 插入對應 HTML，但先不要重構大段內容。
3. 修案例真實性與法規保守語，尤其咖啡市場設定與保健品案例。
4. 修 PRAC3 時間盒與 PRAC4 結尾金句。
5. 最後做設計系統清理：callout 數量、`Step N`、字級 token、箭頭 `aria-hidden`。

## 驗收建議

修完後請至少跑：

```bash
python3 ../../docs/lint-page.py courses/gen-image
```

並人工檢查：

- `CH2-2.html` preset 對照圖是否能清楚看出同骨架不同風格。
- `CH4-2.html` 四變體是否和 PM 決策三問相互對應。
- `CH5-1.html` 五案例是否都有 hero，且不讓案例庫變得過長難掃。
- 所有新增圖片都有 `alt`，且 `loading="lazy"`。
