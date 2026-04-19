#!/usr/bin/env python3
"""
V4 Style Migration — 將 CCS 的編輯式視覺語彙套到其他課程

規則見 _規範/設計升級v4-CCS語彙傳播.md

用法：
  python3 docs/apply-v4-style.py --dry-run courses/office-ai/
  python3 docs/apply-v4-style.py courses/office-ai/
  python3 docs/apply-v4-style.py --file courses/office-ai/part1/CH1-2.html
"""
import argparse, re, sys
from pathlib import Path


# =============================================================================
# 規則定義
# =============================================================================

# 1. Font URL
FONT_URL_OLD = 'https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap'
FONT_URL_NEW = 'https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap'

# 2. Font family string
FONT_FAM_OLD = "'Noto Serif TC',serif"
FONT_FAM_NEW = "'Shippori Mincho',serif"

# 以下每條規則 = (label, pattern_regex, replacement)
# 只匹配精確的 V3 樣式 signature，避免誤傷
RULES = []

def add(label, pattern, replacement):
    RULES.append((label, re.compile(pattern, re.DOTALL), replacement))


# progress-strip
add(
    'progress-strip',
    r'\.progress-strip\{height:3px;background:var\(--c-surface\);',
    '.progress-strip{height:2px;background:transparent;',
)

# hero-part
add(
    'hero-part',
    r'\.hero-part\{font-size:\.73rem;color:var\(--c-muted\);letter-spacing:1px;font-weight:500\}',
    '.hero-part{font-size:.73rem;color:var(--c-muted);letter-spacing:.08em;font-weight:500;font-variant-numeric:tabular-nums}',
)

# hero-num — 使用 --c-a1（課程主色）
add(
    'hero-num',
    r'\.hero-num\{font-size:\.73rem;color:var\(--c-a2\);letter-spacing:1px;font-weight:500\}',
    ".hero-num{font-family:'Shippori Mincho',serif;font-size:.78rem;color:var(--c-a1);letter-spacing:.1em;font-weight:500;font-variant-numeric:tabular-nums}",
)

# lesson-title — 加 letter-spacing（若尚未有）
add(
    'lesson-title',
    r"\.lesson-title\{font-family:'Shippori Mincho',serif;font-size:2rem;font-weight:700;line-height:1\.3;color:var\(--c-text\);margin-bottom:20px\}",
    ".lesson-title{font-family:'Shippori Mincho',serif;font-size:2rem;font-weight:700;line-height:1.3;color:var(--c-text);margin-bottom:20px;letter-spacing:-.005em}",
)

# outcomes（V3 舊版：水平雙線）
add(
    'outcomes',
    r'\.outcomes\{display:flex;flex-direction:column;gap:8px;padding:20px 0;border-top:1px solid var\(--c-border-soft\);border-bottom:1px solid var\(--c-border-soft\)\}\n?'
    r"\.outcomes-label\{font-family:'Shippori Mincho',serif;font-style:italic;font-size:\.78rem;color:var\(--c-muted\);letter-spacing:\.03em;margin-bottom:2px\}\n?"
    r'\.outcome-item\{display:flex;align-items:flex-start;gap:10px;font-size:\.9rem;color:var\(--c-text\)\}\n?'
    r'\.outcome-dot\{width:12px;height:1px;background:var\(--c-faint\);margin-top:14px;flex-shrink:0\}',
    '.outcomes{display:flex;flex-direction:column;gap:10px;padding:4px 0 4px 24px;border-left:1px solid var(--c-text)}\n'
    '.outcomes-label{font-size:.73rem;color:var(--c-text);letter-spacing:.15em;font-weight:500;margin-bottom:4px}\n'
    '.outcome-item{display:flex;align-items:flex-start;gap:10px;font-size:.9rem;color:var(--c-text)}\n'
    '.outcome-dot{width:5px;height:5px;border-radius:50%;background:var(--c-a1);margin-top:8px;flex-shrink:0}',
)

