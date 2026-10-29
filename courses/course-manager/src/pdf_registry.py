"""PDF library inventory and provenance status, separate from folder catalog."""
from __future__ import annotations
import json
import contextlib
import fcntl
import re
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from .pdf_sources import PipelineError, inside, sha, prepare, load_recipe


def now(): return datetime.now().astimezone().isoformat()


@contextlib.contextmanager
def operation_lock(root):
    directory=root.resolve()/'course-manager/operations/pdf-build'; directory.mkdir(parents=True,exist_ok=True)
    with (directory/'.lock').open('a') as stream:
        try: fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as e: raise PipelineError('Another PDF operation is running') from e
        try: yield directory
        finally: fcntl.flock(stream,fcntl.LOCK_UN)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name('.'+path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)


def catalog_path(root): return root / 'course-manager/registry/pdf/catalog.json'


def read_catalog(root):
    path=catalog_path(root)
    return json.loads(path.read_text()) if path.exists() else {'schema_version':1,'artifacts':[]}


def render_index(root: Path, catalog: dict) -> str:
    lines=['# PDF 講義管理索引','','由 course-manager PDF 登錄產生。狀態為最後登錄／提升時的紀錄；取用前以 `status` 重新檢查來源。',
           '',f'登錄時間：{catalog.get("updated_at","未記錄")}','',
           'UNVERIFIED 表示來源一致性尚未驗證；檔案存在不代表已與網頁同步。','']
    for course in sorted({a['course'] for a in catalog['artifacts']}):
        lines.extend([f'## {course}','','| 講義 | 來源狀態 | 來源類型 |','| --- | --- | --- |'])
        for entry in sorted((a for a in catalog['artifacts'] if a['course']==course),key=lambda a:a['output']):
            output=inside(root,entry['output']); label=output.name.replace('[','\\[').replace(']','\\]').replace('|','\\|')
            available=output.exists() or entry.get('source_state')=='CURRENT'
            link=f'[{label}]({quote(course+"/"+output.name)})' if available else label+'（尚無成品）'
            lines.append(f'| {link} | {entry.get("source_state","UNVERIFIED")} | {entry.get("source_type","未指定")} |')
        lines.append('')
    return '\n'.join(lines)+'\n'


def inventory(root: Path):
    files=[]
    library=root/'output/pdf'
    for path in sorted(root.rglob('*')):
        if path.suffix.lower()!='.pdf' or not path.is_file(): continue
        relative=path.relative_to(root).as_posix()
        parts=path.relative_to(root).parts
        if path.is_symlink(): role='symlink-excluded'
        elif any(p in {'.git','.worktrees','worktrees'} for p in parts): role='worktree'
        elif any(re.search(r'backup|archive',p,re.I) for p in parts): role='backup'
        elif any(p in {'_validation','_review','tmp','temp','pdf-build'} for p in parts) or 'course-manager/operations/' in relative: role='evidence-or-temporary'
        elif path.parent.parent==library: role='handout-library'
        else: role='outside-library-review-needed'
        files.append({'path':relative,'bytes':path.lstat().st_size if path.is_symlink() else path.stat().st_size,
                      'sha256':None if path.is_symlink() else sha(path),'role':role})
    return {'checked_at':now(),'files':files,'counts':{r:sum(f['role']==r for f in files) for r in sorted({f['role'] for f in files})}}


def source_candidates(root, path):
    course=path.parent.name
    project=root/course
    name=path.name
    if course=='universal-portfolio-builder':
        return {'source_type':'pdf-only','candidate_sources':[],'reason':'No confirmed HTML source; retain legacy guide'}
    if course=='digital-marketing-70h' and name in {'回家30分鐘復跑手冊.pdf','全課程Prompt工具箱.pdf'}:
        rel='assets/after-class-guide.md' if name.startswith('回家') else 'assets/datasets/prompts-all.md'
        return {'source_type':'markdown-material','candidate_sources':[f'{course}/{rel}'],'reason':'Existing builder reads Markdown; not HTML conversion'}
    if course=='simple-ai' or '速查' in name or '跟課' in name or (course=='personal-automation' and name=='印刷版講義.pdf'):
        kind='edited-or-excerpted'
    else: kind='html-candidates'
    html=[]
    if project.exists():
        for p in sorted(project.rglob('*.html')):
            rel=p.relative_to(project)
            if any(part.startswith(('_','.')) or part in {'tmp','output','assets','node_modules'} for part in rel.parts): continue
            if re.match(r'index|module|handbook|prompt-library',p.stem,re.I): continue
            html.append(p.relative_to(root).as_posix())
    chapter=re.search(r'ADMIN-AI-CH(\d+)',name)
    module=re.search(r'DM70-M(\d+)',name)
    if chapter: html=[p for p in html if Path(p).name==f'CH{int(chapter[1])}.html']
    if module:
        n=int(module[1]); html=[p for p in html if re.match(rf'm{n}(?:[a-z])?-',Path(p).stem)]
    return {'source_type':kind,'candidate_sources':html,'reason':'Candidate association only; PDF/HTML fidelity and order not verified'}


