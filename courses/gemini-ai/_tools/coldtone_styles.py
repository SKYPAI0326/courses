#!/usr/bin/env python3
"""Apply reviewed, page-scoped course styles without changing HTML bodies or scripts."""
from pathlib import Path
import argparse, json, re
from bs4 import BeautifulSoup
STYLE_IDS = ('coldtone-preview-style', 'coldtone-course-style', 'coldtone-table-readability', 'coldtone-prompt-layout', 'coldtone-result-palette', 'coldtone-reading-lists')

def resolve_blocks(config, page):
    blocks = []
    for item in config['pages'].get(page, []):
        if 'ref' in item:
            block = dict(config['shared_styles'][item['ref']])
            block['css'] += item.get('append_css', '')
        else:
            block = item
        assert block['id'] in STYLE_IDS, page
        blocks.append(block)
    assert len({b['id'] for b in blocks}) == len(blocks), page
    return blocks

def apply_html(text, page, site):
    config = Path(site) / '_source/coldtone-styles.json'
    if not config.exists():
        return text
    blocks = resolve_blocks(json.loads(config.read_text()), page)
    if not blocks:
        return text
    doc = BeautifulSoup(text, 'html.parser')
    assert len(doc.select('head')) == 1, page
    for ident in STYLE_IDS:
        assert len(doc.head.select('style#' + ident)) <= 1, page
    match = re.search(r'<head\b[^>]*>[\s\S]*?</head>', text)
    assert match is not None, page
    head = match.group()
    for ident in STYLE_IDS:
        head = re.sub(r'<style id="' + re.escape(ident) + r'">[\s\S]*?</style>\n?', '', head)
    styles = ''.join('<style id="' + block['id'] + '">' + block['css'] + '</style>\n' for block in blocks)
    head = head.replace('</head>', styles + '</head>', 1)
    return text[:match.start()] + head + text[match.end():]

def apply_site(site, check=False):
    site = Path(site)
    config = json.loads((site / '_source/coldtone-styles.json').read_text())
    changed = []
    for page in config['pages']:
        path = site / page
        before = path.read_text()
        after = apply_html(before, page, site)
        if after != before:
            changed.append(page)
            if not check:
                path.write_text(after)
    return changed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = apply_site(args.site, args.check)
    print(json.dumps({'changed': changed, 'check': args.check}, ensure_ascii=False))
    raise SystemExit(bool(args.check and changed))
