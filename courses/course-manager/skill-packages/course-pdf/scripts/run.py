#!/usr/bin/env python3
"""Run an explicitly configured course PDF engine."""
import os
import subprocess
import sys
from pathlib import Path

def locate():
    args=sys.argv[1:]
    if '--root' in args:
        index=args.index('--root')
        if index+1>=len(args): raise SystemExit('--root requires a courses path')
        root=Path(args[index+1]).resolve()
        remaining=[*args[:index],*args[index+2:]]
    else:
        configured=os.environ.get('COURSE_WEB_ROOT')
        if not configured: raise SystemExit('COURSE_WEB_ROOT or --root is required')
        root=(Path(configured)/'courses').resolve()
        remaining=args
    explicit_engine=os.environ.get('COURSE_PDF_ENGINE')
    system_root=os.environ.get('COURSE_DESIGN_SYSTEM_ROOT')
    if explicit_engine:
        engine=Path(explicit_engine).resolve()
    elif system_root:
        engine=Path(system_root).resolve()/'scripts/pdf_pipeline.py'
    else:
        raise SystemExit('COURSE_PDF_ENGINE or COURSE_DESIGN_SYSTEM_ROOT is required')
    if not engine.is_file(): raise SystemExit(f'PDF engine is unavailable: {engine}')
    return root,engine,['--root',str(root),*remaining]


if __name__=='__main__':
    root,engine,args=locate()
    python=os.environ.get('COURSE_PDF_PYTHON',sys.executable)
    raise SystemExit(subprocess.call([python,str(engine),*args]))
