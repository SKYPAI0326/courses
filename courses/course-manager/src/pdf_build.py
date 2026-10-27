"""Candidate rendering, evidence gates, version promotion and guarded rollback."""
from __future__ import annotations
import json
import os
import re
import shutil
import subprocess
import uuid
from collections import Counter
from urllib.parse import quote, urlsplit, urlunsplit
from pathlib import Path
from .pdf_sources import PipelineError, inside, sha, prepare, normalize_text, load_recipe
from .pdf_registry import now, write_json, read_catalog, catalog_path, operation_lock, render_index


def classify_build_error(error: BaseException):
    raw=str(error)
    sandbox_markers=('Sandbox restriction','_RegisterApplication','MachPortRendezvous','signal=SIGABRT','kill EPERM')
    if 'BrowserType.launch' in raw and any(marker in raw for marker in sandbox_markers):
        return {
            'code':'BROWSER_SANDBOX_BLOCKED',
            'message':('BROWSER_SANDBOX_BLOCKED: macOS sandbox 阻擋 Playwright Chromium 啟動。'
                       '正式 PDF 未變更，本次候選未完成；不要重試相同受限路徑，'
                       '請以該建置命令的單次必要權限重跑。'),
            'raw_log':raw,
        }
    return {'code':'BUILD_FAILED','message':raw,'raw_log':None}


def apply_changes(root: Path, changes: list, operation: Path):
    """Each replace is atomic; a persisted journal allows recovery across files."""
    root=root.resolve(); operation=operation.resolve()
    records=[]
    for i,(destination,candidate) in enumerate(changes):
        destination=destination.resolve(); candidate=candidate.resolve()
        if not destination.is_relative_to(root.resolve()) or not candidate.is_relative_to(root.resolve()):
            raise PipelineError('Transaction path escapes workspace')
        if not candidate.is_file(): raise PipelineError('Missing transaction candidate')
        backup=operation/f'backup-{i}{destination.suffix}'
        before=sha(destination) if destination.exists() else None
        if before: shutil.copy2(destination,backup)
        records.append({'destination':destination.relative_to(root).as_posix(),
                        'before':before,'after':sha(candidate),
                        'backup':backup.relative_to(root).as_posix() if before else None,
                        'applied':False})
    journal=operation/'transaction.json'
    write_json(journal,{'status':'PREPARED','changes':records})
    try:
        for record,(_,candidate) in zip(records,changes):
            destination=inside(root,record['destination'])
            current=sha(destination) if destination.exists() else None
            if current!=record['before']: raise PipelineError('Destination changed during transaction')
            destination.parent.mkdir(parents=True,exist_ok=True)
            temporary=destination.with_name('.'+destination.name+'.'+uuid.uuid4().hex+'.tmp')
            shutil.copy2(candidate,temporary)
            os.replace(temporary,destination)
            record['applied']=True
            write_json(journal,{'status':'APPLYING','changes':records})
        write_json(journal,{'status':'APPLIED','changes':records})
    except BaseException:
        # Recover only our exact writes; never overwrite a later unrelated edit.
        rollback_changes(root,[r for r in records if r['applied']],apply=True)
        write_json(journal,{'status':'ROLLED_BACK','changes':records})
        raise
    return records


def rollback_changes(root: Path, records: list, apply=False):
    root=root.resolve()
    for record in records:
        destination=inside(root,record['destination'])
        current=sha(destination) if destination.exists() else None
        if current!=record['after']: raise PipelineError('Rollback refused: output has later edits')
        if record.get('backup'):
            backup=inside(root,record['backup'])
            if not backup.exists() or sha(backup)!=record['before']: raise PipelineError('Rollback backup missing or modified')
    if apply:
        for record in reversed(records):
            destination=inside(root,record['destination'])
            if record.get('backup'):
                temporary=destination.with_name('.'+destination.name+'.rollback.tmp')
                shutil.copy2(inside(root,record['backup']),temporary); os.replace(temporary,destination)
            else: destination.unlink()
    return {'status':'ROLLED_BACK' if apply else 'DRY_RUN','files':len(records)}


