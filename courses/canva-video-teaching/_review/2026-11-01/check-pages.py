"""PM 自動檢查：改寫稿是否守住規格書的硬規則（只做篩選，需要判斷的再人工看）。

用法（在 repo 根目錄）：
python3 courses/canva-video-teaching/_review/2026-11-01/check-pages.py courses/canva-video-teaching/_review/2026-11-01/round1 CH1-1 CH1-2 ...
只檢查學員正文（「## 自我檢查」之前）。
"""
import re, sys
from pathlib import Path

lessons = Path(__file__).resolve().parents[4] / '_lessons/canva-video-teaching'
FORBIDDEN = re.compile(r'(?<![A-Za-z0-9])(?:CH\d-\d|EXT\d|O\d|M\d|v[12]|[\w-]+\.(?:mp4|wav|svg|png|jpg|zip|txt|csv|pptx|srt|md))(?![A-Za-z0-9])')
CAVEAT = re.compile(r'不能|不要|不可|不必|不代表|仍(?:須|要|需)|才能')
PEER = re.compile(r'同伴|同學|旁邊的人|分組|互相')
LABEL = re.compile(r'\*\*(?:完成檢查|卡住時|用途|判斷方式|現在應該看到|獨自檢查)[:：]?\*\*')
TONE = re.compile(r'很簡單|只要|顯然|！')
BRANCH = re.compile(r'備援|平面備援|34 秒|38 秒|十秒位置|課程 WAV|舊頁面')
NEED = {
    'CH1-1': ['影片', '主軌', '上方軌', '音訊軌', '播放頭', '新增文字方塊', '復原'],
    'CH1-2': ['上傳', '主軌', '裁切', '元素', '圖層'],
    'CH1-3': ['滑動', '分割', '圖庫影片', 'Ctrl'],
    'CH1-4': ['製作動畫', '新增轉場', '預覽', '第 2 秒'],
    'CH1-5': ['建立複本', '取代', '圖庫影片', '魔法文案', '速度', '先完成自己的版本'],
    'CH1-6': ['下載', 'MP4', '專案紀錄'],
    'CH2-1': ['建立複本', '有聲字幕版'],
    'CH2-2': ['AI 語音', '錄製旁白', '錄製自己', '麥克風'],
    'CH2-3': ['分割', '音樂庫', '音量', '全部平衡', '淡入淡出', '節拍標記'],
    'CH2-4': ['輔助字幕', '口說語言', '翻譯', '逐字顯示', '下載'],
    'CH2-5': ['預覽', '靜音', '無痕', '學生製作任務'],
    'CH2-6': ['下載', '可供檢視', '無痕'],
}

src, units = Path(sys.argv[1]), sys.argv[2:]
for u in units:
    text = (src / f'{u}.md').read_text()
    body = re.split(r'\n## 自我檢查', text)[0]
    issues = []
    head = body[:body.index('\n## ')] if '\n## ' in body else body
    extra = [l for l in head.splitlines()[1:] if l.strip() and not l.startswith('本節完成物')][1:]
    if extra:
        issues.append(f'第一個小節前有正文 {len(extra)} 行')
    prose = re.sub(r'```[\s\S]*?```', '', body)
    nolink = re.sub(r'\]\([^)]*\)', ']', prose)
    nolink = re.sub(r'`姓名_[^`]+`', '', nolink)
    if f := sorted(set(FORBIDDEN.findall(nolink))):
        issues.append(f'代碼／檔名：{f}')
    if p := re.findall(r'```[^\n]*\n([^\n]{0,20})', body):
        issues.append(f'框內開頭（人工看動詞）：{p}')
    if p := re.findall(r'```[^\n]*\n((?:你是|請扮演|扮演一位)[^\n]{0,15})', body):
        issues.append(f'提示詞開頭：{p}')
    for name, pat in (('同伴字樣', PEER), ('標籤卡', LABEL), ('語氣詞', TONE), ('分支詞', BRANCH)):
        if p := pat.findall(prose):
            issues.append(f'{name} {len(p)} 處：{sorted(set(p))}')
    secs = re.split(r'\n(?=## )', prose)[1:]
    over = [i + 1 for i, s in enumerate(secs) if len([x for x in re.split(r'[。！？\n]', s) if CAVEAT.search(x)]) > 1]
    if over:
        issues.append(f'限制語超過一句的小節：{over}')
    missing = [l for l in re.findall(r'\]\((\.\./\.\./[^)#\s]+)', body) if not (lessons / l).resolve().exists()]
    if missing:
        issues.append(f'連結不存在：{missing}')
    lack = [k for k in NEED.get(u, []) if k not in body]
    if lack:
        issues.append(f'缺功能關鍵字：{lack}')
    n = len(re.sub(r'\s', '', body))
    print(f'{u}（{n} 字）：' + ('；'.join(issues) if issues else '無硬規則問題'))
