"""_lessons/digital-marketing-70h/*.md → 單元頁 HTML（2026-11-01 改寫起，學員正文唯一落筆層）。

用法（在 repo 根目錄）：python3 courses/digital-marketing-70h/_tools/render-lessons.py [m3-2 m4-1 …]
不給單元就轉製所有已有 md 的頁面。只替換：lesson-body、標題、副標、本節完成物、頂欄與單元號、
<title> 與 description 類 meta、上一節／下一節導覽（依 lesson-meta.json 的順序重建）。其餘外殼、密碼閘、頁內 CSS 保留。
md 格式：`# 標題`、副標一行、`學習目標：…｜…`（選用）、`本節完成物：…`、各 `##` 小節；`## 自我檢查` 起的內容不轉製。
元件：段落、清單、表格、```提示詞框```、> 提醒（callout）、> 參考方向：…（收合的參考區）、標題以「模組作業」開頭的小節（作業框）。
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
import json, re, sys

root = Path(__file__).resolve().parents[1]
lessons = root.parents[1] / '_lessons' / root.name
meta = json.loads((lessons / 'lesson-meta.json').read_text())
pages, modules = meta['pages'], meta['modules']
md = MarkdownIt('commonmark').enable('table')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Anchors(HTMLParser):
    # 記下每個元素的原始位置，只替換指定區段，不重新序列化整份 HTML
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.lines = [0] + [m.end() for m in re.finditer('\n', text)]
        self.stack, self.nodes = [], []
        self.feed(text)

    def pos(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        n = {'tag': tag, 'attrs': dict(attrs), 'start': self.pos(), 'inner': self.pos() + len(self.get_starttag_text())}
        if tag in VOID:
            n['close'] = n['end'] = n['inner']
            self.nodes.append(n)
        else:
            self.stack.append(n)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                for n in self.stack[i + 1:]:
                    n['close'] = n['end'] = self.pos()
                    self.nodes.append(n)
                n = self.stack[i]
                del self.stack[i:]
                n['close'] = self.pos()
                n['end'] = self.pos() + len(f'</{tag}>')
                self.nodes.append(n)
                return

    def find(self, cls, many=False):
        n = [x for x in self.nodes if cls in (x['attrs'].get('class') or '').split()]
        if many:
            return n
        assert len(n) == 1, (cls, len(n))
        return n[0]


def parse(text):
    lines = text.split('\n')
    title = lines[0].removeprefix('# ').strip()
    head = text.split('\n## ', 1)[0].splitlines()[1:]
    head = [l.strip() for l in head if l.strip()]
    artifact = next(l for l in head if l.startswith('本節完成物：')).removeprefix('本節完成物：')
    # 學習目標（2026-11-05 起）：一行，以「｜」分隔多條；沒有這行就只顯示完成物
    goal_line = next((l for l in head if l.startswith('學習目標：')), '')
    goals = [g.strip() for g in goal_line.removeprefix('學習目標：').split('｜') if g.strip()]
    tagline = next(l for l in head if not l.startswith(('本節完成物：', '學習目標：')))
    body = '## ' + text.split('\n## ', 1)[1]
    body = re.split(r'\n## (?:自我檢查|事實核對)', body)[0].strip()
    return title, tagline, goals, artifact, body


def outcomes(goals, artifact):
    item = '\n    <div class="outcome-item"><div class="outcome-dot"></div><span>{}</span></div>'
    h = ''
    if goals:
        h += '\n    <div class="outcomes-label">學習目標</div>' + ''.join(item.format(escape(g)) for g in goals)
    h += '\n    <div class="outcomes-label">本節完成物</div>' + item.format(escape(artifact))
    return h + '\n  '


def render(body):
    s = BeautifulSoup(md.render(body), 'html.parser')
    out, cur = [], None
    for n in list(s.contents):
        if getattr(n, 'name', None) == 'h2':
            assign = n.get_text().startswith('模組作業')
            cur = s.new_tag('div', attrs={'class': 'lesson-section rw-assign' if assign else 'lesson-section'})
            eb = s.new_tag('div', attrs={'class': 'section-eyebrow'})
            eb.string = '模組作業' if assign else f'{len(out) + 1:02}'
            n['class'] = 'section-heading'
            cur.append(eb)
            cur.append(n.extract())
            out.append(cur)
        elif cur is not None:
            cur.append(n.extract())
    for sec in out:
        for p in sec.find_all('p', recursive=False):
            p['class'] = 'body-text'
        for l in sec.find_all(['ul', 'ol'], recursive=False):
            l['class'] = 'body-list'
        for pre in sec.find_all('pre'):
            box = s.new_tag('div', attrs={'class': 'rw-prompt', 'data-copy-prompt': ''})
            lab = s.new_tag('div', attrs={'class': 'dialog-label'})
            lab.string = '提示詞'
            box.append(lab)
            box.append('\n' + pre.get_text().rstrip('\n'))  # 換行讓標籤自成一行（white-space:pre-line）
            pre.replace_with(box)
        for t in sec.find_all('table'):
            t['class'] = 'rw-table'
            t.wrap(s.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0', 'role': 'region', 'aria-label': '資料表，可水平捲動'}))
        for q in sec.find_all('blockquote'):
            # 「> 參考方向：…」轉成預設收合的參考區，學員做完練習再展開（2026-11-05 試讀：參考答案緊接題目下方）
            first = q.find('p')
            if first and first.get_text().startswith(('參考方向', '參考寫法', '參考結果')):
                d = s.new_tag('details', attrs={'class': 'rw-reference'})
                sm = s.new_tag('summary')
                sm.string = '做完再展開：' + first.get_text().split('：', 1)[0]
                d.append(sm)
                lead = first.decode_contents().split('：', 1)
                first.clear()
                first.append(BeautifulSoup(lead[1] if len(lead) > 1 else lead[0], 'html.parser'))
                for x in list(q.children):
                    d.append(x.extract())
                q.replace_with(d)
                continue
            c = s.new_tag('div', attrs={'class': 'callout'})
            icon = s.new_tag('span', attrs={'class': 'callout-icon', 'aria-hidden': 'true'})
            icon.string = '→'
            b = s.new_tag('div', attrs={'class': 'callout-body'})
            b.append(BeautifulSoup(''.join(str(x) for x in q.find_all('p')).replace('<p>', '').replace('</p>', '<br>').removesuffix('<br>'), 'html.parser'))
            c.append(icon)
            c.append(b)
            q.replace_with(c)
        for a in sec.select('a[href^="assets/"]'):
            a['target'], a['rel'] = '_blank', 'noopener'
    return '\n'.join(str(x) for x in out)


def nav(i):
    p, mod = pages[i], pages[i]['module']
    prev = pages[i - 1] if i > 0 and pages[i - 1]['module'] == mod else None
    nxt = pages[i + 1] if i + 1 < len(pages) else None
    h = ['<nav class="nav-footer">']
    if prev:
        h.append(f'  <a href="{prev["file"]}" class="nav-btn nav-prev" aria-label="上一單元" data-nav-role="prev"><span aria-hidden="true">←</span> {prev["num"]} {escape(prev["short"])}</a>')
    if nxt and nxt['module'] == mod:
        h.append(f'  <a href="{nxt["file"]}" class="nav-btn primary nav-next" aria-label="下一單元" data-nav-role="next">{nxt["num"]} {escape(nxt["short"])} <span aria-hidden="true">→</span></a>')
    elif nxt:
        m = nxt['module']
        h.append(f'  <a href="module{m[1:]}.html" class="nav-btn primary nav-next" aria-label="下一模組" data-nav-role="next">進入 {m} {escape(modules[m])} <span aria-hidden="true">→</span></a>')
    return '\n'.join(h + ['</nav>'])


units = sys.argv[1:] or [p['unit'] for p in pages if (lessons / f'{p["unit"]}.md').exists()]
for u in units:
    i = next(k for k, p in enumerate(pages) if p['unit'] == u)
    p = pages[i]
    f = root / p['file']
    title, tagline, goals, artifact, body = parse((lessons / f'{u}.md').read_text())
    for link in re.findall(r'\]\((assets/[^)#\s]+)', body):
        assert (root / link).is_file(), (u, link)
    text = f.read_text()
    a = Anchors(text)
    rep = []
    n = a.find('lesson-body')
    rep.append((n['inner'], n['close'], '\n' + render(body) + '\n'))
    for cls, val in [('lesson-title', escape(title)), ('lesson-tagline', escape(tagline)),
                     ('topbar-tag', f'{p["num"]} · {escape(p["short"])}'), ('hero-num', f'單元 {p["num"]}'),
                     ('outcomes', outcomes(goals, artifact))]:
        n = a.find(cls)
        rep.append((n['inner'], n['close'], val))
    navs = a.find('nav-footer', many=True)
    assert len(navs) == 1, (u, 'nav-footer', len(navs))
    rep.append((navs[0]['start'], navs[0]['end'], nav(i)))
    for n in a.find('nav-return-link', many=True):
        rep.append((n['start'], n['end'], ''))
    t = next(x for x in a.nodes if x['tag'] == 'title')
    page_title = f'{p["num"]} {title}｜{p["module"]} {modules[p["module"]]}｜數位行銷人才培訓'
    rep.append((t['inner'], t['close'], escape(page_title)))
    for x in a.nodes:
        k = x['attrs'].get('name') or x['attrs'].get('property')
        if x['tag'] == 'meta' and k in ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description'):
            attrs = dict(x['attrs'], content=page_title if k.endswith('title') else tagline)
            rep.append((x['start'], x['end'], '<meta ' + ' '.join(f'{kk}="{escape(v)}"' for kk, v in attrs.items()) + '>'))
    for s0, e0, new in sorted(rep, reverse=True):
        text = text[:s0] + new + text[e0:]
    if 'assets/lesson-rewrite.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="assets/lesson-rewrite.css">\n</head>', 1)
    dom = BeautifulSoup(text, 'html.parser')
    assert len(dom.select('.lesson-body')) == 1 and len(dom.select('.nav-footer')) == 1, u
    f.write_text(text)
print('Rendered', len(units), 'pages')
