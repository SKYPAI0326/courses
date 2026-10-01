#!/usr/bin/env python3
"""Deterministic page/asset checks only. Teaching quality requires cited review."""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
EXCLUDED={'_archive','_backup','_repair','_validation','_review','assets','web-starter'}
ASSET_EXTENSIONS={'.csv','.doc','.docx','.json','.md','.pdf','.png','.jpg','.jpeg','.gif','.py','.svg','.txt','.tsv','.webp','.xlsx','.zip','.mp3','.mp4'}
def digest(value):
    return hashlib.sha256(value if isinstance(value,bytes) else value.encode()).hexdigest()
def within(path,root):
    try: path.relative_to(root); return True
    except ValueError: return False

class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.links=[]; self.stack=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        hidden=(any(x[1] for x in self.stack) or tag in {'head','script','style','template'} or 'hidden' in attrs or
                bool(re.search(r'(display\s*:\s*none|visibility\s*:\s*hidden)',attrs.get('style',''),re.I)))
        if not hidden:
            for k in ('href','src'):
                if attrs.get(k): self.links.append({'href':attrs[k],'tag':tag,'download':'download' in attrs})
            if tag=='img' and attrs.get('alt'): self.parts.append(attrs['alt'])
        if tag not in VOID: self.stack.append((tag,hidden))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag: del self.stack[i:]; break
    def handle_data(self,data):
        if not any(x[1] for x in self.stack): self.parts.append(data)
    @property
    def text(self): return re.sub(r'\s+',' ',' '.join(self.parts)).strip()

def is_local_asset_link(link):
    u=urlsplit(link);p=Path(unquote(u.path))
    return bool(u.path and not u.scheme and not u.netloc and ('assets' in p.parts or p.suffix.lower() in ASSET_EXTENSIONS))

def audit_page(course_dir,path,site_root=None):
    course_dir=Path(course_dir).resolve();path=Path(path).resolve();site_root=Path(site_root or course_dir).resolve()
    if not within(path,course_dir): raise ValueError('page outside course directory')
    raw=path.read_bytes();source=raw.decode('utf-8');parser=VisibleTextParser();parser.feed(source)
    assets=[];missing=[];broken=[];external=[];links=[]
    for link in parser.links:
        href=link['href'];u=urlsplit(href)
        if u.scheme or u.netloc:
            if u.scheme in ('http','https') or u.netloc: external.append(href)
            continue
        if not u.path: continue
        decoded=unquote(u.path)
        target=((site_root/decoded.lstrip('/')) if decoded.startswith('/') else (path.parent/decoded)).resolve()
        item={'href':href,'path':str(target.relative_to(site_root)) if within(target,site_root) else None}
        if not within(target,site_root): item['error']='outside_site_root'
        elif not target.is_file(): item['error']='missing_file'
        else: item['sha256']=digest(target.read_bytes())
        links.append(item)
        asset=is_local_asset_link(href) or link['download']
        if asset: assets.append(item)
        if 'error' in item:
            broken.append(href)
            if asset: missing.append(href)
    checks={'title':bool(re.search(r'<title>\s*[^<\s]',source,re.I)),
            'h1':bool(re.search(r'<h1\b',source,re.I)),
            'visible_body':bool(parser.text),
            'local_links':not broken}
    # No keyword, step-count or grammar inference may become a teaching verdict.
    failures=[key for key,value in checks.items() if not value]
    return {'path':str(path.relative_to(course_dir)),'html_sha256':digest(raw),
            'visible_text_sha256':digest(parser.text),'visible_text_chars':len(parser.text),
            'visible_text_method':'HTML extraction; CSS classes, layout and interactions require browser review',
            'asset_links':len(assets),'assets':assets,'missing_assets':missing,'broken_links':broken,
            'local_links':links,'external_links_pending':external,'checks':checks,'hard_failures':failures,
            'warnings':[],'semantic_review':'PENDING','status':'BLOCK' if failures else 'MACHINE_CHECKED'}

def discover_pages(course_dir):
    return sorted(p for p in course_dir.rglob('*.html')
        if not any(x in EXCLUDED or x.startswith('.') for x in p.relative_to(course_dir).parts[:-1])
        and p.name not in {'index.html','handbook.html'} and not re.fullmatch(r'module\d+\.html',p.name))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('slug');ap.add_argument('--page',type=Path)
    ap.add_argument('--build-evidence-manifest',action='store_true');args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',args.slug): ap.error('invalid slug')
    course=(root/'courses'/args.slug).resolve()
    if not within(course,root/'courses') or not course.is_dir(): ap.error('course directory not found or outside courses')
    if args.page:
        candidates=[args.page] if args.page.is_absolute() else [course/args.page,root/args.page,Path.cwd()/args.page]
        candidates=list(dict.fromkeys(p.resolve() for p in candidates if p.is_file() and within(p.resolve(),course)))
        if len(candidates)!=1: ap.error('--page must resolve unambiguously to an existing page inside course')
        pages=candidates
    else: pages=discover_pages(course)
    if not pages:
        print(json.dumps({'course':args.slug,'pages':0,'status':'BLOCK'}));return 1
    try: records=[audit_page(course,p,root) for p in pages]
    except (OSError,UnicodeError,ValueError) as e: ap.error(str(e))
    summary={'pages':len(records),'block':sum(r['status']=='BLOCK' for r in records),
             'machine_checked':sum(r['status']=='MACHINE_CHECKED' for r in records),'semantic_review':'PENDING',
             'missing_assets':sum(len(r['missing_assets']) for r in records)}
    report={'generated_at':datetime.now(timezone.utc).isoformat(),'course':args.slug,'summary':summary,'pages':records}
    if args.build_evidence_manifest:
        target=course/'_validation/L5-evidence-manifest.json';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
    for r in records:
        if r['hard_failures']: print(f"BLOCK: {r['path']} {r['hard_failures']} {r['broken_links']}")
    return int(bool(summary['block']))
if __name__=='__main__': raise SystemExit(main())
