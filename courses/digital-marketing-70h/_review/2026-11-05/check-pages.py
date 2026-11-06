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
    # 生成式 AI 模組（取自設計卡 C1、C2 的新名詞，挑每頁核心的幾個）
    'm2a-1': ['LLM', 'token', '上下文視窗', '知識截止', '幻覺', '捏造', '假引用', '混淆', '過時'],
    'm2a-2': ['產品形態', '深度研究', '代理', '人工核准點', '停止條件', '專案', '記憶'],
    'm2a-3': ['個人資料', '去識別', '著作權', 'AI 內容標示', 'C2PA'],
    'm2b-1': ['Prompt', '任務', '情境', '素材', '格式', '限制', '角色'],
    'm2b-2': ['Zero-shot', 'Few-shot', 'Prompt Chaining', '角色設定', '追問', '迭代'],
    'm2b-3': ['提示詞庫', '模板', '變數', '驗收清單', '自訂指令'],
    'm2c-1': ['品牌卡', '品牌語氣', '切角', 'CTA', '核查'],
    'm2c-2': ['主體', '風格', '光線', '氛圍', '構圖', '負向提示', '提示詞卡', '版位'],
    'm2c-3': ['SRT', '時間碼', '語音轉文字', '剪輯點', '內容再利用', 'Gemini Notebook'],
    'm2d-1': ['深度研究', '研究計畫', '子問題', '停止條件', 'Google Trends', '未找到'],
    'm2d-2': ['觸發', '動作', 'CSV', '資料契約', '驗證', '人工核准點', '重跑'],
    'm2d-3': ['欄位定義', '平均', '占比', '口徑', '試算表', 'SUM'],
    # 市場洞察與策略定位（設計卡 C3）
    'm3-1': ['3C', '直接競品', '間接競品', 'SWOT', 'TOWS', 'SO', 'WT', '證據鏈', '反證'],
    'm3-3': ['顧客旅程', '接觸點', '缺口', '行銷任務', '未觀察到'],
    'm3-4': ['4P', '4C', 'USP', '差異化', '相關性', '可信度', '替換測試', '定位聲明'],
    # 社群行銷（設計卡 C3）
    'm4-1': ['Hook', '前三秒', '觀看承諾', '觀看曲線', '停滯點'],
    'm4-2': ['官方說明', '自家帳號', '假設', '不可直接推論', '停止條件'],
    'm4-3': ['四段', '情緒弧線', 'CTA', '完播率', '短影音格式'],
    'm4-4': ['內容月曆', '內容角色', '產能', '分裝', '初步聲明'],
    'm4-5': ['KOL', 'KOC', '粉絲規模', '互動率', 'Brief', '薦證', '揭露', 'UGC'],
    # 搜尋（設計卡 C4）
    'm5-1': ['SERP', 'SEO', 'AI 摘要', 'AI 模式', '商家檔案', '社群搜尋', 'E-E-A-T'],
    'm5-2': ['搜尋意圖', '資訊型', '導航型', '商業型', '交易型', '修飾詞', '意圖地圖'],
    'm5-3': ['Search Console', '曝光', '點閱率', '平均排序', '主題群集', '支柱頁', '關鍵字地圖'],
    'm5-4': ['On-page', '<head>', 'Title', 'Meta', 'H1', '結構化資料', 'JSON-LD', 'Product'],
    'm5-5': ['檢索', '索引', 'robots.txt', 'noindex', 'canonical', '301', 'LCP', 'INP', 'CLS', 'PageSpeed'],
    'm5-6': ['E-E-A-T', 'YMYL', '反向連結', '連結垃圾', 'sponsored', 'nofollow'],
    # GA4 數據分析（設計卡 C5）
    'm6-1': ['事件', '使用者', '工作階段', '資源', '資料串流', '關鍵事件', '示範帳戶'],
    'm6-2': ['來源', '媒介', '預設管道群組', 'UTM', 'utm_source', 'utm_medium', 'utm_campaign', '未指派'],
    'm6-3': ['活躍使用者', '參與率', '跳出率', '平均參與時間', '同類群組', '維度', '指標'],
    'm6-4': ['探索', '漏斗', '封閉式', '開放式', '使用者', '細分', '區隔'],
    'm6-5': ['一頁決策摘要', '根因', 'A/B', '主要指標', '護欄指標', '停止條件', '量測決策表'],
    # GTM（設計卡 C5）
    'm7-1': ['GTM', '容器', '代碼', '觸發條件', '變數', '資料層', 'dataLayer', '追蹤規格', 'Consent Initialization'],
    'm7-3': ['自訂事件', '資料層變數', '建議事件', '捲動深度', '自訂維度', 'line_join', '內部流量'],
    'm7-4': ['同意模式', 'analytics_storage', 'ad_storage', '進階模式', '行為建模', 'Meta 像素', '轉換 API', '去重', 'Schedule'],
}
# 型態：操作型允許第一段就提到案例練習頁（SOP 第 4 節）
TYPE = {'m7-2': '操作型', 'm2c-3': '操作型', 'm7-3': '操作型'}
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
    # 從第一個 ## 起算，標題區（含學習目標）不計；連結網址不計，否則附來源會被字數上限逼著刪掉（m7-2 退回時發生）
    n = len(re.sub(r'\s', '', re.sub(r'\]\([^)]*\)', ']', ''.join(secs))))
    issues = []
    cap = 3600 if unit in ('m1-4', 'm7-2', 'm2d-3', 'm3-4', 'm4-5', 'm5-6', 'm6-5', 'm7-4') else 3300  # m1-4 含模組作業；m7-2 依決策多了建立 GA4 資源一節
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
