#!/usr/bin/env python3
"""Locate the shared course PDF engine; do not keep a second implementation."""
import os
import subprocess
import sys
from pathlib import Path

DEFAULT=Path('/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses')


def locate():
    args=sys.argv[1:]
    if '--root' in args:
        index=args.index('--root')
        if index+1>=len(args): raise SystemExit('--root requires a courses path')
        root=Path(args[index+1]).resolve()
        return root,['--root',str(root),*args[:index],*args[index+2:]]
    for candidate in (Path.cwd(),*Path.cwd().parents):
        for root in (candidate,candidate/'courses'):
            if (root/'course-manager/scripts/pdf_pipeline.py').is_file(): return root.resolve(),['--root',str(root.resolve()),*args]
    return DEFAULT,['--root',str(DEFAULT),*args]


if __name__=='__main__':
    root,args=locate(); engine=root/'course-manager/scripts/pdf_pipeline.py'
    if not engine.is_file(): raise SystemExit('找不到 PDF 引擎；請使用 --root 指定 courses 資料夾。')
    python=os.environ.get('COURSE_PDF_PYTHON',sys.executable)
    raise SystemExit(subprocess.call([python,str(engine),*args]))
