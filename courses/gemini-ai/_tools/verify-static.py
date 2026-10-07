from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote
import argparse
import collections
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent.parent

parser = argparse.ArgumentParser(description='Validate course links, route, source fidelity, and bundled materials.')
parser.add_argument('--out-dir', type=Path, default=Path('_repair/2026-10-07'), help='evidence directory, relative to the course root unless absolute')
parser.add_argument('--skip-shared-ops', action='store_true', help='defer shared search-index and sitemap checks')
args = parser.parse_args()
OUT = (args.out_dir if args.out_dir.is_absolute() else ROOT / args.out_dir).resolve()
if not OUT.is_relative_to(ROOT):
    parser.error('--out-dir must be inside the course root')
OUT.mkdir(parents=True, exist_ok=True)

meta = json.loads((ROOT / '_source/lesson-map.json').read_text(encoding='utf-8'))
route = list(meta)
files = [ROOT / 'index.html', *sorted(ROOT.glob('part*/*.html')), *sorted((ROOT / 'assets/tools').glob('*.html'))]
broken = []
badanchors = []
duplicates = []
copies = collections.defaultdict(list)
fidelity = []
# This exact sentence is shared orientation copy above self-contained practice
# tools, not duplicated lesson instruction. Keep it visible in the audit.
KNOWN_SHARED_GUIDANCE = '先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。'

for page in files:
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    ids = [node['id'] for node in soup.select('[id]')]
    if len(ids) != len(set(ids)):
        duplicates.append(str(page.relative_to(ROOT)))
    for anchor in soup.select('a[href]'):
        url = urlsplit(anchor['href'])
        if url.scheme or url.netloc:
            continue
        target = (page.parent / unquote(url.path)).resolve() if url.path else page
        if not target.is_file():
            broken.append([str(page.relative_to(ROOT)), anchor['href']])
            continue
        if url.fragment and target.suffix == '.html' and not BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser').find(id=unquote(url.fragment)):
            badanchors.append([str(page.relative_to(ROOT)), anchor['href']])
    # Shared extension banners intentionally repeat role/prerequisite guidance;
    # compare lesson prose while excluding that routing shell.
    for node in soup.select('.lesson-body > .lesson-section:not(.optional-route) .body-text'):
        if node.find_parent('details'):
            continue
        text = node.get_text(' ', strip=True)
        if len(text) > 40:
            copies[text].append(str(page.relative_to(ROOT)))
    rel = str(page.relative_to(ROOT))
    if rel in meta:
        source = ROOT / '_source/fragments' / meta[rel]['fragment']
        source_soup = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
        for section in source_soup.select('.lesson-section'):
            actual = soup.select_one('.lesson-body > #' + section['id'])
            assert actual is not None, (rel, section['id'], 'missing source section')
            assert actual.get_text(' ', strip=True) == section.get_text(' ', strip=True), (rel, section['id'], 'source text mismatch')
            assert [(a.get('href'), a.get('download')) for a in actual.select('a')] == [(a.get('href'), a.get('download')) for a in section.select('a')], (rel, section['id'], 'source link mismatch')
        fidelity.append({'page': rel, 'source': str(source.relative_to(ROOT)), 'text_and_links': 'MATCH'})

# The manifest, homepage checklist/catalog, and every core-page navigation form one route contract.
assert route and len(route) == len(set(route)), route
index = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
checklist = [node.get('data-core-complete') for node in index.select('#required-route input[data-core-complete]')]
assert checklist == route, {'manifest': route, 'homepage_checklist': checklist}
assert index.select_one('#core-progress-count').get_text(strip=True) == f'0 / {len(route)}'
catalog = index.select('#optional-catalog .lesson-list a.lesson-card, #optional-catalog .prac-list a.prac-card')
assert len(catalog) == 39, f'new-catalog-count={len(catalog)}'
roles = collections.Counter(card.get('data-learning-role') for card in catalog)
assert roles == {'core': 7, 'extension': 29, 'reference': 3}, dict(roles)
assert not index.select('#optional-catalog a[href="part2/PRAC2-2.html"]')
assert (ROOT / 'part2/PRAC2-2.html').is_file(), 'historical timezone page must remain present'
for page in route:
    assert (ROOT / page).is_file(), f'missing route page: {page}'

