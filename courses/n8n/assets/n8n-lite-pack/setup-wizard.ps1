# n8n Lite Pack · setup-wizard.ps1 (Windows) v1.3.2
# 由 setup-wizard.bat 呼叫。十步驟自動化安裝。
# 採納 Codex L3 審核建議：UTF-8 BOM / SecureString token / .Replace() / Invoke-Native exit code 檢查
# v1.1：Telegram 改為可選（Y/N gate）— 不用 TG 的學員零摩擦過關
# v1.2.3 / v1.2.4：smoke test 與 endpoints 解析強化（純版號 bump）
# v1.3：⚠ 安全修補 — Gemini key 改走 $env.GEMINI_API_KEY 路徑（不再字串替換 jsCode）
#       原機制：把 __GEMINI_API_KEY__ 替換成真 key 寫進 workflow JSON → 學員匯出 JSON 會洩漏
#       新機制：寫到 starter-kit/.env 的 GEMINI_API_KEY 環境變數 → n8n Code node 透過 $env 讀
#       需要 n8n-compose.yml 含 N8N_BLOCK_ENV_ACCESS_IN_NODE=false（本 wizard 會自動 patch）
#       偵測到舊版安裝（personalization.env 殘留）會跳警告，提醒撤銷舊 key
# v1.3.1：修 Invoke-Native 對 docker compose stderr 過度敏感的 bug
#         症狀：Step 4.5 重啟 n8n 時，docker compose down 輸出 "Container ... Stopping" 到 stderr，
#         在 $ErrorActionPreference='Stop' 下被 PowerShell 當 RemoteException 拋出 →
#         script 中斷在 down 跟 up 之間 → container 被 stop 沒被 up 起來 → 看起來「被刪除」
#         修：Invoke-Native 內暫時 ErrorActionPreference=Continue，呼完還原；判斷成敗只看 $LASTEXITCODE
# v1.3.2：修偵測舊版的 false positive — v1.3 自己寫 .env 後下次跑 wizard 也會誤觸警告。
#         加 .env 內 marker comment（# Provisioned by setup-wizard v1.3+），有 marker 就不再警告。

$ErrorActionPreference = 'Stop'
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ════════ PowerShell 版本檢查 ════════
$PSMajor = $PSVersionTable.PSVersion.Major
if ($PSMajor -lt 5) {
  Write-Host "需要 Windows PowerShell 5.1 或 PowerShell 7+，當前版本 $($PSVersionTable.PSVersion)" -ForegroundColor Red
  exit 1
}

$ScriptDir = $PSScriptRoot
Set-Location $ScriptDir

$Log = "$ScriptDir\setup-wizard.log"
"$(Get-Date) - setup-wizard 開始 (PS $($PSVersionTable.PSVersion))" | Out-File $Log -Encoding UTF8

Write-Host ""
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  n8n Lite Pack · setup-wizard for Windows v1.3.2" -ForegroundColor Cyan
Write-Host "  PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor Gray
Write-Host "  log: $Log" -ForegroundColor Gray
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ════════ Helper functions ════════

# Read-Host with SecureString → plain string (避免 token 顯示在 console)
function Read-SecretPlainText {
  param([string]$Prompt)
  $secure = Read-Host $Prompt -AsSecureString
  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
  try {
    return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  } finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
  }
}

