#!/usr/bin/env python3
"""Exercise extracted ZIP and local Git history in an isolated temporary folder."""
from pathlib import Path
import tempfile,zipfile,subprocess,json
from PIL import Image
from psd_tools import PSDImage
root=Path(__file__).resolve().parents[1];results=[]
with tempfile.TemporaryDirectory(prefix='uiux-cold-project-') as tmp:
    with zipfile.ZipFile(root/'assets/shared/studio-tasks-web.zip') as z:z.extractall(tmp)
    project=Path(tmp)/'studio-tasks-web'
    def run(*args):
        r=subprocess.run(args,cwd=project,text=True,capture_output=True)
        assert r.returncode==0,r.stderr
        results.append({'command':list(args),'stdout':r.stdout.strip()})
        return r.stdout
    run('git','init','-b','main')
    run('git','config','user.name','Course Test')
    run('git','config','user.email','course-test@example.test')
    run('git','add','index.html','styles.css','app.js','README.md','assets/status-badge.png')
    run('git','diff','--cached','--stat')
    run('git','commit','-m','Create task demo')
    p=project/'index.html';p.write_text(p.read_text().replace('工作室任務</h1>','活動報名確認</h1>'))
    run('git','diff','--','index.html')
    run('git','add','index.html')
    run('git','commit','-m','Update activity title')
    assert not run('git','status','--porcelain')
    run('git','log','--oneline','-2')
psd=PSDImage.open(root/'assets/shared/status-badge.psd')
assert psd.size==(512,512) and len(psd)==3
png=Image.open(root/'assets/shared/status-badge.png').convert('RGBA')
assert png.size==(512,512) and png.getpixel((0,0))[3]==0
report={'actor':'tool-run','date':'2026-10-09','git_scope':'Temporary extracted ZIP only; no remote, real repo index or global identity changed','git_checks':results,'psd':{'size':psd.size,'layers':[{'name':x.name,'visible':x.visible} for x in psd]},'png':{'size':png.size,'corner_alpha':png.getpixel((0,0))[3]},'signup_rows':len((root/'assets/shared/SIGNUP-DATA.csv').read_text(encoding='utf-8-sig').splitlines())-1,'status':'PASS','pending':'Photoshop desktop reopening/export and GitHub Pages public deployment not run'}
(root/'_validation/repair-2026-10-09/runtime-assets-git.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='git_checks'},ensure_ascii=False))
