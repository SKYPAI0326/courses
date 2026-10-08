#!/usr/bin/env python3
"""Apply reviewed, page-scoped course styles without changing HTML bodies or scripts."""
from pathlib import Path
import argparse, json, re
STYLE_IDS = ('coldtone-preview-style', 'coldtone-course-style', 'coldtone-table-readability', 'coldtone-prompt-layout')

def apply_html(text, page, site):
    config = Path(site) / '_source/coldtone-styles.json'
    if not config.exists():
        return text
    blocks = json.loads(config.read_text())['pages'].get(page)
    if not blocks:
        return text
    for ident in STYLE_IDS:
        text = re.sub(r'<style id="' + re.escape(ident) + r'">[\s\S]*?</style>\n?', '', text)
    assert '</head>' in text, page
    styles = ''.join('<style id="' + block['id'] + '">' + block['css'] + '</style>\n' for block in blocks)
    return text.replace('</head>', styles + '</head>', 1)

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
