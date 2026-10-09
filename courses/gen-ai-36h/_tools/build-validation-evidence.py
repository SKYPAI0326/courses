#!/usr/bin/env python3
"""Bind this repair's already reviewed sources, pages and assets to evidence logs.

This script only fingerprints files. It does not perform or claim a review.
Update the logs after actually rechecking changed materials before rerunning.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
import hashlib
import json
import re

course = Path(__file__).resolve().parents[1]
site = course.parents[1]
metadata = json.loads((course / '_repair/2026-10-09/lesson-meta.json').read_text())
evidence_dir = course / '_validation/2026-10-09'


def rel(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(site) or not resolved.is_file():
        raise ValueError(f'Unavailable evidence file: {path}')
    return resolved.relative_to(site).as_posix()


def snapshot(path):
    file = site / path
    return {'path': path, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}


units = []
for unit_id, item in metadata.items():
    source = site / '_lessons/gen-ai-36h' / f'{unit_id}.md'
    page = course / item['path']
    body = source.read_text()
    kind = re.search(r'^course_type:\s*(\S+)', body, re.MULTILINE)
    if not kind:
        raise ValueError(f'Missing course_type: {unit_id}')
    assets = set()
    for link in re.findall(r'\]\((\.\./assets/[^)]+)\)', body):
        assets.add(rel(page.parent / link))
    dom = BeautifulSoup(page.read_text(), 'html.parser')
    for element in dom.select('[href], [src]'):
        for key in ('href', 'src'):
            url = element.get(key)
            if not url:
                continue
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if target.is_relative_to(course / 'assets') and target.is_file():
                assets.add(rel(target))
    units.append({
        'id': unit_id,
        'course_type': kind.group(1),
        'source': rel(source),
        'page': rel(page),
        'assets': sorted(assets),
        'platform_required': True,
    })


def record(layer, actor, log_name, selected, notes, extra=()):
    log = rel(evidence_dir / log_name)
    paths = set(extra)
    for unit in selected:
        paths.add(unit['source'])
        if layer != 'content':
            paths.add(unit['page'])
        paths.update(unit['assets'])
    return {
        'layer': layer,
        'unit_ids': [unit['id'] for unit in selected],
        'actor': actor,
        'verdict': 'PASS',
        'notes': notes,
        'log': snapshot(log),
        'artifacts': [snapshot(path) for path in sorted(paths)],
    }


make_units = [unit for unit in units if unit['id'] in {'CH5-1', 'CH5-2', 'CH5-3', 'CH5-4', 'PRAC5'}]
screenshots = [
    rel(course / '_repair/2026-10-09' / name)
    for name in ('make-flow-verified.png', 'make-t07-error.png', 'make-blueprint-import.png')
]
records = [
    record('content', 'author-self-check', 'content-self-review.md', units,
           '28 單元逐頁正文及核心素材作者自審；平台與真人理解未由本筆通過。'),
    record('fidelity', 'author-self-check', 'fidelity-self-review.md', units,
           '逐項來源至 HTML 比對與作者抽查；瀏覽器呈現另待驗。'),
    record('technical', 'tool-run', 'technical-checks.md', units,
           '28 頁來源保真、33 頁 lint／結構、功能及 DOM 模擬通過；真實瀏覽器待驗。'),
    record('platform', 'tool-run', 'make-platform-run.md', make_units,
           '教學工作區 T01–T07 實際執行；學員重新連線尚待驗。', screenshots),
]
result = {
    'schema_version': 1,
    'outline': snapshot(rel(site / '_outlines/gen-ai-36h.md')),
    'scope_note': '涵蓋大綱 Part 1–7 全部 28 個主線 CH／PRAC；五份原有 AI 秘書藍圖為進階延伸，不列入主線驗收。',
    'units': units,
    'records': records,
}
target = course / '_validation/evidence.json'
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(f'Bound {len(units)} units and {len(records)} reviewed records: {target}')