# 寫純 UTF-8（無 BOM）— PS 5.1 的 Set-Content -Encoding UTF8 會加 BOM 導致 JSON parser 炸
function Write-Utf8NoBom {
  param([string]$Path, [string]$Content)
  $utf8NoBom = New-Object System.Text.UTF8Encoding $false
  [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

# native command wrapper：顯示輸出給學員看 + 寫 log + exit code 檢查
# 用 [void] 包呼叫避免 return value 印到 console
# v1.3.1 修補：$ErrorActionPreference='Stop' 下 docker compose 把進度訊息寫 stderr（如
# "Container n8n-...n8n-1 Stopping"），2>&1 合流後 PowerShell 會把 stderr 當 RemoteException 拋。
# 結果：docker compose down 已執行（container 停了），但 throw 中斷 script，up -d 沒跑 → 容器消失。
# 修：呼叫 native command 期間暫時 ErrorActionPreference=Continue，呼完還原。判失敗只看 $LASTEXITCODE。
function Invoke-Native {
  param(
    [string]$Label,
    [string]$FilePath,
    [string[]]$NativeArgs,
    [switch]$ContinueOnError
  )
  $prevEAP = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $output = & $FilePath @NativeArgs 2>&1
  } finally {
    $ErrorActionPreference = $prevEAP
  }
  # 顯示輸出讓學員看到實際進度 / 錯誤訊息（stderr 進度訊息也會在這印，但不算錯誤）
  if ($output) {
    $output | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
  }
  $output | Out-File -FilePath $Log -Append -Encoding UTF8
  if ($LASTEXITCODE -ne 0) {
    if ($ContinueOnError) {
      Write-Host "  ⚠ $Label 失敗（exit $LASTEXITCODE），繼續往下" -ForegroundColor Yellow
      return $false
    } else {
      throw "$Label 失敗，exit code: $LASTEXITCODE`n看上方 docker 輸出找根因。常見：n8n Owner Account 沒建（到 http://localhost:5678 完成首次設定後重跑）"
    }
  }
  return $true
}

# 註：本 PS1 完全不需要 Python（credentials JSON 用 ConvertTo-Json，placeholder 替換用 .Replace()）
# 如果你看到舊版 .command 內 Python 步驟，那是 bash 版本的限制，PS 版本已內建處理

# ════════ Step 1: 環境檢查 ════════
Write-Host "[1/10] 環境檢查..." -ForegroundColor Yellow

# 1a. Docker
try {
  docker --version | Out-Null
} catch {
  Write-Host "  ❌ 找不到 docker 指令" -ForegroundColor Red
  Write-Host "  請先安裝 Docker Desktop：https://www.docker.com/products/docker-desktop/" -ForegroundColor Red
  exit 1
}

# 1b. Docker daemon
try {
  docker info 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "docker info failed" }
} catch {
  Write-Host "  ❌ Docker Desktop 未啟動" -ForegroundColor Red
  Write-Host "  請打開 Docker Desktop（工具列鯨魚 icon）等左下角 Engine running 後再次執行" -ForegroundColor Red
  exit 1
}
Write-Host "  ✓ Docker daemon 正常" -ForegroundColor Green

# 1c. n8n 在跑
try {
  $resp = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
  if ($resp.StatusCode -ne 200) { throw "n8n not healthy" }
} catch {
  Write-Host "  ❌ n8n 沒跑在 localhost:5678" -ForegroundColor Red
  Write-Host "  請先到 n8n-starter-kit/ 雙擊 start.bat 啟動 n8n" -ForegroundColor Red
  exit 1
}
Write-Host "  ✓ n8n 服務正常" -ForegroundColor Green

# 1e. n8n container（採納 Codex 建議：Count 檢查 + fail fast）
$containers = @(docker ps --filter "name=n8n" --format "{{.Names}}" | Where-Object { $_ -match "n8n" -and $_ -notmatch "postgres" })
if ($containers.Count -eq 0) {
  Write-Host "  ❌ 找不到 n8n container。請先到 starter-kit 雙擊 start.bat" -ForegroundColor Red
  exit 1
}
if ($containers.Count -gt 1) {
  Write-Host "  ⚠ 找到多個 n8n container：" -ForegroundColor Yellow
  $containers | ForEach-Object { Write-Host "    - $_" -ForegroundColor Yellow }
  Write-Host "  使用第一個。如果不對請手動 docker rm 舊的後重跑。" -ForegroundColor Yellow
}
$N8nContainer = $containers[0]
Write-Host "  ✓ n8n container: $N8nContainer" -ForegroundColor Green

# 1f. starter-kit 路徑
$StarterKit = "$env:USERPROFILE\Downloads\n8n-starter-kit"
if (-not (Test-Path "$StarterKit\n8n-compose.yml")) {
  $StarterKit = Read-Host "找不到預設位置。請貼上 n8n-starter-kit 完整路徑（含 n8n-compose.yml 的資料夾）"
  if (-not (Test-Path "$StarterKit\n8n-compose.yml")) {
    Write-Host "  ❌ 該路徑沒有 n8n-compose.yml" -ForegroundColor Red
    exit 1
  }
}
Write-Host "  ✓ starter-kit: $StarterKit" -ForegroundColor Green

# 1g. workflows 資料夾
if (-not (Test-Path "$ScriptDir\workflows")) {
  Write-Host "  ❌ 找不到 workflows 資料夾，試跑包不完整請重新下載" -ForegroundColor Red
  exit 1
}
$WorkflowCount = (Get-ChildItem "$ScriptDir\workflows\*.json").Count
Write-Host "  ✓ workflows 資料夾就緒（$WorkflowCount 個 JSON）" -ForegroundColor Green

# ════════ Step 2: 收集 3 個 key（採納 Codex 建議用 SecureString）════════
Write-Host ""
Write-Host "[2/10] 收集 personalization 資料（不會顯示在畫面上）..." -ForegroundColor Yellow

