"""把承作稿寫回正式講義。

用法：在 courses/uiux-designer/ 下執行 python3 _review/2026-11-02/apply.py <round 目錄> [單元 ...]
寫入：講義 HTML（頁首、正文、meta、頁尾日期）、_lessons 教案的 learner-content 段、
該單元 START-HERE 與完成檢查表的標題／副標、EXPECTED-CHECK 的檢查列。
首頁卡片與導覽列文字另由 sync-titles 步驟處理（本檔 sync_titles()）。
"""
import html, importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # courses/uiux-designer
BASE = ROOT.parents[1]                              # repo 根
spec = importlib.util.spec_from_file_location('r', ROOT / '_tools/repair_render_reference.py')
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
UNITS = {u[0].split('-')[0]: (u[0], u[1]) for u in R.UNITS}   # A1 -> (A1-visual-foundations, part1/CH1-....html)
DATE = '2026-11-02'


def parse(md):
    md = re.split(r'^## 自我檢查', md, flags=re.M)[0].strip()
    head, *secs = re.split(r'^## ', md, flags=re.M)
    lines = [l.strip() for l in head.splitlines() if l.strip()]
    title = lines[0].lstrip('# ').strip()
    sub = next(l for l in lines if l.startswith('副標')).split('：', 1)[1].strip()
    outs = [x.strip() for x in next(l for l in lines if l.startswith('本堂完成物')).split('：', 1)[1].split('；') if x.strip()]
    sections = []
    for s in secs:
        h, _, body = s.partition('\n')
        sections.append((h.strip(), body.strip()))
    return title, sub, outs, sections, md


def checklist(sections):
    """收尾小節（倒數第二節，查證來源之前）的第一個項目清單＝完成條件。"""
    for h, body in reversed(sections):
        if h == '本堂查證來源':
            continue
        items = re.findall(r'^[-*] (.+)$', body, flags=re.M)
        if items:
            return [re.sub(r'\*\*|`', '', i) for i in items]
    return []


def render(body):
    out = R.render(body)
    out = re.sub(r'<a href="(?!#)([^"]+)">', r'<a href="\1" target="_blank" rel="noopener noreferrer">', out)
    return out


def esc(s):
    return html.escape(s, quote=True)


