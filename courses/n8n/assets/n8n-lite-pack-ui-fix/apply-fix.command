#!/usr/bin/env bash
set -Eeuo pipefail

PATCH_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
KIT_DIR="$(cd -- "$PATCH_DIR/.." && pwd)"
COMPOSE_FILE="$KIT_DIR/n8n-compose.yml"
SHARED_DIR="$KIT_DIR/shared"

if [[ ! -f "$COMPOSE_FILE" || ! -d "$SHARED_DIR" ]]; then
  echo "找不到同層的 n8n-compose.yml / shared。請把 n8n-lite-pack-ui-fix 資料夾放在 n8n-starter-kit 裡。"
  read -r -p "按 Enter 關閉……" _ || true
  exit 1
fi
if ! command -v docker >/dev/null 2>&1; then
  echo "找不到 Docker。請先開啟 Docker Desktop，再重新執行。"
  read -r -p "按 Enter 關閉……" _ || true
  exit 1
fi

cd "$KIT_DIR"
compose() { docker compose -f "$COMPOSE_FILE" "$@"; }

if ! N8N_VERSION="$(compose exec -T n8n n8n --version 2>/dev/null)"; then
  echo "無法連到正在執行的 n8n。請先用 starter-kit 的 start.command 啟動，再執行修補。"
  read -r -p "按 Enter 關閉……" _ || true
  exit 1
fi
if [[ "$N8N_VERSION" != "2.37.7" ]]; then
  echo "此修補包已針對 n8n 2.37.7 驗證；目前版本是：$N8N_VERSION。沒有修改任何 workflow。"
  read -r -p "按 Enter 關閉……" _ || true
  exit 1
fi

echo "此工具只修補 #06 與 #12 的本機 UI，會短暫停止再啟動 n8n。"
read -r -p "確認繼續請輸入 YES；其他輸入會取消：" APPLY_CONFIRM || true
if [[ "$APPLY_CONFIRM" != "YES" ]]; then
  echo "已取消，尚未匯出或修改 workflow。"
  read -r -p "按 Enter 關閉……" _ || true
  exit 0
fi

STAMP="$(date '+%Y%m%d-%H%M%S')-$$"
WORK_DIR="$SHARED_DIR/lite-pack-ui-fix-$STAMP"
CONTAINER_DIR="/files/shared/lite-pack-ui-fix-$STAMP"
mkdir -p "$WORK_DIR/backup" "$WORK_DIR/merged" "$WORK_DIR/package/workflows"
cp "$PATCH_DIR/merge-workflow.cjs" "$WORK_DIR/package/merge-workflow.cjs"
cp "$PATCH_DIR/workflows/06-webhook-gemini-file.json" "$WORK_DIR/package/workflows/06-webhook-gemini-file.json"
cp "$PATCH_DIR/workflows/12-knowledge-rag.json" "$WORK_DIR/package/workflows/12-knowledge-rag.json"

ID06="lite-pack-06-webhook-gemini-file"
ID12="lite-pack-12-knowledge-rag"
ORIG06="$CONTAINER_DIR/backup/06-original.json"
ORIG12="$CONTAINER_DIR/backup/12-original.json"
PUBLISHED06="$CONTAINER_DIR/backup/06-published.json"
PUBLISHED12="$CONTAINER_DIR/backup/12-published.json"
PATCH06="$CONTAINER_DIR/package/workflows/06-webhook-gemini-file.json"
PATCH12="$CONTAINER_DIR/package/workflows/12-knowledge-rag.json"
MERGED06="$CONTAINER_DIR/merged/06-merged.json"
MERGED12="$CONTAINER_DIR/merged/12-merged.json"
VERIFY06="$CONTAINER_DIR/merged/06-verify.json"
VERIFY12="$CONTAINER_DIR/merged/12-verify.json"
MERGER="$CONTAINER_DIR/package/merge-workflow.cjs"
ACTIVE06=""
ACTIVE12=""
IMPORT_STARTED=0
SUCCESS=0