$GeminiKey = Read-SecretPlainText "請貼上 Gemini API key（AIza... 開頭，輸入時不顯示）"
if ($GeminiKey -notmatch '^AIza') {
  Write-Host "  ❌ Gemini API key 格式不對（應以 AIza 開頭）" -ForegroundColor Red
  exit 1
}

# Telegram 改成 Y/N 可選（v1.1）— 不用 TG 的學員直接過，省 BotFather 5-10 分鐘
$useTgRaw = Read-Host "要用 Telegram 接收 workflow 通知嗎？(Y / N，預設 N，可隨時重跑 wizard 補)"
$UseTelegram = $useTgRaw -match '^[Yy]'

if ($UseTelegram) {
  $TgToken = Read-SecretPlainText "請貼上 Telegram bot token（123456:ABC-DEF... 格式）"
  if ($TgToken -notmatch '^\d+:') {
    Write-Host "  ❌ Telegram bot token 格式不對" -ForegroundColor Red
    exit 1
  }
  $TgChatId = Read-Host "請貼上 Telegram Chat ID（純數字，可顯示）"
  if ($TgChatId -notmatch '^-?\d+$') {
    Write-Host "  ❌ Chat ID 應該是純數字" -ForegroundColor Red
    exit 1
  }
  Write-Host "  ✓ 3 個 personalization 資料收齊（Gemini + Telegram）" -ForegroundColor Green
} else {
  $TgToken = ""
  $TgChatId = ""
  Write-Host "  ↳ 跳過 Telegram。8 個用 TG 的 workflow（05/06/07/09/10/11/13/14）匯入後仍是 inactive，要用再去 n8n UI 補 credential。" -ForegroundColor DarkGray
  Write-Host "  ✓ 1 個 personalization 資料收齊（Gemini）" -ForegroundColor Green
}

# ════════ Step 3: 偵測舊版安裝 + 統一 patch compose.yml（file access + env access + key pass-through）════════
Write-Host ""
Write-Host "[3/10] 偵測舊版安裝 + patch compose.yml 環境變數..." -ForegroundColor Yellow

# v1.3: 偵測舊版（personalization.env 殘留）→ 警告撤銷舊 key
$OldMarker = "$ScriptDir\personalization.env"
# 另一個 marker：starter-kit/.env 內既有 GEMINI_API_KEY=AIzaSy... 真實值
# v1.3.2 修補：v1.3+ wizard 寫 .env 時會加 marker comment，有 marker 就不再誤判為舊版
$V13Marker = '# Provisioned by setup-wizard v1.3+'
$OldEnvHasKey = $false
$StarterEnv = "$StarterKit\.env"
if (Test-Path $StarterEnv) {
  $hasAIza = Select-String -Path $StarterEnv -Pattern '^\s*GEMINI_API_KEY\s*=\s*"?AIzaSy' -Quiet
  $hasMarker = Select-String -Path $StarterEnv -Pattern ([regex]::Escape($V13Marker)) -Quiet
  if ($hasAIza -and -not $hasMarker) {
    $OldEnvHasKey = $true
  }
}

if ((Test-Path $OldMarker) -or $OldEnvHasKey) {
  $msg = @"
偵測到舊版 wizard 安裝過。

舊版（v1.2 之前）會把你的 Gemini API key 字串替換進 workflow JSON。
你以前從 n8n UI 匯出（Download）過的任何 workflow JSON 都可能含真 key 明文。

強烈建議：
  1. 立刻到 https://aistudio.google.com/apikey 撤銷（Delete）舊 key
  2. 重新申請一把新 key
  3. 繼續本 wizard，新機制（環境變數）會把新 key 寫進 starter-kit/.env
     workflow JSON 不再含 key，匯出也不會洩漏

按 Enter 繼續，或 Ctrl+C 中止。
"@
  Write-Host $msg -ForegroundColor Yellow
  Read-Host "確認後按 Enter"
  if (Test-Path $OldMarker) {
    Move-Item $OldMarker "$OldMarker.migrated-$(Get-Date -Format 'yyyyMMddHHmmss')" -Force
    Write-Host "  ⚠ 舊版 marker (personalization.env) 已重新命名" -ForegroundColor Yellow
  }
  if ($OldEnvHasKey) {
    Write-Host "  ⚠ 偵測到 .env 已含 AIzaSy 開頭真實 key — 舊 wizard 寫過。新 key 會覆蓋此值" -ForegroundColor Yellow
  }
}

