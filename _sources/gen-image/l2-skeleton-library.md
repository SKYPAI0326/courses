# L2 骨架庫｜5 種跨風格通用的商業廣告版面語言

> 本檔為 `gen-image` 課程的核心教材資產。course-designer 寫 CH2-1 / CH3-1 / CH4-1 / CH7 時必讀。
>
> **教材策略**：本課**不備固定示範圖**，走引導發現法。每骨架以「文字描述 + L0 結構 JSON + ASCII 線框示意」教學，學員現場自跑 AI 或用 IG / Pinterest 真實案例對照。詳見本檔「圖片資產策略」段。
>
> **風格基準與延伸（重要）**：
>
> - 本課 5 骨架是**跨風格通用的結構模式**——同一個骨架可以穿日系、韓系、美式、歐陸、極簡、復古等任何風格的「衣服」
> - **日系為教學基準**（CH 示範段預設 preset），因為日系排版佔位符語意最清楚、最適合教結構
> - **其他風格（韓系 / 美式復古 / 矽谷科技 / 北歐極簡 / 歐陸法式 / 美式海報 / 瑞士排版 / 手繪童趣 / 工業風 / 街頭潮流）為演練延伸**，PRAC 段學員自選
> - **結構（骨架）不變、表象（風格）隨 preset 切換**——這是本課最重要的觀念之一
> - 風格 preset 對照表見 `10-industries-brief-library.md` § 跨風格演練段

---

## 分類總覽

| # | 骨架代號 | 中文名稱 | 視覺動線 | 代表案例調性 | 適用業種 |
|---|---|---|---|---|---|
| 1 | `product-left-text-right` | 商品左・文字右 | Z 型 | LUNÉA 精華液、HANAKO 手工皂 | 美妝保養、居家生活、醫美、保健品 |
| 2 | `mockup-right-text-left` | mockup 右・文字左 | F 型 | notero 筆記 App | App/SaaS、數位產品、線上工具 |
| 3 | `scene-bg-info-bottom` | 風景底・資訊下 | 上→下 | 瀨戶內慢旅 | 旅遊、地方創生、活動 |
| 4 | `product-center-props-around` | 商品中心・道具環繞 | 中央放射 | HARUKA CAFÉ 抹茶拿鐵 | 餐飲、甜點、禮盒、寵物 |
| 5 | `big-type-stack` | 大字堆疊・小圖輔助 | 左上→右下 | 課程招生、講座 | 教育、講座、海報、招生 |

---

## 骨架 1｜商品左・文字右（`product-left-text-right`）

### 視覺描述

畫面縱向分成兩半：左半是商品主視覺（精華液瓶、肥皂塊、保健品罐），右半是文字資訊層。視覺重心從商品圖開始（左），眼睛沿對角線移到右上標題，再往下讀副標、內文、特徵條列，最終落在 CTA。典型的 Z 型動線。

### 結構 JSON（L0）

```json
{
  "canvas": {"ratio": "1:1", "grid": "8pt"},
  "layout": "vertical-split 40/60, product-left-text-right",
  "elements": [
    {"role": "logo",      "position": "top-left",     "size": "xs"},
    {"role": "headline",  "position": "top-right",    "size": "xl", "weight": "bold"},
    {"role": "subcopy",   "position": "below-headline","size": "md"},
    {"role": "product",   "position": "left-center",  "size": "40%"},
    {"role": "badge",     "position": "product-overlap-top-right", "shape": "circle", "size": "sm"},
    {"role": "product_name", "position": "right-upper","size": "lg"},
    {"role": "category",  "position": "below-product_name","size": "xs"},
    {"role": "features",  "position": "right-middle", "size": "md", "count": 3, "icon": true},
    {"role": "cta",       "position": "right-bottom", "shape": "pill", "size": "md"}
  ],
  "visual_hierarchy": ["product", "headline", "features", "cta", "badge", "subcopy"]
}
```

### 文字佔位符對照

| 位置 | 日文佔位符 | 中文解釋 |
|---|---|---|
| top-right | 見出し（大） | 主標題 |
| below-headline | サブコピー | 副標 |
| right-upper | 商品名 | 商品名 |
| below-product_name | 商品カテゴリ / 説明 | 商品分類 / 簡介 |
| right-middle ×3 | 特徴・効果 1 / 2 / 3 | 特徵條列 |
| badge | バッジ / 割引・特典 / 期間・日付 | 圓徽章 |
| cta | CTA ボタン | 行動按鈕 |

