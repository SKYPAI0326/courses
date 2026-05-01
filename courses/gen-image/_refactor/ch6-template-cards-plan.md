# CH6 模板速查站 製作計畫

**建檔**：2026-05-01
**來源**：`ConardLi/garden-skills` (MIT License, 2026)，本機快照於 `~/garden-skills/skills/gpt-image-2/`
**定位**：CH1-CH5 教技法／工作流；**CH6 是「做完想用時來查」的速查素材庫**，不是 CH1 的延伸知識
**先決條件**：v31-v42 補圖 + Codex 修補清單收尾後再開工
**依據對話**：sky8697@gmail.com / 2026-05-01 設計討論

---

## 章節骨架

```
courses/gen-image/
├── module6.html       章節總覽：什麼時候來查、怎麼選模板、卡片頁怎麼讀
├── CH6-1.html         模板速查方法論：如何把模板套到自己的場景
├── CH6-A1.html ... CH6-A6.html   品牌行銷 6 張
├── CH6-B1.html ... CH6-B6.html   商品電商 6 張
├── CH6-C1.html ... CH6-C6.html   內容創作 6 張
└── CH6-X.html         自我練習：3 個情境，挑模板 + 改寫 + 出圖
```

放置位置：CH5 之後、PRAC 之前。前 5 章卡關處 callout 引導「→ 看 CH6 第 N 張卡片」。

**追加項數**：1 module 總覽 + 1 方法論 + 18 模板卡 + 1 練習 = **21 個 HTML**（與現有 21 上線頁同量級，注意工時）

---

## 18 張模板候選（已 lock-in）

### A 組 · 品牌行銷

| ID | 模板 | 來源檔 | 一句話定位 |
|---|---|---|---|
| A1 | banner-hero | `poster-and-campaigns/banner-hero.md` | 官網首屏巨幅 banner |
| A2 | campaign-kv | `poster-and-campaigns/campaign-kv.md` | 季度／節慶大促主視覺，可延展多平台 |
| A3 | brand-poster | `poster-and-campaigns/brand-poster.md` | 單張品牌張力海報 |
| A4 | editorial-cover | `poster-and-campaigns/editorial-cover.md` | 雜誌／電子書／報告封面 |
| A5 | brand-identity-board | `branding-and-packaging/brand-identity-board.md` | 品牌識別 mood board |
| A6 | bilingual-layout-visual | `typography-and-text-layout/bilingual-layout-visual.md` | 中英雙語版面 |

### B 組 · 商品電商

| ID | 模板 | 來源檔 | 一句話定位 |
|---|---|---|---|
| B1 | white-background-product | `product-visuals/white-background-product.md` | 純白底電商主圖（蝦皮／momo／PChome 必備） |
| B2 | lifestyle-product-scene | `product-visuals/lifestyle-product-scene.md` | 商品在真實情境被「使用中」（IG／Threads） |
| B3 | premium-studio-product | `product-visuals/premium-studio-product.md` | 影棚高質感氛圍 hero |
| B4 | packaging-showcase | `product-visuals/packaging-showcase.md` | 包裝多面視角展示 |
| B5 | product-card-overlay | `ui-mockups/product-card-overlay.md` | 商品圖 + UI 卡疊加（電商詳情頁） |
| B6 | beverage-label-design | `branding-and-packaging/beverage-label-design.md` | 飲料／瓶身標籤設計 |

### C 組 · 內容創作

| ID | 模板 | 來源檔 | 一句話定位 |
|---|---|---|---|
| C1 | bento-grid-infographic | `infographics/bento-grid-infographic.md` | 便當格資訊圖（IG／Threads 熱門） |
| C2 | comparison-infographic | `infographics/comparison-infographic.md` | 對比型資訊圖 |
| C3 | step-by-step-infographic | `infographics/step-by-step-infographic.md` | 步驟教學資訊圖 |
| C4 | founder-portrait | `portraits-and-characters/founder-portrait.md` | 創辦人／個人品牌肖像 |
| C5 | sticker-set | `avatars-and-profile/sticker-set.md` | LINE 貼圖組 |
| C6 | lookbook-grid | `grids-and-collages/lookbook-grid.md` | 服飾／時尚 lookbook 多格 |

每張的「小工作室／個人接案兩個台灣化情境」見對話紀錄附錄（製作時逐張帶入）。

---

## 卡片頁 anatomy（6 區塊）

每張卡片頁固定六段，**密度比 CH1-CH5 教學頁低、比純 cheatsheet 高**：

1. **適用場景** — 一句話 + 3 個典型用途
2. **模板拆解** — 原 prompt 結構分段標註：構圖／風格／文字／限制
3. **台灣化範例** — 2 個情境（小工作室 + 個人接案）
4. **Codex 示範圖** — 1-2 張 + 短評「為何這張成立」
5. **改成你的場景** — 3 個替換槽位提示 + 1 個常見踩雷
6. **延伸 + 失敗案例** — prompt 動了哪一處會壞掉