def apply_unit(key, md):
    unit, page = UNITS[key]
    title, sub, outs, sections, learner = parse(md)
    p = ROOT / page; t = p.read_text(encoding='utf-8')
    # 兩種頁首外殼：title／tagline（多數頁）與 lesson-title／lesson-tagline（A4、B4）
    h1 = re.search(r'<h1 class="((?:lesson-)?title)">(.*?)</h1>', t); tg = re.search(r'<p class="((?:lesson-)?tagline)">(.*?)</p>', t)
    old_title, old_sub = h1[2], tg[2]
    t = t.replace(h1[0], f'<h1 class="{h1[1]}">{html.escape(title)}</h1>', 1)
    t = t.replace(tg[0], f'<p class="{tg[1]}">{html.escape(sub)}</p>', 1)
    t = re.sub(r'(<div class="outcomes-label">這堂要完成</div>)(?:<div class="outcome-item">.*?</div>)+',
               lambda m: m[1] + ''.join(f'<div class="outcome-item">{html.escape(o)}</div>' for o in outs), t, count=1, flags=re.S)
    t = re.sub(r'返回第 ?\d+ ?堂：', '返回上一堂：', t)
    sec_cls = 'lesson-section section' if 'class="lesson-section section"' in t else 'lesson-section'
    t = re.sub(r'<title>(第\d+堂 )[^｜<]*｜', lambda m: f'<title>{m[1]}{html.escape(title)}｜', t, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        t = re.sub(rf'(<meta (?:content="[^"]*" )?{attr}(?: content="[^"]*")?)', lambda m: re.sub(r'content="[^"]*"', f'content="{esc(sub)}"', m[1]), t)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        t = re.sub(rf'(<meta (?:content="[^"]*" )?{attr}(?: content="[^"]*")?)', lambda m: re.sub(r'content="[^"]*"', f'content="{esc(title)}"', m[1]), t)
    body = ''.join(f'<section class="{sec_cls}" id="section-{i}"><h2 class="section-heading">{html.escape(h)}</h2>\n{render(b)}\n</section>'
                   for i, (h, b) in enumerate(sections, 1))
    t, n = re.subn(r'<div class="lesson-body">.*?</div>\n(<(?:nav class="nav|div class="nav-footer)(?:-footer)?")', lambda m: f'<div class="lesson-body">{body}</div>\n' + m[1], t, count=1, flags=re.S)
    assert n == 1, f'{page}：找不到正文區塊'
    t = re.sub(r'(data-nav-role="prev">.*?</span> )第 ?\d+ ?堂：', r'\1上一堂：', t)
    t = re.sub(r'data-built-at="[^"]*"', f'data-built-at="{DATE}"', t)
    t = re.sub(r'data-platform-version="[^"]*"', f'data-platform-version="官方文件查證{DATE}"', t)
    t = re.sub(r'實作講義 · [0-9-]+修訂', f'實作講義 · {DATE}修訂', t)
    p.write_text(t, encoding='utf-8')

    les = BASE / '_lessons/uiux-designer' / f'{unit}.md'
    lt = les.read_text(encoding='utf-8')
    lt = re.sub(r'(<!-- learner-content:start -->\n).*?(\n<!-- learner-content:end -->)', lambda m: m[1] + learner.replace('../assets/', '../../courses/uiux-designer/assets/') + m[2], lt, flags=re.S)
    lt = re.sub(r'^title: .*$', f'title: {title}', lt, count=1, flags=re.M)
    lt = re.sub(r'^revision: .*$', f'revision: {DATE}', lt, count=1, flags=re.M)
    lt = re.sub(r'^platform_version: .*$', f'platform_version: 官方文件 {DATE} 查證（_review/2026-11-02/platform-*.md）', lt, count=1, flags=re.M)
    les.write_text(lt, encoding='utf-8')

    adir = ROOT / 'assets' / unit
    for f in [adir / 'START-HERE.html', adir / 'START-HERE.md', *sorted((adir / 'reference').glob('*'))]:
        if not f.exists() or f.suffix not in ('.html', '.md'):
            continue
        s = f.read_text(encoding='utf-8')
        s2 = s.replace(html.unescape(old_title), title).replace(old_title, html.escape(title))
        s2 = s2.replace(html.unescape(old_sub), sub).replace(old_sub, html.escape(sub))
        if f.name in ('EXPECTED-CHECK.html', 'HANDOFF-CHECK.html', 'TASK-TEST-FORM.html'):
            items = checklist(sections)
            rows = ''.join(f'<tr><td>{html.escape(x)}</td><td><label>實際結果／證據檔名<textarea name="actual-{i}" placeholder="寫下觀察、檔名或連結；沒做就寫原因"></textarea></label><label><input type="checkbox" name="pass-{i}"> 已核對此項</label></td><td><label>問題／修復與重跑<textarea name="repair-{i}"></textarea></label></td></tr>'
                           for i, x in enumerate(items))
            # 完成條件表：一般檢查表是唯一的表；任務測試表是最後一張表
            spans = [m.span() for m in re.finditer(r'<tbody>.*?</tbody>', s2, flags=re.S)]
            a, b = spans[-1] if f.name == 'TASK-TEST-FORM.html' else spans[0]
            s2 = s2[:a] + f'<tbody>{rows}</tbody>' + s2[b:]
            s2 = re.sub(r'data-record-key="([^"]+)-\d{4}-\d{2}-\d{2}"', rf'data-record-key="\1-{DATE}"', s2)
            s2 = s2.replace('本堂新條件練習：我的判斷與理由', '換你做（報名確認 App）：我的做法與自我檢查結果')
        if s2 != s:
            f.write_text(s2, encoding='utf-8')
    return unit, page, title, old_title


if __name__ == '__main__':
    rd = Path(sys.argv[1]); keys = sys.argv[2:] or sorted(UNITS)
    done = []
    for k in keys:
        src = rd / f'{k}.md'
        if src.exists():
            done.append(apply_unit(k, src.read_text(encoding='utf-8')))
    json.dump(done, open(rd / 'applied.json', 'w'), ensure_ascii=False, indent=1)
    for d in done:
        print(*d, sep=' | ')
