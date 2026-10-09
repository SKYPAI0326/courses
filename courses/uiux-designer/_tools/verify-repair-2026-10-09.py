#!/usr/bin/env python3
"""Verify repaired source/page fidelity, local links and the downloadable project.
Runs read-only checks; semantic review and platform tests remain separate.
"""
from repair_render_reference import ROOT, BASE, UNITS, render
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote
from pathlib import Path
import json, re, zipfile, hashlib

def normalized(value):
    return re.sub(r'\s+', ' ', value).strip()

def atoms(soup):
    result = []
    for tag in soup.select('h2,h3,h4,p,li,th,td,pre,summary,img'):
        if tag.find_parent('pre') or (tag.name == 'p' and tag.find_parent('li')):
            continue
        text = tag.get('alt', '') if tag.name == 'img' else tag.get_text(' ', strip=True)
        if tag.name == 'pre': text = tag.get_text()
        result.append((tag.name, text if tag.name == 'pre' else normalized(text)))
    return result

pages = []
for unit, page, hours in UNITS:
    source = (BASE / '_lessons/uiux-designer' / (unit + '.md')).read_text()
    formal = source.split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0].strip()
    expected = BeautifulSoup(render(formal), 'html.parser')
    title = expected.find('h1').get_text()
    expected.find('h1').decompose()
    intro = expected.find('p').get_text()
    expected.find('p').decompose()
    actual = BeautifulSoup((ROOT / page).read_text(), 'html.parser')
    body = actual.select_one('.lesson-body')
    assert len(actual.select('.lesson-body')) == 1, unit
    assert normalized(actual.find('h1').get_text()) == normalized(title), unit + ': title'
    assert atoms(expected) == atoms(body), unit + ': source/page content mismatch'
    tag = actual.select_one('.lesson-tagline,.tagline')
    assert tag and normalized(tag.get_text()) == normalized(intro), unit + ': intro'
    pages.append({'unit':unit,'page':page,'compared_atoms':len(atoms(expected)), 'code_blocks':len(body.select('pre')),'verdict':'PASS'})

links = 0
public = []
for path in ROOT.rglob('*.html'):
    if any(part.startswith(('_','.')) for part in path.relative_to(ROOT).parts): continue
    public.append(path)
    for tag in BeautifulSoup(path.read_text(), 'html.parser').select('[href],[src]'):
        href = tag.get('href', tag.get('src', ''))
        url = urlsplit(href)
        if url.scheme or url.netloc: continue
        target = ((BASE / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_file(), str(path.relative_to(ROOT)) + ': ' + href
        if url.fragment and target.suffix == '.html':
            target_soup = BeautifulSoup(target.read_text(), 'html.parser')
            assert target_soup.find(id=unquote(url.fragment)), str(path.relative_to(ROOT)) + ': anchor ' + href
        links += 1

source = (BASE / '_lessons/uiux-designer/B8-web-git-deploy.md').read_text()
codes = re.findall(r'^```(?:html|css|javascript)\n(.*?)^```',source,re.M|re.S)
assert len(codes) == 3
for code,name in zip(codes,['index.html','styles.css','app.js']):
    assert code.strip() == (ROOT/'web-starter'/name).read_text().strip(), name + ': embedded code differs'
names = ['index.html','styles.css','app.js','README.md','assets/status-badge.png']
with zipfile.ZipFile(ROOT/'assets/shared/studio-tasks-web.zip') as archive:
    assert archive.testzip() is None
    assert sorted(archive.namelist()) == sorted('studio-tasks-web/'+name for name in names)
    for name in names: assert archive.read('studio-tasks-web/'+name) == (ROOT/'web-starter'/name).read_bytes(), name

print(json.dumps({'scope':'2026-10-09 actual current files','fidelity':pages,'local_html_pages':len(public),'local_links_and_anchors':links,'broken_links':0,'embedded_web_files_equal':3,'zip_crc_and_byte_equal_files':5,'status':'PASS','limitation':'Item fidelity and deterministic checks do not prove a novice can operate Figma, Photoshop or GitHub.'},ensure_ascii=False,indent=2))
