from pathlib import Path
import json,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT.parent.parent;V=ROOT/'_validation';V.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(p):return {'path':str(p.relative_to(SITE)),'sha256':sha(p)}
spec=importlib.util.spec_from_file_location('audit',SITE/'docs/audit-course-substance.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
meta=json.loads((ROOT/'_source/lesson-map.json').read_text());units=[];source_files=set();full_files=set()
for file,d in meta.items():
    source=ROOT/'_source/fragments'/d['fragment'];page=ROOT/file
    result=audit.audit_page(ROOT,page,SITE);assert result['status']=='MACHINE_CHECKED'
    assets=sorted({x['path'] for x in result['assets'] if x.get('sha256')})
    ident=Path(file).stem;platform=ident not in {'CH1-2','CH2-1'}
    u={'id':ident,'course_type':'integration-capstone' if ident=='PRAC4-3' else 'skill-operation','source':str(source.relative_to(SITE)),'page':str(page.relative_to(SITE)),'assets':assets,'platform_required':platform}
    if not platform:u['platform_reason']='本單元只讀取與判斷提供的參考品及資料，不要求外部模型生成。'
    units.append(u);source_files.add(source);source_files.update(SITE/x for x in assets)
    full_files.add(source);full_files.add(page);full_files.update(SITE/x for x in assets)
records=[];ids=[u['id'] for u in units]
for layer,actor,log,files,notes in [
 ('content','author-self-check',ROOT/'_review/2026-10-06-CONTENT-FIDELITY.md',source_files,'逐站自審源頭、素材、完整例子、同步判斷、修復與獨立改造；未冒充獨立審查或真人。'),
 ('fidelity','author-self-check',ROOT/'_review/2026-10-06-CONTENT-FIDELITY.md',full_files,'逐站讀取正式HTML並比對核心指令、數字、答案、資產與修復；字串檢查為輔助。'),
 ('technical','tool-run',ROOT/'_repair/2026-10-06/TECHNICAL-VERIFICATION.md',full_files,'記錄實際lint、結構、連結與受測本機成品；外部平台生成與真人學習另列PENDING。')]:
    records.append({'layer':layer,'unit_ids':ids,'actor':actor,'verdict':'PASS','notes':notes,'log':snap(log),'artifacts':[snap(p) for p in sorted(files)]})
records.append({'layer':'platform','unit_ids':[u['id'] for u in units if u['platform_required']],'actor':'tool-run','verdict':'PENDING','notes':'Google要求重新驗證身分；未生成Chat/Build成果或呼叫模型。'})
data={'schema_version':1,'outline':snap(ROOT/'_source/OUTLINE.md'),'scope_note':'覆蓋修訂大綱的10站必修；其餘30頁只記技術與用途分流，不含選修完整真人驗收。參考工具測試不能替代學員AI生成與模型呼叫。','units':units,'records':records}
(V/'evidence.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('已綁定10站來源、頁面、全部實際引用素材與三層證據版本。')
