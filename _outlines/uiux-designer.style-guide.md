---
slug: uiux-designer
extends: _style_guide_template.md
---

# UI/UX Designer Style Guide 覆寫

## 課程語氣與視覺邊界

- 語氣：技術友善、紮實、清楚、可驗證。每段直接交代角色、動作、畫面結果或檢查方式。
- 學員視角固定使用「你」。頁面不能出現內部代號、機器試點標籤、授課調度或製作流程備註。
- 延續課程系統的 V4 CCS 無印風：使用 `_規範/design-tokens.md` 的 `--c-*` 色彩、Shippori Mincho 標題與 Noto Sans TC 內文；新頁面以 `_規範/lesson-template-v3.html` 為結構來源。
- 章節頁要有進度條、情境、任務、操作、驗收與下一單元入口。卡片只用來承載可執行任務，不用來堆疊標籤。

## 固定情境與角色

- 公司：弄一下行銷工作室，10 人數位行銷團隊。
- 主角：阿凱（27 歲，行銷專員）。涉及客戶決策時使用雯姊（35 歲，業務主管）。同一單元只保留一個主要視角。
- UI/UX 案例以「行動、畫面、狀態、測試結果、交接檔案」為主詞；避免空泛的設計宣傳語。

## UI/UX 術語

| 英文 | 講義用語 | 使用規則 |
|---|---|---|
| Frame | Frame／畫板 | 首次出現同時給英文與中文 |
| Component | 主元件 | 說明可重用來源 |
| Instance | Instance／實例 | 說明它跟主元件的同步關係 |
| Variant | Variant／變體 | 連同 Property 與 Value 一起寫 |
| Property | 屬性 | 保留 Figma 面板名稱 |
| Prototype | Prototype／原型 | 只在互動單元使用 |
| Overlay | Overlay／覆蓋層 | 連同觸發與返回路徑說明 |
| Inspect | Inspect／檢查 | 與交接檔案、尺寸與色值連結 |

## 平台與證據標記

- 主要環境：Google Chrome、Figma 網頁版 Starter／Free。頁面必須標出本單元平台版本與測試日期。
- 已在 `PROBE-A.md` 實測的 Component、Variant、Instance 路徑可教；Form、List、獨立 Button、完整 Prototype、Photoshop、GitHub 與公開部署仍須依證據標為 `CONDITIONAL` 或 `NOT_RUN`。
- `MACHINE_READY_PENDING_HUMAN` 只代表機器驗證完成，不能當作學員冷讀通過。
- 教案可使用 `A4` 等內部 unit_id；學員頁顯示「第 04 堂」與中文單元名稱，不顯示 A/B 編號。

## 文案檢查

- 直接寫出任務與結果，避免公式化否定對比、空泛開場、未附來源的「研究顯示」、以及無法驗收的「完整／全面／有效」。
- Figma 操作必須寫出面板名稱、預期畫面與卡住時的修復；只寫「建立元件」「完成設計」視為內容不足。