### 適用情境舉例

- LUNÉA 美容精華液新品上市（發売記念 10% OFF）
- HANAKO 職人手工皂禮盒（母親節限定）
- 某保健品季節折扣

### 學員自跑引導（不備固定示範圖）

- 鼓勵學員用 Prompt A（見本檔末）跑 1 張 L4，再同對話跑 Prompt B 轉 L2
- 課堂示範時讓學員一起跑、各自看各自的結果
- 若要蒐集真實世界參考：IG hashtag `#スキンケア広告`、`#日系コスメバナー`、`#美容液`

---

## 骨架 2｜mockup 右・文字左（`mockup-right-text-left`）

### 視覺描述

左右對稱分割，但文字在左、產品 mockup 在右。視覺動線走 F 型：從左上主標開始閱讀，橫掃到右邊看 mockup，再回到左側中段讀次標與特徵標籤，最後到底部 CTA。mockup 通常是手機 / 平板 / 筆電截圖，帶陰影或邊框。

### 結構 JSON（L0）

```json
{
  "canvas": {"ratio": "1:1", "grid": "8pt"},
  "layout": "horizontal-split 55/45, text-left-mockup-right",
  "elements": [
    {"role": "subcopy_top",  "position": "top-left",      "size": "sm"},
    {"role": "headline",     "position": "upper-left",    "size": "xxl", "weight": "bold", "lines": 2},
    {"role": "emphasis",     "position": "below-headline","size": "lg",  "weight": "medium"},
    {"role": "mockup",       "position": "right-center",  "size": "45%", "type": "phone/tablet"},
    {"role": "app_icon",     "position": "middle-left",   "size": "xs"},
    {"role": "app_name",     "position": "next-to-icon",  "size": "md"},
    {"role": "body",         "position": "middle-left",   "size": "md"},
    {"role": "feature_tags", "position": "lower-left",    "size": "sm", "count": 3, "shape": "capsule"},
    {"role": "cta",          "position": "bottom-left",   "shape": "pill", "size": "md", "bg": "primary"}
  ],
  "visual_hierarchy": ["headline", "mockup", "app_name", "cta", "feature_tags", "body"]
}
```

### 文字佔位符對照

| 位置 | 日文佔位符 |
|---|---|
| top-left | サブコピー / ブランドメッセージ |
| upper-left | 見出し（大）（通常 2 行）|
| below-headline | 強調コピー（新しい価値など）|
| middle-left (app 區) | アプリアイコン / アプリ名 / 読み仮名 |
| middle-left (本文) | 本文テキスト（説明・価値訴求など）|
| lower-left ×3 | 特徴・機能 1 / 2 / 3 |
| cta | CTA ボタン（無料で始める など）|

### 適用情境舉例

- notero 筆記 App 上市宣傳
- 效率工具 SaaS 免費試用
- 健身 App 新功能公告
- 線上學習平台功能介紹

### 學員自跑引導

- 現場讓學員跑：主題「notero｜AI 筆記工具」、mockup 含任務清單畫面
- 真實世界對照：IG 搜 `#SaaSバナー`、`#アプリ広告`、`#UIデザイン`，或逛 Product Hunt、App Store 今日推薦

---

## 骨架 3｜風景底・資訊下（`scene-bg-info-bottom`）

### 視覺描述

上半部是風景或場景照鋪滿作底（海景、山景、老街、旅館），下半部放資訊區塊（白底或半透明底）。主標常常疊在風景上半部，圓形徽章壓在右側。下半部橫排 3 個特徵 icon + 說明，最底一顆粗體 CTA 按鈕。

### 結構 JSON（L0）