# section-eyebrow
add(
    'section-eyebrow',
    r"\.section-eyebrow\{font-family:'Shippori Mincho',serif;font-style:italic;font-size:\.8rem;color:var\(--c-muted\);letter-spacing:\.02em;font-weight:400;margin-bottom:12px\}",
    ".section-eyebrow{font-family:'Shippori Mincho',serif;font-size:.8rem;color:var(--c-faint);letter-spacing:.1em;font-weight:500;margin-bottom:10px;font-variant-numeric:tabular-nums}",
)

# section-heading + em
add(
    'section-heading',
    r"\.section-heading\{font-family:'Shippori Mincho',serif;font-size:1\.45rem;font-weight:700;color:var\(--c-text\);margin-bottom:20px;line-height:1\.35\}\n?"
    r"\.section-heading em\{font-family:'Shippori Mincho',serif;font-style:italic;font-weight:500;color:inherit\}",
    ".section-heading{font-family:'Shippori Mincho',serif;font-size:1.45rem;font-weight:700;color:var(--c-text);margin-bottom:20px;line-height:1.4;letter-spacing:-.005em}\n"
    ".section-heading em{font-style:normal;color:var(--c-text)}",
)

# lesson-section margin
add(
    'lesson-section-margin',
    r'\.lesson-section\{margin-bottom:72px\}',
    '.lesson-section{margin-bottom:64px}',
)

# section-rule margin
add(
    'section-rule-margin',
    r'\.section-rule\{border:none;border-top:1px solid var\(--c-border\);margin:72px 0\}',
    '.section-rule{border:none;border-top:1px solid var(--c-border);margin:64px 0}',
)

# callout
add(
    'callout',
    r'\.callout\{display:flex;gap:14px;padding:12px 0 12px 18px;border-left:2px solid var\(--c-border\);background:transparent;border-radius:0;margin:24px 0\}',
    '.callout{display:flex;gap:16px;padding:18px 22px;border-radius:var(--radius);margin:24px 0;background:var(--c-surface);border-left:2px solid var(--c-text)}\n'
    '.callout.info,.callout.tip,.callout.key{background:var(--c-surface);border-left:2px solid var(--c-text)}',
)

# lesson-nav — 舊的實心強調按鈕式
add(
    'lesson-nav',
    r'\.lesson-nav\{max-width:var\(--content-w\);margin:0 auto;padding:0 48px 80px;display:flex;justify-content:space-between;gap:12px\}\n?'
    r'\.nav-btn\{display:inline-flex;align-items:center;gap:8px;font-size:\.85rem;font-weight:500;padding:10px 20px;border-radius:var\(--radius\);text-decoration:none;transition:all \.15s\}\n?'
    r'\.nav-prev\{background:var\(--c-surface\);color:var\(--c-text\);border:1px solid var\(--c-border\)\}\n?'
    r'\.nav-prev:hover\{background:var\(--c-border\)\}\n?'
    r'\.nav-next\{background:var\(--c-a2\);color:#fff\}\n?'
    r'\.nav-next:hover\{background:#b8852e\}\n?'
    r'\.nav-label\{font-size:\.73rem;opacity:\.8\}',
    '.lesson-nav{max-width:var(--content-w);margin:0 auto;padding:0 48px 80px;display:flex;gap:16px}\n'
    '.nav-btn{display:flex;align-items:center;gap:10px;padding:14px 22px;background:var(--c-card);border:1px solid var(--c-border);border-radius:var(--radius);text-decoration:none;color:var(--c-text);font-size:.85rem;transition:border-color .2s;flex:1}\n'
    '.nav-btn:hover{border-color:var(--c-a1)}\n'
    '.nav-prev{background:var(--c-card);color:var(--c-text);border:1px solid var(--c-border)}\n'
    '.nav-prev:hover{background:var(--c-card);border-color:var(--c-a1)}\n'
    '.nav-next{background:var(--c-card);color:var(--c-text);border:1px solid var(--c-border);justify-content:flex-end;text-align:right}\n'
    '.nav-next:hover{background:var(--c-card);border-color:var(--c-a1)}\n'
    '.nav-label{font-size:.7rem;color:var(--c-muted);margin-bottom:2px}',
)