def inspect_pdf(path: Path, prepared: dict):
    from pypdf import PdfReader
    reader=PdfReader(path)
    texts=[re.sub(r'Page\s+\d+\s*/\s*\d+', '', p.extract_text() or '') for p in reader.pages]
    actual=normalize_text('\n'.join(texts))
    expected=normalize_text(prepared['expected_text'])
    errors=[]
    if not reader.pages: errors.append('empty-pdf')
    # Chrome paints positioned boxes and emphasized spans separately from their
    # surrounding text. Verify source runs with independent reading orders,
    # together with glyph multiplicity; do not rewrite or discard source text.
    poppler=subprocess.run(['pdftotext','-layout',str(path),'-'],check=True,capture_output=True,text=True).stdout
    variants=[actual,normalize_text(re.sub(r'Page\s+\d+\s*/\s*\d+','',poppler))]
    from bs4 import BeautifulSoup
    body=BeautifulSoup(prepared['html'],'html.parser').body
    for node in body.select('style,script'): node.decompose()
    runs=[normalize_text(str(s)) for s in body.strings if normalize_text(str(s))]
    # VS16 selects emoji presentation, has no visible glyph of its own, and is
    # often omitted from the PDF's ToUnicode mapping. Preserve it in source DOM.
    missing_runs=[r for r in runs if not any(r.replace('\ufe0f','') in v.replace('\ufe0f','') for v in variants)]
    missing_glyphs=dict(Counter(expected.replace('\ufe0f',''))-Counter(actual.replace('\ufe0f','')))
    if missing_runs or missing_glyphs: errors.append('teaching-text-not-preserved')
    uris=[]; internal_links=0
    for page in reader.pages:
        for ref in page.get('/Annots',[]):
            annotation=ref.get_object(); action=annotation.get('/A',{})
            if annotation.get('/Dest') or action.get('/S')=='/GoTo': internal_links+=1
            uri=str(action.get('/URI',''))
            if uri:
                uris.append(uri)
                if uri.startswith(('file:','about:','javascript:')): errors.append('local-runtime-url-leaked')
    external={l['mapped'] for l in prepared['links'] if not l['mapped'].startswith('#')}
    def canonical_uri(uri):
        # Match an IRI to Chrome's UTF-8 escaped URI without decoding reserved
        # ASCII path delimiters, query operators, or an encoded slash.
        parsed=urlsplit(uri)
        # Chrome canonicalizes an HTTP origin's empty path to '/'. This is
        # the same resource; preserve all nonempty paths and query operators.
        if parsed.scheme in {'http','https'} and parsed.netloc and not parsed.path:
            uri=urlunsplit(parsed._replace(path='/'))
        return re.sub(r'%[0-9a-fA-F]{2}',lambda m:m.group().upper(),quote(uri,safe=":/?#[]@!$&'()*+,;=%"))
    for uri in external:
        if canonical_uri(uri) not in {canonical_uri(u) for u in uris}: errors.append('pdf-link-missing:'+uri)
    required_internal=len([l for l in prepared['links'] if l['mapped'].startswith('#')])
    if internal_links<required_internal: errors.append('internal-links-missing')
    locations=[]
    for unit in prepared['units']:
        prefix=normalize_text(unit['text'])[:48]
        pages=[i+1 for i,text in enumerate(texts) if prefix in normalize_text(text)]
        locations.append({'source':unit['source'],'start_page_candidates':pages})
    return {'status':'PASS' if not errors else 'FAILED','errors':errors,'page_count':len(reader.pages),
            'text_verification':{'method':'exact-source-runs-plus-glyph-multiplicity; print-DOM order checked before rendering',
                                 'source_runs':len(runs),'missing_runs':missing_runs,'missing_glyphs':missing_glyphs},
            'pdf_sha256':sha(path),'text_characters':len(actual),'uris':uris,
            'internal_link_count':internal_links,'source_locations':locations,
            'external_live_check':'NOT_PERFORMED'}