$Compose = "$StarterKit\n8n-compose.yml"
$ComposeContent = Get-Content $Compose -Raw -Encoding UTF8
Copy-Item $Compose "$Compose.bak-$(Get-Date -Format 'yyyyMMddHHmmss')"
Write-Host "  ✓ 已備份 compose.yml" -ForegroundColor Green

# 統一 patch 4 個必要 env vars（idempotent）
$Required = @(
  @{ Key = 'N8N_RESTRICT_FILE_ACCESS_TO';       Line = '      - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared' },
  @{ Key = 'N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES';Line = '      - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false' },
  @{ Key = 'N8N_BLOCK_ENV_ACCESS_IN_NODE';      Line = '      - N8N_BLOCK_ENV_ACCESS_IN_NODE=false' },
  @{ Key = 'GEMINI_API_KEY';                    Line = '      - GEMINI_API_KEY=${GEMINI_API_KEY:-}' }
)
# Codex 建議：line-anchored regex，避免被註解誤導
$Missing = $Required | Where-Object {
  $pat = '(?m)^\s*-\s*' + [regex]::Escape($_.Key) + '='
  $ComposeContent -notmatch $pat
}

if ($Missing.Count -eq 0) {
  Write-Host "  ✓ compose.yml 4 個必要 env vars 都齊（跳過 patch）" -ForegroundColor Green
  $RestartNeeded = $false
} else {
  # 用 regex 在 n8n service 的 environment: 區段最後一個 env line 後追加
  $pattern = '(?ms)^(  n8n:\r?\n(?:.*?\r?\n)*?    environment:\r?\n(?:      - [^\r\n]+\r?\n)+)'
  $injectLines = ($Missing | ForEach-Object { $_.Line }) -join "`n"
  $injectLines += "`n"
  if ($ComposeContent -match $pattern) {
    $patched = [regex]::Replace($ComposeContent, $pattern, "`${1}$injectLines", 1)
    Write-Utf8NoBom $Compose $patched
    $injectedKeys = ($Missing | ForEach-Object { $_.Key }) -join ', '
    Write-Host "  ✓ compose.yml 已加入：$injectedKeys" -ForegroundColor Green
    $RestartNeeded = $true
  } else {
    Write-Host "  ❌ compose.yml patch 失敗（找不到 n8n service environment 區段）" -ForegroundColor Red
    Write-Host "  請手動編輯 compose.yml 在 n8n service 的 environment: 區段加入：" -ForegroundColor Yellow
    $Missing | ForEach-Object { Write-Host "    $($_.Line)" -ForegroundColor Yellow }
    exit 1
  }
}

# 注意：實際 restart 移到 Step 4 之後（.env 寫完才重啟，這樣容器能讀到新 GEMINI_API_KEY）

# ════════ Step 4: 寫/合併 starter-kit/.env（GEMINI_API_KEY；idempotent）════════
Write-Host ""
Write-Host "[4/10] 合併 GEMINI_API_KEY 到 starter-kit/.env..." -ForegroundColor Yellow

$EnvFile = "$StarterKit\.env"
if (-not (Test-Path $EnvFile)) {
  if (Test-Path "$StarterKit\.env.example") {
    Copy-Item "$StarterKit\.env.example" $EnvFile
    Write-Host "  ↳ 從 .env.example 建立 .env" -ForegroundColor DarkGray
  } else {
    Write-Utf8NoBom $EnvFile ""
    Write-Host "  ↳ 建立空 .env" -ForegroundColor DarkGray
  }
}

# 備份
Copy-Item $EnvFile "$EnvFile.bak-$(Get-Date -Format 'yyyyMMddHHmmss')"