def register_existing(root: Path):
    with operation_lock(root): return _register_existing(root.resolve())


def _register_existing(root: Path):
    catalog=read_catalog(root)
    known={a['output']:a for a in catalog['artifacts']}
    imported=0
    for path in sorted((root/'output/pdf').glob('*/*')):
        if path.suffix.lower()!='.pdf' or not path.is_file() or path.is_symlink(): continue
        relative=path.relative_to(root).as_posix()
        if relative in known: continue
        record={'course':path.parent.name,'output':relative,'imported_at':now(),
                'imported_sha256':sha(path),'recipe':None,'last_verified_build':None,
                'source_state':'UNVERIFIED',**source_candidates(root,path)}
        # Identity depends on path, not iteration or engine revision.
        import hashlib
        record['artifact_id']='legacy-'+hashlib.sha256(relative.encode()).hexdigest()[:16]
        catalog['artifacts'].append(record); imported+=1
    catalog['updated_at']=now()
    write_json(catalog_path(root),catalog)
    index=root/'output/pdf/INDEX.md'
    temporary=index.with_name('.INDEX.md.tmp'); temporary.write_text(render_index(root,catalog),encoding='utf-8'); temporary.replace(index)
    return {'registered':imported,'total':len(catalog['artifacts']),'catalog':str(catalog_path(root))}


def derive_state(proof, fingerprint, current_hash):
    if not proof or proof.get('verified') is not True: return 'UNVERIFIED'
    if current_hash != proof.get('pdf_sha256'): return 'UNVERIFIED'
    return 'CURRENT' if fingerprint==proof.get('fingerprint') else 'STALE'


def status(root: Path, artifact_id=None):
    rows=[]
    for entry in read_catalog(root)['artifacts']:
        if artifact_id and entry['artifact_id']!=artifact_id: continue
        path=inside(root,entry['output'])
        row={k:entry.get(k) for k in ('artifact_id','course','output','source_type','recipe','candidate_build','last_build_result')}
        row['checked_at']=now()
        if not path.exists(): row.update(source_state='BLOCKED',reason='Output missing')
        elif not entry.get('recipe'): row.update(source_state='UNVERIFIED',reason='No confirmed build recipe')
        else:
            try:
                recipe=load_recipe(root,inside(root,entry['recipe']))
                if recipe['output']!=entry['output'] or recipe['artifact_id']!=entry['artifact_id']:
                    raise PipelineError('Catalog and recipe identity mismatch')
                result=prepare(root,recipe)
                proof=entry.get('last_verified_build') or {}
                if proof:
                    manifest_path=inside(root,proof.get('manifest',''))
                    if not manifest_path.is_relative_to(root/'course-manager/operations/pdf-build'):
                        raise PipelineError('Invalid provenance manifest location')
                    manifest=json.loads(manifest_path.read_text())
                    review=manifest_path.parent/'accepted-review.json'
                    if manifest.get('status')!='PROMOTED' or manifest.get('pdf_sha256')!=proof.get('pdf_sha256') or manifest.get('fingerprint')!=proof.get('fingerprint'):
                        raise PipelineError('Incomplete or inconsistent promotion provenance')
                    if not review.exists() or sha(review)!=manifest.get('accepted_review_sha256'):
                        raise PipelineError('Accepted review evidence missing or changed')
                row.update(source_state=derive_state(proof,result['fingerprint'],sha(path)),fingerprint=result['fingerprint'])
            except (PipelineError,OSError,ValueError) as e: row.update(source_state='BLOCKED',reason=str(e))
        rows.append(row)
    if artifact_id and not rows: raise PipelineError(f'Unknown artifact_id: {artifact_id}')
    return {'checked_at':now(),'artifacts':rows,'counts':{s:sum(r['source_state']==s for r in rows) for s in sorted({r['source_state'] for r in rows})}}


def bind_recipe(root: Path, recipe_path: Path):
    with operation_lock(root): return _bind_recipe(root.resolve(),recipe_path)


def _bind_recipe(root: Path, recipe_path: Path):
    recipe=load_recipe(root,recipe_path)
    prepare(root,recipe)  # Confirm dependencies and selectors before registering a recipe.
    catalog=read_catalog(root)
    record=next((a for a in catalog['artifacts'] if a['output']==recipe['output']),None)
    if record is None:
        record={'artifact_id':recipe['artifact_id'],'course':recipe['course'],'output':recipe['output'],
                'last_verified_build':None,'source_state':'UNVERIFIED'}
        catalog['artifacts'].append(record)
    if any(a is not record and a['artifact_id']==recipe['artifact_id'] for a in catalog['artifacts']): raise PipelineError('artifact_id collision')
    record.update(artifact_id=recipe['artifact_id'],recipe=recipe_path.resolve().relative_to(root).as_posix(),source_type='confirmed-html-recipe')
    catalog['updated_at']=now(); write_json(catalog_path(root),catalog)
    return {'artifact_id':record['artifact_id'],'source_state':'UNVERIFIED','recipe':record['recipe']}
