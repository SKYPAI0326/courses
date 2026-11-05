"""assets/datasets/*.md → 同名 .html 閱讀頁（2026-11-05 起，舊問題 D：學員點 .md 只看到原始 Markdown 符號）。

用法（在 repo 根目錄）：python3 courses/digital-marketing-70h/_tools/render-materials.py
.md 仍是來源檔，也保留給學員「複製全部文字貼進 AI 對話」；.html 只給閱讀。
render-lessons.py 轉製單元頁時，若同名 .html 存在，會把 `assets/datasets/*.md` 連結改指向 .html。
"""
from pathlib import Path
from html import escape
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
src = root / 'assets' / 'datasets'
md = MarkdownIt('commonmark').enable('table')

CSS = ':root{--paper:#fbf7ef;--surface:#fffdf8;--text:#34312d;--muted:#6d675f;--line:#ded5c8;--accent:#c9963a;--accent-soft:#f5e7c7}' \
      '*{box-sizing:border-box}body{margin:0;color:var(--text);background:var(--paper);font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;line-height:1.75}' \
      '.container{width:min(920px,calc(100% - 32px));margin:0 auto;padding:32px 0 64px}' \
      '.copy-note{background:var(--accent-soft);border:1px solid var(--line);border-radius:6px;padding:10px 14px;font-size:.95rem}' \
      'h1{font-size:1.75rem;line-height:1.35;margin:1.2rem 0 .8rem}h2{font-size:1.35rem;margin:2rem 0 .6rem;padding-top:.6rem;border-top:1px solid var(--line)}h3{font-size:1.1rem;margin:1.4rem 0 .4rem}' \
      '.table-scroll{overflow-x:auto;margin:1rem 0}table{border-collapse:collapse;min-width:100%;background:var(--surface);font-size:.95rem}' \
      'th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;min-width:7em}th{background:var(--accent-soft)}' \
      'code{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:.9em;word-break:break-all}' \
      'blockquote{margin:1rem 0;padding:.6rem 1rem;border-left:3px solid var(--accent);background:var(--surface)}a{color:#765416}'

n = 0
for f in sorted(src.glob('*.md')):
    text = f.read_text()
    title = next((l.removeprefix('# ').strip() for l in text.splitlines() if l.startswith('# ')), f.stem)
    s = BeautifulSoup(md.render(text), 'html.parser')
    for t in s.find_all('table'):
        t.wrap(s.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0', 'role': 'region', 'aria-label': '資料表，可水平捲動'}))
    for a in s.find_all('a', href=True):
        # 素材之間的連結（不論寫成 x.md 或 assets/datasets/x.md）都改指同資料夾的閱讀版
        name = Path(a['href']).name
        if name.endswith('.md') and (src / name).exists():
            a['href'] = Path(name).with_suffix('.html').name
    desc = escape(title)
    page = f'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="數位行銷人才培訓課程素材閱讀版：{desc}">
  <title>{escape(title)}｜數位行銷人才培訓素材</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="container">
    <p class="copy-note">這是閱讀版。要把內容貼進 AI 對話時，打開<a href="{escape(f.name)}">文字版（{escape(f.name)}）</a>，全選複製。</p>
{s}
  </main>
</body>
</html>
'''
    f.with_suffix('.html').write_text(page)
    n += 1
print('Rendered', n, 'materials')
