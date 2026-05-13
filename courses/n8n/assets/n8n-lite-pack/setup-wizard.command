#!/bin/bash
# n8n Lite Pack · setup-wizard v1.3 (macOS)
# 「下載安裝後設兩個 key 即用」最短路徑
# v0.4：file access patch 自動化 / 自動重啟 / Telegram + Gemini smoke test
# v1.1：Telegram 改為可選（GUI 對話框 Y/N gate）— 不用 TG 的學員零摩擦過關
# v1.2.3：修 Mac/Win 不對齊 — Gemini smoke test 加 thinkingConfig.thinkingBudget=0
# v1.2.4：#14 endpoints 解析 robust
# v1.3：⚠ 安全修補 — Gemini key 改走 $env.GEMINI_API_KEY 路徑（不再字串替換 jsCode）
#       原機制：把 __GEMINI_API_KEY__ 替換成真 key 寫進 workflow JSON → 學員匯出 JSON 會洩漏
#       新機制：寫到 starter-kit/.env 的 GEMINI_API_KEY 環境變數 → n8n Code node 透過 $env 讀
#       需要 n8n-compose.yml 含 N8N_BLOCK_ENV_ACCESS_IN_NODE=false（本 wizard 會自動 patch）
#       偵測到舊版安裝（personalization.env 殘留）會跳警告，提醒撤銷舊 key
# 用法：在 Finder 雙擊本檔；首次被 Gatekeeper 擋請去「系統設定 → 隱私權與安全性 → 強制打開」

cd "$(dirname "$0")"
N8N_URL="http://localhost:5678"
WORKFLOW_DIR="$(pwd)/workflows"
CRED_FILE="/tmp/lite-pack-credentials-$$.json"
WORKFLOW_TMP="/tmp/lite-pack-workflows-$$"
LOG="/tmp/n8n-lite-setup-$$.log"
exec > >(tee -a "$LOG") 2>&1

echo "═════════════════════════════════════════════════════════════"
echo "  n8n Lite Pack · setup-wizard v1.3"
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

# ═════════ Step 3: 偵測舊版安裝 + patch compose.yml（file access + env access + key pass-through）═════════
echo ""
echo "[3/10] 偵測舊版安裝 + patch compose.yml 環境變數..."

COMPOSE="$STARTER_KIT/n8n-compose.yml"

# v1.3: 偵測舊版 — 兩種 marker：
#   A. personalization.env 殘留（舊 wizard 寫入的 memo 檔）
#   B. starter-kit/.env 內既有 GEMINI_API_KEY=AIzaSy... 真實值（舊 wizard 已替換過 workflow JSON 的證據）
OLD_INSTALL_MARKER="$(dirname "$0")/personalization.env"
OLD_ENV_HAS_KEY=false
if [ -f "$STARTER_KIT/.env" ] && grep -qE '^\s*GEMINI_API_KEY\s*=\s*"?AIzaSy' "$STARTER_KIT/.env"; then
  OLD_ENV_HAS_KEY=true
fi

if [ -f "$OLD_INSTALL_MARKER" ] || [ "$OLD_ENV_HAS_KEY" = "true" ]; then
  osascript -e 'display dialog "⚠ 偵測到舊版 wizard 安裝過

舊版（v1.2 之前）會把你的 Gemini API key 字串替換進 workflow JSON。
你以前從 n8n UI 匯出（Download）過的任何 workflow JSON 都可能含真 key 明文。

強烈建議：
1. 立刻到 https://aistudio.google.com/apikey 撤銷（Delete）舊 key
2. 重新申請一把新 key
3. 繼續本 wizard，新機制（環境變數）會把新 key 寫進 starter-kit/.env
   workflow JSON 不再含 key，匯出也不會洩漏

點「我懂了，繼續」就會繼續安裝新版本。" buttons {"取消", "我懂了，繼續"} default button 2 with icon caution' >/dev/null || exit 1
  if [ -f "$OLD_INSTALL_MARKER" ]; then
    mv "$OLD_INSTALL_MARKER" "$OLD_INSTALL_MARKER.migrated-$(date +%Y%m%d%H%M%S)"
    echo "  ⚠ 舊版 marker (personalization.env) 已重新命名"
  fi
  if [ "$OLD_ENV_HAS_KEY" = "true" ]; then
    echo "  ⚠ 偵測到 .env 已含 AIzaSy 開頭真實 key — 舊 wizard 寫過。新 key 會覆蓋此值"
  fi
fi

