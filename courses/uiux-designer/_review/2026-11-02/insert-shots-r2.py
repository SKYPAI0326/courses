"""第二輪新增技法的操作截圖插入點（圖檔在 assets/shared/ui/，來自 Figma 示範檔實機）。可重複執行。"""
from pathlib import Path
R = Path(__file__).parent / 'round2'
U = '../assets/shared/ui/'
SHOTS = [
 ('A1', '2. 點最左側圖示列的 **Variables**', 'figma-variables-create', '左側圖示列的 Variables，空白變數表中央 Create 會列出變數類型（紅框）'),
 ('A1', '5. 從表格底部點 **Create variable**', 'figma-variables-table', '集合改名後的變數表：左欄是集合名稱，底部 Create variable 新增下一個變數（紅框）'),
 ('A1', '6. 選取登入畫面，點 Fill 標題列的四點圖示', 'figma-fill-variable', 'Fill 標題列的四點圖示打開 Libraries，最上方是本檔建立的顏色變數（紅框）'),
 ('A2', '2. 選取標題，點 X／Y 右側的小圖示展開 Constraints', 'figma-constraints', 'X／Y 右側的小圖示展開 Constraints，水平方向可選 Left、Right、Left + Right、Center、Scale（紅框）'),
 ('A3', '4. 回到畫布選取登入卡片，把滑鼠移到 Padding', 'figma-padding-variable', '滑鼠移到 Padding 欄右端出現變數圖示，點開後選本檔的間距變數（紅框）'),
 ('A3', '2. 選取登入卡片，點 W 欄的下拉箭頭', 'figma-min-max-width', 'W 欄下拉選單裡的 Add min width 與 Add max width（紅框）'),
 ('A5', '2. 在 Appearance 標題列找到眼睛旁的', 'figma-boolean-property', 'Appearance 標題列的 Apply variable/property 圖示，按 ＋ 開啟 Create property 視窗，預設值 True（紅框）'),
 ('B2', '4. 將 Action 設為 **Change to**', 'figma-hover-change-to', 'Variant 的互動：Trigger 選 While hovering，Action 選 Change to，下方選目標 Variant（紅框）'),
 ('B4', '8. 將 Trigger 設為 After delay', 'figma-trigger-list', 'Trigger 清單：While hovering、While pressing 與最下方的 After delay（紅框）'),
 ('B1', '4. 使用 Arrow（箭頭）工具', 'figma-shape-menu', '矩形工具旁的下拉選單有 Arrow（⇧L）與 Image/video（紅框）'),
 ('A7', '3. 點 **Upload from computer**', 'figma-image-fill', 'Fill 類型列的 Image，縮放方式選單與 Upload from computer（紅框）'),
 ('B7', '2. 在 Export 標題列再點一次', 'figma-export-2x', 'Export 標題列的 ＋ 再加一列，新列預設 2x，兩列各自選格式（紅框）'),
]
n = 0
for unit, prefix, img, cap in SHOTS:
    p = R / f'{unit}.md'; t = p.read_text(encoding='utf-8')
    if f'{U}{img}.webp' in t: continue
    lines = t.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, (unit, prefix, len(idx))
    lines[idx[0]+1:idx[0]+1] = ['', f'![{cap}]({U}{img}.webp)', '']
    p.write_text('\n'.join(lines), encoding='utf-8'); n += 1
print(n, 'images placed')
