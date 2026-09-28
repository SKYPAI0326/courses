$ErrorActionPreference = 'Stop'

$PatchDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$KitDir = Split-Path -Parent $PatchDir
$ComposeFile = Join-Path $KitDir 'n8n-compose.yml'
$SharedDir = Join-Path $KitDir 'shared'
$Id06 = 'lite-pack-06-webhook-gemini-file'
$Id12 = 'lite-pack-12-knowledge-rag'
$ImportStarted = $false
$Success = $false
$Active06 = ''
$Active12 = ''

function Invoke-ComposeCapture {
  param([string[]]$ComposeArgs)
  $AllArgs = @('-f', $ComposeFile) + $ComposeArgs
  $Output = & docker compose @AllArgs
  $ExitCode = $LASTEXITCODE
  if ($ExitCode -ne 0) { throw "docker compose 失敗（$ExitCode）：$($ComposeArgs -join ' ')" }
  return (($Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine).Trim()
}

function Invoke-Compose {
  param([string[]]$ComposeArgs)
  $AllArgs = @('-f', $ComposeFile) + $ComposeArgs
  & docker compose @AllArgs
  $ExitCode = $LASTEXITCODE
  if ($ExitCode -ne 0) { throw "docker compose 失敗（$ExitCode）：$($ComposeArgs -join ' ')" }
}

function Invoke-Rollback {
  param([string]$WorkContainerDir)
  Write-Host '修補未完成，正在從備份回復 #06/#12……' -ForegroundColor Yellow
  try { Invoke-Compose -ComposeArgs @('stop', 'n8n') } catch { Write-Host $_.Exception.Message }
  try { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'import:workflow', "--input=$WorkContainerDir/backup/06-original.json") } catch { Write-Host '回復 #06 失敗，請保留備份並聯絡課程支援。' }
  try { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'import:workflow', "--input=$WorkContainerDir/backup/12-original.json") } catch { Write-Host '回復 #12 失敗，請保留備份並聯絡課程支援。' }
  if ($Active06 -eq 'true') {
    try { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'publish:workflow', "--id=$Id06") } catch { Write-Host '回復 #06 發佈狀態失敗。' }
  }
  if ($Active12 -eq 'true') {
    try { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'publish:workflow', "--id=$Id12") } catch { Write-Host '回復 #12 發佈狀態失敗。' }
  }
  try { Invoke-Compose -ComposeArgs @('start', 'n8n') } catch { Write-Host 'n8n 啟動失敗；請回到 starter-kit 執行 start.bat。' }
  Write-Host "備份位置：$(Join-Path $SharedDir (Split-Path -Leaf $WorkContainerDir))/backup" -ForegroundColor Yellow
}