# dotenv quote helper（跳脫 \ " $；避免 docker compose env var 展開）
function Get-DotenvQuoted {
  param([string]$Value)
  $escaped = $Value.Replace('\', '\\').Replace('"', '\"').Replace('$', '\$')
  return '"' + $escaped + '"'
}

# idempotent merge — 對非註解的 GEMINI_API_KEY= 行替換，沒有就 append
# v1.3.2：寫入時保證 v1.3+ marker comment 存在 → 下次跑 wizard 不會誤判舊版
$EnvLines = Get-Content $EnvFile -Encoding UTF8
$NewGeminiLine = "GEMINI_API_KEY=$(Get-DotenvQuoted $GeminiKey)"
$Replaced = $false
$HasMarker = $false
$OutLines = @()
foreach ($line in $EnvLines) {
  $trimmed = $line.TrimStart()
  if (-not $trimmed.StartsWith('#') -and $trimmed -match '^GEMINI_API_KEY=') {
    $OutLines += $NewGeminiLine
    $Replaced = $true
  } else {
    if ($line -match [regex]::Escape($V13Marker)) { $HasMarker = $true }
    $OutLines += $line
  }
}
if (-not $Replaced) {
  $OutLines += ''
  $OutLines += '# ---- Gemini API key（setup-wizard v1.3 自動寫入） ----'
  $OutLines += $NewGeminiLine
}
# v1.3.2: 保證 v1.3+ marker 存在
if (-not $HasMarker) {
  $OutLines += ''
  $OutLines += "$V13Marker (do not remove - used for old-install detection)"
}
$EnvResult = if ($Replaced) { 'replaced' } else { 'appended' }

# Telegram secrets 也寫進 .env（若選用）
if ($UseTelegram) {
  $TgTokenLine = "TELEGRAM_BOT_TOKEN=$(Get-DotenvQuoted $TgToken)"
  $TgChatLine  = "TELEGRAM_CHAT_ID=$(Get-DotenvQuoted $TgChatId)"
  $TgTokenSeen = $false
  $TgChatSeen  = $false
  $NewOut = @()
  foreach ($line in $OutLines) {
    $trimmed = $line.TrimStart()
    if (-not $trimmed.StartsWith('#') -and $trimmed -match '^TELEGRAM_BOT_TOKEN=') {
      $NewOut += $TgTokenLine; $TgTokenSeen = $true
    } elseif (-not $trimmed.StartsWith('#') -and $trimmed -match '^TELEGRAM_CHAT_ID=') {
      $NewOut += $TgChatLine; $TgChatSeen = $true
    } else {
      $NewOut += $line
    }
  }
  if (-not $TgTokenSeen) { $NewOut += $TgTokenLine }
  if (-not $TgChatSeen)  { $NewOut += $TgChatLine }
  $OutLines = $NewOut
}

Write-Utf8NoBom $EnvFile (($OutLines -join "`r`n") + "`r`n")
Write-Host "  ✓ GEMINI_API_KEY $EnvResult 到 $EnvFile" -ForegroundColor Green
if ($UseTelegram) {
  Write-Host "  ✓ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 也已寫入" -ForegroundColor Green
}

# Step 4.5: 重啟 n8n（讀 compose patch + .env 新 GEMINI_API_KEY）
# 因 .env 一定會變（每次 wizard 都會寫新 key），所以這裡無條件重啟
Write-Host "  ⏳ 重啟 n8n container（讀新 .env 與 compose env vars）..." -ForegroundColor Yellow
Push-Location $StarterKit
Invoke-Native "docker compose down" "docker" @("compose", "-f", "n8n-compose.yml", "down") -ContinueOnError | Out-Null
Invoke-Native "docker compose up -d" "docker" @("compose", "-f", "n8n-compose.yml", "up", "-d")
Pop-Location

Write-Host "  ⏳ 等 n8n 就緒..." -NoNewline
$ready = $false
for ($i = 0; $i -lt 40; $i++) {
  Start-Sleep -Seconds 2
  try {
    Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 3 | Out-Null
    Write-Host " ✓" -ForegroundColor Green
    $ready = $true
    break
  } catch {
    Write-Host "." -NoNewline
  }
}
if (-not $ready) {
  Write-Host ""
  Write-Host "  ❌ n8n 重啟後 80 秒內未就緒" -ForegroundColor Red
  exit 1
}
$containers = @(docker ps --filter "name=n8n" --format "{{.Names}}" | Where-Object { $_ -match "n8n" -and $_ -notmatch "postgres" })
$N8nContainer = $containers[0]
Write-Host "  ✓ n8n 重啟完成（container: $N8nContainer）" -ForegroundColor Green

# ════════ Step 5: 建 sample 資料夾 ════════
Write-Host ""
Write-Host "[5/10] 建 sample 資料夾..." -ForegroundColor Yellow
$Shared = "$StarterKit\shared"
$Folders = @(
  'pdf-inbox','pdf-renamed',
  'batch-inbox','batch-inbox\processed','batch-inbox\failed',
  'daily-input','daily-output','ai-output',
  'client-inbox','client-organized',
  # v1.1：#10 客戶分類 6 個子夾預建（n8n writeFile 不會自動建父目錄）
  'client-organized\contracts','client-organized\invoices','client-organized\presentations',
  'client-organized\images','client-organized\docs','client-organized\others',
  'leads-inbox','leads-output',
  'knowledge-docs','knowledge-index',
  'ops-input','ops-history','ops-snapshots','ops-incidents'
)
foreach ($sub in $Folders) {
  New-Item -Path "$Shared\$sub" -ItemType Directory -Force | Out-Null
}
Write-Host "  ✓ shared/ 子資料夾建好（$($Folders.Count) 個，位於 $Shared）" -ForegroundColor Green

# ════════ Step 6: credentials JSON ════════
Write-Host ""
Write-Host "[6/10] 生成 decrypted credentials JSON..." -ForegroundColor Yellow
$CredFile = "$ScriptDir\credentials.json"
$Creds = @(
  @{
    id = "lite-pack-gemini"
    name = "Lite Pack · Gemini API"
    type = "httpHeaderAuth"
    data = @{ name = "x-goog-api-key"; value = $GeminiKey }
  }
)
if ($UseTelegram) {
  $Creds += @{
    id = "lite-pack-telegram"
    name = "Lite Pack · Telegram Bot"
    type = "telegramApi"
    data = @{ accessToken = $TgToken; baseUrl = "https://api.telegram.org" }
  }
}
# 用 @() 強制陣列形狀（PS 對單元素 array 會 collapse 成單 object）
$CredsJson = ConvertTo-Json -InputObject @($Creds) -Depth 10
Write-Utf8NoBom $CredFile $CredsJson
Write-Host "  ✓ credentials JSON 生成" -ForegroundColor Green

# ════════ Step 7: workflow JSON 處理（v1.3：sanity scan + 只替換 Telegram placeholder，不再碰 Gemini）════════
Write-Host ""
Write-Host "[7/10] sanity scan + 替換 __TELEGRAM_* placeholder..." -ForegroundColor Yellow

$WorkflowTmp = "$ScriptDir\workflows-tmp"
if (Test-Path $WorkflowTmp) { Remove-Item $WorkflowTmp -Recurse -Force }
Copy-Item "$ScriptDir\workflows" $WorkflowTmp -Recurse

# Step 7a: sanity scan — 模板絕對不該含真實 API key 字串（防下載到被污染版本）
$LeakPatterns = @(
  @{ Pattern = 'AIzaSy[A-Za-z0-9_-]{30,}';                 Label = 'Google API key (AIzaSy...)' },
  @{ Pattern = 'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}';     Label = 'OpenAI/Anthropic key (sk-...)' },
  @{ Pattern = 'hf_[A-Za-z0-9]{30,}';                      Label = 'Hugging Face token (hf_...)' },
  @{ Pattern = 'ghp_[A-Za-z0-9]{30,}';                     Label = 'GitHub PAT (ghp_...)' },
  @{ Pattern = 'github_pat_[A-Za-z0-9_]{50,}';             Label = 'GitHub fine-grained PAT' },
  @{ Pattern = 'xox[baprs]-[A-Za-z0-9-]{20,}';             Label = 'Slack token (xox*-)' },
  @{ Pattern = '(?<![\d:])\d{8,10}:[A-Za-z0-9_-]{35}\b';   Label = 'Telegram bot token (digits:35chars)' }
)
$LeakHits = @()
Get-ChildItem "$WorkflowTmp\*.json" | ForEach-Object {
  $content = Get-Content $_.FullName -Raw -Encoding UTF8
  foreach ($p in $LeakPatterns) {
    $matches = [regex]::Matches($content, $p.Pattern)
    foreach ($m in $matches) {
      $preview = $m.Value.Substring(0, [Math]::Min(12, $m.Value.Length))
      $LeakHits += "  ✗ $($_.Name): $($p.Label) → ${preview}..."
    }
  }
}
if ($LeakHits.Count -gt 0) {
  $LeakHits | ForEach-Object { Write-Host $_ -ForegroundColor Red }
  Write-Host ""
  Write-Host "⚠ 偵測到 workflow 模板含真實 API key 字串！" -ForegroundColor Red
  Write-Host "你下載到的可能是被污染的版本（不該含真 key）。setup-wizard 中止以避免進一步散播。" -ForegroundColor Red
  Write-Host ""
  Write-Host "請：" -ForegroundColor Yellow
  Write-Host "  1. 刪除整個 n8n-lite-pack 資料夾" -ForegroundColor Yellow
  Write-Host "  2. 重新下載最新版本" -ForegroundColor Yellow
  Write-Host "  3. 立刻撤銷該 key（看 log: $Log）" -ForegroundColor Yellow
  exit 1
}
Write-Host "  ✓ 模板 sanity scan 通過（無真實 key 字串殘留）" -ForegroundColor Green

# Step 7b: 只替換 __TELEGRAM_CHAT_ID__（非 secret，公開）
# Gemini key 走 $env.GEMINI_API_KEY；Telegram bot token 走 n8n credential，workflow JSON 不含
if ($UseTelegram) {
  Get-ChildItem "$WorkflowTmp\*.json" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $newContent = $content.Replace('__TELEGRAM_CHAT_ID__', $TgChatId)
    if ($newContent -ne $content) {
      Write-Utf8NoBom $_.FullName $newContent
      Write-Host "  ✓ $($_.Name) 已替換 __TELEGRAM_CHAT_ID__"
    }
  }
} else {
  Write-Host "  ↳ 未啟用 Telegram，跳過 chat_id 替換" -ForegroundColor DarkGray
}

