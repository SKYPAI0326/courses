#!/usr/bin/env python3
"""Prepare the complete source-backed Canva handout, then optionally build it.

Run --prepare-only for the recipe/media-link appendix; --create-pdf authors a
candidate. Review every page and use standard verify/promote afterwards.
Only empty embedded-player containers are replaced by an appendix of their
existing labels, source URLs and poster images. No lesson text is rewritten.
"""
import argparse
import json
import os
import sys
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from unittest.mock import patch

from bs4 import BeautifulSoup, Tag

MANAGER = Path(__file__).resolve().parents[1]
ROOT = MANAGER.parent
COURSE = ROOT / 'canva-video-teaching'
PUBLIC = 'https://skypai0326.github.io/courses/courses/'
RECIPE = MANAGER / 'registry/pdf/recipes/canva-video-teaching-full.json'
APPENDIX = MANAGER / 'registry/pdf/derived/canva-video-teaching-media.html'
EVIDENCE = MANAGER / 'registry/pdf/derived/canva-video-teaching-coverage.json'
sys.path.insert(0, str(MANAGER))
from src.pdf_sources import normalize_text, sha, prepare
from src.pdf_registry import write_json
from src.pdf_build import build


def selector(node):
    parts = []
    while node.name != 'body':
        index = len(node.find_previous_siblings(node.name)) + 1
        parts.append(f'{node.name}:nth-of-type({index})')
        node = node.parent
    return 'body > ' + ' > '.join(reversed(parts))


def body_selection(node):
    if node.name in {'video', 'audio'}:
        assert not normalize_text(node.get_text()), 'Media has fallback text: inspect manually'
        return []
    if not node.select('video,audio'):
        return [node]
    assert all(not normalize_text(str(c)) for c in node.children if not isinstance(c, Tag)), 'Unwrapped text needs manual selection'
    selected = []
    for child in node.find_all(recursive=False):
        if child.name not in {'video', 'audio'} and not child.select('video,audio'):
            selected.append(child)
        else:
            selected.extend(body_selection(child))
    return selected


