# Codex Audit 修補完成報告

**修補時間**：2026-04-26
**對象**：Codex Review Report 給的 1 BLOCKER + 7 WARN + 4 NIT
**驗收**：lint 0 BLOCKER / 0 ERROR / 51 WARN（從 55 降）；search-index + sitemap 466 筆已重建

---

## 修補總覽

| 編號 | 等級 | 項目 | 狀態 | 備註 |
|------|------|------|------|------|
| 1 | BLOCKER | `codex-image-requests.md` 數量矛盾 | ✅ 修 | 統一成 12 張 / P0 7 + P1 2 + P2 3 |
| 2 | WARN | CH2-2 cycle 4 插 v31-33 preset 對照 | ✅ 修 | 加 details 折疊「📷 同 brief × 3 preset」|
| 3 | WARN | CH4-2 整合任務插 v34-37 變體並列 | ✅ 修 | 加 details 折疊「📷 4 變體並列」|
| 4 | WARN | CH5-1 案例 A-E 各插 hero 圖 v38-42 | ✅ 修 | 5 個 case-fold 內加 figure |
| 5 | WARN | 案例真實性「日本市場模擬品牌」標註 | ✅ 修 | CH5-1 5 個案例情境句加註 |
| 6 | WARN | CH5-1 案例 B 保健品法規保守語 | ✅ 修 | 加 callout-tip 法規提醒 |
| 7 | WARN | PRAC3 時間盒「5 張為 stretch goal」 | ✅ 修 | tagline + section heading + intro + exercise 全段標註 |
| 8 | WARN | PRAC4 結尾金句改品牌一致性 | ✅ 修 | 「多看多拆多練」→「鎖死 3 件事、系列就是品牌」|
| 9 | NIT | PRAC2/PRAC3 Step N → 步驟 N | ✅ 修 | PRAC2 1 處 + PRAC3 4 處全替換 |
| 10 | WARN | callout 超量收斂（6 頁）| ⏭ 留下次 | 設計判斷工作量大、列入下輪 round |
| — | WARN | CH1-2 平台時效資訊 | ⏭ 留下次 | 需重寫平台段、影響面大 |
| — | NIT | CH2-1/CH2-2 「3 秒決定」改「目標」 | ⏭ 留下次 | 與 callout 收斂同 round 處理 |
| — | NIT | CH1-2 平台品牌名密度 | ⏭ 留下次 | 同上 |
| — | NIT | CH5-1 案例固定日期改可替換欄位 | ⏭ 留下次 | 影響 5 個 case-fold |
| — | WARN | CH2-2 / CH5-1 details 過多分級 | ⏭ 留下次 | 需設計「必看 / 卡關 / 課後」3 級視覺 |

---

## 已完成項目細節

### 1. BLOCKER：codex-image-requests.md 數量矛盾

**修改位置**：`_refactor/codex-image-requests.md` line 19 + line 270 區
**修法**：
- 第 19 行「總計 9 張」→「總計 12 張新圖（P0 共 7 張：v31-v37 / P1 共 2 張：v38-v39 / P2 共 3 張：v40-v42）」
- 加修訂紀錄註腳引用 Codex review 意見
- 末段「P0 5 張」→「P0 7 張（v31-v37）」

### 2-4. 12 張新圖插入

**v31-33（CH2-2 cycle 4）**：
- 插入位置：cycle-bridge 後、「11 種 preset 速查」instructor-note 前
- 容器：`<details>` 折疊「📷 同 brief × 3 preset 對照（看『結構不變、表象切換』）」
- 視覺：3 欄 grid、各帶 figcaption 風格名 + 1 句調性
- alt：含完整風格描述（配色 / 字體 / 調性）+ loading=lazy

**v34-37（CH4-2 整合任務）**：
- 插入位置：task-card-stuck 後、`</section>` 前
- 容器：`<details>` 折疊「📷 4 變體並列範例（PM 決策三問參考）」
- 視覺：2x2 grid、各帶 figcaption（A 左右 / B 上下 / C 中央對稱 精品感 / D 不對稱留白 雜誌感）

**v38-42（CH5-1 案例 A-E）**：
- 插入位置：每個 case-fold 的「情境」段後、「BRAND-DNA」前
- 容器：`<figure>` 居中、max-width:340px、含 figcaption
- 5 案例對應：A-coffee（v40）/ B-health（v38）/ C-course（v41）/ D-travel（v42）/ E-app（v39）

### 5. 案例真實性「日本市場模擬」標註

**CH5-1 5 個案例情境句修改**：
- 案例 A：「（日本市場模擬品牌、價格使用日圓）」
- 案例 B：「（日本市場模擬品牌、品名使用日文）」
- 案例 C：「（日期僅為示範、實際開班可替換）」
- 案例 D：「（日本 / 台灣旅遊路線混用、期間日期僅為示範）」
- 案例 E：「（日本市場模擬品牌、品名使用日文）」