# Step 7c: 替換後二次 scan（Codex 建議：防替換邏輯本身漏洞 / 未來新增 secret placeholder）
$LeakHits2 = @()
Get-ChildItem "$WorkflowTmp\*.json" | ForEach-Object {
  $content = Get-Content $_.FullName -Raw -Encoding UTF8
  foreach ($p in $LeakPatterns) {
    $matches = [regex]::Matches($content, $p.Pattern)
    foreach ($m in $matches) {
      $preview = $m.Value.Substring(0, [Math]::Min(12, $m.Value.Length))
      $LeakHits2 += "  ✗ $($_.Name): $($p.Label) → ${preview}..."
    }
  }
}
if ($LeakHits2.Count -gt 0) {
  $LeakHits2 | ForEach-Object { Write-Host $_ -ForegroundColor Red }
  Write-Host ""
  Write-Host "⚠ 替換邏輯異常 — 替換後 workflow 仍含真實 key 字串。setup-wizard 中止。" -ForegroundColor Red
  exit 1
}
Write-Host "  ✓ 替換後 sanity scan 通過" -ForegroundColor Green

# ════════ Step 8: import credentials ════════
Write-Host ""
Write-Host "[8/10] 匯入 credentials 到 n8n..." -ForegroundColor Yellow

try {
  [void](Invoke-Native "docker cp credentials" "docker" @("cp", $CredFile, "${N8nContainer}:/tmp/credentials.json"))
  [void](Invoke-Native "n8n import:credentials" "docker" @("exec", "-u", "node", $N8nContainer, "n8n", "import:credentials", "--input=/tmp/credentials.json"))
  Write-Host "  ✓ credentials 匯入成功" -ForegroundColor Green
} catch {
  Write-Host "  ❌ credentials 匯入失敗" -ForegroundColor Red
  Write-Host "  看上方 docker exec 輸出找根因。常見：" -ForegroundColor Yellow
  Write-Host "    - n8n Owner Account 沒建 → 到 http://localhost:5678 完成首次設定" -ForegroundColor Yellow
  Write-Host "    - JSON 解析錯（BOM）→ 已用 Write-Utf8NoBom 寫入無 BOM，理應已修" -ForegroundColor Yellow
  Write-Host "    - 完整錯誤 log: $Log" -ForegroundColor Yellow
  exit 1
}