```json
{
  "canvas": {"ratio": "1:1", "grid": "8pt"},
  "layout": "vertical-60/40, scene-top-info-bottom",
  "elements": [
    {"role": "scene_bg",    "position": "top-full",       "size": "60%", "type": "landscape-photo"},
    {"role": "subcopy_intro","position": "overlay-top-left","size": "md"},
    {"role": "headline",    "position": "overlay-middle-left", "size": "xxl", "weight": "bold", "lines": 2},
    {"role": "subcopy_supp","position": "overlay-bottom-left", "size": "sm"},
    {"role": "badge",       "position": "overlay-top-right","shape": "circle","size": "md","content": "期間・日付 + 割引率"},
    {"role": "feature_grid","position": "bottom-center", "layout": "3-columns", "size": "md", "icon": true},
    {"role": "cta",         "position": "bottom-full",   "shape": "pill",  "size": "lg", "width": "80%"}
  ],
  "visual_hierarchy": ["scene_bg", "headline", "badge", "cta", "feature_grid", "subcopy_supp"]
}
```

### 文字佔位符對照

| 位置 | 日文佔位符 |
|---|---|
| overlay-top-left | サブコピー / 導入コピー / 共感を呼ぶ一文など |
| overlay-middle-left | 見出し（大）（常 2 行）|
| overlay-bottom-left | サブコピー / 補足コピー |
| badge | バッジ / キャンペーン情報 / 期間・日付 / 割引率 ％OFF |
| feature_grid ×3 | 特徴ポイント 1/2/3 + 説明テキスト + 補足テキスト |
| cta | CTA ボタン |

### 適用情境舉例

- 瀨戶內慢旅溫泉行程（期間限定 20% OFF）
- 地方創生活動招募
- 民宿夏季預訂
- 觀光局季節推廣

### 學員自跑引導

- 現場讓學員跑：主題「瀨戶內・ゆるり旅」、場景含海景 + 白色希臘式小屋
- 真實世界對照：IG 搜 `#旅行バナー`、`#観光プロモーション`、`#地方創生`；或逛 JR 東日本 / JTB 季節活動頁

---

## 骨架 4｜商品中心・道具環繞（`product-center-props-around`）

### 視覺描述

商品主視覺放在畫面中央（飲品杯、甜點盤、寵物食品），周圍散佈輔助道具（原料、湯匙、葉子、小包裝）強化產品故事。文字在左半，分主標 / 新品 accent / 本文 / 價格 / CTA。常見季節限定、道具暗示口味原料（抹茶粉、茶葉、水果切片）。

### 結構 JSON（L0）

```json
{
  "canvas": {"ratio": "1:1", "grid": "8pt"},
  "layout": "asymmetric, product-center-text-left",
  "elements": [
    {"role": "label_tag",    "position": "top-left",      "size": "sm", "shape": "rect-tag"},
    {"role": "headline",     "position": "upper-left",    "size": "xxl","weight": "bold", "lines": 2},
    {"role": "accent",       "position": "below-headline","size": "lg", "style": "italic/cursive"},
    {"role": "body",         "position": "middle-left",   "size": "md", "lines": 3},
    {"role": "product",      "position": "center-right",  "size": "50%","type": "photo-realistic"},
    {"role": "prop_left",    "position": "left-bottom",   "size": "xs", "type": "ingredient-bowl"},
    {"role": "prop_tool",    "position": "bottom-center", "size": "xs", "type": "spoon/utensil"},
    {"role": "prop_leaves",  "position": "top-right",     "size": "xs", "type": "decoration"},
    {"role": "price_label",  "position": "lower-left",    "size": "sm"},
    {"role": "price",        "position": "lower-left",    "size": "xl", "weight": "bold", "count": 2},
    {"role": "cta",          "position": "bottom-left",   "shape": "pill", "size": "md"},
    {"role": "badge",        "position": "bottom-right",  "shape": "circle","size": "sm", "content": "補足テキスト"}
  ],
  "visual_hierarchy": ["product", "headline", "price", "accent", "cta", "props"]
}
```

### 文字佔位符對照

| 位置 | 日文佔位符 |
|---|---|
| top-left | ラベル / タグ（例：季節限定）|
| upper-left | 見出し（大）|
| below-headline | アクセントコピー（例：New!）|
| middle-left | 本文テキスト（商品説明、味やこだわりなど）|
| lower-left | 価格ラベル（例：税込）+ 価格（大）|
| cta | CTA ボタン（例：メニューをチェック）|
| badge | バッジ / テイクアウト可 / 補足テキスト |

### 適用情境舉例

