#!/bin/bash
# n8n Lite Pack · setup-wizard v1.2.3 (macOS)
# 「下載安裝後設兩個 key 即用」最短路徑
# v0.4：file access patch 自動化 / 自動重啟 / Telegram + Gemini smoke test
# v1.1：Telegram 改為可選（GUI 對話框 Y/N gate）— 不用 TG 的學員零摩擦過關
# v1.2.3：修 Mac/Win 不對齊 — Gemini smoke test 加 thinkingConfig.thinkingBudget=0
#         （Win 版 setup-wizard.ps1:386 早就有，Mac 版這條漏 patch）
#         Gemini 2.5 Flash 預設啟用 thinking，maxOutputTokens=20 會被 thinking 吃光
#         → response candidates[0].content 沒 parts.text → 回 EMPTY → smoke 誤報異常
# 用法：在 Finder 雙擊本檔；首次被 Gatekeeper 擋請去「系統設定 → 隱私權與安全性 → 強制打開」

cd "$(dirname "$0")"
N8N_URL="http://localhost:5678"
WORKFLOW_DIR="$(pwd)/workflows"
CRED_FILE="/tmp/lite-pack-credentials-$$.json"
WORKFLOW_TMP="/tmp/lite-pack-workflows-$$"
LOG="/tmp/n8n-lite-setup-$$.log"
exec > >(tee -a "$LOG") 2>&1

echo "═════════════════════════════════════════════════════════════"
echo "  n8n Lite Pack · setup-wizard v1.1"
echo "  log: $LOG"
echo "═════════════════════════════════════════════════════════════"

# ═════════ Step 1: 環境檢查 + 偵測 starter-kit 路徑 ═════════
echo ""
echo "[1/10] 環境檢查..."

if ! command -v docker >/dev/null 2>&1; then
  osascript -e 'display dialog "找不到 docker 指令。\n\n請先依課程 1.1 安裝 Docker Desktop 並雙擊 start.command 啟動 n8n。" buttons {"知道了"} default button 1 with icon stop'
  exit 1
fi

if ! curl -sf "$N8N_URL/healthz" >/dev/null 2>&1; then
  osascript -e 'display dialog "n8n 沒有跑在 localhost:5678。\n\n請先到 ~/Downloads/n8n-starter-kit/ 雙擊 start.command 啟動 n8n。" buttons {"知道了"} default button 1 with icon stop'
  exit 1
fi

N8N_CONTAINER=$(docker ps --filter "name=n8n" --format "{{.Names}}" | grep -E "n8n-[0-9]+$" | head -1)
if [ -z "$N8N_CONTAINER" ]; then
  osascript -e 'display dialog "找不到 n8n container。請確認 start.command 已啟動。" buttons {"知道了"} default button 1 with icon stop'
  exit 1
fi
echo "  ✓ n8n container: $N8N_CONTAINER"

# 偵測 starter-kit 資料夾位置（含 n8n-compose.yml）
STARTER_KIT=""
for path in "$HOME/Downloads/n8n-starter-kit" "$HOME/Desktop/n8n-starter-kit" "$HOME/n8n-starter-kit"; do
  if [ -f "$path/n8n-compose.yml" ]; then STARTER_KIT="$path"; break; fi
done

if [ -z "$STARTER_KIT" ]; then
  STARTER_KIT=$(osascript -e 'text returned of (display dialog "找不到 n8n-starter-kit 資料夾（含 n8n-compose.yml）。\n\n請貼上完整路徑：" default answer "~/Downloads/n8n-starter-kit")' 2>/dev/null)
  STARTER_KIT="${STARTER_KIT/#\~/$HOME}"
  if [ ! -f "$STARTER_KIT/n8n-compose.yml" ]; then
    osascript -e 'display dialog "該路徑沒有 n8n-compose.yml。setup-wizard 中止。" buttons {"知道了"} default button 1 with icon stop'
    exit 1
  fi
fi
echo "  ✓ starter-kit: $STARTER_KIT"

if [ ! -d "$WORKFLOW_DIR" ]; then
  osascript -e 'display dialog "找不到 workflows 資料夾。試跑包不完整，請重新下載。" buttons {"知道了"} default button 1 with icon stop'
  exit 1
fi
echo "  ✓ workflows 資料夾就緒"