# =============================================================================
# topbar-tag — 需抓 --c-a1 hex 算 RGB
# =============================================================================

HEX_RE = re.compile(r'--c-a1:(#[0-9a-fA-F]{6})')

def hex_to_rgb(h):
    h = h.lstrip('#')
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def apply_topbar_tag(text):
    """偵測舊的 topbar-tag 格式並用課程自身 --c-a1 RGB 改寫。"""
    m = HEX_RE.search(text)
    if not m:
        return text, 0
    r, g, b = hex_to_rgb(m.group(1))
    rgb_str = f'{r},{g},{b}'

    # 舊 pattern：color:var(--c-a2)，rgba() 可能是任何值
    pattern = re.compile(
        r'\.topbar-tag\{font-size:\.75rem;color:var\(--c-a2\);'
        r'border:1px solid rgba\(\d+,\d+,\d+,\.3\);'
        r'background:rgba\(\d+,\d+,\d+,\.07\);'
        r'padding:3px 12px;border-radius:99px;font-weight:500\}'
    )
    new_rule = (
        '.topbar-tag{font-size:.75rem;color:var(--c-a1);'
        f'border:1px solid rgba({rgb_str},.3);'
        f'background:rgba({rgb_str},.07);'
        'padding:3px 12px;border-radius:99px;font-weight:500}'
    )
    new_text, n = pattern.subn(new_rule, text)
    return new_text, n


# =============================================================================
# 主流程
# =============================================================================

def process_file(path: Path, dry_run=False):
    src = path.read_text(encoding='utf-8')
    out = src
    changes = {}

    # Font URL
    if FONT_URL_OLD in out:
        out = out.replace(FONT_URL_OLD, FONT_URL_NEW)
        changes['font-url'] = 1

    # Font family（全檔替換）
    if FONT_FAM_OLD in out:
        cnt = out.count(FONT_FAM_OLD)
        out = out.replace(FONT_FAM_OLD, FONT_FAM_NEW)
        changes['font-family'] = cnt

    # topbar-tag
    out, n = apply_topbar_tag(out)
    if n:
        changes['topbar-tag'] = n

    # 其他規則
    for label, pat, rep in RULES:
        new_out, n = pat.subn(rep, out)
        if n:
            changes[label] = n
            out = new_out

    if out != src:
        if not dry_run:
            path.write_text(out, encoding='utf-8')
        return changes
    return None


def main():
    ap = argparse.ArgumentParser(description='V4 Style Migration')
    ap.add_argument('target', nargs='?', help='course dir or file')
    ap.add_argument('--file', help='single file')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if args.file:
        files = [Path(args.file)]
    elif args.target:
        p = Path(args.target)
        if p.is_file():
            files = [p]
        else:
            files = sorted(p.rglob('*.html'))
            # 排除 _pilots, _backup 等
            files = [f for f in files if '_pilots' not in f.parts and '_backup' not in f.parts]
    else:
        ap.error('need target dir or --file')

    total_changed = 0
    total_rules = 0
    skipped = []
    for f in files:
        try:
            c = process_file(f, dry_run=args.dry_run)
        except Exception as e:
            print(f'  ✗ {f}: {e}', file=sys.stderr)
            continue
        if c:
            total_changed += 1
            total_rules += sum(c.values())
            summary = ','.join(f'{k}:{v}' for k,v in c.items())
            tag = '[dry]' if args.dry_run else '[ok]'
            print(f'  {tag} {f.relative_to(Path.cwd()) if f.is_absolute() else f}  {summary}')
        else:
            skipped.append(f)

    print(f'\n═══ 摘要 ═══')
    print(f'掃描：{len(files)} 檔')
    print(f'異動：{total_changed} 檔 ({total_rules} 處替換)')
    print(f'未動：{len(skipped)} 檔')
    if args.dry_run:
        print('(dry-run — 無實際寫入)')


if __name__ == '__main__':
    main()