def build(root: Path, recipe: dict, create_pdf=False):
    if not create_pdf: raise PipelineError('PDF creation requires explicit --create-pdf and user authorization')
    from playwright.sync_api import sync_playwright
    if not shutil.which('pdftoppm'): raise PipelineError('pdftoppm is required for full-page review evidence')
    with operation_lock(root) as directory:
        prepared=prepare(root,recipe)
        operation=directory/(recipe['artifact_id']+'-'+uuid.uuid4().hex[:12]); operation.mkdir()
        manifest={'schema_version':1,'artifact_id':recipe['artifact_id'],'created_at':now(),
                  'status':'RENDERING','recipe':recipe,'fingerprint':prepared['fingerprint'],
                  'dependencies':prepared['dependencies'],'environment':prepared['environment'],
                  'transformations':prepared['transformations'],'links':prepared['links'],'units':prepared['units']}
        current_output=inside(root,recipe['output'])
        manifest['previous_output_sha256']=sha(current_output) if current_output.exists() else None
        manifest_path=operation/'manifest.json'; write_json(manifest_path,manifest)
        snapshot=operation/'print-source.html'; snapshot.write_text(prepared['html'],encoding='utf-8')
        manifest['snapshot_sha256']=sha(snapshot)
        candidate=operation/'candidate.pdf'
        try:
            for i,source in enumerate(recipe['sources']):
                shutil.copy2(inside(root,source['path']),operation/f'original-{i}.html')
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=p.chromium.executable_path)
                try:
                    context=browser.new_context(java_script_enabled=False)
                    blocked=[]
                    def route_request(route):
                        if route.request.url.startswith(('http:','https:')):
                            blocked.append(route.request.url); route.abort()
                        else: route.continue_()
                    context.route('**/*',route_request)
                    page=context.new_page(); page.goto(snapshot.as_uri(),wait_until='load')
                    supported=page.evaluate("() => {const s=new CSSStyleSheet();s.replaceSync('@scope (.x){p{color:red}}');return s.cssRules[0]?.constructor.name==='CSSScopeRule'}")
                    if not supported: raise PipelineError('Chromium CSS scope support is required for multi-page styles')
                    page.emulate_media(media='print')
                    page.evaluate('() => document.fonts.ready')
                    if recipe.get('font_files') and not page.evaluate("() => document.fonts.check('12px CoursePDF0')"):
                        raise PipelineError('Declared PDF font failed to load')
                    if blocked: raise PipelineError('Unpinned network render requests: '+', '.join(blocked))
                    if page.evaluate('() => [...document.images].some(i => !i.complete || i.naturalWidth === 0)'):
                        raise PipelineError('Image failed to load')
                    visible=page.locator('body').inner_text()
                    if normalize_text(prepared['expected_text'])!=normalize_text(visible):
                        raise PipelineError('Print DOM differs from selected teaching content; resolve hidden/UI content explicitly')
                    if re.search(r'Page\s+\d+\s*/\s*\d+',prepared['expected_text']): raise PipelineError('Footer label collides with source text')
                    page.pdf(path=str(candidate),format='A4',print_background=True,prefer_css_page_size=True,
                             display_header_footer=True,header_template='<span></span>',
                             footer_template='<div style="font-size:8px;width:100%;text-align:center">Page <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                finally: browser.close()
            machine=inspect_pdf(candidate,prepared); write_json(operation/'machine-verification.json',machine)
            if machine['status']!='PASS': raise PipelineError('PDF machine fidelity check failed: '+', '.join(machine['errors']))
            prefix=operation/'page'
            subprocess.run(['pdftoppm','-png','-r','110',str(candidate),str(prefix)],check=True,capture_output=True)
            images=sorted(operation.glob('page-*.png'),key=lambda p:int(p.stem.rsplit('-',1)[1]))
            if len(images)!=machine['page_count']: raise PipelineError('Full-page render evidence incomplete')
            review={'pdf_sha256':machine['pdf_sha256'],'reviewer':{'kind':None,'name':None},'accepted':False,
                    'pages':[{'page':i+1,'image':p.name,'sha256':sha(p),'reviewed':False,'issues':[]} for i,p in enumerate(images)],
                    'checks':{'missing_glyphs':False,'clipping':False,'overlap':False,'tables_and_code':False,'images':False,'links':False}}
            write_json(operation/'review-template.json',review)
            if prepare(root,recipe)['fingerprint']!=prepared['fingerprint']: raise PipelineError('Source changed during build')
            manifest.update(status='PENDING_REVIEW',pdf_sha256=sha(candidate),page_count=machine['page_count'],machine='machine-verification.json',images=[p.name for p in images])
            write_json(manifest_path,manifest)
            catalog=read_catalog(root); record=next((a for a in catalog['artifacts'] if a['artifact_id']==recipe['artifact_id']),None)
            if record is not None:
                record.update(candidate_build=manifest_path.relative_to(root).as_posix(),last_build_result='PENDING_REVIEW')
                write_json(catalog_path(root),catalog)
            return {'status':'PENDING_REVIEW','manifest':str(manifest_path),'review_template':str(operation/'review-template.json')}
        except BaseException as e:
            failure=classify_build_error(e)
            error_log=None
            if failure['raw_log'] is not None:
                error_log=operation/'browser-launch-error.log'
                error_log.write_text(failure['raw_log']+'\n',encoding='utf-8')
            manifest.update(status='FAILED',error_code=failure['code'],error=failure['message'])
            if error_log is not None: manifest['error_log']=error_log.relative_to(root).as_posix()
            write_json(manifest_path,manifest)
            catalog=read_catalog(root); record=next((a for a in catalog['artifacts'] if a['artifact_id']==recipe['artifact_id']),None)
            if record is not None:
                record.update(last_build_result='FAILED',last_build_error_code=failure['code'],last_build_error=failure['message'])
                if error_log is not None: record['last_build_error_log']=error_log.relative_to(root).as_posix()
                write_json(catalog_path(root),catalog)
            if isinstance(e,Exception): raise PipelineError(failure['message']) from e
            raise


def validate_review(review: dict, pdf_hash: str, page_count: int, images: list, operation: Path):
    if review.get('accepted') is not True or review.get('pdf_sha256')!=pdf_hash: raise PipelineError('Review does not approve this exact candidate')
    reviewer=review.get('reviewer',{})
    if reviewer.get('kind') not in {'human','ai','author'} or not reviewer.get('name'): raise PipelineError('Actual reviewer identity and kind are required')
    required_checks={'missing_glyphs','clipping','overlap','tables_and_code','images','links'}
    if set(review.get('checks',{}))!=required_checks or not all(v is True for v in review['checks'].values()): raise PipelineError('Review quality checks incomplete')
    pages=review.get('pages',[])
    if any(not isinstance(p.get('page'),int) for p in pages) or sorted(p['page'] for p in pages)!=list(range(1,page_count+1)):
        raise PipelineError('Every rendered page must be reviewed exactly once')
    for entry in pages:
        if entry.get('image')!=images[entry['page']-1]: raise PipelineError('Review image/page mismatch')
        image=inside(operation,entry['image'])
        if entry.get('reviewed') is not True or entry.get('issues')!=[] or sha(image)!=entry.get('sha256'): raise PipelineError('Unreviewed/modified page or unresolved issue')
    return review


def verify(root: Path, manifest_path: Path, review_path: Path | None=None):
    root=root.resolve()
    manifest_path=manifest_path.resolve()
    if not manifest_path.is_relative_to(root/'course-manager/operations/pdf-build'): raise PipelineError('Manifest must belong to the PDF operations directory')
    manifest=json.loads(manifest_path.read_text()); operation=manifest_path.parent
    if manifest['status'] not in {'PENDING_REVIEW','VERIFIED','PROMOTED'}: raise PipelineError('Build is not a reviewable candidate')
    prepared=prepare(root,manifest['recipe'])
    if prepared['fingerprint']!=manifest['fingerprint']: raise PipelineError('Build evidence is stale')
    if sha(operation/'print-source.html')!=manifest['snapshot_sha256']: raise PipelineError('Source snapshot modified')
    candidate=operation/'candidate.pdf'
    if sha(candidate)!=manifest['pdf_sha256']: raise PipelineError('Candidate PDF modified')
    machine=inspect_pdf(candidate,prepared)
    if machine['status']!='PASS': raise PipelineError('Machine checks failed')
    if review_path is None: return {'status':'PENDING_REVIEW','machine':machine,'manifest':str(manifest_path)}
    review=json.loads(review_path.read_text())
    validate_review(review,sha(candidate),machine['page_count'],manifest['images'],operation)
    return {'status':'VERIFIED','machine':machine,'review':review,'manifest':str(manifest_path)}


def promote(root: Path, manifest_path: Path, review_path: Path):
    root=root.resolve(); manifest_path=manifest_path.resolve()
    with operation_lock(root):
        result=verify(root,manifest_path,review_path)
        manifest=json.loads(manifest_path.read_text()); operation=manifest_path.parent
        if manifest['status']=='PROMOTED': raise PipelineError('Candidate already promoted')
        recipe=manifest['recipe']; catalog=read_catalog(root)
        current_output=inside(root,recipe['output'])
        if (sha(current_output) if current_output.exists() else None)!=manifest.get('previous_output_sha256'):
            raise PipelineError('Published PDF changed after candidate build; preserve later work')
        entry=next((a for a in catalog['artifacts'] if a['artifact_id']==recipe['artifact_id']),None)
        if not entry or not entry.get('recipe'): raise PipelineError('Bind the inspected recipe before promotion')
        current_recipe=load_recipe(root,inside(root,entry['recipe']))
        if prepare(root,current_recipe)['fingerprint']!=manifest['fingerprint']: raise PipelineError('Registered recipe changed')
        entry.update(last_verified_build={'verified':True,'fingerprint':manifest['fingerprint'],'pdf_sha256':manifest['pdf_sha256'],
                                         'manifest':manifest_path.relative_to(root).as_posix(),'verified_at':now()},
                     source_state='CURRENT',last_build_result='VERIFIED',candidate_build=None,
                     page_count=manifest['page_count'],bytes=(operation/'candidate.pdf').stat().st_size)
        catalog['updated_at']=now(); write_json(operation/'catalog-candidate.json',catalog)
        write_json(operation/'accepted-review.json',result['review'])
        (operation/'index-candidate.md').write_text(render_index(root,catalog),encoding='utf-8')
        manifest.update(status='PROMOTING',accepted_review_sha256=sha(operation/'accepted-review.json')); write_json(manifest_path,manifest)
        changes=apply_changes(root,[(inside(root,recipe['output']),operation/'candidate.pdf'),
                                   (catalog_path(root),operation/'catalog-candidate.json'),
                                   (root/'output/pdf/INDEX.md',operation/'index-candidate.md')],operation)
        manifest.update(status='PROMOTED',changes=changes,promoted_at=now()); write_json(manifest_path,manifest)
        return {'status':'PROMOTED','output':str(inside(root,recipe['output'])),'manifest':str(manifest_path)}


def rollback(root: Path, manifest_path: Path, apply=False):
    root=root.resolve(); manifest_path=manifest_path.resolve()
    if not manifest_path.is_relative_to(root/'course-manager/operations/pdf-build'): raise PipelineError('Manifest must belong to PDF operations')
    with operation_lock(root):
        manifest=json.loads(manifest_path.read_text())
        if manifest.get('status') not in {'PROMOTED','PROMOTING'}: raise PipelineError('Only promoted/interrupted promotions can be rolled back')
        if manifest['status']=='PROMOTING':
            journal=json.loads((manifest_path.parent/'transaction.json').read_text())
            records=[]
            for record in journal['changes']:
                dest=inside(root,record['destination']); current=sha(dest) if dest.exists() else None
                if current==record['after']: records.append(record)
                elif current!=record['before']: raise PipelineError('Interrupted transaction has later edits')
        else: records=manifest['changes']
        result=rollback_changes(root,records,apply=apply)
        if apply:
            manifest.update(status='ROLLED_BACK',rolled_back_at=now()); write_json(manifest_path,manifest)
        return result
