"""第二次改寫 PM 檢查：概念先教、核心術語齊全、套路句。
用法（repo 根目錄）：python3 courses/digital-marketing-70h/_review/2026-11-05/check-pages.py round1/m1-1.md …
路徑相對於本檔所在資料夾。腳本只攔得到可量測的項目；概念是否講懂仍要人工逐頁讀。
"""
import re, sys
from pathlib import Path
from collections import Counter

here = Path(__file__).parent
# 每頁必教術語：攔「概念被刪掉或只剩名詞」的失效（上一輪 System 1 7→0、JTBD 10→0）
TERMS = {
    'm1-1': ['雙歷程', 'System 1', 'System 2', 'Kahneman', 'Stanovich'],
    'm1-2': ['Cialdini', '互惠', '承諾', '一致', '社會認同', '社會證明', '喜好', '權威', '稀缺', '團結'],
    'm1-3': ['Tversky', '錨定', '損失趨避', '展望理論', '稀缺', '峰終', '1.96'],
    'm1-4': ['Jobs to Be Done', 'JTBD', 'Christensen', '功能', '情感', '社會', '替代'],
    'm3-2': ['STP', 'Segmentation', 'Targeting', 'Positioning', '人口', '地理', '心理', '行為', 'Persona', '代表', '發起者', '建議者', '出資者', '使用者', '優先路徑'],
    'm8-1': ['CTR', 'CPC', 'CVR', 'CPL', 'CPA', 'ROAS', 'Performance Max', 'Demand Gen', '停止條件', '自然流量'],
    'm7-2': ['資料層', 'dataLayer', 'Tag Assistant', 'DebugView', 'Initialization - All Pages', '<head>', '<body>', 'line_join', '接受'],
    'm10-1': ['對象', '承諾', '行動', '量測', '不做', '已驗證', '待補'],
}
# 型態：操作型允許第一段就提到案例練習頁（SOP 第 4 節）
TYPE = {'m7-2': '操作型'}
CASE = re.compile(r'山徑|品牌包|阿傑|麗芬|柏翰')
STOCK = ['換你做', '常見卡關與修法', '先完成自己的版本']
CODES = re.compile(r'\bM\d{1,2}[A-D]?\b|(?<![\d,$.])[1-9]0?-[1-9](?![\d,])|INT-0|WEB-0|REV-0|SOCIAL-0|\bPASS\b|PENDING|VERIFIED')
LIMIT = re.compile(r'不要|不能|不可|仍須')
heads = Counter()
fail = 0

for arg in sys.argv[1:]:
    f = here / arg
    unit = f.stem
    text = f.read_text()
    body = text.split('## 自我檢查')[0]
    secs = re.split(r'\n(?=## )', body)
    pre, secs = secs[0], secs[1:]
    flat = re.sub(r'\s', '', ''.join(secs))
    n = len(re.sub(r'\s', '', ''.join(secs)))  # 從第一個 ## 起算，標題區（含學習目標）不計
    issues = []
    cap = 3600 if unit == 'm1-4' else 3300  # m1-4 含模組作業，退回意見放寬
    if not 2300 <= n <= cap: issues.append(f'字數 {n}')
    if not 4 <= len(secs) <= 7: issues.append(f'## 數 {len(secs)}')
    # 案例位置：攔「一開頭就上案例」
    idx = next((i for i, s in enumerate(secs, 1) if CASE.search(s)), None)
    m = CASE.search(flat)
    pos = m.start() / len(flat) if m else 1
    if TYPE.get(unit) != '操作型' and (idx is None or idx < 3 or pos < 0.30):
        issues.append(f'案例太早：第 {idx} 節、全頁 {pos:.0%} 處')
    if CASE.search(re.sub(r'本節完成物：.*', '', pre)): issues.append('標題或副標提到案例')
    missing = [t for t in TERMS.get(unit, []) if t not in body]
    if missing: issues.append('缺術語 ' + '、'.join(missing))
    for s in STOCK:
        if s in body: issues.append(f'套路句「{s}」×{body.count(s)}')
    if len(re.findall(r'不是[^。！？\n]{1,40}而是', body)) > 1: issues.append('「不是…而是」>1')
    if len(re.findall(r'上一(頁|節)', body)) > 2: issues.append('「上一頁／上一節」>2')
    if re.search(r'有了[^。\n]{1,15}，就能', body): issues.append('「有了…，就能」')
    c = CODES.findall(body)
    if c: issues.append(f'代碼 {c[:5]}')
    if unit.startswith('m1-') and '```' in body: issues.append('M1 出現程式框')
    if re.search(r'\bAI\b', body) and unit.startswith('m1-') and unit != 'm1-1': issues.append('M1 提到 AI（確認是否為學員使用）')
    for s in secs:
        k = len(LIMIT.findall(s))
        if k > 1: issues.append(f'限制語 {k}：{s.splitlines()[0]}')
    if '（2026-11 查證）' not in body and unit not in ('m10-1',): issues.append('沒有查證標記')  # m10-1 的框架是本課自訂，沒有外部理論
    if body.count('## 用 AI 加速') > 1: issues.append('「用 AI 加速」超過一節')
    # 提示詞以動詞開頭：攔「請…」「你是…」「幫我…」「以下是…」開頭的提示詞框（m8-1 樣頁漏過）
    for blk in re.findall(r'```text\n(.*?)```', body, re.S):
        first = blk.strip().splitlines()[0] if blk.strip() else ''
        if re.match(r'(請|你是|幫我|以下是|我是)', first) or re.search(r'(^|\n)(請|幫我)', blk): issues.append(f'提示詞開頭或內含「請／幫我」：{first[:20]}')
    for s in secs: heads[s.splitlines()[0]] += 1
    print(f'{unit}: {n} 字、{len(secs)} 節、案例首見第 {idx} 節（{pos:.0%}）')
    for i in issues: print('   ✗', i)
    fail += bool(issues)

dup = [h for h, k in heads.items() if k > 1 and not h.startswith('## 模組作業')]
if dup: print('跨頁重複標題：', dup); fail += 1
sys.exit(1 if fail else 0)
