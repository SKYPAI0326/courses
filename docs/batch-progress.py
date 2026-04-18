#!/usr/bin/env python3
"""batch-progress.py — 子代理批次進度追蹤（通用版）

原為 progress_helper.py（只給課程 lesson-writer subagent 用），
這版放到 docs/ 下、manifest 位置改進課程專案資料夾，讓其他批次 subagent 場景也能共用。

場景：
  主會話派多個 subagent 並行做 N 個單元/頁/資產，中途若任一 agent 崩了或超時，
  靠 manifest 知道誰完成、誰還沒，可續派缺的那幾個。

用法：
  python3 docs/batch-progress.py init JOB_ID TASK1 TASK2 ...
  python3 docs/batch-progress.py mark-done JOB_ID TASK_ID
  python3 docs/batch-progress.py mark-failed JOB_ID TASK_ID [--reason "說明"]
  python3 docs/batch-progress.py status JOB_ID
  python3 docs/batch-progress.py pending JOB_ID       # 只印待辦 task_id（續跑代理讀）
  python3 docs/batch-progress.py list                 # 列所有 job
  python3 docs/batch-progress.py clean JOB_ID         # 砍掉 manifest

Manifest 放在專案根的 `.batch-progress/`（已加入 .gitignore 的話就好；沒加也不影響功能）。

Exit code：
  0 = 成功
  1 = 指定 JOB_ID / TASK_ID 不存在
  2 = 使用錯誤
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS_DIR = ROOT / ".batch-progress"
PROGRESS_DIR.mkdir(parents=True, exist_ok=True)


def manifest_path(job_id: str) -> Path:
    return PROGRESS_DIR / f"{job_id}.json"


def load(job_id: str) -> dict:
    p = manifest_path(job_id)
    if not p.exists():
        print(f"Error: job '{job_id}' 不存在", file=sys.stderr)
        sys.exit(1)
    return json.loads(p.read_text(encoding="utf-8"))


def save(job_id: str, data: dict):
    data["updated_at"] = now()
    manifest_path(job_id).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def cmd_init(job_id: str, tasks: list):
    p = manifest_path(job_id)
    if p.exists():
        print(f"Warning: job '{job_id}' 已存在，覆寫", file=sys.stderr)
    data = {
        "job_id": job_id,
        "created_at": now(),
        "updated_at": now(),
        "total": len(tasks),
        "tasks": {t: {"status": "pending"} for t in tasks},
    }
    save(job_id, data)
    print(f"[init] job={job_id}，共 {len(tasks)} 個任務")
    for t in tasks:
        print(f"  - {t}")


def cmd_mark_done(job_id: str, task_id: str):
    data = load(job_id)
    if task_id not in data["tasks"]:
        print(f"Error: task '{task_id}' 不在 job '{job_id}' 中", file=sys.stderr)
        sys.exit(1)
    data["tasks"][task_id] = {"status": "done", "completed_at": now()}
    save(job_id, data)
    done = sum(1 for t in data["tasks"].values() if t["status"] == "done")
    print(f"[done] {task_id} ✓  ({done}/{data['total']})")


def cmd_mark_failed(job_id: str, task_id: str, reason: str = ""):
    data = load(job_id)
    if task_id not in data["tasks"]:
        print(f"Error: task '{task_id}' 不在 job '{job_id}' 中", file=sys.stderr)
        sys.exit(1)
    data["tasks"][task_id] = {"status": "failed", "reason": reason, "failed_at": now()}
    save(job_id, data)
    print(f"[failed] {task_id}  reason={reason!r}")


def cmd_status(job_id: str):
    data = load(job_id)
    tasks = data["tasks"]
    done    = [k for k, v in tasks.items() if v["status"] == "done"]
    pending = [k for k, v in tasks.items() if v["status"] == "pending"]
    failed  = [k for k, v in tasks.items() if v["status"] == "failed"]

    print(f"Job: {job_id}")
    print(f"建立：{data['created_at']}  更新：{data['updated_at']}")
    print(f"進度：{len(done)}/{data['total']}  ✓{len(done)}  ○{len(pending)}  ✗{len(failed)}")

    if pending:
        print("\n待辦：")
        for t in pending:
            print(f"  ○ {t}")
    if failed:
        print("\n失敗：")
        for t in failed:
            reason = tasks[t].get("reason", "")
            print(f"  ✗ {t}  {f'({reason})' if reason else ''}")
    if not pending and not failed:
        print("\n全部完成 ✓")


def cmd_pending(job_id: str):
    data = load(job_id)
    for k, v in data["tasks"].items():
        if v["status"] == "pending":
            print(k)


def cmd_list():
    manifests = sorted(PROGRESS_DIR.glob("*.json"))
    if not manifests:
        print("（無進行中的 job）")
        return
    for p in manifests:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            tasks = data["tasks"]
            done    = sum(1 for v in tasks.values() if v["status"] == "done")
            pending = sum(1 for v in tasks.values() if v["status"] == "pending")
            failed  = sum(1 for v in tasks.values() if v["status"] == "failed")
            total   = data["total"]
            bar = "▓" * done + "░" * pending + "✗" * failed
            print(f"{data['job_id']:30s}  [{bar}] {done}/{total}  更新:{data['updated_at']}")
        except Exception:
            print(f"{p.stem}  (讀取失敗)")


def cmd_clean(job_id: str):
    p = manifest_path(job_id)
    if not p.exists():
        print(f"Error: job '{job_id}' 不存在", file=sys.stderr)
        sys.exit(1)
    p.unlink()
    print(f"[clean] job '{job_id}' 已刪除")


def main():
    ap = argparse.ArgumentParser(description="子代理批次進度追蹤（通用版）")
    sub = ap.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init", help="建立新 job")
    p_init.add_argument("job_id")
    p_init.add_argument("tasks", nargs="+")

    p_done = sub.add_parser("mark-done", help="標記任務完成")
    p_done.add_argument("job_id")
    p_done.add_argument("task_id")

    p_fail = sub.add_parser("mark-failed", help="標記任務失敗")
    p_fail.add_argument("job_id")
    p_fail.add_argument("task_id")
    p_fail.add_argument("--reason", default="")

    p_status = sub.add_parser("status", help="查看 job 進度")
    p_status.add_argument("job_id")

    p_pending = sub.add_parser("pending", help="列出待辦（供續跑代理）")
    p_pending.add_argument("job_id")

    sub.add_parser("list", help="列出所有 job")

    p_clean = sub.add_parser("clean", help="刪除 job manifest")
    p_clean.add_argument("job_id")

    args = ap.parse_args()

    if args.cmd == "init":
        cmd_init(args.job_id, args.tasks)
    elif args.cmd == "mark-done":
        cmd_mark_done(args.job_id, args.task_id)
    elif args.cmd == "mark-failed":
        cmd_mark_failed(args.job_id, args.task_id, args.reason)
    elif args.cmd == "status":
        cmd_status(args.job_id)
    elif args.cmd == "pending":
        cmd_pending(args.job_id)
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "clean":
        cmd_clean(args.job_id)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
