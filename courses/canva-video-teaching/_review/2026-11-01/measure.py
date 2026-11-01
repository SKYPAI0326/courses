"""canva-video-teaching 改寫前後代理指標（只做分流，不做裁決）。

用法（在 repo 根目錄）：python3 courses/canva-video-teaching/_review/2026-11-01/measure.py [正文資料夾]
預設讀 _lessons/canva-video-teaching/ 的 learner-content 段；給資料夾時讀該處 CH*.md 的「## 自我檢查」之前。
"""
import re, sys
from pathlib import Path

CODE = re.compile(r'(?<![A-Za-z0-9])(?:CH\s?\d(?:[-.]\d)?|EXT\d|O\d|M\d|v\d|[\w-]+\.(?:mp4|wav|svg|png|jpg|pptx|srt|csv|md|html|txt|zip)|[a-z]+_[a-z_]+|`[^`]+`)(?![A-Za-z0-9])')
CAVEAT = re.compile(r'不能|不要|不可|不必|不代表|不等於|仍(?:須|要|需)|才能|才可')
BRANCH = re.compile(r'備援|不可用|找不到|沒有入口|改用|選做|補做|重練|舊專案|副本')
CONN = re.compile(r'因為|所以|這樣|為什麼|接下來|上一節|剛才|於是|這表示|好處|現在|剛剛')
FEATURES = ['上傳', '主軌', '裁短', '裁切', '分割', '圖層', '動畫', '轉場', '錄製配音', 'Record Voiceover', 'AI Voice', '配樂', '音量', '淡入', '字幕', '下載', '分享',
            '範本', '模板', 'Magic', 'Beat Sync', '節拍', '去背', 'Background Remover', '降噪', 'Enhance', '強化語音', '素材庫', '元素', '音訊庫', '文字轉語音',
            'Magic Write', '魔法', 'Highlights', '精彩片段', '調整尺寸', 'Resize', '品牌', '濾鏡', '調整', '速度', '貼圖', '繪圖', '錄製自己', '簡報錄製', '圖庫影片', '滑動', '取代', 'AI 語音', '音樂庫', '全部平衡', '淡入淡出', '節拍標記', '輔助字幕', '翻譯', '魔法文案', '錄製旁白', '無痕', '預覽']

src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
root = Path(__file__).resolve().parents[4]
print('頁,字數,識別碼/千字,限制語,分支語,銜接詞,Canva功能種類,功能清單')
for f in sorted((src or root / '_lessons/canva-video-teaching').glob('CH*.md')):
    t = f.read_text()
    if src:
        body = re.split(r'\n## 自我檢查', t)[0]
    else:
        body = t.split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0]
    prose = re.sub(r'\]\([^)]*\)', ']', body)
    n = len(re.sub(r'\s', '', prose)) or 1
    feats = [k for k in FEATURES if k in prose]
    print(f'{f.stem},{n},{round(len(CODE.findall(prose)) / n * 1000, 1)},{len(CAVEAT.findall(prose))},{len(BRANCH.findall(prose))},{len(CONN.findall(prose))},{len(feats)},{"/".join(feats)}')
