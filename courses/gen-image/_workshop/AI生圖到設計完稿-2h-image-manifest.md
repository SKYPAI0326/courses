# 兩小時工作坊圖片素材與提示詞紀錄

**建立日期**：2026-10-17  
**生成紀錄核對**：2026-10-22
**用途**：`workshop-2h-poster-social.html` 的獨立教學素材  
**生成方式**：Codex 內建 `image_gen`  

## 原創與使用邊界

- `共同筆記.pdf` 只用來分析暖白留白、自然材質、側光商品攝影、商品主體與 CTA 等視覺語法。
- 沒有把 PDF 內的圖片、品牌、人物、提示詞或具體版面當作生成輸入。
- 本工作坊使用虛構品牌「島嶼果日」與虛構商品「炙香鳳梨茶果禮盒」。
- 包裝採霧面象牙白紙盒、茶葉綠飾帶、焦糖橘圓日與葉片圖形；不對應真實品牌。
- 正式中文、價格、成分與行動按鈕交由 Canva 排版；AI 圖片不承擔可驗證的商品宣稱。

## 生成事件與輸出身分

以下紀錄把 `image_gen` 生成事件輸出與課程 workspace 素材做 SHA-256 比對。七筆均為完全相同檔案；這能證明目前素材對應到本次生成事件，但不取代參考 PDF 的獨立相似度檢查。

| Workspace 素材 | `image_gen` 事件輸出 | SHA-256 | 比對 |
|---|---|---|---|
| `island-day-product-anchor.png` | `exec-16917278-437c-498e-ba73-7a2bb20b0f3b.png` | `8a918a4530bf10f99a82ecd41303b0cb8ca28a4669eb4652bf94dd8e638e6ab6` | MATCH |
| `c1-bento-campaign.png` | `exec-9ffe4437-c025-4f62-b681-64bcd756cdb2.png` | `3f555c94a5ea7b7c920c0de6d55c04ce2d30a536ebe5de42920132e52fdb0f55` | MATCH |
| `c2-fair-comparison.png` | `exec-016625e8-a8cc-4b84-9a84-34168e178957.png` | `67b8b70da111c51c96e7cd3bf70bfa59d16ee6849404001d54b8dcabeac99651` | MATCH |
| `c3-process-story.png` | `exec-db6d3517-78c5-4155-8766-a14f6749e879.png` | `b1c0015150d899a05d0807ab71feefa29391a44706dc91538ecf6ca843445dfe` | MATCH |
| `c4-founder-story.png` | `exec-5f46c47d-04e5-484f-b239-26e8fa76cb59.png` | `f33362ff1da45d3bf7c9b37dcb853ac5cb1c3152756eeeea258158ef4029615d` | MATCH |
| `c5-mascot-stickers.png` | `exec-3f91bf6e-82e0-4d92-b527-64f763cd628b.png` | `ab8b0d18841e3ffe1d5dfd9337e6d5c4b38b1103efd3bf985da501bdb89c5958` | MATCH |
| `c6-product-lookbook.png` | `exec-76105652-f0ae-49a5-a1de-cc6b84f56b5f.png` | `c43aa8b6989c5caf7e2fb216b0121d66e7e4e6340ee185d290bbdcea04efc14a` | MATCH |

## 品牌視覺契約

| 欄位 | 固定設定 |
|---|---|
| 商品 | 炙香鳳梨果乾與烏龍茶點心禮盒 |
| 包裝 | 象牙白霧面長方盒、兩個紙質夾鏈袋、茶葉綠直向飾帶、焦糖橘封印 |
| 原創圖形 | 圓日、葉片與緩坡構成的抽象符號，無文字 |
| 色板 | 暖象牙白、茶葉綠、焦糖橘、淺木與天然鳳梨金 |
| 材質 | 未塗佈紙、亞麻、淺木、陶器、真實果乾纖維 |
| 光線 | 左上自然窗光、柔和方向陰影 |
| 禁止 | 真實商標、名人、公眾人物、亂碼、價格、無法證實的宣稱、水印 |

## 圖片與最終提示詞

### 1. 商品基準圖

**檔案**：`img/workshop2h/island-day-product-anchor.png`

