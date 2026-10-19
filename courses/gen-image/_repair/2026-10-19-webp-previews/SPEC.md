# Gen-image WebP preview specification

- Date: 2026-10-19
- Authorized request: replace learner-page raster displays with WebP previews; clicking any course image opens its original file in a new tab.
- Scope classification: narrowly authorized HTML behavior and asset-source change. No visible learning copy, page order, image order, dimensions, `alt`, `loading`, inline style, navigation, or lesson wrappers may change.

## Required behavior

1. Convert the 61 unique PNG files referenced by top-level learner HTML to same-dimension WebP previews with `cwebp -q 90 -mt`.
2. Keep every PNG original at its current path. Display the sibling `.webp`; link to the original `.png`.
3. Keep the 10 SVG originals as SVG displays. Link each SVG display to the same SVG original.
4. Wrap all 79 `<img>` occurrences in an anchor with `target="_blank"` and `rel="noopener"`. If an image already has an anchor, update that anchor instead of nesting another anchor.
5. Give each image anchor an accessible label composed from the existing image `alt` plus `開啟原圖（新分頁）`.
6. Remove the workshop page's image-only `download` behavior because the requested behavior is opening a new tab.
7. Do not convert or rewrite backups, validation screenshots, editable source HTML, temporary files, or unreferenced images.

## Acceptance criteria

- 61 unique WebP previews exist, decode successfully, retain the original dimensions, and are smaller than their PNG originals.
- Combined WebP preview size is at most 15 MiB.
- The 29 top-level pages containing images have 79 image occurrences; every occurrence has an existing local display source and original target.
- All raster `<img src>` values end in `.webp`; all raster anchor targets end in `.png`.
- SVG display sources and original targets remain `.svg`.
- Every image anchor has `target="_blank"`, `rel` containing `noopener`, no `download`, and no nested anchor.
- Visible text, image `alt`, `loading`, inline style, image order, and course wrappers remain unchanged.
- Course structure, lint, image-refresh validation, representative browser rendering, keyboard activation, and new-tab target checks pass.
- No commit or push occurs without a separate user request.