# 備份 compose
COMPOSE_BAK="$COMPOSE.bak-$(date +%Y%m%d%H%M%S)"
cp "$COMPOSE" "$COMPOSE_BAK"
echo "  ✓ 已備份 compose.yml → $(basename "$COMPOSE_BAK")"

# 用 Python 統一 patch 4 個必要 env vars（idempotent）
# Codex 建議：missing 判斷用 `^\s*-\s*KEY=` line-anchored（避免被註解誤導），且支援 CRLF
RESTART_NEEDED=false
export COMPOSE
COMPOSE_PATCHED=$(python3 - <<'PY'
import re, sys, os
compose = os.environ['COMPOSE']
with open(compose, 'r', encoding='utf-8') as f:
    txt = f.read()

# 目標 env vars（key → 完整 yaml 行 stub）
required = [
    ('N8N_RESTRICT_FILE_ACCESS_TO',     '      - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared'),
    ('N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES','      - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false'),
    ('N8N_BLOCK_ENV_ACCESS_IN_NODE',    '      - N8N_BLOCK_ENV_ACCESS_IN_NODE=false'),
    ('GEMINI_API_KEY',                  '      - GEMINI_API_KEY=${GEMINI_API_KEY:-}'),
]

def has_env(key, source):
    # 只匹配實際 environment item（- KEY=...）；註解 # ... KEY 不算
    return re.search(rf'(?m)^\s*-\s*{re.escape(key)}=', source) is not None

missing = [(k, line) for k, line in required if not has_env(k, txt)]
if not missing:
    print('SKIP')
    sys.exit(0)

# 找 n8n service 的 environment: 區段；在最後一個既有 env 行後追加（支援 CRLF）
m = re.search(r'^(  n8n:\r?\n(?:.*\r?\n)*?    environment:\r?\n((?:      - [^\r\n]+\r?\n)+))', txt, re.MULTILINE)
if not m:
    print('FAIL', file=sys.stderr)
    sys.exit(1)
prefix = m.group(0)
# 偵測既有 line ending（保持一致）
sep = '\r\n' if '\r\n' in prefix else '\n'
inject = ''.join(line + sep for _, line in missing)
new_txt = txt.replace(prefix, prefix + inject, 1)
with open(compose, 'w', encoding='utf-8') as f:
    f.write(new_txt)
print('PATCHED:' + ','.join(k for k, _ in missing))
PY
) || { osascript -e 'display dialog "compose.yml patch 失敗。請手動編輯 compose.yml 在 n8n service 的 environment: 區段加入：\n\n  - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared\n  - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false\n  - N8N_BLOCK_ENV_ACCESS_IN_NODE=false\n  - GEMINI_API_KEY=${GEMINI_API_KEY:-}\n\n然後重新跑本 wizard。" buttons {"知道了"} default button 1 with icon stop'; exit 1; }
COMPOSE="$STARTER_KIT/n8n-compose.yml"  # restore COMPOSE var after subshell heredoc

if [[ "$COMPOSE_PATCHED" == "SKIP" ]]; then
  echo "  ✓ compose.yml 4 個必要 env vars 都齊（跳過 patch）"
elif [[ "$COMPOSE_PATCHED" == PATCHED:* ]]; then
  echo "  ✓ compose.yml 已加入：${COMPOSE_PATCHED#PATCHED:}"
  RESTART_NEEDED=true
fi

# ═════════ Step 4: 寫/合併 starter-kit/.env（GEMINI_API_KEY；idempotent）═════════
echo ""
echo "[4/10] 合併 GEMINI_API_KEY 到 starter-kit/.env..."

ENV_FILE="$STARTER_KIT/.env"
if [ ! -f "$ENV_FILE" ]; then
  # 沒 .env → 從 .env.example 複製（與 start.command 一致）
  if [ -f "$STARTER_KIT/.env.example" ]; then
    cp "$STARTER_KIT/.env.example" "$ENV_FILE"
    echo "  ↳ 從 .env.example 建立 .env"
  else
    echo "" > "$ENV_FILE"
    echo "  ↳ 建立空 .env"
  fi
fi

# 先備份 .env
cp "$ENV_FILE" "$ENV_FILE.bak-$(date +%Y%m%d%H%M%S)"

