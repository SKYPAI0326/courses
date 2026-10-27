#!/usr/bin/env python3
"""Standalone course PDF CLI; default sync/plan/status do not create PDFs."""
from __future__ import annotations
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.pdf_sources import PipelineError, load_recipe, prepare, inside, environment
from src.pdf_registry import inventory, register_existing, status, bind_recipe, read_catalog, write_json
from src.pdf_build import build, verify, promote, rollback


def require_browser_launch_permission():
    if sys.platform=='darwin' and os.environ.get('CODEX_SANDBOX'):
        raise PipelineError(
            'BROWSER_PERMISSION_REQUIRED: PDF 產製需要在 macOS 的 Codex sandbox 外啟動 '
            'Playwright Chromium。尚未啟動瀏覽器，正式 PDF 未變更；'
            '請以同一建置命令申請單次必要權限。'
        )


def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2],help='courses directory')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    for name in ('inventory','register-existing','status','sync'):
        c=sub.add_parser(name)
        if name in {'status','sync'}: c.add_argument('--artifact'); c.add_argument('--course')
        if name=='sync': c.add_argument('--create-pdf',action='store_true')
        if name in {'inventory','status'}: c.add_argument('--write',type=Path,help='Write a JSON report explicitly')
    for name in ('plan','bind','build'):
        c=sub.add_parser(name); c.add_argument('--recipe',type=Path,required=True)
        if name=='build': c.add_argument('--create-pdf',action='store_true')
        if name=='plan': c.add_argument('--write',type=Path)
    for name in ('verify','promote','rollback'):
        c=sub.add_parser(name); c.add_argument('--manifest',type=Path,required=True)
        if name in {'verify','promote'}: c.add_argument('--review',type=Path,required=name=='promote')
        if name=='rollback': c.add_argument('--apply',action='store_true')
    return p


def main(argv=None):
    args=parser().parse_args(argv); root=args.root.resolve()
    try:
        if not (root/'course-manager').is_dir(): raise PipelineError('--root must contain course-manager')
        if args.command=='doctor':
            env=environment(); result={'environment':env,'pdftoppm':shutil.which('pdftoppm'),
                                     'creation_enabled_by_default':False,'continuous_watch_configured':False,
                                     'browser_launch':{
                                         'engine':'playwright-managed-chromium',
                                         'uses_system_chrome':False,
                                         'codex_execution_policy':('request-scoped-permission-before-create'
                                                                   if sys.platform=='darwin' else 'standard'),
                                         'same_restricted_route_retries':0,
                                         'published_pdf_on_launch_failure':'unchanged'}}
        elif args.command=='inventory': result=inventory(root)
        elif args.command=='register-existing': result=register_existing(root)
        elif args.command in {'plan','bind','build'}:
            recipe=load_recipe(root,args.recipe)
            if args.command=='bind': result=bind_recipe(root,args.recipe)
            elif args.command=='build':
                if args.create_pdf: require_browser_launch_permission()
                result=build(root,recipe,create_pdf=args.create_pdf)
            else:
                prepared=prepare(root,recipe)
                result={k:prepared[k] for k in ('fingerprint','dependencies','transformations','links','environment')}
                result.update(artifact_id=recipe['artifact_id'],output=recipe['output'],source_count=len(recipe['sources']),
                              text_characters=len(prepared['expected_text']),creation_performed=False)
        elif args.command in {'status','sync'}:
            result=status(root,args.artifact)
            if args.course: result['artifacts']=[r for r in result['artifacts'] if r['course']==args.course]
            result['counts']={s:sum(r['source_state']==s for r in result['artifacts']) for s in sorted({r['source_state'] for r in result['artifacts']})}
            if args.command=='sync':
                eligible=[r for r in result['artifacts'] if r['recipe'] and r['source_state'] in {'STALE','UNVERIFIED'}]
                result.update(mode='CREATE_CANDIDATES' if args.create_pdf else 'PLAN_ONLY',
                              affected=[r['artifact_id'] for r in eligible],builds=[])
                if args.create_pdf and eligible:
                    require_browser_launch_permission()
                    for entry in eligible:
                        recipe=load_recipe(root,inside(root,entry['recipe']))
                        result['builds'].append(build(root,recipe,create_pdf=True))
        elif args.command=='verify': result=verify(root,args.manifest,args.review)
        elif args.command=='promote': result=promote(root,args.manifest,args.review)
        else: result=rollback(root,args.manifest,apply=args.apply)
        if getattr(args,'write',None):
            dest=args.write.resolve()
            if not dest.is_relative_to(root/'course-manager/reports'): raise PipelineError('Reports may only be written under course-manager/reports')
            write_json(dest,result)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (PipelineError,OSError,ValueError,ImportError) as e:
        print(json.dumps({'status':'BLOCKED','error':str(e)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=='__main__': raise SystemExit(main())