每頁約 250-400 字 + 1-2 張圖。

---

## 在地化硬規則（中→台用語轉換）

不只字符轉換，**情境替換**才是大頭：

| 簡中原文 | 台灣化 |
|---|---|
| 视频 | 影片 |
| 软件／硬盘／默认 | 軟體／硬碟／預設 |
| 网络／互联网 | 網路／網際網路 |
| 双 11／618 | 雙 11／週年慶（或保留雙 11） |
| 天猫／淘宝 | momo／蝦皮／PChome |
| 京东 | momo／東森購物 |
| 滴滴 | Uber／LINE TAXI |
| 抖音 | TikTok／Reels |
| 小红书 | Threads／Instagram |
| 微信／朋友圈 | LINE／Threads |
| 公众号 | 電子報／Substack |
| 春节 | 過年／春節 |
| 地铁 | 捷運 |
| 视频号 | YouTube Shorts／Reels |
| 直播带货 | 直播電商（蝦皮直播） |
| 一线／三线城市 | 雙北／中南部／東部 |
| 小哥／师傅 | 師傅／外送員 |
| 元 | 元（NTD） |

**品牌情境替換原則**：原模板若以中國品牌舉例（茶顏悅色、瑞幸、元氣森林⋯⋯），改成台灣對應品牌（鮮乳坊、迷客夏、原萃、伊藤園⋯⋯）。**不確定就用泛化描述**（「在地手作茶飲品牌」）避免誤舉例。

---

## Pilot：B2 lifestyle-product-scene 端到端

**目標**：跑通單張卡片完整流程，測量真實工時 + 卡片 anatomy 是否順、Codex 出圖品質是否堪用。

**步驟**：
1. 讀 `~/garden-skills/skills/gpt-image-2/references/product-visuals/lifestyle-product-scene.md` 全文
2. 套 anatomy 6 區塊起草 `CH6-B2.html`：
   - 適用場景（IG／Threads／品牌官網／節慶／雜誌風）
   - 模板拆解（場景 / 光線 / 道具 / 人物局部 / 文案）
   - 台灣化範例 ① 工作室幫客戶拍「燕麥奶在週末早餐桌」
   - 台灣化範例 ② 接案攝影師把客戶產品擺進咖啡桌
   - 改成你的場景：3 個替換槽（商品／時段／光線）
   - 失敗案例：背景過於「商業攝影感」會破壞生活方式氛圍
3. 用對話式 Codex Phase B（`codex_bridge.py --task imagegen`）產 1-2 張示範圖：
   - 「燕麥奶 + 週末早餐桌 + 自然晨光」(台灣化情境①)
4. 套 lesson-template-v3.html，跑 lint：`python3 ../../docs/lint-page.py courses/gen-image/CH6-B2.html`
5. **量測**：實際工時、字數、Codex 圖品質、anatomy 區塊是否需調整
6. **決策點**：pilot 結果決定後續 17 張要不要批量做、要不要修 anatomy

---

## 批次製作流程（pilot 通過後）

每張卡片步驟（估 30-60 分鐘／張）：

1. 讀原模板 .md
2. 起草 6 區塊內容 + 台灣化情境（依對話紀錄附錄）
3. Codex Phase B 產 1-2 張示範圖
4. 套 template、lint、加入 module6 / CH6-X 的 callout
5. 進度紀錄：`_refactor/ch6-build-log.md`（追蹤 18 張完成度）

**順序建議**：B 組（商品電商，學員最有感）→ C 組（內容創作）→ A 組（品牌行銷，較抽象放最後）

---

## 驗收標準

- 21 個新 HTML 全數通過 `lint-page.py`（0 BLOCKER／0 ERROR）
- module6 / CH6-X 練習頁可順利導引到 18 張卡片
- 18 張卡片每張至少 1 張 Codex 示範圖（含 alt + loading="lazy"）
- 每張卡片完整六區塊、無遺漏
- 所有原文中國品牌／用語已替換為台灣化版本（見硬規則表）
- CH1-CH5 至少 5 處新增 callout 引用 CH6 對應卡片
- LICENSE / 來源說明在 module6.html 註明（致敬 ConardLi/garden-skills MIT）

---

## 相依與風險

- **相依**：v31-v42 補圖完成 + Codex 修補清單收尾，否則並行會搞亂版本
- **scope 風險**：21 HTML ≈ 重做半個課程，務必 pilot 後再評估全量
- **Codex 預算**：21+ 張 imagegen，建議分批跑、品質不滿意立即停止重構 prompt
- **iCloud 衝突**：_refactor/ 內 ` 2.md` 結尾為同步副本，編輯時注意只動正本

---

## 後續產出檔

- `ch6-build-log.md` — 18 張製作進度（pilot 後建）
- `ch6-codex-image-log.md` — Codex 產圖紀錄（每張 prompt + verdict）
- `ch6-localization-glossary.md` — 在地化術語擴充表（過程中發現的補進來）
