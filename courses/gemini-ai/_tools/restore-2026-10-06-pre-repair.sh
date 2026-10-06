#!/bin/bash
set -euo pipefail
COURSE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$COURSE_ROOT" "${1:-}" <<'PY'
from pathlib import Path
import sys,json,hashlib,shutil,re
root=Path(sys.argv[1]);backup=root/'_backup/2026-10-06-pre-repair'
m=json.loads((backup/'manifest.json').read_text())
for r in m['files']:
    assert hashlib.sha256((backup/r['file']).read_bytes()).hexdigest()==r['sha256'], r['file']
for r in m['files']:
    shutil.copy2(backup/r['file'],root/r['file'])
# New assets are retained for inspection; no unrelated files are removed.
print(f"已還原 {len(m['files'])} 個原有頁面；新素材保留。")
if sys.argv[2]=='--site':
    site=root.parent.parent
    p=site/'search-index.json'
    old=json.loads((backup/'site-ops/search-index.json').read_text())
    current=json.loads(p.read_text()) if p.is_file() else old
    restored=[x for x in old if x['course']=='gemini-ai']
    merged=[];inserted=False
    for x in current:
        if x['course']=='gemini-ai':
            if not inserted:merged.extend(restored);inserted=True
        else:merged.append(x)
    if not inserted:merged.extend(restored)
    p.write_text(json.dumps(merged,ensure_ascii=False,separators=(',',':')))
    p=site/'sitemap.xml';oldxml=(backup/'site-ops/sitemap.xml').read_text()
    currentxml=p.read_text() if p.is_file() else oldxml
    pattern=r'  <url>\n.*?  </url>\n'
    for block in re.findall(pattern,currentxml,re.S):
        if '/courses/gemini-ai/' in block:currentxml=currentxml.replace(block,'',1)
    blocks=[b for b in re.findall(pattern,oldxml,re.S) if '/courses/gemini-ai/' in b]
    p.write_text(currentxml.replace('</urlset>',''.join(blocks)+'</urlset>'))
    print('已還原搜尋與 sitemap 的本課紀錄；其他課程保留。')
else:
    print('如需一併還原搜尋與 sitemap，請加 --site；其備份位於 site-ops/。')
PY
