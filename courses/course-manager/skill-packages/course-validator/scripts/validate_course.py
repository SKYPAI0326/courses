#!/usr/bin/env python3
"""Validate versioned course evidence; never infer learning from scores or lint."""
import argparse, hashlib, importlib.util, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True
TYPES={'concept','skill-operation','programming','integration-capstone'}
LAYERS={'technical','content','fidelity','entry','completion','understanding','transfer','platform','sequence'}
ACTORS={'author-self-check','independent-ai','human','tool-run'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_file(root,value):
    if not isinstance(value,str) or not value: raise ValueError('empty or non-string path')
    p=(root/value).resolve()
    if not p.is_relative_to(root) or not p.is_file(): raise ValueError(f'file unavailable or outside project: {value}')
    return p

def evaluate(root,slug,content_only=False,only_unit=None):
    root=root.resolve();course=(root/'courses'/slug).resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',slug) or not course.is_relative_to(root/'courses') or not course.is_dir():
        raise ValueError('invalid course directory')
    ep=course/'_validation/evidence.json';errors=[];pending=[];machine=[]
    if not ep.exists():
        raise ValueError('missing _validation/evidence.json; use references/evidence-format.md')
    data=json.loads(ep.read_text())
    if not isinstance(data,dict): raise ValueError('evidence must be an object')
    if data.get('schema_version')!=1: raise ValueError('unsupported evidence schema_version')
    units=data.get('units');records=data.get('records',[])
    if not isinstance(units,list) or not units or not isinstance(records,list): raise ValueError('units and records must be lists; units cannot be empty')
    ids=[u.get('id') for u in units if isinstance(u,dict)]
    if len(ids)!=len(units) or any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=len(ids): raise ValueError('invalid or duplicate unit ids')
    if only_unit and only_unit not in ids: raise ValueError('unknown --unit')
    outline=data.get('outline')
    if not isinstance(outline,dict): raise ValueError('outline path/hash required')
    op=safe_file(root,outline.get('path'))
    if sha(op)!=outline.get('sha256'): errors.append('outline version changed; reconcile unit scope and dependencies')
    scope=data.get('scope_note')
    if not isinstance(scope,str) or not scope.strip(): errors.append('scope_note must state covered units and excluded branches')
    required={};selected=[u for u in units if not only_unit or u['id']==only_unit]
    if not content_only:
        spec=importlib.util.spec_from_file_location('course_audit',root/'docs/audit-course-substance.py')
        audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    for u in selected:
        ident=u['id']
        if u.get('course_type') not in TYPES: errors.append(f'{ident}: invalid course_type')
        if not isinstance(u.get('platform_required'),bool): errors.append(f'{ident}: platform_required must be boolean')
        elif not u['platform_required'] and not u.get('platform_reason'): errors.append(f'{ident}: platform N/A reason missing')
        try:
            source=safe_file(root,u.get('source'));body=source.read_text()
            if body.count('<!-- learner-content:start -->')!=1 or body.count('<!-- learner-content:end -->')!=1:
                raise ValueError('formal learner-content boundaries missing or duplicated')
            start=body.index('<!-- learner-content:start -->')+len('<!-- learner-content:start -->');end=body.index('<!-- learner-content:end -->')
            if end<=start or not body[start:end].strip(): raise ValueError('formal learner body empty or boundaries reversed')
            assets=u.get('assets',[])
            if not isinstance(assets,list): raise ValueError('assets must be list')
            required[ident]={str(source.relative_to(root))}
            for a in assets: required[ident].add(str(safe_file(root,a).relative_to(root)))
            if not content_only:
                page=safe_file(root,u.get('page'))
                if not page.is_relative_to(course) or page.suffix!='.html': raise ValueError('page must be HTML inside course')
                required[ident].add(str(page.relative_to(root)))
                result=audit.audit_page(course,page,root);machine.append(result)
                if result['status']=='BLOCK': errors.append(f'{ident}: page check failed {result["hard_failures"]} {result["broken_links"]}')
                # Every learner asset discovered on page must be version-bound too.
                required[ident].update(a['path'] for a in result['assets'] if a.get('sha256'))
        except (ValueError,OSError,UnicodeError) as e: errors.append(f'{ident}: {e}')
    # Keep record history; only the latest same layer/unit-set/actor is active.
    latest={}
    for r in records:
        if not isinstance(r,dict) or r.get('layer') not in LAYERS or r.get('actor') not in ACTORS or r.get('verdict') not in {'PASS','FAIL','PENDING'}:
            errors.append('invalid record layer/actor/verdict');continue
        rids=r.get('unit_ids')
        if not isinstance(rids,list) or not rids or any(x not in ids for x in rids) or len(set(rids))!=len(rids):
            errors.append('record unit_ids invalid');continue
        latest[(r['layer'],tuple(sorted(rids)),r['actor'])]=r
    valid=[]
    for r in latest.values():
        affected=set(r['unit_ids']) & set(required)
        if not affected or (content_only and r['layer']!='content'): continue
        label=f"{r['layer']}/{','.join(r['unit_ids'])}/{r['actor']}"
        if r['verdict']=='PENDING': pending.append(label);continue
        if r['verdict']=='FAIL': errors.append(label+': unresolved FAIL');continue
        try:
            if not isinstance(r.get('notes'),str) or not r['notes'].strip(): raise ValueError('notes missing')
            log=r.get('log',{});lp=safe_file(root,log.get('path'))
            if sha(lp)!=log.get('sha256'): raise ValueError('log hash mismatch')
            if not lp.read_text().strip(): raise ValueError('empty evidence log')
            snaps=r.get('artifacts')
            if not isinstance(snaps,list) or not snaps: raise ValueError('artifact snapshots missing')
            seen=set()
            for a in snaps:
                p=safe_file(root,a.get('path'));key=str(p.relative_to(root))
                if key in seen: raise ValueError('duplicate artifact snapshot')
                seen.add(key)
                if sha(p)!=a.get('sha256'): raise ValueError(f'stale artifact: {key}')
            expected=set().union(*(required[x] for x in affected))
            if r['layer']=='content':
                expected={str(safe_file(root,x).relative_to(root)) for u in selected if u['id'] in affected for x in [u['source'],*u.get('assets',[])]}
            if not expected <= seen: raise ValueError('record omits required source/page/assets: '+', '.join(sorted(expected-seen)))
            if r['layer']=='sequence' and len(r['unit_ids'])<min(3,len(units)): raise ValueError('sequence scope too short')
            valid.append(r)
        except (AttributeError,TypeError,ValueError,OSError,UnicodeError) as e: errors.append(label+': '+str(e))
    def has(layer,unit,actors=None):
        return any(r['layer']==layer and unit in r['unit_ids'] and (actors is None or r['actor'] in actors) for r in valid)
    for u in selected:
        for layer in (['content'] if content_only else ['content','fidelity']):
            if not has(layer,u['id'],{'author-self-check','independent-ai','human'}): errors.append(f'{u["id"]}: missing valid {layer} review')
        if content_only: continue
        if not has('technical',u['id'],{'human','tool-run'}): errors.append(f'{u["id"]}: missing valid technical checks (lint and applicable runtime)')
        for layer in ['entry','completion','understanding','transfer']:
            if not has(layer,u['id'],{'human'}): pending.append(f'{u["id"]}: human {layer}')
        if u['platform_required'] and not has('platform',u['id'],{'human','tool-run'}): pending.append(f'{u["id"]}: actual platform run')
    if not content_only and not only_unit and len(units)>1:
        if not any(r['layer']=='sequence' and r['actor']=='human' and len(r['unit_ids'])>=min(3,len(units)) for r in valid): pending.append('human sequence test')
    status='BLOCKED' if errors else ('MACHINE_CHECKED' if content_only else 'MACHINE_READY_PENDING_HUMAN' if pending else 'HUMAN_READY')
    return {'generated_at':datetime.now(timezone.utc).isoformat(),'course':slug,'status':status,'scope_note':scope,
            'unit_ids':[u['id'] for u in selected],'content_only':content_only,'errors':errors,'pending':sorted(set(pending)),
            'valid_record_count':len(valid),'pages':machine,
            'limitation':'Hashes verify attribution and freshness; semantic truth and actor identity require honest reviewer records.'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('slug');ap.add_argument('mode',nargs='?',default='all',choices=['all','preflight','status','report','content'])
    ap.add_argument('--unit');ap.add_argument('--root',type=Path);a=ap.parse_args()
    if a.root is None:
        configured=os.environ.get('COURSE_WEB_ROOT')
        if not configured: ap.error('COURSE_WEB_ROOT or --root is required')
        a.root=Path(configured)
    try: result=evaluate(a.root,a.slug,a.mode=='content',a.unit)
    except (ValueError,TypeError,KeyError,OSError,UnicodeError) as e:
        print(json.dumps({'status':'BLOCKED','error':str(e)},ensure_ascii=False));return 2
    if a.mode in {'all','report'}:
        d=a.root/'courses'/a.slug/'_validation';d.mkdir(parents=True,exist_ok=True)
        (d/'validation-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        (d/'L5-evidence-manifest.json').write_text(json.dumps({'course':a.slug,'pages':result['pages'],'generated_at':result['generated_at']},ensure_ascii=False,indent=2)+'\n')
        lines=[f'# 課程驗證：{a.slug}',f'\n狀態：{result["status"]}',f'\n範圍：{result["scope_note"]}',f'\n有效證據：{result["valid_record_count"]} 筆（不代表真人學會）','\n## 阻擋項目',*['- '+x for x in result['errors']],'\n## 待驗項目',*['- '+x for x in result['pending']],'\n完整機器結果：validation-result.json；原始證據：evidence.json。雜湊只驗版本，語意與受測者身分須如實記錄。']
        (d/'FINAL-REPORT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='pages'},ensure_ascii=False,indent=2))
    return int(bool(result['errors']))
if __name__=='__main__': raise SystemExit(main())