# ════════ Step 9: import workflows ════════
Write-Host ""
Write-Host "[9/10] 匯入 $WorkflowCount 個 workflows 到 n8n..." -ForegroundColor Yellow
$ImportSuccess = 0
$ImportFail = 0

Get-ChildItem "$WorkflowTmp\*.json" | Sort-Object Name | ForEach-Object {
  $f = $_.Name
  $copied = Invoke-Native "docker cp $f" "docker" @("cp", $_.FullName, "${N8nContainer}:/tmp/$f") -ContinueOnError
  [void]$copied  # 避免 True 印 console
  if (-not $copied) { $ImportFail++; return }
  $imported = Invoke-Native "import:workflow $f" "docker" @("exec", "-u", "node", $N8nContainer, "n8n", "import:workflow", "--input=/tmp/$f") -ContinueOnError
  if ($imported) {
    Write-Host "  ✓ $f" -ForegroundColor Green
    $ImportSuccess++
  } else {
    Write-Host "  ⚠ $f 匯入失敗（看 log: $Log）" -ForegroundColor Yellow
    $ImportFail++
  }
}

if ($ImportFail -gt 0) {
  Write-Host ""
  Write-Host "  ⚠ $ImportSuccess 成功 / $ImportFail 失敗" -ForegroundColor Yellow
  Write-Host "  失敗的 workflow 可在 n8n UI 內手動 Workflows → Import from File 重試" -ForegroundColor Yellow
} else {
  Write-Host "  ✓ $ImportSuccess 個 workflow 全部匯入成功" -ForegroundColor Green
}

