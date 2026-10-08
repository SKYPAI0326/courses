#!/usr/bin/env python3
"""Safely restore only this repair's unchanged outputs; defaults to dry run."""
from pathlib import Path
import argparse,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BACKUP=ROOT/'_backup/2026-10-08-playground-pre'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');args=p.parse_args();data=json.loads((BACKUP/'restore-manifest.json').read_text());conflicts=[]
for r in data['files']:
    path=ROOT/r['path'];before=BACKUP/'before'/r['path']
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=r['after_sha256']:conflicts.append(r['path'])
    if r['before_sha256'] and (not before.exists() or hashlib.sha256(before.read_bytes()).hexdigest()!=r['before_sha256']):conflicts.append('backup:'+r['path'])
if conflicts:raise SystemExit('偵測後續變更或備份差異，不回復：'+str(conflicts))
print('可回復',sum(bool(r['before_sha256']) for r in data['files']),'個舊檔、移除',sum(not r['before_sha256'] for r in data['files']),'個本輪新增檔')
if args.apply:
    for r in data['files']:
        dst=ROOT/r['path']
        if r['before_sha256']:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BACKUP/'before'/r['path'],dst)
        else:dst.unlink()
    print('本輪範圍已回復，歷史與審核證據保留。')
else:print('只驗證，未修改；確定回復時使用 --apply。')