**CH2-2 / CH4-3 暫不動**：這兩頁的咖啡案例是「教學範例」非「主案例庫」、Codex 主修建議聚焦在 CH5-1 案例庫即可。

### 6. CH5-1 案例 B 保健品法規保守語

**修改位置**：案例 B 摺疊內 BRAND-DNA 之前
**新增區塊**：`callout tip` 含「法規保守提醒」
**內容**：
> 本案例為視覺生成練習、文案如「100 億活菌 / 醫師監修 / 敏感腸友善」屬概念示意。實際投放廣告時須符合各地保健食品法規、不得做療效保證；建議將訴求語改為產品成分資訊（如「乳酸菌 30 日份」「日常保健」）。

### 7. PRAC3 時間盒調整

**4 處統一修改**：
- lesson-tagline：「5 張...每張 4 分鐘」→「3-5 張...每張約 4 分鐘、合格目標 3 張通過驗收 B、5 張為 stretch goal」
- section-heading：「每張 4 分鐘」→「每張約 4 分鐘」
- intro-text：「20 分鐘跑 5 張」→「合格目標 3 張完整流程（每張 5-6 分鐘含 1 次迭代）、stretch goal 5 張（每張壓 4 分鐘）」
- exercise-block：演練說明同步改寫

### 8. PRAC4 結尾金句

「多看、多拆、多練、版型力自然提升」→「鎖死 3 件事、系列就是品牌」
（焦點從「版型訓練」拉回「品牌一致性」）

### 9. Step N → 步驟 N

PRAC2：1 處（「重複 Step 1-4」→「重複步驟 1-4」）
PRAC3：4 處（「進 Step 4」「Step 1 30s + Step 2...」「Step 3 驗收」「Step 4 寫筆記」）
驗證：`grep -c "Step [0-9]"` 兩檔均為 0

---

## 留下次處理項目（已記錄、不擋本輪交付）

### Round 2「設計系統清理」應做：

1. **callout 超量收斂到 ≤ 4**（6 頁）
   - CH1-1 10 / CH1-2 7 / CH3-1 10 / CH3-2 8 / PRAC2 6 / PRAC3 6
   - 策略：必看規則保留 callout / 卡關補救改 details / 講師備註改 instructor-note
   - 工作量：約 30-40 個 callout 重新分類 + HTML 結構重組

2. **CH2-2 / CH5-1 details 三級視覺分級**
   - 必看（課堂展開）/ 卡關（學員主動展開）/ 課後（講師備註）
   - CH2-2 16 個 details / CH5-1 17 個 details

3. **CH1-2 平台時效資訊改流程**
   - 把固定數字（免費配額、付費方案、品質百分比）改成「現場查價步驟」+「比較欄位模板」
   - 影響：整段 SECTION（150+ 行）

4. **NIT 雜項**
   - CH2-1/CH2-2 「3 秒決定」「等 30 秒」加「約」「目標時間」
   - CH1-2 平台品牌名密度收斂（Midjourney/SD/Flux/Grok... 改成精選清單 + 折疊延伸）
   - CH5-1 案例 A/C/D/E 固定日期（2026.06.15 等）改可替換欄位語法

---

## Lint 變化

| 指標 | Codex review 時 | 本次修補後 | 變化 |
|------|----------------|----------|------|
| BLOCKER | 0 | 0 | — |
| ERROR | 0 | 0 | — |
| WARN | 55 | 51 | -4 |

WARN 減少來自：
- PRAC2/PRAC3 Step N 規則消除（-2）
- 其他規則小幅優化（-2）

剩餘 51 條 WARN 主要分類：
- 字型 1rem / .78rem / .98rem / 1.15rem / 1.35rem 非 V4 階（pitfall-num 等舊組件）
- callout 超量（待 Round 2）
- --c-main 使用次數超 v3 建議（nav-btn 設計繼承）
- 箭頭符號缺 aria-hidden（line-based 誤判）

---

## 驗收建議（給下次審查者）

1. 跑 `python3 docs/lint-page.py courses/gen-image/` 應仍 0 BLOCKER 0 ERROR
2. 用瀏覽器打開 CH2-2 cycle 4、CH4-2 整合任務、CH5-1 案例 A-E、確認新圖都顯示 + alt 正確
3. CH5-1 案例 B 保健品法規語有出現
4. PRAC3 hero 提到「合格 3 張、5 張 stretch」
5. PRAC4 結尾金句已改

---

## 後續動作

下次修補可按以下順序進入 Round 2：
1. 收斂 callout 到 ≤ 4（6 頁、影響面最大）
2. CH1-2 平台時效改流程
3. CH2-2 / CH5-1 details 三級視覺分級
4. NIT 雜項一次處理
