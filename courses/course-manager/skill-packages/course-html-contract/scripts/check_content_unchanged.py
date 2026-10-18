#!/usr/bin/env python3
"""Compare visible text and links for syntax/layout-only HTML edits."""
from __future__ import annotations
import sys
from html.parser import HTMLParser
from pathlib import Path
import re

class Snapshot(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip=0; self.text=[]; self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        tag=tag.lower()
        if tag in {'script','style','template'}: self.skip += 1
        if self.skip == 0:
            for k,v in attrs:
                if k.lower() == 'href': self.hrefs.append(v or '')
    def handle_endtag(self, tag):
        if tag.lower() in {'script','style','template'} and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if self.skip == 0: self.text.append(data)
    def result(self):
        text=re.sub(r'\s+', ' ', ' '.join(self.text)).strip()
        return text, tuple(self.hrefs)

def snap(path):
    p=Snapshot(); p.feed(Path(path).read_text(encoding='utf-8')); p.close(); return p.result()

def main(before, after):
    a=snap(before); b=snap(after)
    if a == b:
        print('content unchanged')
        return 0
    print('CONTENT CHANGE BLOCK')
    if a[0] != b[0]:
        print(f'- visible text differs: before={len(a[0])} chars after={len(b[0])} chars')
    if a[1] != b[1]:
        print(f'- href sequence differs: before={len(a[1])} after={len(b[1])}')
    return 1

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print('usage: check_content_unchanged.py BEFORE.html AFTER.html', file=sys.stderr); raise SystemExit(2)
    raise SystemExit(main(sys.argv[1],sys.argv[2]))
