#!/usr/bin/env python3
"""Check or restore the exact five-chapter integration scope; stop on later edits."""
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / '_backup/2026-10-08-main-before-five-chapters'
sha = lambda value: hashlib.sha256(value).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((BACKUP / 'manifest.json').read_text())
    failures = []
    for item in manifest['files']:
        path = ROOT / item['path']
        assert path.resolve().is_relative_to(ROOT)
        current = sha(path.read_bytes()) if path.is_file() else None
        if current != item.get('integrated_sha256'):
            failures.append(item['path'])
        if item['existed']:
            saved = BACKUP / 'main' / item['path']
            if not saved.is_file() or sha(saved.read_bytes()) != item['before_sha256']:
                failures.append('backup: ' + item['path'])
    if failures:
        print('停止：整併後檔案或備份已變更。\n' + '\n'.join(failures))
        return 1
    if not args.apply:
        print(f"可還原 {len(manifest['files'])} 個目標；本次只核對，沒有改檔。")
        return 0
    for item in manifest['files']:
        path = ROOT / item['path']
        if item['existed']:
            path.write_bytes((BACKUP / 'main' / item['path']).read_bytes())
        elif path.is_file():
            path.unlink()
    print('已還原精確目標範圍；其他檔案未更動。')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