rollback_on_failure() {
  local status=$?
  trap - EXIT
  if [[ "$status" -ne 0 && "$IMPORT_STARTED" -eq 1 && "$SUCCESS" -eq 0 ]]; then
    echo "修補未完成，正在從備份回復 #06/#12……"
    compose stop n8n >/dev/null 2>&1 || true
    compose run -T --rm --no-deps n8n import:workflow --input="$ORIG06" || true
    compose run -T --rm --no-deps n8n import:workflow --input="$ORIG12" || true
    if [[ "$ACTIVE06" == "true" ]]; then compose run -T --rm --no-deps n8n publish:workflow --id="$ID06" || true; fi
    if [[ "$ACTIVE12" == "true" ]]; then compose run -T --rm --no-deps n8n publish:workflow --id="$ID12" || true; fi
    compose start n8n || true
    echo "已嘗試回復。原始備份保留於：$WORK_DIR/backup"
  fi
  exit "$status"
}
trap rollback_on_failure EXIT

echo "正在備份目前 #06 與 #12；其他 workflow 不會被匯出或修改。"
compose exec -T n8n n8n export:workflow --id="$ID06" --output="$ORIG06"
compose exec -T n8n n8n export:workflow --id="$ID12" --output="$ORIG12"
[[ -s "$WORK_DIR/backup/06-original.json" && -s "$WORK_DIR/backup/12-original.json" ]] || { echo "備份不完整，停止，尚未套用修補。"; exit 1; }

ACTIVE06="$(compose exec -T n8n node "$MERGER" --active "$ORIG06")"
ACTIVE12="$(compose exec -T n8n node "$MERGER" --active "$ORIG12")"
[[ "$ACTIVE06" == "true" || "$ACTIVE06" == "false" ]] || { echo "無法辨識 #06 原本的啟用狀態，停止。"; exit 1; }
[[ "$ACTIVE12" == "true" || "$ACTIVE12" == "false" ]] || { echo "無法辨識 #12 原本的啟用狀態，停止。"; exit 1; }
if [[ "$ACTIVE06" == "true" ]]; then
  compose exec -T n8n n8n export:workflow --id="$ID06" --published --output="$PUBLISHED06"
  compose exec -T n8n node "$MERGER" --assert-published "$ORIG06" "$PUBLISHED06"
fi
if [[ "$ACTIVE12" == "true" ]]; then
  compose exec -T n8n n8n export:workflow --id="$ID12" --published --output="$PUBLISHED12"
  compose exec -T n8n node "$MERGER" --assert-published "$ORIG12" "$PUBLISHED12"
fi
compose exec -T n8n node "$MERGER" "$ORIG06" "$PATCH06" "$MERGED06"
compose exec -T n8n node "$MERGER" "$ORIG12" "$PATCH12" "$MERGED12"

echo "備份與差異檢查完成。現在只暫停 n8n 服務；Postgres、volume、shared 檔案會保留。"
IMPORT_STARTED=1
compose stop n8n
compose run -T --rm --no-deps n8n import:workflow --input="$MERGED06"
compose run -T --rm --no-deps n8n import:workflow --input="$MERGED12"
if [[ "$ACTIVE06" == "true" ]]; then compose run -T --rm --no-deps n8n publish:workflow --id="$ID06"; fi
if [[ "$ACTIVE12" == "true" ]]; then compose run -T --rm --no-deps n8n publish:workflow --id="$ID12"; fi
compose start n8n

echo "等待 n8n 重新啟動……"
READY=0
for _ in {1..30}; do
  if compose exec -T n8n n8n --version >/dev/null 2>&1; then READY=1; break; fi
  sleep 2
done
[[ "$READY" -eq 1 ]] || { echo "n8n 未能在 60 秒內回應，將嘗試回復備份。"; exit 1; }
compose exec -T n8n n8n export:workflow --id="$ID06" --output="$VERIFY06"
compose exec -T n8n n8n export:workflow --id="$ID12" --output="$VERIFY12"
compose exec -T n8n node "$MERGER" --verify "$VERIFY06" "$PATCH06"
compose exec -T n8n node "$MERGER" --verify "$VERIFY12" "$PATCH12"

SUCCESS=1
echo "修補完成。備份位置：$WORK_DIR/backup"
echo "請在瀏覽器重新整理 #06 /ai-ui 與 #12 /kb-ui；修補包不會清除其他練習。"
read -r -p "按 Enter 關閉……" _ || true