# ═════════ Step 2: 收集學員資料 ═════════
echo ""
echo "[2/10] 收集學員 personalization 資料..."

GEMINI_KEY=$(osascript -e 'text returned of (display dialog "請貼上你的 Gemini API key（AIza... 開頭那串）\n\n沒有？到 https://aistudio.google.com/apikey 申請（免費）。" default answer "" with hidden answer)' 2>/dev/null) || exit 1
if [[ ! "$GEMINI_KEY" =~ ^AIza ]]; then
  osascript -e 'display dialog "Gemini API key 格式不對（應以 AIza 開頭）。" buttons {"知道了"} default button 1 with icon stop'
  exit 1
fi

# Telegram 改成可選（v1.1）— GUI 對話框 Y/N gate
TG_CHOICE=$(osascript -e 'set theChoice to button returned of (display dialog "要用 Telegram 接收 workflow 通知嗎？\n\n• 用 Telegram：要先有 BotFather token + chat ID（5-10 分鐘設定）\n• 略過：只要 Gemini key 就能跑非 TG 的 6 個 workflow（01-04 / 08 / 12）\n\n隨時可重跑 wizard 補 Telegram 設定。" buttons {"略過（預設）", "用 Telegram"} default button 1)' 2>/dev/null) || exit 1
USE_TELEGRAM=false
TG_TOKEN=""
TG_CHAT_ID=""

if [[ "$TG_CHOICE" == "用 Telegram" ]]; then
  USE_TELEGRAM=true
  TG_TOKEN=$(osascript -e 'text returned of (display dialog "請貼上你的 Telegram bot token（格式如 123456:ABC-DEF...）\n\n沒有？到 Telegram 找 @BotFather → /newbot → 拿 token。" default answer "" with hidden answer)' 2>/dev/null) || exit 1
  if [[ ! "$TG_TOKEN" =~ ^[0-9]+: ]]; then
    osascript -e 'display dialog "Telegram bot token 格式不對。" buttons {"知道了"} default button 1 with icon stop'
    exit 1
  fi

  TG_CHAT_ID=$(osascript -e 'text returned of (display dialog "請貼上你的 Telegram Chat ID（一串數字）\n\n找方法：對你的 bot 發任意訊息後，瀏覽器開：\nhttps://api.telegram.org/bot你的TOKEN/getUpdates\n找 chat.id 那串數字。" default answer "")' 2>/dev/null) || exit 1
  if [[ ! "$TG_CHAT_ID" =~ ^-?[0-9]+$ ]]; then
    osascript -e 'display dialog "Chat ID 應該是純數字。" buttons {"知道了"} default button 1 with icon stop'
    exit 1
  fi
  echo "  ✓ 3 個 personalization 資料收齊（Gemini + Telegram）"
else
  echo "  ↳ 跳過 Telegram。8 個用 TG 的 workflow（05/06/07/09/10/11/13/14）匯入後仍是 inactive，要用再去 n8n UI 補 credential。"
  echo "  ✓ 1 個 personalization 資料收齊（Gemini）"
fi

# ═════════ Step 3: file access patch + 重啟 n8n ═════════
echo ""
echo "[3/10] 偵測並 patch file access 環境變數..."

COMPOSE="$STARTER_KIT/n8n-compose.yml"
if grep -q "N8N_RESTRICT_FILE_ACCESS_TO" "$COMPOSE"; then
  echo "  ✓ compose.yml 已含 file access patch（跳過）"
  RESTART_NEEDED=false
else
  # 備份
  cp "$COMPOSE" "$COMPOSE.bak-$(date +%Y%m%d%H%M%S)"
  echo "  ✓ 已備份 compose.yml"

  # awk 在 N8N_BASIC_AUTH_ACTIVE 那行下面插入兩行環境變數
  awk '/N8N_BASIC_AUTH_ACTIVE=false/{print; print "      - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared"; print "      - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false"; next}1' "$COMPOSE" > "$COMPOSE.new"

  if grep -q "N8N_RESTRICT_FILE_ACCESS_TO" "$COMPOSE.new"; then
    mv "$COMPOSE.new" "$COMPOSE"
    echo "  ✓ patch 完成（加入 N8N_RESTRICT_FILE_ACCESS_TO + N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES）"
    RESTART_NEEDED=true
  else
    rm -f "$COMPOSE.new"
    osascript -e 'display dialog "compose.yml patch 失敗（找不到 N8N_BASIC_AUTH_ACTIVE 那行）。\n\n請手動編輯 compose.yml 加入：\n  - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared\n  - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false\n\n然後重新跑本 wizard。" buttons {"知道了"} default button 1 with icon stop'
    exit 1
  fi