- 弄一下咖啡工作室春季抹茶拿鐵
- 伴手禮禮盒（茶葉、和菓子）
- 寵物食品新口味
- 甜點外帶新品

### 學員自跑引導

- 現場讓學員跑：主題 HARUKA CAFÉ 抹茶ティラミスラテ、道具含抹茶粉盤、湯匙、茶葉
- 真實世界對照：IG 搜 `#日系カフェ`、`#季節限定メニュー`、`#職人スイーツ`；或逛你追蹤的 7-11、全家季節新品 banner

---

## 骨架 5｜大字堆疊・小圖輔助（`big-type-stack`）

### 視覺描述

文字為主角，多行大字粗體堆疊佔滿上半或左半；小圖或裝飾圖放在角落、邊緣或下方作點綴，不喧賓奪主。視覺動線從大字最上行開始，逐行下讀，最後落在 CTA。常見課程招生、活動公告、海報。

### 結構 JSON（L0）

```json
{
  "canvas": {"ratio": "1:1", "grid": "8pt"},
  "layout": "text-dominant-70, image-accent-30",
  "elements": [
    {"role": "date_tag",     "position": "top-left",     "size": "sm", "shape": "line-highlight"},
    {"role": "eyebrow",      "position": "below-date",   "size": "md"},
    {"role": "headline_1",   "position": "upper-left",   "size": "xxxl","weight": "bold"},
    {"role": "headline_2",   "position": "below-h1",     "size": "xxxl","weight": "bold"},
    {"role": "headline_3",   "position": "below-h2",     "size": "xxl", "weight": "bold", "color": "accent"},
    {"role": "subcopy",      "position": "middle-left",  "size": "md",  "lines": 2},
    {"role": "accent_image", "position": "bottom-right", "size": "20%", "type": "small-illustration"},
    {"role": "meta_info",    "position": "bottom-left",  "size": "xs",  "count": 3, "type": "date/location/instructor"},
    {"role": "cta",          "position": "bottom-center","shape": "pill","size": "lg"}
  ],
  "visual_hierarchy": ["headline_1", "headline_2", "headline_3", "cta", "eyebrow", "accent_image"]
}
```

### 文字佔位符對照

| 位置 | 日文佔位符 |
|---|---|
| top-left | 日付 / 期間（線條 highlight）|
| below-date | アイブロウ（小前置語）|
| upper-left ×3 | 見出し 1 / 2 / 3（大、多行堆疊）|
| middle-left | サブコピー |
| meta_info ×3 | 日時 / 場所 / 講師 |
| cta | CTA ボタン（例：今すぐ申し込む）|

### 適用情境舉例

- 工作室課程招生（商業用圖片生成）
- 線上講座公告
- 市集/展覽海報
- 認證班開課宣傳

### 學員自跑引導

- 現場讓學員跑：主題「弄一下工作室｜商業用圖片生成 工作坊」
- 真實世界對照：IG 搜 `#セミナー告知`、`#ワークショップ ポスター`、`#イベントバナー`；或逛你追蹤的線上課程品牌 IG

---

## 骨架 × 業種配對建議表

| 業種 | 首選骨架 | 次選骨架 |
|---|---|---|
| 美妝保養 | 1 商品左 | 4 商品中心 |
| 餐飲 | 4 商品中心 | 5 大字堆疊 |
| App / SaaS | 2 mockup 右 | 5 大字堆疊 |
| 旅遊 | 3 風景底 | 5 大字堆疊 |
| 教育課程 | 5 大字堆疊 | 2 mockup 右 |
| 活動講座 | 5 大字堆疊 | 3 風景底 |
| 醫美 / 健康 | 1 商品左 | 2 mockup 右 |
| 寵物 | 4 商品中心 | 1 商品左 |
| 居家生活 | 1 商品左 | 4 商品中心 |
| 健身運動 | 2 mockup 右 | 5 大字堆疊 |

---

## 🎯 圖片資產策略｜引導發現法（不備固定示範圖）

**本課設計決策（2026-04-24 更新）**：**不產製固定示範圖**，改走引導發現法。

### 為什麼不備固定示範圖？

1. **AI 生圖本質不穩定**——同 prompt 跑 3 次結果都不同，若給固定示範圖，學員會以為「跑不出那樣是自己失敗」
2. **骨架是結構、不是長相**——真正的教學目標是「看懂結構」，不是「做出像老師那張的圖」
3. **學員實跑 > 看老師的圖**——自己跑才會體驗到模型行為，知道如何修 prompt

