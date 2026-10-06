"""Run official builders to candidates, merge only gemini-ai records."""
from pathlib import Path
import runpy,sys,json,re,hashlib,shutil
COURSE=Path(__file__).resolve().parents[1];SITE=COURSE.parent.parent;OUT=COURSE/'_repair/2026-10-06'
BACKUP=COURSE/'_backup/2026-10-06-pre-repair/site-ops';BACKUP.mkdir(exist_ok=True)
sys.path.insert(0,str(SITE/'docs'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--apply' not in sys.argv:
    baseline={}
    for name,script in [('search-index.json','build-search-index.py'),('sitemap.xml','build-sitemap.py')]:
        p=SITE/name;baseline[name]=digest(p);shutil.copy2(p,BACKUP/name)
        ns=runpy.run_path(str(SITE/'docs'/script));ns['main'].__globals__['OUT']=OUT/('generated-'+name);ns['main']()
    old=json.loads((SITE/'search-index.json').read_text());generated=json.loads((OUT/'generated-search-index.json').read_text())
    selected=[x for x in generated if x['course']=='gemini-ai'];assert len(selected)==45
    merged=[];inserted=False
    for x in old:
        if x['course']=='gemini-ai':
            if not inserted:merged.extend(selected);inserted=True
        else:merged.append(x)
    if not inserted:merged.extend(selected)
    assert [x for x in old if x['course']!='gemini-ai']==[x for x in merged if x['course']!='gemini-ai']
    (OUT/'scoped-search-index.json').write_text(json.dumps(merged,ensure_ascii=False,separators=(',',':')))
    oldxml=(SITE/'sitemap.xml').read_text();newxml=(OUT/'generated-sitemap.xml').read_text()
    blocks=re.findall(r'  <url>\n.*?  </url>\n',newxml,re.S)
    selectedxml=[x for x in blocks if '/courses/gemini-ai/' in x]
    oldblocks=re.findall(r'  <url>\n.*?  </url>\n',oldxml,re.S)
    mergedxml=oldxml
    for x in oldblocks:
        if '/courses/gemini-ai/' in x:mergedxml=mergedxml.replace(x,'',1)
    mergedxml=mergedxml.replace('</urlset>',''.join(selectedxml)+'</urlset>')
    assert [x for x in oldblocks if '/courses/gemini-ai/' not in x]==[x for x in re.findall(r'  <url>\n.*?  </url>\n',mergedxml,re.S) if '/courses/gemini-ai/' not in x]
    (OUT/'scoped-sitemap.xml').write_text(mergedxml)
    (OUT/'ops-baseline.json').write_text(json.dumps({'sha256':baseline,'course_search_entries':len(selected),'course_public_sitemap_entries':len(selectedxml),'other_courses_unchanged':True},indent=2))
    print('已建立本課索引差異與備份；其他課程紀錄完全保留。')
else:
    b=json.loads((OUT/'ops-baseline.json').read_text())
    for name,hash in b['sha256'].items():assert digest(SITE/name)==hash, 'Concurrent change: '+name
    for name in ['search-index.json','sitemap.xml']:shutil.copy2(OUT/('scoped-'+name),SITE/name)
    print('已套用本課搜尋／sitemap；其他課程紀錄未變。')
