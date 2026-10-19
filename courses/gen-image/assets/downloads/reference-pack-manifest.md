# 課程 Reference Pack Manifest

版本日期：2026-10-16

## 授權與用途

- 產製者：本課修復流程透過 Codex 內建 OpenAI 圖像生成工具產製。
- 使用者授權：僅供「商業用圖片生成」課程教學、課堂示範與學員練習。
- 不包含：對外商用、轉售、素材庫散布或替第三方背書。
- 人物同意：不適用；6 張圖片均刻意不含人物或可辨識身份。
- 品牌／商標：prompt 明確排除品牌、商標、logo、角色與正式文字；仍須由使用者在每次練習前目視確認。
- 來源證據：本 manifest、原始生成 prompt、生成日期、專案內檔案與 SHA256。
- C2PA／Content Credentials／SynthID：未主張已嵌入或可由本機驗證；不能以沒有可見標記推論「非 AI」。教學使用下以 manifest 與 SHA256 作主要來源紀錄。

## READY 清單

| ID | 檔案 | 尺寸 | 練習角色 | SHA256 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| REF-01 | [course-ref-01-coffee-square.png](../reference-pack/course-ref-01-coffee-square.png) | 1254×1254 | 中央商品、上方留白、前中後景 | `5ffa2e110b34b1cd593fe65811ad312dcd937203c5053c64427fbcb929bb1e05` | READY_COURSE_ONLY |
| REF-02 | [course-ref-02-skincare-portrait.png](../reference-pack/course-ref-02-skincare-portrait.png) | 1122×1402 | 非對稱主體、左上留白、材質 | `f4852438667c179ed88bc38219a025e4b3c442b10c7704d9b75fe4528b7107e1` | READY_COURSE_ONLY |
| REF-03 | [course-ref-03-travel-landscape.png](../reference-pack/course-ref-03-travel-landscape.png) | 1672×941 | 引導線、左三分主體、天空安全區 | `24b451836861c41fa77ac73779c50841ab7205a42465ab7573ebee163b60b0e4` | READY_COURSE_ONLY |
| REF-04 | [course-ref-04-learning-square.png](../reference-pack/course-ref-04-learning-square.png) | 1254×1254 | 右主體、左負空間、桌面層次 | `7b7dfe57ff15b9e6f2b3117c0aef010a2374917c3063bf5a10d13ce39c25128d` | READY_COURSE_ONLY |
| REF-05 | [course-ref-05-drink-bento.png](../reference-pack/course-ref-05-drink-bento.png) | 1122×1402 | 俯拍模組、中央焦點、色彩節奏 | `1fc1b6cae134cfd791bd1313e8b2f61eaa433a4e3c1eddf6b9ff4ab173c70272` | READY_COURSE_ONLY |
| OFFLINE-01 | [course-offline-candidate-sheet.png](../reference-pack/course-offline-candidate-sheet.png) | 1536×1024 | 同骨架三風格、線稿、跨業種反控與 release QA | `94d0242e6196669bf7c19117147b1674953123a47dd9e43b8f5d9620299980b0` | READY_COURSE_ONLY |

## 最終生成 Prompt Set

### REF-01｜Coffee square

```text
Create a polished 1:1 commercial still life for a fictional specialty coffee product: warm ivory studio backdrop with subtle paper texture and soft arched shadow; one matte cream coffee pouch with a completely blank label, a small ceramic cup, and roasted coffee beans; realistic editorial product photography; product centered slightly below midpoint with strong negative space above; ivory, espresso brown, muted terracotta. No people, hands, readable text, letters, numbers, logo, trademark, watermark, recognizable brand, or copyrighted character.
```

### REF-02｜Skincare portrait

```text
Create a polished 4:5 commercial still life for a fictional skincare serum: pale stone studio, translucent acrylic panel, one frosted glass dropper bottle with a completely blank label, two smooth stones, and a green leaf; realistic premium product photography; asymmetric layout with product in lower-right third and negative space in upper-left; cool white, sage, soft gray. No people, hands, text, logo, trademark, watermark, recognizable brand, or copyrighted character.
```

### REF-03｜Travel landscape

```text
Create a 16:9 fictional outdoor travel campaign image: invented alpine lake, layered blue hills, winding shoreline, open sky; one plain orange canoe with no markings and no people; realistic travel editorial photography; shoreline leads from lower foreground to distance, canoe on left third, broad clean sky; lake blue, pine green, warm sand, orange accent. No recognizable landmark, buildings, people, text, logo, trademark, watermark, flag, or copyrighted character.
```

### REF-04｜Learning square

```text
Create a 1:1 promotional still life for a fictional online learning service: tidy light-wood desk against muted blue wall; generic laptop showing blank abstract color blocks, notebook, pencil, desk lamp; realistic workspace photography; laptop on right, notebook creates lower-left diagonal, upper-left negative space; navy, sky blue, cream, wood. No people, hands, text, logo, trademark, watermark, recognizable software interface, or copyrighted character.
```

### REF-05｜Drink bento

```text
Create a 4:5 overhead commercial arrangement for a fictional sparkling drink: matte peach surface; three slim blank aluminum cans in pastel colors, citrus slices, mint, ice; realistic product photography; modular bento-like arrangement with one focal can and four supporting zones; peach, lemon, mint, lavender. No people, hands, text, logo, trademark, watermark, recognizable brand, or copyrighted character.
```

### OFFLINE-01｜Six-panel candidate sheet

```text
Create a single high-resolution course-only visual worksheet as a clean 3-column by 2-row contact sheet, with six equal panels and thin neutral gutters. No text, letters, numbers, logos, watermarks, people, or recognizable brands. All panels share one layout skeleton: object on the right, empty headline zone upper left, empty badge placeholder lower left. Top row shows the same fictional coffee product in natural minimal, Swiss editorial, and American retro presets. Bottom row shows the grayscale wireframe, the same skeleton adapted to a fictional skincare serum, and the same skeleton adapted to a fictional lake travel visual. Professional educational reference sheet, precise alignment, 3:2 overall ratio.
```

## 學員使用流程

1. 只從 READY 清單選圖，不另存 IG、Pinterest 或電商圖片。
2. 先指定 reference 角色：商品、構圖、品牌或場景；一張圖不要同時負責全部角色。
3. 列出必須保留、可以改變、禁止帶入三欄。
4. 生成或分析後，記錄平台／版本、日期、prompt、reference ID 與人工修改。
5. 若結果出現疑似 logo、文字、人物或相似 trade dress，停止使用並換另一張 reference。
6. 平台不可用時，改用 [offline candidate workbook](offline-candidate-workbook.md) 與 OFFLINE-01 完成同一組比較、線稿判讀、反控與 release gate 證據。

