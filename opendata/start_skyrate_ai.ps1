# Launch SkyRate AI Streamlit app reliably from the opendata repo root.
# Starts Streamlit in a separate process so you can keep using this terminal.

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$appDir = Join-Path $repoRoot 'skyrate-ai'
$appFile = Join-Path $appDir 'app.py'

if (-not (Test-Path $appFile)) {
  throw "SkyRate AI entrypoint not found: $appFile"
}

$port = if ($env:SKYRATE_PORT) { $env:SKYRATE_PORT } else { '8502' }

Write-Host "Starting SkyRate AI from: $appFile" -ForegroundColor Cyan
Write-Host "Port: $port" -ForegroundColor Cyan

# Start in a new process so the app keeps running even if you run more commands.
Start-Process -WorkingDirectory $appDir -FilePath 'python' -ArgumentList @(
  '-m', 'streamlit', 'run', $appFile,
  '--server.port', $port,
  '--server.headless', 'true'
)

Write-Host "SkyRate AI launching... Open http://localhost:$port" -ForegroundColor Green