fi

if [ "$RESTART_NEEDED" = "true" ]; then
  echo "  ⏳ 重啟 n8n container（讀新環境變數）..."
  cd "$STARTER_KIT"
  docker compose -f n8n-compose.yml down 2>&1 | tail -3
  docker compose -f n8n-compose.yml up -d 2>&1 | tail -3
  cd "$(dirname "$0")"

  # 等 n8n 就緒
  echo -n "  ⏳ 等 n8n 就緒"
  for i in {1..40}; do
    if curl -sf "$N8N_URL/healthz" >/dev/null 2>&1; then
      echo " ✓"
      break
    fi
    echo -n "."
    sleep 2
  done

  # 重新取得 container 名（重啟後可能略有差異）
  N8N_CONTAINER=$(docker ps --filter "name=n8n" --format "{{.Names}}" | grep -E "n8n-[0-9]+$" | head -1)
  echo "  ✓ n8n 重啟完成（container: $N8N_CONTAINER）"
fi

# ═════════ Step 4: 寫 personalization.env ═════════
echo ""
echo "[4/10] 寫入 personalization.env..."

{
  echo "# n8n Lite Pack 個人化設定（setup-wizard v1.1 自動產生 $(date '+%Y-%m-%d %H:%M:%S'))"
  echo "# 不要 commit 到 git！"
  echo "GEMINI_API_KEY=$GEMINI_KEY"
  if [ "$USE_TELEGRAM" = "true" ]; then
    echo "TELEGRAM_BOT_TOKEN=$TG_TOKEN"
    echo "TELEGRAM_CHAT_ID=$TG_CHAT_ID"
  fi
} > personalization.env
chmod 600 personalization.env
echo "  ✓ personalization.env 寫入完成"

# ═════════ Step 5: 建 sample 資料夾 ═════════
echo ""
echo "[5/10] 建 sample 資料夾..."

SHARED="$STARTER_KIT/shared"
# v1.1：完整 24 個 shared 子資料夾（與 Win 版同步）+ #10 客戶分類 6 個子夾預建
for sub in \
  pdf-inbox pdf-renamed \
  batch-inbox batch-inbox/processed batch-inbox/failed \
  daily-input daily-output ai-output \
  client-inbox \
  client-organized \
  client-organized/contracts client-organized/invoices client-organized/presentations \
  client-organized/images client-organized/docs client-organized/others \
  leads-inbox leads-output \
  knowledge-docs knowledge-index \
  ops-input ops-history ops-snapshots ops-incidents; do
  mkdir -p "$SHARED/$sub"
done
echo "  ✓ 24 個 shared/ 子資料夾建好（含 #10 客戶分類 6 個子夾，位於 $SHARED）"

# ═════════ Step 6: 生成 credentials JSON（含 id 欄位）═════════
echo ""
echo "[6/10] 生成 decrypted credentials JSON..."

if [ "$USE_TELEGRAM" = "true" ]; then
  python3 - <<EOF > "$CRED_FILE"
import json
creds = [
    {
        "id": "lite-pack-gemini",
        "name": "Lite Pack · Gemini API",
        "type": "httpHeaderAuth",
        "data": {"name": "x-goog-api-key", "value": "$GEMINI_KEY"}
    },
    {
        "id": "lite-pack-telegram",
        "name": "Lite Pack · Telegram Bot",
        "type": "telegramApi",
        "data": {"accessToken": "$TG_TOKEN", "baseUrl": "https://api.telegram.org"}
    }
]
print(json.dumps(creds, indent=2, ensure_ascii=False))
EOF
else
  python3 - <<EOF > "$CRED_FILE"
import json
creds = [
    {
        "id": "lite-pack-gemini",
        "name": "Lite Pack · Gemini API",
        "type": "httpHeaderAuth",
        "data": {"name": "x-goog-api-key", "value": "$GEMINI_KEY"}
    }
]
print(json.dumps(creds, indent=2, ensure_ascii=False))
EOF
fi

