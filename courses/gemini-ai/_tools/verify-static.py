from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import collections,json,hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT.parent.parent;OUT=ROOT/'_repair/2026-10-06'
meta=json.loads((ROOT/'_source/lesson-map.json').read_text());route=list(meta)
files=[ROOT/'index.html',*sorted(ROOT.glob('part*/*.html')),*sorted((ROOT/'assets/tools').glob('*.html'))]
broken=[];badanchors=[];duplicates=[];copies=collections.defaultdict(list);fidelity=[]
for p in files:
    s=BeautifulSoup(p.read_text(),'html.parser');ids=[x['id'] for x in s.select('[id]')]
    if len(ids)!=len(set(ids)):duplicates.append(str(p.relative_to(ROOT)))
    for a in s.select('a[href]'):
        u=urlsplit(a['href'])
        if u.scheme or u.netloc:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if not target.is_file():broken.append([str(p.relative_to(ROOT)),a['href']]);continue
        if u.fragment and target.suffix=='.html' and not BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment)):
            badanchors.append([str(p.relative_to(ROOT)),a['href']])
    for n in s.select('.lesson-body > .lesson-section .body-text'):
        if n.find_parent('details'):continue
        t=n.get_text(' ',strip=True)
        if len(t)>40:copies[t].append(str(p.relative_to(ROOT)))
    rel=str(p.relative_to(ROOT))
    if rel in meta:
        source=ROOT/'_source/fragments'/meta[rel]['fragment'];ss=BeautifulSoup(source.read_text(),'html.parser')
        for sec in ss.select('.lesson-section'):
            actual=s.select_one('.lesson-body > #'+sec['id']);assert actual is not None
            assert actual.get_text(' ',strip=True)==sec.get_text(' ',strip=True),(rel,sec['id'])
            assert [(a.get('href'),a.get('download')) for a in actual.select('a')]==[(a.get('href'),a.get('download')) for a in sec.select('a')]
        fidelity.append({'page':rel,'source':str(source.relative_to(ROOT)),'text_and_links':'MATCH'})
for i,f in enumerate(route):
    s=BeautifulSoup((ROOT/f).read_text(),'html.parser')
    actual=(ROOT/f).parent/s.select_one('.lesson-nav [data-nav-role="next"]')['href']
    assert actual.resolve()==(ROOT/(route[i+1] if i+1<len(route) else 'index.html')).resolve()
    assert s.select_one('#legacy-reference') is not None
assert not broken and not badanchors and not duplicates,(broken,badanchors,duplicates)
shared=[(t,ps) for t,ps in copies.items() if len(ps)>2];assert not shared,shared
with zipfile.ZipFile(ROOT/'assets/materials/materials.zip') as z:
    for p in (ROOT/'assets/materials').iterdir():
        if p.suffix!='.zip':assert z.read(p.name)==p.read_bytes(),p.name
baseline=json.loads((ROOT/'_repair/2026-10-06/ops-baseline.json').read_text())
old=json.loads((ROOT/'_backup/2026-10-06-pre-repair/site-ops/search-index.json').read_text())
current=json.loads((SITE/'search-index.json').read_text())
assert [x for x in old if x['course']!='gemini-ai']==[x for x in current if x['course']!='gemini-ai']
assert len([x for x in current if x['course']=='gemini-ai'])==45
report={'pages':len(files),'broken_links':broken,'broken_fragments':badanchors,'duplicate_ids':duplicates,'shared_long_copy':shared,'required_route':route,'fidelity':fidelity,'zip_matches_materials':True,'other_course_search_entries_unchanged':True,'versions':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(OUT/'link-and-copy-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('PASS：45頁連結與錨點、10站路線與源頭保真、素材ZIP、長文去重與搜尋範圍。')
