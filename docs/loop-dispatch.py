#!/usr/bin/env python3
"""
loop-dispatch.py — 循環作業夜班派工入口
-----------------------------------------------------------
依 `_規範/循環作業.md`：列出各佇列可交給夜班的卡；指定卡片時，從 origin/main
開 worktree、啟動全新 Codex session 執行該卡，回報存到主 checkout 的
`_local/night-reports/`，並在 `log.tsv` 記一筆量測。不 push、不 merge。

使用：
  python3 docs/loop-dispatch.py                 # 列出可派的卡
  python3 docs/loop-dispatch.py --run T-03      # 派工（耗時，建議背景執行）
  python3 docs/loop-dispatch.py --run T-03 --dry-run   # 只印出將執行的動作
"""
import argparse
import re
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

CARD_ID = re.compile(r"\b[A-Z]-\d+(?:-[A-Z])?\b")


def main_checkout() -> Path:
    out = subprocess.run(["git", "worktree", "list", "--porcelain"], capture_output=True,
                         text=True, check=True, cwd=Path(__file__).resolve().parent).stdout
    return Path(out.split("\n", 1)[0].removeprefix("worktree "))


def parse_queue(path: Path) -> dict:
    cards = {}
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        lines = block.splitlines()
        match = CARD_ID.match(lines[0])
        if not match:
            continue
        fields = {}
        for line in lines[1:]:
            m = re.match(r"- (類型|證據要求|相依|狀態)：(.*)", line)
            if m and m.group(1) not in fields:
                fields[m.group(1)] = m.group(2).strip()
        cards[match.group(0)] = {"title": lines[0], **fields}
    return cards


def dispatchable(card: dict, cards: dict) -> tuple[bool, str]:
    if not card.get("狀態", "").startswith("todo"):
        return False, "狀態非 todo"
    evidence = card.get("證據要求", "")
    night = "夜班" in card.get("類型", "") or re.match(r"(M|A)(?![A-Za-z])", evidence)
    if not night or re.search(r"\b[HE]\b|加 ?[HE]", evidence):
        return False, "證據要求需人或真人"
    for dep in CARD_ID.findall(card.get("相依", "")):
        if not cards.get(dep, {}).get("狀態", "").startswith("done"):
            return False, f"相依 {dep} 未完成"
    return True, ""


def queues(root: Path) -> list[Path]:
    return sorted(root.glob("courses/*/_local/loop-backlog.md")) + sorted(root.glob("_規範/_local/loop-backlog.md"))


def main() -> int:
    ap = argparse.ArgumentParser(description="循環作業夜班派工入口")
    ap.add_argument("--run", metavar="CARD", help="派工的卡片代號")
    ap.add_argument("--dry-run", action="store_true", help="只印出將執行的動作")
    args = ap.parse_args()

    root = main_checkout()
    found = []
    for queue in queues(root):
        cards = parse_queue(queue)
        for cid, card in cards.items():
            ok, reason = dispatchable(card, cards)
            found.append((queue, cid, card, ok, reason))

    if not args.run:
        for queue, cid, card, ok, reason in found:
            if ok:
                print(f"可派  {cid:8} {queue.relative_to(root)}  {card['title']}")
        blocked = [f for f in found if not f[3] and f[2].get("狀態", "").startswith("todo")]
        print(f"\n可派 {sum(f[3] for f in found)} 張；todo 但不可派 {len(blocked)} 張"
              + ("：" + "、".join(f"{f[1]}（{f[4]}）" for f in blocked) if blocked else ""))
        return 0

    target = [f for f in found if f[1] == args.run]
    if len(target) != 1:
        print(f"找不到唯一的卡 {args.run}（符合 {len(target)} 張）", file=sys.stderr)
        return 1
    queue, cid, card, ok, reason = target[0]
    if not ok:
        print(f"{cid} 不可派：{reason}", file=sys.stderr)
        return 1

    stamp = date.today().strftime("%Y%m%d")
    branch = f"codex/night-{cid.lower()}-{stamp}"
    worktree = root / ".claude" / "worktrees" / f"night-{cid.lower()}-{stamp}"
    reports = root / "_local" / "night-reports"
    report = reports / f"{stamp}-{cid}.txt"
    prompt = (
        f"你是本 repository 的夜班執行者。依載入的 AGENTS.md 與它指向的規範，只執行佇列 {queue} 的卡 {cid}。"
        f"你目前已在從 origin/main 開出的 worktree（分支 {branch}）。不得 push、不得 merge。"
        "最終回報依規範的卡片格式，列出實際變動、驗收逐項結果與狀態，範圍外發現寫成新卡建議。"
    )
    steps = [
        ["git", "-C", str(root), "fetch", "-q", "origin", "main"],
        ["git", "-C", str(root), "worktree", "add", "-q", "-b", branch, str(worktree), "origin/main"],
        ["codex", "exec", "--ephemeral", "--color", "never", "-s", "workspace-write", "-C", str(worktree), prompt],
    ]
    if args.dry_run:
        for step in steps:
            print(" ".join(step[:-1] + [repr(step[-1])]) if step[0] == "codex" else " ".join(step))
        print(f"回報：{report}")
        return 0

    reports.mkdir(parents=True, exist_ok=True)
    for step in steps[:2]:
        subprocess.run(step, check=True)
    started = time.time()
    with report.open("w", encoding="utf-8") as fh:
        result = subprocess.run(steps[2], stdout=fh, stderr=subprocess.STDOUT, timeout=3600)
    text = report.read_text(encoding="utf-8")
    tokens = re.findall(r"tokens used\n([\d,]+)", text)
    commits = subprocess.run(["git", "-C", str(worktree), "log", "--oneline", "origin/main..HEAD"],
                             capture_output=True, text=True).stdout.strip().splitlines()
    log = reports / "log.tsv"
    if not log.exists():
        log.write_text("時間\t卡片\t結束碼\t分鐘\ttokens\tcommits\t分支\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now():%Y-%m-%d %H:%M}\t{cid}\t{result.returncode}\t"
                 f"{(time.time() - started) / 60:.0f}\t{tokens[-1] if tokens else '?'}\t{len(commits)}\t{branch}\n")
    print(f"{cid} 結束碼 {result.returncode}；commits {len(commits)}；回報 {report}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
