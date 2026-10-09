from pathlib import Path
import json,hashlib,shutil,sys,importlib.util
root=Path(__file__).resolve().parents[1];site=root.parents[1];backup=root/'_backup/2026-10-09-pre-repair';manifest=json.loads((backup/'manifest.json').read_text())
search=site/'search-index.json';rel=search.relative_to(site).as_posix()
if not any(x['path']==rel for x in manifest['files']):
 dst=backup/'site'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(search,dst);manifest['files'].append({'path':rel,'sha256':hashlib.sha256(search.read_bytes()).hexdigest()});(backup/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# No unrelated course source is modified.
lessons=site/'_lessons/gen-ai-36h';lessons.mkdir(exist_ok=True)
for p in (root/'_repair/2026-10-09/lesson-plans').glob('*.md'):shutil.copy2(p,lessons/p.name)
shutil.copy2(root/'_repair/2026-10-09/outline-updated.md',site/'_outlines/gen-ai-36h.md')
# Use site extraction rules, updating only this course's public page entries.
sys.path.insert(0,str(site/'docs'));spec=importlib.util.spec_from_file_location('search_builder',site/'docs/build-search-index.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
entries=json.loads(search.read_text());before=[x for x in entries if x.get('course')!='gen-ai-36h'];new=[]
for p in sorted(mod.iter_public_html(root,site)):
 if not mod.should_ignore(p):
  t,d=mod.extract(p);new.append({'url':p.relative_to(site).as_posix(),'title':t,'desc':d,'course':'gen-ai-36h','course_label':mod.COURSE_LABEL['gen-ai-36h'],'type':mod.classify(p)})
# Stable insertion position, preserving other course entries byte-equivalent as objects.
idx=next((i for i,x in enumerate(entries) if x.get('course')=='gen-ai-36h'),len(entries));out=entries[:idx]+new+[x for x in entries[idx:] if x.get('course')!='gen-ai-36h'];assert [x for x in out if x.get('course')!='gen-ai-36h']==before
search.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('Synced 28 same-course sources, outline and',len(new),'public search entries; other courses preserved.')
