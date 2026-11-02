"""uiux-designer 機器初篩（只做分流，不做裁決）。
用法：在 courses/uiux-designer/ 下執行 python3 _review/2026-11-02/measure.py > _review/2026-11-02/baseline.csv
"""
import csv, glob, re, sys
LAYER = re.compile(r'<code>[^<]*</code>')                                   # 正文中的圖層名／程式碼片段
NUM = re.compile(r'(?<![A-Za-z0-9])[WHXYxy]\s?\d{2,4}(?![0-9])|\d{2,4}\s?×\s?\d{2,4}')  # W402、x24、402×874
XREF = re.compile(r'第\s?\d{1,2}\s?堂|前堂|上一堂|下一堂')                         # 用堂號跨頁引用
TID = re.compile(r'(?<![A-Za-z0-9])T\d{2}(?![0-9])')                         # 任務代碼 T01
ENG = re.compile(r'[A-Za-z][A-Za-z ./]{2,}')
CAVEAT = re.compile(r'不能|不要|不可|不代表|不等於|不是|仍(?:須|要|需)|才能|才算|不算|假裝')
PEER = re.compile(r'同伴|同學|分組|小組|組員|兩人一組|互評|同儕|別人|他人|另一人|測試者')
CONN = re.compile(r'因為|所以|這樣|為什麼|原因|也就是|換句話說|例如|比如|接下來|剛才|於是|這表示|好處|如果你')
def body(html):
    m = re.search(r'<main[\s\S]*?</main>', html); main = m.group(0) if m else html
    main = re.sub(r'<section class="lesson-section section" id="section-\d+"><h2 class="section-heading">本堂查證來源[\s\S]*?</section>', '', main)
    return main, re.sub(r'\s', '', re.sub(r'<[^>]+>', '', main))
w = csv.writer(sys.stdout)
w.writerow(['page','chars','code_tags','dims','xref','task_ids','eng_per_k','caveats_per_k','peer','connectives_per_k'])
for f in sorted(glob.glob('part*/*.html')):
    main, t = body(open(f, encoding='utf-8').read()); n = len(t) or 1; k = lambda x: round(x / n * 1000, 1)
    w.writerow([f[:-5], n, len(LAYER.findall(main)), len(NUM.findall(t)), len(XREF.findall(t)), len(TID.findall(t)),
                k(len(ENG.findall(re.sub(r'<[^>]+>', ' ', main)))), k(len(CAVEAT.findall(t))), len(PEER.findall(t)), k(len(CONN.findall(t)))])
