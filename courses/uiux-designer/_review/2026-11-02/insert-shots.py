"""把 assets/shared/ui/ 的操作截圖插進承作稿（插在指定段落或步驟之後）。可重複執行：已插入的圖不會重複。"""
from pathlib import Path
R = Path(__file__).parent / 'round1'
U = '../assets/shared/ui/'
SHOTS = [
 ('A1', '在檔案首頁進入 Drafts', 'figma-drafts-design-button', '草稿頁：左側選 Drafts，右上角點 Design 建立設計檔（紅框）'),
 ('A1', '在檔案首頁進入 Drafts', 'figma-new-file-left-rail', '新檔可能先開對話面板；點最左側圖示列的 File（紅框）才會看到 Pages 與 Layers'),
 ('A1', '1. 按 **F** 畫一個 Frame', 'figma-editor-overview', '編輯器三區：左側 Layers、右上 Design／Prototype 分頁、Frame 的 W 與 H 欄（紅框）'),
 ('A1', '2. 選取登入畫面，將 Fill', 'figma-fill-hex', '點 Fill 的色塊開啟取色器，在 Hex 欄輸入色碼（紅框）'),
 ('A1', '5. 選取「登入工作室」，點 Typography', 'figma-text-style-create', 'Typography 右上的樣式圖示 → Text styles 面板的 ＋（Create style）；下方紅框是字型、字重、字級與行高'),
 ('A2', '1. 選取 `Screen / Login`（手機登入畫面），在右側 Design', 'figma-layout-guide-add', 'Layout guide 區塊的 ＋（Add layout guide）；新增後預設類型是 Grid（紅框）'),
 ('A2', '2. 把類型下拉選單', 'figma-layout-guide-columns', '類型改成 Columns 後，依序填 Count、Type、Margin、Gutter（紅框）'),
 ('A3', '3. 建立 `Label`（按鈕文字），輸入「登入」後按 **Shift+A**', 'figma-auto-layout-panel', 'Shift+A 後右側出現 Auto layout：Flow 方向、寬高的 Hug、Gap 與 Padding（紅框）'),
 ('A4', '2. 依規格表檢查外框', 'figma-create-component-menu', '在按鈕上按右鍵，選 Create component（紅框）'),
 ('A4', '5. 回到左側 **Assets**', 'figma-assets-created-in-file', '左側 Assets → Created in this file，把元件拖到畫面上（紅框）'),
 ('A4', '10. 選取完成按鈕', 'figma-go-to-main-component', '使用處右側「From this file」旁的箭頭就是 Go to main component（紅框）'),
 ('A4', '4. 選取取消按鈕，點右側元件名稱列的', 'figma-reset-instance', '元件名稱列的 ⋯ → Reset instance（紅框）'),
 ('A5', '1. 在元件區的 `Button / Base` 上按右鍵', 'figma-add-variant-menu', '右鍵 → Main component → Add variant（紅框）'),
 ('A5', '2. 點虛線框下方的', 'figma-component-set', '元件集外框是紫色虛線，下方 ＋ 可再加版本；右側 Properties 顯示屬性（紅框）'),
 ('A5', '5. 選取元件集，在 Properties', 'figma-create-property-menu', 'Properties 的 ＋ 開啟 Create property 選單：Variant、Text、Boolean、Instance swap、Slot（紅框）'),
 ('A5', '7. 選取元件集，在 Properties 點', 'figma-text-property-dialog', 'Create property 視窗：填 Name 與 Value，按 Create property（紅框）'),
 ('A5', '8. 逐一選取四個版本內的', 'figma-apply-property', '選文字層後，Content 欄旁的 Apply variable/property 圖示 → 選 Label（紅框）'),
 ('B1', '5. 選取流程起點並把「Flow 1」改名', 'figma-overflow-flow-start', '選起點畫面時，Prototype 分頁上方的 Flow starting point 可以直接改名（上方紅框）'),
 ('B1', '7. 開啟 Preview', 'figma-preview-menu', '播放鍵旁的小箭頭：Present 另開分頁，Preview（⇧Space）在編輯器內預覽（紅框）'),
 ('B2', '2. 切到右側 Prototype 分頁', 'figma-prototype-tab', 'Prototype 分頁：Interactions 的 ＋ 新增互動，下方是 Scroll behavior（紅框）'),
 ('B2', '4. 將 Action 設為 Navigate to', 'figma-action-list', 'Action 選單：本課用 Navigate to，彈層用 Open／Swap／Close overlay（紅框）'),
 ('B2', '4. 將 Action 設為 Navigate to', 'figma-navigate-flow', '設好 Destination 後畫布出現連線箭頭，起點畫面左上自動出現 Flow 1（紅框）'),
 ('B3', '3. 保留 On click、Navigate to 與原本目的地', 'figma-move-in-animation', 'Move in 的 Direction 四個箭頭、Easing 與 Duration（紅框）'),
 ('B4', '3. 將 Action 設為 Open overlay', 'figma-open-overlay', 'Open overlay 的 Position、Close when clicking outside 與 Background（紅框）'),
 ('B4', '5. 將選單 Position 設為 Top right', 'figma-overlay-position', 'Position 選單：選單用 Top right，底部面板用 Bottom center（紅框）'),
 ('B5', '6. 切到 Prototype 分頁，在 Scroll behavior', 'figma-overflow-flow-start', '選最外層畫面，Scroll behavior 的 Overflow 選 Vertical（下方紅框）'),
 ('B5', '有了真正的捲動，接著加入固定頁首', 'figma-scroll-position', '子層的 Position：Fixed 固定在視窗，Sticky 捲到頂才停（紅框）'),
 ('B7', '3. 選 PNG 與 1x', 'figma-export-panel', 'Design 面板的 Export：倍率、格式與 Export 按鈕；名稱含「/」時按鈕只顯示最後一段（紅框）'),
 ('B7', '接著保存可編輯的 Figma 來源', 'figma-file-menu', '左上 Main menu → File：Save local copy 另存 .fig（紅框）'),
 ('B8', '19. 從 GitHub 右上「+」選', 'github-new-repository', 'New repository：Repository name、Public、Add README 保持 Off（紅框）'),
 ('B8', '22. Mac 到 GitHub 頭像', 'github-token-new', 'Fine-grained tokens 頁：先填 Token name（紅框）'),
 ('B8', '22. Mac 到 GitHub 頭像', 'github-token-access', 'Repository access 選 Only select repositories，Permissions 按 Add permissions 加入 Contents（紅框）'),
 ('B8', '25. 選 Deploy from a branch', 'github-pages-settings', 'repo 的 Settings → Pages：Source 選 Deploy from a branch，Branch 選 main 與 /(root)，上線後出現 Visit site（紅框）'),
]
done = {}
for unit, prefix, img, cap in SHOTS:
    p = R / f'{unit}.md'; t = p.read_text(encoding='utf-8')
    tag = f'![{cap}]({U}{img}.webp)'
    if f'{U}{img}.webp' in t.split('## 自我檢查')[0] and (unit, img) not in done:
        done[(unit, img)] = 1; continue
    lines = t.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, (unit, prefix, len(idx))
    i = idx[0]
    # 跳過同一插入點已插入的圖
    j = i + 1
    while j < len(lines) and lines[j].startswith('!['): j += 1
    lines.insert(j, tag)
    p.write_text('\n'.join(lines), encoding='utf-8'); done[(unit, img)] = 1
print(len(done), 'images placed')