for i, rel in enumerate(route):
    page = ROOT / rel
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    nav = soup.select_one('.lesson-nav')
    assert nav is not None, (rel, 'missing lesson navigation')
    previous = nav.select_one('[data-nav-role="prev"]')
    following = nav.select_one('[data-nav-role="next"]')
    assert previous is not None and following is not None, (rel, 'missing prev/next link')
    expected_prev = ROOT / (route[i - 1] if i else 'index.html')
    expected_next = ROOT / (route[i + 1] if i + 1 < len(route) else 'index.html')
    actual_prev = (page.parent / unquote(urlsplit(previous['href']).path)).resolve()
    actual_next = (page.parent / unquote(urlsplit(following['href']).path)).resolve()
    assert actual_prev == expected_prev.resolve(), (rel, 'previous link', previous['href'], str(expected_prev))
    assert actual_next == expected_next.resolve(), (rel, 'next link', following['href'], str(expected_next))
    title = soup.select_one('.lesson-title')
    assert title is not None and title.get_text(' ', strip=True) == meta[rel]['title'], (rel, 'route title mismatch', title.get_text(' ', strip=True) if title else None, meta[rel]['title'])
    assert soup.select_one('.lesson-hero[data-learning-role="core"]') is not None, (rel, 'route page role')

for rel in ('part3/PRAC3-3.html', 'part6/CH6-1.html', 'part6/PRAC6-1.html'):
    soup = BeautifulSoup((ROOT / rel).read_text(encoding='utf-8'), 'html.parser')
    assert soup.select_one('.lesson-hero[data-learning-role="extension"]') is not None, (rel, 'supplement role')

assert not broken and not badanchors and not duplicates, (broken, badanchors, duplicates)
shared = [(text, pages) for text, pages in copies.items() if len(pages) > 2 and text != KNOWN_SHARED_GUIDANCE]
known_shared_guidance = [
    {'text': text, 'pages': pages}
    for text, pages in copies.items()
    if text == KNOWN_SHARED_GUIDANCE and len(pages) > 2
]
assert not shared, shared
with zipfile.ZipFile(ROOT / 'assets/materials/materials.zip') as archive:
    for material in (ROOT / 'assets/materials').iterdir():
        if material.suffix != '.zip':
            assert archive.read(material.name) == material.read_bytes(), material.name

if args.skip_shared_ops:
    shared_ops = {'status': 'DEFERRED', 'reason': '--skip-shared-ops'}
else:
    old = json.loads((ROOT / '_backup/2026-10-06-pre-repair/site-ops/search-index.json').read_text(encoding='utf-8'))
    current = json.loads((SITE / 'search-index.json').read_text(encoding='utf-8'))
    assert [item for item in old if item['course'] != 'gemini-ai'] == [item for item in current if item['course'] != 'gemini-ai']
    assert len([item for item in current if item['course'] == 'gemini-ai']) == 45
    shared_ops = {'status': 'PASS', 'other_course_search_entries_unchanged': True}

report = {
    'pages': len(files),
    'broken_links': broken,
    'broken_fragments': badanchors,
    'duplicate_ids': duplicates,
    'shared_long_copy': shared,
    'known_shared_guidance': known_shared_guidance,
    'required_route': route,
    'required_route_count': len(route),
    'new_catalog_count': len(catalog),
    'catalog_roles': dict(roles),
    'excluded_historical_page': 'part2/PRAC2-2.html',
    'fidelity': fidelity,
    'zip_matches_materials': True,
    'shared_ops': shared_ops,
    'versions': {str(page.relative_to(ROOT)): hashlib.sha256(page.read_bytes()).hexdigest() for page in files},
}
(OUT / 'link-and-copy-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'PASS：{len(files)}頁連結與錨點、{len(route)}站導覽與來源保真、{len(catalog)}頁首頁目錄、素材ZIP；shared_ops={shared_ops["status"]}。')
