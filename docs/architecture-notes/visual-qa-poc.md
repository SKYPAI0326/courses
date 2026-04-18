---
title: Visual QA PoC — Chrome MCP + Vision Model
status: Proposed
date: 2026-04-18
decision: 以 Chrome MCP 截圖 + vision 模型做視覺檢核，補 lint-page.py 抓不到的「排版亂」盲點
consequence: 只在 G3 關卡手動觸發；不進 pre-commit（太慢且需要 API 額度）
---

# Visual QA PoC

## 問題

`lint-page.py` 能擋 HTML 結構 / SEO / design tokens / 禁用組件，但擋不了：

- 元素對齊跑掉（margin 疊錯、grid 欄寬爆版）
- 字體 8 階誤用（標題與內文混為一階）
- 顏色對比不足（背景色太深）
- 空白/留白比例失衡（版面擁擠或空洞）

這些是「眼睛看得出、規則寫不出」的問題。目前唯一防線是使用者肉眼 review，成本高且不穩。

## 提案

Chrome MCP 自動截圖 + vision 模型給分，列入 G3 檢核清單一項。

### 流程

```
lesson-writer 產出 HTML
    → python3 docs/visual-qa.py <file.html>
        ├─ Chrome MCP: start → navigate → screenshot (desktop + mobile)
        ├─ vision 模型 prompt: 「這頁是否有排版/對比/留白問題？列出 ≤5 項」
        └─ 寫入 docs/.visual-qa/<slug>/<unit>.json
              { score, issues: [...], screenshots: [...] }
    → 使用者在 _gates.md G3 答題時參考
```

### Vision prompt（初稿）

```
你是課程講義的視覺檢核員。以下是一頁 HTML 講義的螢幕截圖（桌面 + 手機各一）。
設計規範：無印良品風格、Noto Sans TC、8 階字型、圓角 ≤ 8px、留白充足。

請檢查：
1. 是否有元素對齊跑掉 / 疊加 / 溢出？
2. 字體層級是否混亂？
3. 色彩對比是否足夠（WCAG AA）？
4. 留白比例是否失衡？
5. 手機版是否有橫向捲動？

回傳 JSON：
{ "score": 0-10, "issues": [{"severity":"BLOCKER|WARN","text":"..."}] }
```

### 觸發時機

- **不進 pre-commit**：慢（每頁 ~15s + API 成本）
- **G3 放行前手動跑**：`python3 docs/visual-qa.py courses/<slug>/<unit>.html`
- **批次**：`python3 docs/visual-qa.py courses/<slug>/ --all`

### 成功標準

PoC 過關條件：
1. 能穩定對 10 個既有單元頁截圖（桌面 + 手機）
2. Vision 模型至少能抓到 1 個 lint-page.py 漏掉的真實問題
3. 總時間 < 20 秒/頁

### 不做的事

- 不做「自動修正」（只報告，人類決定）
- 不做 CI/CD 整合（個人專案，手動跑即可）
- 不做視覺 regression（無 baseline 機制）

## 後續

PoC 驗證後決定是否：
- 納入 `build-all.py --visual`
- 寫進 `_規範/課程製作團隊系統手冊.md` G3 清單

預估工時：1-2 天（含 vision prompt 調教）。
