#!/usr/bin/env python3
"""
status.jsonl 安全寫入工具

用法：
    python3 status_write.py <status-file> <run-id> <layer> <case_id> <status> [key=val ...]

範例：
    python3 status_write.py /path/status.jsonl r-20260514-2100 preflight all OK detail="全綠"
    python3 status_write.py /path/status.jsonl r-20260514-2100 L4a case2 PENDING_VERDICT call_id=abc123 score=8/10

避免 shell 拼接破 JSON：所有欄位用 json.dumps escape。
"""

import sys
import json
import datetime


def main():
    if len(sys.argv) < 6:
        print("usage: status_write.py <status-file> <run-id> <layer> <case_id> <status> [k=v ...]",
              file=sys.stderr)
        sys.exit(1)

    status_file = sys.argv[1]
    run_id = sys.argv[2]
    layer = sys.argv[3]
    case_id = sys.argv[4]
    status = sys.argv[5]

    record = {
        'run_id': run_id,
        'layer': layer,
        'case_id': case_id,
        'status': status,
        'updated_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    }

    # 額外 k=v
    for arg in sys.argv[6:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            record[k] = v

    with open(status_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"✓ status written: run_id={run_id} layer={layer}/{case_id} status={status}")


if __name__ == '__main__':
    main()