def prepare_recipe():
    index = BeautifulSoup((COURSE / 'index.html').read_text(), 'html.parser')
    ordered = []
    for link in index.select('main a.lesson-card[href]'):
        rel = link['href']
        if rel not in ordered:
            ordered.append(rel)
    assert len(ordered) == 25 and len([p for p in ordered if p.startswith('ch')]) == 12
    sources = [{'path': 'canva-video-teaching/index.html', 'selectors': ['main > .hero'],
                'source_url': PUBLIC + 'canva-video-teaching/index.html', 'static_content_confirmed': True}]
    coverage, media, dependencies = [], [], set()
    for rel in ordered:
        path = COURSE / rel
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        body = soup.select_one('.lesson-body')
        selected = body_selection(body)
        original = normalize_text(body.get_text())
        retained = normalize_text(''.join(n.get_text() for n in selected))
        assert original == retained, f'Body text lost: {rel}'
        images = body.select('img')
        selected_images = [n for s in selected for n in ([s] if s.name == 'img' else s.select('img'))]
        assert [str(n) for n in images] == [str(n) for n in selected_images], rel
        selectors = ['.lesson-hero > :not(.section-toc):not(button)'] + [selector(n) for n in selected]
        sources.append({'path': path.relative_to(ROOT).as_posix(), 'selectors': selectors,
                        'source_url': PUBLIC + path.relative_to(ROOT).as_posix(), 'static_content_confirmed': True})
        coverage.append({'source': path.relative_to(ROOT).as_posix(), 'source_sha256': sha(path),
                         'title': soup.h1.get_text(), 'body_text_preserved': True,
                         'body_characters': len(original), 'images_preserved': len(images), 'selectors': selectors})
        for player in body.select('video,audio'):
            src = player.select_one('source[src]')['src'] if player.select_one('source[src]') else player['src']
            local = (path.parent / unquote(urlsplit(src).path)).resolve()
            assert local.is_file() and local.is_relative_to(COURSE)
            dependencies.add(local.relative_to(ROOT).as_posix())
            entry = {'source': path.relative_to(ROOT).as_posix(), 'source_sha256': sha(path),
                     'type': player.name, 'label': player['aria-label'], 'media': local.relative_to(ROOT).as_posix(),
                     'media_sha256': sha(local), 'url': urljoin(PUBLIC + path.relative_to(ROOT).as_posix(), src),
                     'original_markup': str(player)}
            if player.get('poster'):
                poster = (path.parent / player['poster']).resolve();assert poster.is_file()
                dependencies.add(poster.relative_to(ROOT).as_posix())
                entry['poster'] = poster.relative_to(ROOT).as_posix();entry['poster_sha256'] = sha(poster)
            media.append(entry)
    assert len(media) == 5
    APPENDIX.parent.mkdir(parents=True, exist_ok=True)
    html = ['<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>影音取用連結</title></head><body><main>',
            '<h1>影音取用連結</h1>']
    for entry in media:
        html.append('<section class="media-link"><h2>' + escape(entry['label']) + '</h2>')
        if entry.get('poster'):
            poster = os.path.relpath(ROOT / entry['poster'], APPENDIX.parent)
            html.append('<a href="' + escape(entry['url'], quote=True) + '"><img src="' + escape(poster, quote=True) + '" alt="' + escape(entry['label'], quote=True) + '"></a>')
        html.append('<p><a href="' + escape(entry['url'], quote=True) + '">' + escape(entry['label']) + '</a></p></section>')
    html.append('</main></body></html>')
    APPENDIX.write_text('\n'.join(html), encoding='utf-8')
    write_json(EVIDENCE, {'sources': coverage, 'media_fallbacks': media,
                          'method': 'Exact full body text/image preservation. Empty embedded players use original aria-label/source/poster in an administrative media-link appendix; no media transcript invented.'})
    sources.append({'path': APPENDIX.relative_to(ROOT).as_posix(), 'selectors': ['main'],
                    'source_url': PUBLIC + 'canva-video-teaching/index.html', 'static_content_confirmed': True})
    dependencies.update([Path(__file__).resolve().relative_to(ROOT).as_posix(), EVIDENCE.relative_to(ROOT).as_posix(),
                         'canva-video-teaching/module1.html', 'canva-video-teaching/module2.html'])
    recipe = {'schema_version': 1, 'artifact_id': 'canva-video-teaching-full', 'course': 'canva-video-teaching',
              'output': 'output/pdf/canva-video-teaching/Canva教學短片製作-完整講義.pdf',
              'profile': 'course-manager/pdf-profiles/canva-video-teaching.css', 'sources': sources,
              'source_courses': ['canva-video-teaching', 'course-manager'],
              'font_files': ['/Library/Fonts/Arial Unicode.ttf'], 'exclude': [], 'expand': [],
              'dependencies': sorted(dependencies), 'remote_assets': {},
              'notes': '完整合冊：依正式 index 順序收錄 12 單元、12 資源頁及 EXT1，含原文 details 補充。封面取自正式首頁 hero。僅省略返回導覽、重複頁內目錄、列印按鈕與空白影音播放器；全部正文與原有圖片完整保留。五個播放器的原有 aria-label、source URL、poster 逐一對照保存在 derived 媒體附錄；course-manager 僅作此管理附錄來源，不混入其他課程。音訊／影片以連結取用，不捏造逐字稿。建置入口 python3.12 course-manager/scripts/build_canva_video_handout.py --create-pdf 會刷新原文對照、附錄及配方，再用標準引擎建候選；原生頁碼 12px（9pt），須逐頁驗收及 promote。'}
    write_json(RECIPE, recipe)
    prepared = prepare(ROOT, recipe)
    return recipe, prepared


def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare-only', action='store_true')
    mode.add_argument('--create-pdf', action='store_true')
    args = p.parse_args()
    recipe, prepared = prepare_recipe()
    if args.prepare_only:
        print(json.dumps({'status': 'PLANNED', 'sources': len(recipe['sources']), 'fingerprint': prepared['fingerprint'], 'dependencies': len(prepared['dependencies'])}, indent=2))
        return
    from playwright.sync_api import Page
    native_pdf = Page.pdf

    def pdf_with_footer(page, *positional, **options):
        original = '<div style="font-size:8px;width:100%;text-align:center">Page <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        assert options.get('footer_template') == original, 'Inspect changed renderer footer'
        options['footer_template'] = original.replace('font-size:8px', 'font-size:12px')
        return native_pdf(page, *positional, **options)

    with patch.object(Page, 'pdf', pdf_with_footer):
        result = build(ROOT, recipe, create_pdf=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
