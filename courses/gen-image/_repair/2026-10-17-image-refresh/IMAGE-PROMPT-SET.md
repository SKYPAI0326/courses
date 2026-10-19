# 2026-10 Course Visual Prompt Set

## Shared production contract

Raster assets were generated with the built-in image generator, then copied into `assets/course-visuals/2026-10/`. The reusable prompt frame was:

> Create a course-owned commercial visual for a Taiwanese generative-image course. Preserve the named channel, composition skeleton, aspect-ratio purpose, subject, lighting, palette, and copy-safe zones. Use fictional or unbranded products and people. Do not reproduce a real logo, trademark, copyrighted character, public figure, watermark, medical claim, or unverifiable performance claim. Avoid long generated copy; use blank hierarchy bars or short exact teaching labels when text is essential. Produce a polished 2026 commercial-art-direction reference.

Each PNG has a stable `P-vNN` prompt ID. Its normalized, reproducible prompt recipe is the shared production contract above, followed by the matching directive below and the asset role recorded in `IMAGE-MANIFEST.tsv`. The exact generator output filename, final checksum, and any later edit are recorded in `ASSET-PROVENANCE.tsv`; this is the durable course record even when the interactive tool transcript is unavailable.

The PNG outputs use the original lesson role as the per-asset directive:

- `P-v01–P-v08`: one fictional beverage campaign expressed through eight distinct composition skeletons: hero, banner, social, series, gift box, close-up, promotion, and lifestyle.
- `P-v09–P-v10`: visually contrast a vague brief with a structured six-part brief.
- `P-v11`: product-right / copy-left L4 matcha-tiramisu-latte commercial finish.
- `P-v13–P-v15`: keep the same left-copy/right-product-or-mockup wireframe while transferring it to skincare, online-course, and a physical travel-retail kit. `P-v15` must not depict a destination landscape; it demonstrates a travel product that genuinely fits the product slot.
- `P-v16–P-v18`: one fictional cafe seasonal system for spring matcha, summer iced coffee, and winter cocoa.
- `P-v22–P-v24`: six-tile minimal, organic, and restrained-luxury lookbooks.
- `P-v25`: intentionally leak the exact internal instruction `FONT: MINCHO` into the artwork.
- `P-v26`: intentionally show duplicated subtitle rows and nonsensical glyph fragments.
- `P-v27`: intentionally produce only an attractive stock photo with no commercial hierarchy.
- `P-v28`: intentionally collide quiet premium editorial art direction with a loud red-yellow discount flyer.
- `P-v29`: intentionally crowd more than twelve competing elements into one frame.
- `P-v30`: intentional single-variable NG counterpart to `P-v15`: preserve the same physical travel kit, object positions, left-copy/right-product skeleton, camera, and light; change only the brand surface styling to matcha green, tea-leaf motifs, and washi texture so legacy visual pollution is causally visible.
- `P-v31–P-v33`: fictional product presets for Japanese craft, Korean refined, and American vintage directions.
- `P-v38–P-v42`: five square capstone heroes for probiotic wellness, AI notes app, spring cafe drink, AI design course, and a fictional island-travel brand. `P-v42` is a synthetic atmosphere image, not evidence of any real destination.
- `P-v45`: oat-milk lifestyle breakfast in a compact Taipei apartment, cropped hand only.
- `P-v46`: marketplace-ready unbranded kraft coffee bag on pure white.
- `P-v47`: premium coffee-bag studio hero on deep-brown velvet with gold rim light.
- `P-v48`: Mid-Autumn coffee gift set with osmanthus, round lantern, mooncake, three blank pouches, filters, scoop, and card; explicitly remove Christmas cues.
- `P-v49`: ecommerce hero with copy-ready bars, CTA shape, product bag, origin/rating cards, and shipping strip.
- `P-v50`: cold-brew bottle label mockup with condensation, icon, dividers, and blank specification hierarchy.
- `P-v51`: 21:9 website hero with the short exact headline `COFFEE REIMAGINED`, blank subtitle, CTA shape, bag, beans, and roaster.
- `P-v52`: 1:1 sale KV with exact numerals `11.11`, central unbranded bag, beans, and a blank gold claim badge.
- `P-v53`: extreme-negative-space poster with cup line icon and exact statement `SLOW IS BETTER`.
- `P-v54`: 2:3 editorial cover with exact `STUDIO QUARTERLY` and `NO.04`, bag anchor, and blank topic lines.
- `P-v55`: six-zone identity board using an original abstract bean-and-circle mark, swatches, type bars, mockups, and cafe mood image.
- `P-v56`: bilingual-event hierarchy at 70/30 visual weight with coffee and plant props; no real event logo.
- `P-v57`: 4:5 five-topic coffee-trends bento grid with exact short header `COFFEE TRENDS 2026` and copy-ready bars.
- `P-v58`: intentionally biased two-column plan comparison, with one plain gray option and one oversized glowing gold option.
- `P-v59`: 4:5 five-step hand-pour sequence with exact short header `HAND-POUR IN 5 STEPS`, numbered icons, arrows, and blank copy bars.
- `P-v60`: fictional Asian male cafe founder around age 30, not resembling a public figure, in a real work context.
- `P-v61`: original coffee-bean mascot in a 4×2 sheet with eight distinct expressions; no copyrighted-character resemblance.
- `P-v62`: 3×2 spring-fashion lookbook with exactly six distinct fictional adult East Asian models, one per panel; include masculine, feminine, and androgynous presentations, visibly varied ages and body types, different faces and hairstyles, cream-and-sage outfits, and a coherent editorial grade.

## Deterministic diagrams

`v12`, `v20`, `v21`, and `v34–v37` are course-owned SVG diagrams rather than probabilistic raster generations. They preserve readable structure for the L2 wireframe, PM responsibilities, six-part brief, and four composition variants.

## Release rule

Generated copy is illustrative. Any external publication still requires human checks for spelling, product truth, rights, claims, accessibility text, target-platform dimensions, and brand approval.