```text
Use case: product-mockup
Asset type: master product anchor for an original commercial social-media campaign
Create an original premium Taiwanese roasted pineapple and tea snack gift set.
Show one matte ivory rectangular gift box, two slim paper pouches and a ceramic dish of golden dried pineapple.
Use an original abstract orange sun-and-green-leaf symbol without letters, a tea-green band and a burnt-orange seal.
Warm ivory plaster, linen and pale wood; vertical 4:5; product slightly right of center; clean headline space upper-left.
Photorealistic premium product photography with warm natural side light.
No readable text, numbers, people, real logos, glass jar, mango or copied layout.
```

### 2. Bento Grid 便當格資訊圖

**檔案**：`img/workshop2h/c1-bento-campaign.png`  
**參考輸入**：商品基準圖，只用來維持包裝一致。

```text
Use case: ads-marketing
Create a vertical 4:5 asymmetric Bento Grid with one dominant hero cell and four smaller cells.
Hero: complete gift set. Smaller cells: pineapple ingredient macro, tea pairing, portable pouch and wrapped gifting scene.
Keep gutters, packaging, side light and color palette consistent. Reserve headline and CTA zones.
No readable text, people, real logos, extra brands or copied layout.
```

### 3. Comparison 對比資訊圖

**檔案**：`img/workshop2h/c2-fair-comparison.png`  
**參考輸入**：商品基準圖。

```text
Use case: ads-marketing
Compare two valid choices fairly: a compact daily snack set and a larger gifting set.
Use equal left-right columns, identical camera height, lighting and neutral background.
Provide three empty comparison bands plus a bottom decision zone.
No winner badge, unsupported claim, readable text, real logo or unequal visual treatment.
```

### 4. Step by Step 步驟教學圖

**檔案**：`img/workshop2h/c3-process-story.png`  
**參考輸入**：商品基準圖。

```text
Use case: ads-marketing
Create a vertical five-stage process story: ripe pineapple at orchard, hand slicing, low-temperature drying, tea pairing and finished packaged gift set.
Use a clean sequential collage with empty caption zones and a clear reading path.
The final package is the strongest concluding image and must match the product anchor.
No readable text, identifiable faces, factory branding or copied layout.
```

### 5. Founder Portrait 創辦人肖像

**檔案**：`img/workshop2h/c4-founder-story.png`  
**參考輸入**：商品基準圖。

```text
Use case: photorealistic-natural
Create a documentary-style portrait of an entirely fictional Taiwanese woman in her mid-thirties running a small pineapple-and-tea craft studio.
She inspects one pouch while the complete gift set remains visible on the worktable.
Natural skin and fabric, oatmeal linen shirt, tea-green apron, warm side window light and clean headline space.
No celebrity resemblance, public figure, exaggerated smile, glossy beauty retouching, extra brand or readable text.
```

### 6. Sticker Set 角色貼圖組

**檔案**：`img/workshop2h/c5-mascot-stickers.png`  
**參考輸入**：商品基準圖的色彩與圓日、葉片語彙。

```text
Use case: illustration-story
Design one original rounded golden pineapple-snack mascot with one tea-green leaf sprout and a burnt-orange sun badge.
Show eight consistent poses: greeting, thank you, cheering, concentrating, tired, tea break, packing a gift and celebrating.
Use refined flat hand-drawn lines, muted colors and subtle paper grain in a 4-by-2 grid on one uniform warm-ivory background.
No vignette, glow, gradient, dark corner, text, speech bubble, copyrighted-character resemblance, neon color or inconsistent accessory.
```

### 7. Lookbook Grid 系列拼貼

**檔案**：`img/workshop2h/c6-product-lookbook.png`  
**參考輸入**：商品基準圖。

```text
Use case: ads-marketing
Create a vertical 4:5, 3-by-2 product lookbook showing office snack, afternoon tea, gift wrapping, weekend picnic, host gift and pantry display.
Keep the package visible in every cell with consistent camera height, scale, side light and color treatment.
No visible faces, real logos, third-party brands, fashion campaign, urban graffiti or copied layout.
```

### 8. L4 商業完稿與 L2 線稿

**檔案**：`img/workshop2h/l4-commercial-poster.png`、`img/workshop2h/l2-commercial-wireframe.svg`  
**可編輯來源**：`img/workshop2h/l4-commercial-poster-source.html`

- L4 使用商品基準圖，加上確定性的 HTML／CSS 中文排版、品牌符號與 CTA，再以 1080×1350 輸出為 PNG。
- L2 依 L4 的品牌、標題、說明、CTA 與商品區位置重建灰階骨架。
- 兩張圖用來比較色彩表象與版面結構，不引用原課程的 L4／L2 圖片。

