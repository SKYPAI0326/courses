from pathlib import Path
from bs4 import BeautifulSoup
import re,html,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parents[1]
UNITS=[('A1-visual-foundations','part1/CH1-visual-foundations.html',5),('A2-grid-layout','part1/CH2-grid-layout.html',6),('A3-auto-layout-pressure','part1/CH3-auto-layout-pressure.html',6),('A4-component-instance','part1/CH4-component-instance.html',5),('A5-variants-properties','part1/CH5-variants-properties.html',6),('A6-button-form','part1/CH6-button-form.html',6),('A7-list-content','part1/CH7-list-content.html',4),('A8-toast-dialog-navigation','part1/CH8-toast-dialog-navigation.html',4),('B1-wireframe-prototype-entry','part2/CH1-wireframe-prototype-entry.html',7),('B2-trigger-navigation-action','part2/CH2-trigger-navigation-action.html',6),('B3-transition-motion-purpose','part2/CH3-transition-motion-purpose.html',6),('B4-overlay-single-action','part2/CH4-overlay-single-action.html',7),('B5-scroll-fixed-floating','part2/CH5-scroll-fixed-floating.html',6),('B6-prototype-task-test','part2/CH6-prototype-task-test.html',6),('B7-figma-handoff-export','part2/CH7-figma-handoff-export.html',6),('B8-web-git-deploy','part3/CH8-web-git-deploy.html',13)]
def inline(s):
    tokens=[]
    def hold(x):tokens.append(x);return f'ZZTOKEN{len(tokens)-1}ZZ'
    s=re.sub(r'`([^`]+)`',lambda m:hold('<code>'+html.escape(m[1])+'</code>'),s)
    s=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',lambda m:hold(f'<figure><img src="{html.escape(m[2],quote=True)}" alt="{html.escape(m[1],quote=True)}" loading="lazy"><figcaption>{html.escape(m[1])}</figcaption></figure>'),s)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:hold(f'<a href="{html.escape(m[2],quote=True)}">{html.escape(m[1])}</a>'),s)
    s=html.escape(s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    for i,t in enumerate(tokens):s=s.replace(f'ZZTOKEN{i}ZZ',t)
    return s

def render(md):
    lines=md.strip().splitlines(); out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('```'):
            lang=line[3:];i+=1;code=[]
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            out.append('<pre><code data-language="'+html.escape(lang)+'">'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=lines[i].strip().strip('|').split('|');i+=1
                if all(re.fullmatch(r'\s*:?-+:?\s*',x) for x in cells):continue
                rows.append(cells)
            out.append('<div class="table-wrap"><table class="data-table"><thead><tr>'+''.join('<th scope="col">'+inline(x.strip())+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x.strip())+'</td>' for x in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
        m=re.match(r'^(#{1,6}) (.+)',line)
        if m:out.append(f'<h{len(m[1])}>'+inline(m[2])+f'</h{len(m[1])}>');i+=1;continue
        if re.match(r'^(\d+\. |[-*] )',line):
            ordered=bool(re.match(r'^\d+\. ',line));items=[]
            while i<len(lines) and re.match(r'^(\d+\. |[-*] )',lines[i].strip()):
                items.append(inline(re.sub(r'^(\d+\. |[-*] )','',lines[i].strip())));i+=1
            tag='ol' if ordered else 'ul';out.append(f'<{tag} class="step-list">'+''.join('<li>'+x+'</li>' for x in items)+f'</{tag}>');continue
        if line.startswith('!['):
            out.append(inline(line));i+=1;continue
        if line.startswith('<'):
            raw=[]
            while i<len(lines) and lines[i].strip():raw.append(lines[i]);i+=1
            out.append('\n'.join(raw));continue
        p=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|\d+\. |[-*] |<)',lines[i].strip()):p.append(lines[i].strip());i+=1
        out.append('<p class="body-text">'+inline(' '.join(p))+'</p>')
    return '\n'.join(out)