try {
  if (-not (Test-Path $ComposeFile) -or -not (Test-Path $SharedDir)) {
    throw '找不到同層的 n8n-compose.yml / shared。請把 n8n-lite-pack-ui-fix 資料夾放在 n8n-starter-kit 裡。'
  }
  Set-Location $KitDir
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw '找不到 Docker。請先開啟 Docker Desktop，再重新執行。' }

  $N8nVersion = Invoke-ComposeCapture -ComposeArgs @('exec', '-T', 'n8n', 'n8n', '--version')
  if ($N8nVersion -ne '2.37.7') { throw "此修補包只支援課程版 n8n 2.37.7；目前版本是 $N8nVersion。沒有修改任何 workflow。" }

  Write-Host '此工具只修補 #06 與 #12 的本機 UI，會短暫停止再啟動 n8n。' -ForegroundColor Cyan
  $Confirm = Read-Host '確認繼續請輸入 YES；其他輸入會取消'
  if ($Confirm -cne 'YES') {
    Write-Host '已取消，尚未匯出或修改 workflow。' -ForegroundColor Yellow
    Read-Host '按 Enter 關閉'
    exit 0
  }

  $Stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
  $WorkName = "lite-pack-ui-fix-$Stamp"
  $WorkDir = Join-Path $SharedDir $WorkName
  $WorkContainerDir = "/files/shared/$WorkName"
  $PackageDir = Join-Path $WorkDir 'package'
  $BackupDir = Join-Path $WorkDir 'backup'
  $MergedDir = Join-Path $WorkDir 'merged'
  New-Item -ItemType Directory -Path (Join-Path $PackageDir 'workflows'), $BackupDir, $MergedDir -Force | Out-Null

  Copy-Item (Join-Path $PatchDir 'merge-workflow.cjs') $PackageDir
  Copy-Item (Join-Path $PatchDir 'workflows\06-webhook-gemini-file.json') (Join-Path $PackageDir 'workflows')
  Copy-Item (Join-Path $PatchDir 'workflows\12-knowledge-rag.json') (Join-Path $PackageDir 'workflows')

  $Original06 = "$WorkContainerDir/backup/06-original.json"
  $Original12 = "$WorkContainerDir/backup/12-original.json"
  $Published06 = "$WorkContainerDir/backup/06-published.json"
  $Published12 = "$WorkContainerDir/backup/12-published.json"
  $Patch06 = "$WorkContainerDir/package/workflows/06-webhook-gemini-file.json"
  $Patch12 = "$WorkContainerDir/package/workflows/12-knowledge-rag.json"
  $Merged06 = "$WorkContainerDir/merged/06-merged.json"
  $Merged12 = "$WorkContainerDir/merged/12-merged.json"
  $Verify06 = "$WorkContainerDir/merged/06-verify.json"
  $Verify12 = "$WorkContainerDir/merged/12-verify.json"
  $Merger = "$WorkContainerDir/package/merge-workflow.cjs"

  Write-Host '正在備份目前 #06 與 #12；其他 workflow 不會被匯出或修改。' -ForegroundColor Cyan
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id06", "--output=$Original06")
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id12", "--output=$Original12")
  if (-not (Test-Path (Join-Path $BackupDir '06-original.json')) -or -not (Test-Path (Join-Path $BackupDir '12-original.json'))) {
    throw '備份不完整，停止；尚未套用修補。'
  }

  $Active06 = Invoke-ComposeCapture -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--active', $Original06)
  $Active12 = Invoke-ComposeCapture -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--active', $Original12)
  if ($Active06 -notin @('true', 'false') -or $Active12 -notin @('true', 'false')) { throw '無法辨識原本啟用狀態，停止。' }
  if ($Active06 -eq 'true') {
    Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id06", '--published', "--output=$Published06")
    Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--assert-published', $Original06, $Published06)
  }
  if ($Active12 -eq 'true') {
    Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id12", '--published', "--output=$Published12")
    Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--assert-published', $Original12, $Published12)
  }

  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, $Original06, $Patch06, $Merged06)
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, $Original12, $Patch12, $Merged12)

  Write-Host '備份與差異檢查完成。現在只暫停 n8n；Postgres、volume、shared 檔案會保留。' -ForegroundColor Cyan
  $ImportStarted = $true
  Invoke-Compose -ComposeArgs @('stop', 'n8n')
  Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'import:workflow', "--input=$Merged06")
  Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'import:workflow', "--input=$Merged12")
  if ($Active06 -eq 'true') { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'publish:workflow', "--id=$Id06") }
  if ($Active12 -eq 'true') { Invoke-Compose -ComposeArgs @('run', '-T', '--rm', '--no-deps', 'n8n', 'publish:workflow', "--id=$Id12") }
  Invoke-Compose -ComposeArgs @('start', 'n8n')

  Write-Host '等待 n8n 重新啟動……'
  $Ready = $false
  for ($Attempt = 0; $Attempt -lt 30; $Attempt++) {
    try {
      $null = Invoke-ComposeCapture -ComposeArgs @('exec', '-T', 'n8n', 'n8n', '--version')
      $Ready = $true
      break
    } catch { Start-Sleep -Seconds 2 }
  }
  if (-not $Ready) { throw 'n8n 未能在 60 秒內回應。' }
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id06", "--output=$Verify06")
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'n8n', 'export:workflow', "--id=$Id12", "--output=$Verify12")
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--verify', $Verify06, $Patch06)
  Invoke-Compose -ComposeArgs @('exec', '-T', 'n8n', 'node', $Merger, '--verify', $Verify12, $Patch12)

  $Success = $true
  Write-Host "修補完成。備份位置：$BackupDir" -ForegroundColor Green
  Write-Host '請在瀏覽器重新整理 #06 /ai-ui 與 #12 /kb-ui；其他 workflow 與憑證參照未更動。'
} catch {
  Write-Host "`n修補停止：$($_.Exception.Message)" -ForegroundColor Red
  if ($ImportStarted -and -not $Success) { Invoke-Rollback -WorkContainerDir $WorkContainerDir }
  Read-Host '按 Enter 關閉'
  exit 1
}

Read-Host '按 Enter 關閉'