### 改走什麼路線？

- **學員自跑**：課堂現場用以下 Prompt A / B 跑，自己看自己的輸出
- **IG / Pinterest 真實案例**：用 hashtag 引導學員找真實商業作品當教材
- **ASCII / 黑白線框圖**：`CH2-1` 教案用純文字結構示意教骨架，永不過時
- **預期差異聲明**：每處提及 AI 生圖必加「每次輸出會不同、重點是結構」

### 下列 Prompt A / B 保留作為「學員自跑範例」

教案引導學員**現場複製貼上跑**，體驗 L4 → L2 轉換。不預期產出統一結果，只求體驗工作流。

### 範例 Prompt A（L4 完稿，丟 Gemini Banana Pro 或 ChatGPT GPT-image-2）

```
請生成一張 1:1 日系商業橫幅：
業種：美妝保養
品牌：LUNÉA（虛構精品美容品牌）
商品：モイストリペアセラム（Moist Repair Serum，修護精華液）30mL
客群：25-40 歲女性、注重敏感肌護理
訴求：発売記念 10% OFF，限定 5/31 止
必要元素：
- 主標：素肌が、目を覚ます。
- 副標：うるおい満ちる、透明ハリ肌へ。
- 商品照（紫色玻璃滴管瓶）置於左側
- 圓形徽章「発売記念 10%OFF 5.31 まで」置於瓶子右上
- 3 項特徵條列（高保湿セラミド配合 / 透明感サポート / 敏感肌にもやさしい 6つのフリー処方）
- CTA「詳しくはこちら」置於左下
風格：日系電商 LP，配色 ≤ 3 色（淡紫 + 米白 + 深紫文字），字體階層清楚
```

### 範例 Prompt B（L2 視覺化線稿，同對話內接續）

```
請將剛才那張圖轉為 Level 2 視覺化 wireframe：

【必須保留】
- 精華液瓶的完整線稿輪廓（外形 + 滴管頭 + 標籤框）
- 圓形徽章的幾何形狀與位置
- 3 個特徵 icon 的幾何輪廓
- CTA 膠囊按鈕的形狀
- 背景水珠的極簡圓圈暗示

【必須移除】
- 所有色彩（全圖灰階）
- 所有照片質感、漸層、反光
- 所有原始文字內容

【文字佔位符對照】
- 主標 → 見出し（大）
- 副標 → サブコピー
- 商品名 → 商品名（LUNÉA / moist repair serum 改為佔位）
- 商品分類 → 商品カテゴリ / 説明
- 容量 → カテゴリ / 容量表記
- 徽章 → バッジ / 割引・特典 / 期間・日付
- 特徵 → 特徴・効果 1 / 2 / 3 + 説明テキスト
- CTA → CTA ボタン
- Logo → ロゴ

【風格】
Figma wireframe kit + 極簡白描手繪混合，細黑線條（0.5-1pt），背景純白，允許 5-10% 灰階填色塊暗示層次。

【尺寸】1:1
```

### 備援：若 Gemini Banana Pro 不可用

- **備案 A**：ChatGPT Plus + GPT-image-2 走同樣雙階段流程
- **備案 B**：ChatGPT Free（GPT-image-1）單次生成能力較弱，建議 L4 與 L2 分開產，L2 階段用英文 prompt 精確度較高
- **備案 C**：開源路線 Flux.2 + ControlNet canny edge 抽邊（需技術底，不適合主教路線）

---

## 給 course-designer 的提醒

1. **圖片資產未備齊前，CH2-1 / CH3-1 / CH4-1 / PRAC2 / PRAC3 / PRAC4 只能寫教案草稿，不能進 HTML 階段**
2. **L0 JSON schema 是本課的智慧財產**，所有 prompt 模板設計應圍繞此 schema 展開（讓學員學會吃 JSON、吐 JSON）
3. **每個骨架的「視覺動線 + 文字佔位符 + 適用業種」三件套**是 CH2-1 的核心教學物，請勿簡化
4. **骨架 × 業種配對表**是 CH7 跨產業套用的教學骨幹，務必沿用
