# n8n Lite Pack · setup-wizard.ps1 (Windows) v1.0
# 由 setup-wizard.bat 呼叫。十步驟自動化安裝。
# 採納 Codex L3 審核建議：UTF-8 BOM / SecureString token / .Replace() / Invoke-Native exit code 檢查

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
Write-Host "  n8n Lite Pack · setup-wizard for Windows v1.0" -ForegroundColor Cyan
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

# native command wrapper with exit code check
function Invoke-Native {
  param(
    [string]$Label,
    [string]$FilePath,
    [string[]]$NativeArgs,
    [switch]$ContinueOnError
  )
  & $FilePath @NativeArgs 2>&1 | Tee-Object -FilePath $Log -Append
  if ($LASTEXITCODE -ne 0) {
    if ($ContinueOnError) {
      Write-Host "  ⚠ $Label 失敗（exit $LASTEXITCODE），繼續往下" -ForegroundColor Yellow
      return $false
    } else {
      throw "$Label 失敗，exit code: $LASTEXITCODE"
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
Write-Host "  ✓ 3 個 personalization 資料收齊" -ForegroundColor Green

# ════════ Step 3: file access patch + 重啟 ════════
Write-Host ""
Write-Host "[3/10] 偵測 file access 環境變數..." -ForegroundColor Yellow

$Compose = "$StarterKit\n8n-compose.yml"
$ComposeContent = Get-Content $Compose -Raw -Encoding UTF8
if ($ComposeContent -match 'N8N_RESTRICT_FILE_ACCESS_TO') {
  Write-Host "  ✓ compose.yml 已含 file access patch（跳過）" -ForegroundColor Green
  $RestartNeeded = $false
} else {
  Copy-Item $Compose "$Compose.bak-$(Get-Date -Format 'yyyyMMddHHmmss')"
  $patched = $ComposeContent.Replace(
    'N8N_BASIC_AUTH_ACTIVE=false',
    "N8N_BASIC_AUTH_ACTIVE=false`n      - N8N_RESTRICT_FILE_ACCESS_TO=/files/shared`n      - N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false"
  )
  Set-Content $Compose $patched -Encoding UTF8 -NoNewline
  Write-Host "  ✓ patch 完成（加入 N8N_RESTRICT_FILE_ACCESS_TO + N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES）" -ForegroundColor Green
  $RestartNeeded = $true
}

if ($RestartNeeded) {
  Write-Host "  ⏳ 重啟 n8n container..." -ForegroundColor Yellow
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
  # 重新抓 container 名
  $containers = @(docker ps --filter "name=n8n" --format "{{.Names}}" | Where-Object { $_ -match "n8n" -and $_ -notmatch "postgres" })
  $N8nContainer = $containers[0]
  Write-Host "  ✓ n8n 重啟完成（container: $N8nContainer）" -ForegroundColor Green
}

# ════════ Step 4: personalization.env ════════
Write-Host ""
Write-Host "[4/10] 寫入 personalization.env..." -ForegroundColor Yellow
$EnvContent = @"
# n8n Lite Pack 個人化設定（setup-wizard 自動產生 $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')）
# 不要 commit 到 git！
GEMINI_API_KEY=$GeminiKey
TELEGRAM_BOT_TOKEN=$TgToken
TELEGRAM_CHAT_ID=$TgChatId
"@
Set-Content "$ScriptDir\personalization.env" $EnvContent -Encoding UTF8
Write-Host "  ✓ personalization.env 寫入完成" -ForegroundColor Green

# ════════ Step 5: 建 sample 資料夾 ════════
Write-Host ""
Write-Host "[5/10] 建 sample 資料夾..." -ForegroundColor Yellow
$Shared = "$StarterKit\shared"
$Folders = @(
  'pdf-inbox','pdf-renamed',
  'batch-inbox','batch-inbox\processed','batch-inbox\failed',
  'daily-input','daily-output','ai-output',
  'client-inbox','client-organized',
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
  },
  @{
    id = "lite-pack-telegram"
    name = "Lite Pack · Telegram Bot"
    type = "telegramApi"
    data = @{ accessToken = $TgToken; baseUrl = "https://api.telegram.org" }
  }
)
$Creds | ConvertTo-Json -Depth 10 | Set-Content $CredFile -Encoding UTF8
Write-Host "  ✓ credentials JSON 生成" -ForegroundColor Green

# ════════ Step 7: 替換 placeholder（採納 Codex 建議用 .Replace 而非 -replace）════════
Write-Host ""
Write-Host "[7/10] 替換 workflow JSON 內 placeholder..." -ForegroundColor Yellow

$WorkflowTmp = "$ScriptDir\workflows-tmp"
if (Test-Path $WorkflowTmp) { Remove-Item $WorkflowTmp -Recurse -Force }
Copy-Item "$ScriptDir\workflows" $WorkflowTmp -Recurse

Get-ChildItem "$WorkflowTmp\*.json" | ForEach-Object {
  $content = Get-Content $_.FullName -Raw -Encoding UTF8
  # .Replace() 是 literal replace，不會被當 regex 處理（避免 token 含 $ \ 等特殊字元出錯）
  $content = $content.Replace('__TELEGRAM_CHAT_ID__', $TgChatId)
  $content = $content.Replace('__GEMINI_API_KEY__', $GeminiKey)
  $content = $content.Replace('__TELEGRAM_BOT_TOKEN__', $TgToken)
  Set-Content $_.FullName $content -Encoding UTF8 -NoNewline
  Write-Host "  ✓ $($_.Name) 已替換 placeholders"
}

# ════════ Step 8: import credentials（採納 Codex 建議檢查 exit code）════════
Write-Host ""
Write-Host "[8/10] 匯入 credentials 到 n8n..." -ForegroundColor Yellow

Invoke-Native "docker cp credentials" "docker" @("cp", $CredFile, "${N8nContainer}:/tmp/credentials.json")
$credResult = Invoke-Native "n8n import:credentials" "docker" @("exec", "-u", "node", $N8nContainer, "n8n", "import:credentials", "--input=/tmp/credentials.json")
if (-not $credResult) {
  Write-Host "  ❌ credentials 匯入失敗" -ForegroundColor Red
  Write-Host "  常見原因：n8n 沒建 Owner Account。先到 http://localhost:5678 完成 owner setup 後重跑" -ForegroundColor Yellow
  exit 1
}
Write-Host "  ✓ credentials 匯入成功" -ForegroundColor Green

# ════════ Step 9: import workflows ════════
Write-Host ""
Write-Host "[9/10] 匯入 $WorkflowCount 個 workflows 到 n8n..." -ForegroundColor Yellow
$ImportSuccess = 0
$ImportFail = 0

Get-ChildItem "$WorkflowTmp\*.json" | Sort-Object Name | ForEach-Object {
  $f = $_.Name
  $copied = Invoke-Native "docker cp $f" "docker" @("cp", $_.FullName, "${N8nContainer}:/tmp/$f") -ContinueOnError
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

# Telegram
try {
  $tgBody = @{chat_id=$TgChatId; text="✅ Lite Pack v1.0 setup-wizard 安裝完成！(Windows)"} | ConvertTo-Json -Compress
  $tgResp = Invoke-RestMethod -Uri "https://api.telegram.org/bot$TgToken/sendMessage" -Method Post -ContentType "application/json; charset=utf-8" -Body $tgBody -TimeoutSec 10
  if ($tgResp.ok) {
    Write-Host "  ✓ Telegram 通知測試成功（請看你手機）" -ForegroundColor Green
  } else {
    Write-Host "  ⚠ Telegram 回 fail: $($tgResp.description)" -ForegroundColor Yellow
  }
} catch {
  Write-Host "  ⚠ Telegram 失敗: $_" -ForegroundColor Yellow
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
} catch {
  Write-Host "  ⚠ Gemini 失敗: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ Lite Pack 安裝完成！" -ForegroundColor Green
Write-Host "═════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  1. 瀏覽器開 http://localhost:5678"
Write-Host "  2. 左側 Workflows 應該看到 $ImportSuccess 個（編號 01 ~ 14）"
Write-Host "  3. Credentials 應該看到 2 個（Lite Pack · Gemini API + Telegram Bot）"
Write-Host "  4. 點 05 · Telegram 通知 → Execute workflow → 確認再次收到通知"
Write-Host ""
Start-Process "http://localhost:5678"

# 清臨時檔
Remove-Item $WorkflowTmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $CredFile -Force -ErrorAction SilentlyContinue
exit 0