if [ ! -s "$CRED_FILE" ]; then
  osascript -e "display dialog \"credentials JSON 生成失敗。log: $LOG\" buttons {\"知道了\"} default button 1 with icon stop"
  exit 1
fi
echo "  ✓ credentials JSON 生成"

# ═════════ Step 7: 替換 workflow JSON placeholder ═════════
echo ""
echo "[7/10] 替換 workflow JSON 內 __TELEGRAM_CHAT_ID__ placeholder..."

rm -rf "$WORKFLOW_TMP"
cp -r "$WORKFLOW_DIR" "$WORKFLOW_TMP"

python3 - <<EOF
import os
tmp = "$WORKFLOW_TMP"
chat_id = "$TG_CHAT_ID"
gemini_key = "$GEMINI_KEY"
tg_token = "$TG_TOKEN"
use_tg = "$USE_TELEGRAM" == "true"
for fname in os.listdir(tmp):
    if not fname.endswith('.json'): continue
    fpath = os.path.join(tmp, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace('__GEMINI_API_KEY__', gemini_key)
    if use_tg:
        new_content = new_content.replace('__TELEGRAM_CHAT_ID__', chat_id).replace('__TELEGRAM_BOT_TOKEN__', tg_token)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {fname} 已替換 placeholders")
EOF

# ═════════ Step 8: 匯入 credentials ═════════
echo ""
echo "[8/10] 匯入 credentials 到 n8n..."

CRED_LABEL=$([ "$USE_TELEGRAM" = "true" ] && echo "2 個 credentials（Gemini + Telegram）" || echo "1 個 credential（Gemini）")
docker cp "$CRED_FILE" "$N8N_CONTAINER:/tmp/lite-pack-cred.json"
if docker exec -u node "$N8N_CONTAINER" n8n import:credentials --input=/tmp/lite-pack-cred.json 2>&1 | tee -a "$LOG"; then
  echo "  ✓ $CRED_LABEL 匯入完成"
else
  osascript -e "display dialog \"credentials 匯入失敗。log: $LOG\n\n常見原因：n8n 沒建 owner account。先到 http://localhost:5678 完成 owner setup。\" buttons {\"知道了\"} default button 1 with icon stop"
  exit 1
fi

# ═════════ Step 9: 匯入 8 個 workflows ═════════
echo ""
echo "[9/10] 匯入 8 個 workflows..."

docker exec "$N8N_CONTAINER" rm -rf /tmp/lite-pack-workflows 2>/dev/null
docker cp "$WORKFLOW_TMP" "$N8N_CONTAINER:/tmp/lite-pack-workflows"

WF_OK=0; WF_FAIL=0
for json in "$WORKFLOW_TMP"/*.json; do
  [ -e "$json" ] || continue
  name=$(basename "$json")
  if docker exec -u node "$N8N_CONTAINER" n8n import:workflow --input="/tmp/lite-pack-workflows/$name" 2>&1 | tee -a "$LOG" | grep -q "Successfully imported"; then
    WF_OK=$((WF_OK+1)); echo "  ✓ $name"
  else
    WF_FAIL=$((WF_FAIL+1)); echo "  ✗ $name"
  fi
done

# ═════════ Step 10: Smoke tests ═════════
echo ""
echo "[10/10] 跑 smoke tests..."

# Telegram smoke test (v1.1：跳過 if 不用 TG)
if [ "$USE_TELEGRAM" = "true" ]; then
  echo "  · Telegram bot..."
  TG_TEST=$(curl -sf -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" -H "Content-Type: application/json" -d "{\"chat_id\":\"${TG_CHAT_ID}\",\"text\":\"✅ Lite Pack v1.1 setup-wizard 安裝完成！\"}" 2>&1)
  if echo "$TG_TEST" | grep -q '"ok":true'; then
    echo "    ✓ Telegram 收到測試訊息"
    TG_OK=true
  else
    echo "    ✗ Telegram 失敗：$TG_TEST"
    TG_OK=false
  fi
else
  echo "  · Telegram bot 跳過（你選不用 TG）"
  TG_OK=skip
fi

# Gemini smoke test（簡單 prompt 看 API 是否真能 work）
echo "  · Gemini API（最小 prompt）..."
GEMINI_TEST=$(curl -sf -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" -H "Content-Type: application/json" -H "x-goog-api-key: ${GEMINI_KEY}" -d '{"contents":[{"parts":[{"text":"Reply exactly: OK"}]}],"generationConfig":{"temperature":0.1,"maxOutputTokens":20,"thinkingConfig":{"thinkingBudget":0}}}' 2>&1)
GEMINI_REPLY=$(echo "$GEMINI_TEST" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('candidates',[{}])[0].get('content',{}).get('parts',[{}])[0].get('text','EMPTY'))" 2>/dev/null || echo "PARSE_ERROR")
echo "    Gemini 回應：$GEMINI_REPLY"
if [[ "$GEMINI_REPLY" == *"OK"* ]]; then
  echo "    ✓ Gemini API 正常"
  GEMINI_OK=true
else
  echo "    ⚠️ Gemini 回應異常（不是 OK）"
  echo "$GEMINI_TEST" > /tmp/gemini-diagnostic.json
  echo "    完整 response 已存到 /tmp/gemini-diagnostic.json 供診斷"
  GEMINI_OK=false
fi

# 清理暫存
rm -f "$CRED_FILE"
rm -rf "$WORKFLOW_TMP"
docker exec "$N8N_CONTAINER" rm -f /tmp/lite-pack-cred.json 2>/dev/null
docker exec "$N8N_CONTAINER" rm -rf /tmp/lite-pack-workflows 2>/dev/null

# ═════════ 結果回報 ═════════
echo ""
echo "═════════════════════════════════════════════════════════════"
echo "  完成回報"
echo "═════════════════════════════════════════════════════════════"
CRED_COUNT_LABEL=$([ "$USE_TELEGRAM" = "true" ] && echo "2 個（Gemini + Telegram）" || echo "1 個（Gemini）")
TG_REPORT_LABEL=$([ "$TG_OK" = "skip" ] && echo "↳ 跳過（你選不用 TG）" || ([ "$TG_OK" = "true" ] && echo "✅ 收到訊息" || echo "❌ 失敗"))
NEXT_STEP_LABEL=$([ "$USE_TELEGRAM" = "true" ] && echo "從 #5 Telegram 通知開始驗證。" || echo "從不用 TG 的 6 個 workflow（01-04 / 08 / 12）開始試。想用 Telegram 重跑本 wizard 即可。")

echo "  Credentials  ：$CRED_COUNT_LABEL"
echo "  Workflows    ：成功 $WF_OK / 失敗 $WF_FAIL"
echo "  File access  ：已 patch /files/shared 白名單"
echo "  Telegram test：$TG_REPORT_LABEL"
echo "  Gemini test  ：$([ "$GEMINI_OK" = "true" ] && echo "✅ API 正常" || echo "⚠️ 回應異常（看 /tmp/gemini-diagnostic.json）")"
echo "  Container    ：$N8N_CONTAINER"
echo "  Log          ：$LOG"
echo "═════════════════════════════════════════════════════════════"

# GUI 結果對話框
SUMMARY="✅ Lite Pack v1.1 安裝完成！

• $CRED_COUNT_LABEL credentials 已建立並加密儲存
• $WF_OK 個 workflows 已匯入並自動關聯 credentials
• File access 環境變數已 patch（/files/shared 可讀寫）
• Telegram 測試：$TG_REPORT_LABEL
• Gemini 測試：$([ "$GEMINI_OK" = "true" ] && echo "✅ 正常" || echo "⚠️ 回應異常")

下一步：打開 n8n 看左側 Workflows 清單，$NEXT_STEP_LABEL"

# v1.1：TG_OK=skip 也算通過（學員選擇不用 TG 不是失敗）
TG_PASS=true
if [ "$USE_TELEGRAM" = "true" ] && [ "$TG_OK" != "true" ]; then
  TG_PASS=false
fi

if [ $WF_FAIL -eq 0 ] && [ "$TG_PASS" = "true" ] && [ "$GEMINI_OK" = "true" ]; then
  osascript -e "display dialog \"$SUMMARY\" buttons {\"打開 n8n\"} default button 1"
  open "$N8N_URL"
else
  osascript -e "display dialog \"⚠️ 部分項目未通過：

$SUMMARY

打開 log 查看細節：
$LOG\" buttons {\"打開 log\", \"打開 n8n\"} default button 2 with icon caution"
  open "$N8N_URL"
fi

echo ""
echo "log 已保存到：$LOG"
