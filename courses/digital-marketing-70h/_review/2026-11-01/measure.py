"""digital-marketing-70h 機器初篩（只做分流，不做裁決）。沿用 gen-ai-36h 版正則，另加模組碼與同伴欄。

用法：在 courses/digital-marketing-70h/ 下執行 python3 _review/2026-11-01/measure.py > _review/2026-11-01/baseline.csv
指標全部是關鍵字代理值，必須搭配人工／代讀評分才能下結論。
"""
import csv, glob, re, sys

# 問題三：學員頁中的識別碼（章節碼、案例碼、工程碼、英文欄位名、檔名）
CODE = re.compile(r'(?<![A-Za-z0-9])(?:CH\s?\d(?:[-.]\d)?|PRAC\d|[A-Z]{2,4}-\d{1,3}|[A-Z]{1,4}\d{1,3}[ab]?(?:[-/–]\d+)?|NOT_RUN|PENDING|ReviewedQueue|ProcessingLog|[a-z]+_[a-z_]+|[\w-]+\.(?:csv|md|html|json|pdf|txt|png|mp3))(?![A-Za-z0-9])')
# 問題二：人工作業詞 vs 學員指揮 AI 的詞
HUMAN = re.compile(r'人工|覆核|核對|比對|查證|逐[筆欄條句]|手動|人(?:確認|決定|查|同意|核准)|自己(?:讀|查|判斷|寫)|先查|核准|勾選|記下|寫下|檢查')
AI = re.compile(r'(?:讓|請|用|交給|貼給|貼進)\s?(?:生成式\s?)?(?:AI|Claude|Gemini|ChatGPT|NotebookLM|模型)|提示詞|AI\s?(?:產生|生成|寫|整理|摘要|提出|建議|改寫|做)')
CAVEAT = re.compile(r'不能|不要|不可|不代表|不等於|仍(?:須|要|需)|才能|才可')
# 問題一：祈使句開頭比例、因果／銜接詞
IMP = re.compile(r'^(先|再|按|開|完成|保存|用|把|對|記下|寫下|查|比較|確認|貼|打開|讀|找|改|選|輸入|逐)')
# 本課另計：模組／單元碼（M2B、M3-3、3-2）與同伴字樣
MCODE = re.compile(r'(?<![A-Za-z0-9])(?:M\d{1,2}[A-D]?(?:-\d)?|\d{1,2}-\d)(?![A-Za-z0-9])')
PEER = re.compile(r'同伴|同學|分組|小組|組員|兩人一組|互評|同儕')
CONN = re.compile(r'因為|所以|這樣|為什麼|原因|也就是|換句話說|例如|比如|接下來|上一節|剛才|於是|這表示|好處|如果你')


def body_text(html):
    html = re.sub(r'<(script|style)[\s\S]*?</\1>', '', html)
    t = re.sub(r'\n\s*\n+', '\n', re.sub(r'<[^>]+>', '\n', html))
    # 正文：hero 的 h1 起到 nav-footer 前（頁首單元標示與返回連結不計）；module*.html 沒有 nav-footer 時取整頁
    m = re.search(r'<h1[\s\S]*?(?=<nav class="nav-footer")', html)
    main = m.group(0) if m else html
    t = re.sub(r'\n\s*\n+', '\n', re.sub(r'<[^>]+>', '\n', main))
    paras = [re.sub(r'<[^>]+>', '', p).strip() for p in re.findall(r'<p\b[^>]*>([\s\S]*?)</p>', main)]
    return t, paras


w = csv.writer(sys.stdout)
w.writerow(['page', 'chars', 'codes', 'codes_uniq', 'codes_per_k', 'human', 'ai', 'human_ai_ratio', 'caveats', 'imperative_pct', 'connectives', 'mcodes', 'peer'])
for f in sorted(glob.glob('m*.html')):
    body, paras = body_text(open(f, encoding='utf-8').read())
    n = len(re.sub(r'\s', '', body)) or 1
    codes = CODE.findall(body)
    hu, ai = len(HUMAN.findall(body)), len(AI.findall(body))
    sents = [s.strip() for p in paras for s in re.split(r'[。；！？]', p) if len(s.strip()) > 4]
    imp = sum(1 for s in sents if IMP.match(s))
    w.writerow([f[:-5], n, len(codes), len(set(codes)), round(len(codes) / n * 1000, 1),
                hu, ai, round(hu / max(ai, 1), 2), len(CAVEAT.findall(body)),
                round(imp / max(len(sents), 1) * 100), sum(len(CONN.findall(p)) for p in paras),
                len(MCODE.findall(body)), len(PEER.findall(body))])