# 用 Python 做 idempotent merge（特別處理含 $ / " / \ 等特殊字元的 dotenv quote）
export ENV_FILE GEMINI_KEY
ENV_RESULT=$(python3 - <<'PY'
import os
env_file = os.environ['ENV_FILE']
gemini_key = os.environ['GEMINI_KEY']

def dotenv_quote(v):
    # 包雙引號，跳脫 \ 與 " 與 $（避免 compose / docker 把 $X 當變數展開）
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$') + '"'

with open(env_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_line = f'GEMINI_API_KEY={dotenv_quote(gemini_key)}\n'
out = []
replaced = False
for line in lines:
    stripped = line.lstrip()
    # 跳過註解；偵測非註解 GEMINI_API_KEY= 行就替換
    if not stripped.startswith('#') and stripped.startswith('GEMINI_API_KEY='):
        out.append(new_line)
        replaced = True
    else:
        out.append(line)

if not replaced:
    # ensure trailing newline
    if out and not out[-1].endswith('\n'):
        out[-1] += '\n'
    out.append('\n# ---- Gemini API key（setup-wizard v1.3 自動寫入）----\n')
    out.append(new_line)

with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(out)
print('replaced' if replaced else 'appended')
PY
) || { osascript -e 'display dialog ".env 寫入失敗。" buttons {"知道了"} default button 1 with icon stop'; exit 1; }
chmod 600 "$ENV_FILE"
echo "  ✓ GEMINI_API_KEY $ENV_RESULT 到 $ENV_FILE（chmod 600）"

# Telegram secret 也寫進 starter-kit/.env（若選用）→ 將來教材若改 TG 走 $env 也已就位
if [ "$USE_TELEGRAM" = "true" ]; then
  export TG_TOKEN TG_CHAT_ID
  python3 - <<'PY'
import os
env_file = os.environ['ENV_FILE']
tg_token = os.environ['TG_TOKEN']
tg_chat = os.environ['TG_CHAT_ID']

def dotenv_quote(v):
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$') + '"'

with open(env_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = {
    'TELEGRAM_BOT_TOKEN': dotenv_quote(tg_token),
    'TELEGRAM_CHAT_ID':   dotenv_quote(tg_chat),
}
seen = set()
out = []
for line in lines:
    stripped = line.lstrip()
    handled = False
    for k, v in targets.items():
        if not stripped.startswith('#') and stripped.startswith(k + '='):
            out.append(f'{k}={v}\n')
            seen.add(k)
            handled = True
            break
    if not handled:
        out.append(line)
for k, v in targets.items():
    if k not in seen:
        if out and not out[-1].endswith('\n'):
            out[-1] += '\n'
        out.append(f'{k}={v}\n')
with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(out)
PY
  echo "  ✓ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 也已寫入（作為未來 $env 路徑備用）"
fi

# Step 4.5: 重啟 n8n（讀 compose patch + .env 的 GEMINI_API_KEY）
if [ "$RESTART_NEEDED" = "true" ] || [ "$ENV_RESULT" = "appended" ] || [ "$ENV_RESULT" = "replaced" ]; then
  echo "  ⏳ 重啟 n8n container（讀新環境變數）..."
  cd "$STARTER_KIT"
  docker compose -f n8n-compose.yml down 2>&1 | tail -3
  docker compose -f n8n-compose.yml up -d 2>&1 | tail -3
  cd "$(dirname "$0")"

  echo -n "  ⏳ 等 n8n 就緒"
  for i in {1..40}; do
    if curl -sf "$N8N_URL/healthz" >/dev/null 2>&1; then
      echo " ✓"
      break
    fi
    echo -n "."
    sleep 2
  done

  N8N_CONTAINER=$(docker ps --filter "name=n8n" --format "{{.Names}}" | grep -E "n8n-[0-9]+$" | head -1)
  echo "  ✓ n8n 重啟完成（container: $N8N_CONTAINER）"
fi

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

# Codex 建議：用 quoted heredoc + os.environ 取值（避免 token 含特殊字元破 heredoc 或 JSON 形變）
export GEMINI_KEY TG_TOKEN USE_TELEGRAM
python3 - > "$CRED_FILE" <<'PY'
import json, os
gemini = os.environ['GEMINI_KEY']
use_tg = os.environ.get('USE_TELEGRAM') == 'true'
creds = [{
    'id': 'lite-pack-gemini',
    'name': 'Lite Pack · Gemini API',
    'type': 'httpHeaderAuth',
    'data': {'name': 'x-goog-api-key', 'value': gemini}
}]
if use_tg:
    creds.append({
        'id': 'lite-pack-telegram',
        'name': 'Lite Pack · Telegram Bot',
        'type': 'telegramApi',
        'data': {'accessToken': os.environ['TG_TOKEN'], 'baseUrl': 'https://api.telegram.org'}
    })
print(json.dumps(creds, indent=2, ensure_ascii=False))
PY

if [ ! -s "$CRED_FILE" ]; then
  osascript -e "display dialog \"credentials JSON 生成失敗。log: $LOG\" buttons {\"知道了\"} default button 1 with icon stop"
  exit 1
fi
echo "  ✓ credentials JSON 生成"

# ═════════ Step 7: workflow JSON 處理（v1.3：sanity scan + 只替換 Telegram placeholder，不再碰 Gemini）═════════
echo ""
echo "[7/10] sanity scan + 替換 __TELEGRAM_* placeholder..."

rm -rf "$WORKFLOW_TMP"
cp -r "$WORKFLOW_DIR" "$WORKFLOW_TMP"

# Step 7a: sanity scan — 模板絕對不該含真實 API key 字串（防下載到被污染版本）
export WORKFLOW_TMP
SCAN_RESULT=$(python3 - <<'PY'
import os, re, sys
tmp = os.environ['WORKFLOW_TMP']
# 多種常見 key prefix 偵測
patterns = [
    (re.compile(r'AIzaSy[A-Za-z0-9_-]{30,}'),                 'Google API key (AIzaSy...)'),
    (re.compile(r'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}'),     'OpenAI/Anthropic key (sk-...)'),
    (re.compile(r'hf_[A-Za-z0-9]{30,}'),                      'Hugging Face token (hf_...)'),
    (re.compile(r'ghp_[A-Za-z0-9]{30,}'),                     'GitHub PAT (ghp_...)'),
    (re.compile(r'github_pat_[A-Za-z0-9_]{50,}'),             'GitHub fine-grained PAT'),
    (re.compile(r'xox[baprs]-[A-Za-z0-9-]{20,}'),             'Slack token (xox*-)'),
    (re.compile(r'(?<![\d:])\d{8,10}:[A-Za-z0-9_-]{35}\b'),   'Telegram bot token (digits:35chars)'),
]
hits = []
for fname in sorted(os.listdir(tmp)):
    if not fname.endswith('.json'): continue
    with open(os.path.join(tmp, fname), 'r', encoding='utf-8') as f:
        content = f.read()
    for pat, label in patterns:
        for m in pat.finditer(content):
            hits.append(f'  ✗ {fname}: {label} → {m.group()[:12]}...')
if hits:
    print('LEAK')
    for h in hits: print(h)
    sys.exit(1)
print('CLEAN')
PY
)
if [[ "$SCAN_RESULT" != CLEAN* ]]; then
  echo "$SCAN_RESULT"
  osascript -e "display dialog \"⚠ 偵測到 workflow 模板含真實 API key 字串！\n\n你下載到的可能是被污染的版本（不該含真 key）。\nsetup-wizard 中止以避免進一步散播。\n\n請：\n1. 刪除整個 n8n-lite-pack 資料夾\n2. 重新下載最新版本\n3. 立刻撤銷該 key（看 log: $LOG）\" buttons {\"知道了\"} default button 1 with icon stop"
  exit 1
fi
echo "  ✓ 模板 sanity scan 通過（無真實 key 字串殘留）"

# Step 7b: 只替換 __TELEGRAM_CHAT_ID__（非 secret，公開）
# Gemini key 走 $env.GEMINI_API_KEY；Telegram bot token 走 n8n credential（lite-pack-telegram），workflow JSON 不含
if [ "$USE_TELEGRAM" = "true" ]; then
  export WORKFLOW_TMP TG_CHAT_ID
  python3 - <<'PY'
import os
tmp = os.environ['WORKFLOW_TMP']
chat_id = os.environ['TG_CHAT_ID']
for fname in sorted(os.listdir(tmp)):
    if not fname.endswith('.json'): continue
    fpath = os.path.join(tmp, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace('__TELEGRAM_CHAT_ID__', chat_id)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {fname} 已替換 __TELEGRAM_CHAT_ID__")
PY
else
  echo "  ↳ 未啟用 Telegram，跳過 chat_id 替換"
fi

# Step 7c: 替換後再掃一次（Codex 建議：第二道防線，防替換邏輯本身漏洞 / 未來新增 secret placeholder 時抓不到）
SCAN2=$(python3 - <<'PY'
import os, re, sys
tmp = os.environ['WORKFLOW_TMP']
patterns = [
    (re.compile(r'AIzaSy[A-Za-z0-9_-]{30,}'),                 'Google API key'),
    (re.compile(r'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}'),     'OpenAI/Anthropic key'),
    (re.compile(r'hf_[A-Za-z0-9]{30,}'),                      'Hugging Face token'),
    (re.compile(r'ghp_[A-Za-z0-9]{30,}'),                     'GitHub PAT'),
    (re.compile(r'github_pat_[A-Za-z0-9_]{50,}'),             'GitHub fine-grained PAT'),
    (re.compile(r'xox[baprs]-[A-Za-z0-9-]{20,}'),             'Slack token'),
    (re.compile(r'(?<![\d:])\d{8,10}:[A-Za-z0-9_-]{35}\b'),   'Telegram bot token'),
]
hits = []
for fname in sorted(os.listdir(tmp)):
    if not fname.endswith('.json'): continue
    with open(os.path.join(tmp, fname), 'r', encoding='utf-8') as f:
        c = f.read()
    for pat, label in patterns:
        for m in pat.finditer(c):
            hits.append(f'  ✗ {fname}: {label} → {m.group()[:12]}...')
if hits:
    print('LEAK')
    for h in hits: print(h)
    sys.exit(1)
print('CLEAN')
PY
)
if [[ "$SCAN2" != CLEAN* ]]; then
  echo "$SCAN2"
  osascript -e "display dialog \"⚠ 替換邏輯異常 — 替換後 workflow 仍含真實 key 字串。\nsetup-wizard 中止以避免污染 n8n DB。\nlog: $LOG\" buttons {\"知道了\"} default button 1 with icon stop"
  exit 1
fi
echo "  ✓ 替換後 sanity scan 通過"

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

# v1.3：先驗證 $env.GEMINI_API_KEY 真的到達 n8n 容器（pass-through 鏈完整性）
echo "  · 容器內 $env.GEMINI_API_KEY pass-through..."
ENV_PASSTHROUGH=$(docker exec "$N8N_CONTAINER" sh -c 'printf %s "${GEMINI_API_KEY:-MISSING}" | head -c 8' 2>/dev/null || echo "EXEC_FAIL")
GEMINI_KEY_HEAD="${GEMINI_KEY:0:8}"
if [ "$ENV_PASSTHROUGH" = "$GEMINI_KEY_HEAD" ]; then
  echo "    ✓ 容器內 GEMINI_API_KEY 與 host 相符（前 8 字元：${ENV_PASSTHROUGH}...）"
  ENV_OK=true
elif [ "$ENV_PASSTHROUGH" = "MISSING" ]; then
  echo "    ✗ 容器內無 GEMINI_API_KEY → compose pass-through 失敗"
  ENV_OK=false
else
  echo "    ✗ 容器內 GEMINI_API_KEY 不符（前 8 字元：${ENV_PASSTHROUGH}... vs host：${GEMINI_KEY_HEAD}...）"
  ENV_OK=false
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

echo "  Credentials   ：$CRED_COUNT_LABEL"
echo "  Workflows     ：成功 $WF_OK / 失敗 $WF_FAIL"
echo "  File access   ：已 patch /files/shared 白名單"
echo "  Env pass-thru ：$([ "$ENV_OK" = "true" ] && echo "✅ 容器內讀得到 GEMINI_API_KEY" || echo "❌ 容器內讀不到（看 log）")"
echo "  Telegram test ：$TG_REPORT_LABEL"
echo "  Gemini test   ：$([ "$GEMINI_OK" = "true" ] && echo "✅ API 正常" || echo "⚠️ 回應異常（看 /tmp/gemini-diagnostic.json）")"
echo "  Container     ：$N8N_CONTAINER"
echo "  Log           ：$LOG"
echo "═════════════════════════════════════════════════════════════"

# GUI 結果對話框
SUMMARY="✅ Lite Pack v1.3 安裝完成！

• $CRED_COUNT_LABEL credentials 已建立並加密儲存
• $WF_OK 個 workflows 已匯入並自動關聯 credentials
• File access 環境變數已 patch（/files/shared 可讀寫）
• Env pass-through：$([ "$ENV_OK" = "true" ] && echo "✅ \$env.GEMINI_API_KEY 在容器內讀得到" || echo "❌ 失敗")
• Telegram 測試：$TG_REPORT_LABEL
• Gemini 測試：$([ "$GEMINI_OK" = "true" ] && echo "✅ 正常" || echo "⚠️ 回應異常")

下一步：打開 n8n 看左側 Workflows 清單，$NEXT_STEP_LABEL"

# v1.1：TG_OK=skip 也算通過（學員選擇不用 TG 不是失敗）
TG_PASS=true
if [ "$USE_TELEGRAM" = "true" ] && [ "$TG_OK" != "true" ]; then
  TG_PASS=false
fi

if [ $WF_FAIL -eq 0 ] && [ "$TG_PASS" = "true" ] && [ "$GEMINI_OK" = "true" ] && [ "$ENV_OK" = "true" ]; then
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
