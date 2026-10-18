#!/usr/bin/env python3
"""
L3 Prompt 5 骨架自動 parser

用法：
    python3 L3-prompt-parser.py path/to/prompts.md [path/to/prompts2.md ...]

輸出：
    每個 prompt 的 5 骨架檢查（角色 / 資料 / 任務 / 輸出格式 / 驗證要求）
    主課 prompt（-2 進階版）必含完整 5 骨架，否則標 BLOCKER

退出碼：
    0 = 全通過
    1 = 有 BLOCKER
"""

import sys
import re
import argparse

BONES = ['角色', '資料', '任務', '輸出', '驗證']

def parse_prompts(filepath):
    """parse prompts.md 回傳 list of (id, body)"""
    with open(filepath, encoding='utf-8') as f:
        text = f.read()
    # 切分每個 prompt：### P{X}-{Y}{Z?}-{N}
    parts = re.split(r'^### (P[\w-]+|B-[\w-]+|NB-[\w-]+|S-[\w-]+)', text, flags=re.MULTILINE)
    prompts = []
    for i in range(1, len(parts), 2):
        pid = parts[i].split()[0]
        body = parts[i+1] if i+1 < len(parts) else ''
        prompts.append((pid, body))
    return prompts


def check_bones(body):
    """檢查 prompt body 是否含 5 骨架"""
    return {
        '角色': '【角色】' in body or '角色：' in body,
        '資料': '【資料】' in body or '資料：' in body,
        '任務': '【任務】' in body or '任務：' in body,
        '輸出': '【輸出格式】' in body or '【輸出】' in body or '輸出格式：' in body,
        '驗證': '【驗證要求】' in body or '【驗證】' in body or '驗證要求：' in body,
    }


def is_main_prompt(pid):
    """判斷是否主課 prompt（-2 進階版必含完整 5 骨架）"""
    # P{X}-{Y}{Z?}-2 = 進階版
    return bool(re.match(r'^P\d+-\d+[A-Z]?-2$', pid))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='prompts.md files')
    parser.add_argument('--strict', action='store_true',
                        help='非主課 prompt 缺骨架也視為 BLOCKER')
    args = parser.parse_args()

    blocker_count = 0
    total_prompts = 0
    issues = []

    for filepath in args.files:
        prompts = parse_prompts(filepath)
        for pid, body in prompts:
            total_prompts += 1
            bones = check_bones(body)
            missing = [k for k, v in bones.items() if not v]

            if missing:
                is_main = is_main_prompt(pid)
                severity = 'BLOCKER' if (is_main or args.strict) else 'WARN'
                if severity == 'BLOCKER':
                    blocker_count += 1
                issues.append({
                    'file': filepath,
                    'pid': pid,
                    'severity': severity,
                    'missing': missing,
                    'is_main': is_main,
                })

    # 輸出
    print(f'═══ L3 Prompt 5 骨架檢查 ═══')
    print(f'掃描：{total_prompts} prompts')
    print(f'BLOCKER：{blocker_count}')
    print(f'WARN：{len(issues) - blocker_count}')
    print()

    if issues:
        print('--- 細項 ---')
        for issue in issues:
            tag = '⛔' if issue['severity'] == 'BLOCKER' else '⚠ '
            main_tag = '(主課)' if issue['is_main'] else '(變奏/風險)'
            print(f"{tag} {issue['pid']} {main_tag}: 缺 {','.join(issue['missing'])}")
    else:
        print('✓ 全部通過')

    sys.exit(1 if blocker_count > 0 else 0)


if __name__ == '__main__':
    main()
