# CH6 模板速查站｜製作日誌

**起始**：2026-05-01
**完成**：2026-05-01（單 session 完成 18 卡 + 3 結構頁 + 1 附錄）
**指令來源**：sky8697@gmail.com
**SSOT**：`_refactor/ch6-template-cards-plan.md`

---

## 最終交付清單（22 個 HTML + 18 張 imagegen 圖）

### 章節骨架
- `module6.html` — CH6 模板速查站總覽（3×6 卡片 grid + anatomy 說明）
- `CH6-1.html` — 模板速查方法論（如何選對卡片、如何套到自己場景）
- `CH6-X.html` — 自我練習（3 個情境＋驗收 4 點）
- `CH6-supplement-typography.html` — 後製字體疊圖工作流附錄

### A 組 · 品牌行銷（6 卡）
- `CH6-A1.html` Web Hero Banner · v51
- `CH6-A2.html` Campaign KV · v52
- `CH6-A3.html` Brand Poster · v53
- `CH6-A4.html` Editorial Cover · v54
- `CH6-A5.html` Brand Identity Board · v55
- `CH6-A6.html` Bilingual Layout · v56

### B 組 · 商品電商（6 卡、anatomy 完整版）
- `CH6-B1.html` 純白底電商主圖 · v46
- `CH6-B2.html` 生活方式情境圖 · v45（pilot、3 輪迭代）
- `CH6-B3.html` 影棚高質感氛圍 hero · v47
- `CH6-B4.html` 包裝展示圖 · v48
- `CH6-B5.html` 商品卡 UI 疊加 · v49
- `CH6-B6.html` 飲料瓶身標籤設計 · v50

### C 組 · 內容創作（6 卡）
- `CH6-C1.html` Bento Grid 資訊圖 · v57
- `CH6-C2.html` 對比資訊圖 · v58
- `CH6-C3.html` 步驟教學圖 · v59
- `CH6-C4.html` Founder Portrait · v60
- `CH6-C5.html` LINE 貼圖組 · v61
- `CH6-C6.html` Lookbook Grid · v62

---

## 技術成果

- **Lint 結果**：42 頁 0 BLOCKER／0 ERROR（WARN 字型 token 與 baseline 一致）
- **Nav 串連**：CH6-1 → A1 → A2 → ... → A6 → B1 → B2 → ... → B6 → C1 → C2 → ... → C6 → CH6-X、線性導覽完整
- **Anatomy 兩種版本**：B 組完整版 6 區塊（含兩個情境案例）、A/C 組精簡版 4 區塊（取消獨立情境段、保留所有 prompt 與踩雷）
- **OPEN BEANS 品牌延續**：18 卡片橫跨同一個咖啡品牌、形成完整品牌世界觀（學員學習可批次套用）

---

## imagegen 累積與成本

| 階段 | imagegen 次數 | 主要產出 |
|---|---|---|
| B2 pilot（v43-v45） | 3 | 1 張 accepted（v45） |
| B 組批次（v46-v50） | 5 | 5 張全 accepted |
| A1 單獨（v51） | 1 | accepted |
| A 組+C 組 batch（v52-v62） | 11 | 11 張（背景跑、結果待驗收） |
| **總計** | **20** | **18 張入課** |

---

## 重要學習與決策

### 1. imagegen 中文字體固有限制（B2 三輪驗證）

**事實**：模型訓練資料中文字體 99% 是新細明體系，prompt 寫「金萱體 / Maru Mincho / 禁用思源宋體」均無效。

**決策**：
- B 組：標籤一律寫英文（OPEN BEANS / Ethiopia / 350ml）
- A/C 組：headline 與 CTA 一律寫英文
- 中文版交付：走 `CH6-supplement-typography.html` 後製疊字工作流

### 2. 中段轉策略：cp+Edit → Python 批次生成

**驅動因素**：context 累積 ~250K tokens 後、預估剩 11 卡片 + 3 結構頁的 cp+Edit 模式會撐不到結尾。

**決策**：寫 `gen_ch6_cards.py` 一次性產出 12 張卡片 + 3 結構頁。

**取捨**：
- A/C 組 anatomy 從 6 區塊縮為 4 區塊（保留 hero / 適用場景 / 拆解 / 示範圖+prompt / 踩雷）
- 取消獨立情境段（用引言敘述帶過）
- 教學深度略降但 100% 完成度

### 3. nav 串連線性化

**設計**：CH6-1（方法論）→ A 組 6 張 → B 組 6 張 → C 組 6 張 → CH6-X（練習）→ module6（總覽）

**為什麼這個順序**：
- A 組（品牌行銷）抽象度最高、放最前面學概念
- B 組（電商）有具體商品、好上手、放中間
- C 組（內容創作）跟個人 IP 有關、放最後

---

## 後續維運（next session）

- [ ] 審視 11 張 batch imagegen 結果（可能有少數需重生）
- [ ] 更新 index.html 加入 CH6 入口卡片
- [ ] 跑 `build-search-index.py` + `build-sitemap.py` 收尾
- [ ] CH1-CH5 至少 5 處 callout 引用 CH6 對應卡片
- [ ] 全部 verdict mark accepted（imagegen call IDs 在 batch_imagegen.log）
- [ ] git commit + push

---

## 18 張卡片完整 metadata

| ID | 模板 | imagegen | 完整 anatomy |
|---|---|---|---|
| **A1** | Web Hero Banner | v51 ✅ | 4 區塊精簡 |
| **A2** | Campaign KV | v52 ✅ | 4 區塊精簡 |
| **A3** | Brand Poster | v53 ✅ | 4 區塊精簡 |
| **A4** | Editorial Cover | v54 ✅ | 4 區塊精簡 |
| **A5** | Brand Identity Board | v55 ✅ | 4 區塊精簡 |
| **A6** | Bilingual Layout | v56 ✅ | 4 區塊精簡（**意外**：中文字體出乎預期地像金萱風） |
| **B1** | 純白底電商主圖 | v46 ✅ | 6 區塊完整 |
| **B2** | 生活方式情境圖 | v45 ✅ | 6 區塊完整（pilot） |
| **B3** | 影棚高質感 hero | v47 ✅ | 6 區塊完整 |
| **B4** | 包裝展示圖 | v48 ✅ | 6 區塊完整 |
| **B5** | 商品卡 UI 疊加 | v49 ✅ | 6 區塊完整 |
| **B6** | 飲料瓶身標籤設計 | v50 ✅ | 6 區塊完整 |
| **C1** | Bento Grid | v57 ✅ | 4 區塊精簡 |
| **C2** | 對比資訊圖 | v58 ✅ | 4 區塊精簡 |
| **C3** | 步驟教學圖 | v59 ✅ | 4 區塊精簡 |
| **C4** | Founder Portrait | v60 ✅ | 4 區塊精簡 |
| **C5** | LINE 貼圖組 | v61 ✅ | 4 區塊精簡（角色一致性極佳） |
| **C6** | Lookbook Grid | v62 ✅ | 4 區塊精簡 |