# ════════ Step 10: smoke test ════════
Write-Host ""
Write-Host "[10/10] Telegram + Gemini smoke test..." -ForegroundColor Yellow

# Telegram (v1.1：跳過 if 不用 TG)
if ($UseTelegram) {
  try {
    $tgBody = @{chat_id=$TgChatId; text="✅ Lite Pack v1.1 setup-wizard 安裝完成！(Windows)"} | ConvertTo-Json -Compress
    $tgResp = Invoke-RestMethod -Uri "https://api.telegram.org/bot$TgToken/sendMessage" -Method Post -ContentType "application/json; charset=utf-8" -Body $tgBody -TimeoutSec 10
    if ($tgResp.ok) {
      Write-Host "  ✓ Telegram 通知測試成功（請看你手機）" -ForegroundColor Green
    } else {
      Write-Host "  ⚠ Telegram 回 fail: $($tgResp.description)" -ForegroundColor Yellow
    }
  } catch {
    Write-Host "  ⚠ Telegram 失敗: $_" -ForegroundColor Yellow
  }
} else {
  Write-Host "  ↳ Telegram smoke test 跳過（你選不用 TG）" -ForegroundColor DarkGray
}

# v1.3：先驗證 $env.GEMINI_API_KEY 真的到達 n8n 容器（pass-through 鏈完整性）
Write-Host "  · 容器內 `$env.GEMINI_API_KEY pass-through..." -ForegroundColor Cyan
$EnvOk = $false
try {
  $passthrough = & docker exec $N8nContainer sh -c 'printf %s "${GEMINI_API_KEY:-MISSING}" | head -c 8' 2>$null
  $head = $GeminiKey.Substring(0, [Math]::Min(8, $GeminiKey.Length))
  if ($passthrough -eq $head) {
    Write-Host "    ✓ 容器內 GEMINI_API_KEY 與 host 相符（前 8 字元：${passthrough}...）" -ForegroundColor Green
    $EnvOk = $true
  } elseif ($passthrough -eq 'MISSING') {
    Write-Host "    ✗ 容器內無 GEMINI_API_KEY → compose pass-through 失敗" -ForegroundColor Red
  } else {
    Write-Host "    ✗ 容器內 GEMINI_API_KEY 不符（前 8 字元：${passthrough}... vs host：${head}...）" -ForegroundColor Red
  }
} catch {
  Write-Host "    ✗ docker exec 失敗: $_" -ForegroundColor Red
}

# Gemini
try {
  $geminiBody = @{
    contents = @(@{parts=@(@{text="Reply exactly: OK"})})
    generationConfig = @{temperature=0.1; maxOutputTokens=20; thinkingConfig=@{thinkingBudget=0}}
  } | ConvertTo-Json -Depth 10
  $geminiResp = Invoke-RestMethod -Uri "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" -Method Post -Headers @{"x-goog-api-key"=$GeminiKey} -ContentType "application/json; charset=utf-8" -Body $geminiBody -TimeoutSec 30
  $reply = $geminiResp.candidates[0].content.parts[0].text
  Write-Host "  ✓ Gemini reply: $reply" -ForegroundColor Green
  $GeminiOk = $true
} catch {
  Write-Host "  ⚠ Gemini 失敗: $_" -ForegroundColor Yellow
  $GeminiOk = $false
}

Write-Host ""
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
if ($EnvOk -and $GeminiOk) {
  Write-Host "  ✅ Lite Pack v1.3 安裝完成！" -ForegroundColor Green
} else {
  Write-Host "  ⚠ Lite Pack v1.3 安裝完成（但有警告，看上方輸出）" -ForegroundColor Yellow
}
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  1. 瀏覽器開 http://localhost:5678"
Write-Host "  2. 左側 Workflows 應該看到 $ImportSuccess 個（編號 01 ~ 14）"
if ($UseTelegram) {
  Write-Host "  3. Credentials 應該看到 2 個（Lite Pack · Gemini API + Telegram Bot）"
  Write-Host "  4. 點 05 · Telegram 通知 → Execute workflow → 確認收到 TG 通知"
} else {
  Write-Host "  3. Credentials 應該看到 1 個（Lite Pack · Gemini API）"
  Write-Host "  4. 不用 TG 的 6 個 workflow 可直接試（01/02/03/04/08/12）"
  Write-Host "  5. 想用 Telegram 通知再重跑本 wizard（idempotent）"
}
Write-Host ""
Start-Process "http://localhost:5678"

# 清臨時檔
Remove-Item $WorkflowTmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $CredFile -Force -ErrorAction SilentlyContinue
exit 0
