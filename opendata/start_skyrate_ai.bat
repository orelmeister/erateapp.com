@echo off
setlocal

set REPO_ROOT=%~dp0
set APP_FILE=%REPO_ROOT%skyrate-ai\app.py

if not exist "%APP_FILE%" (
  echo SkyRate AI entrypoint not found: %APP_FILE%
  exit /b 1
)

if "%SKYRATE_PORT%"=="" set SKYRATE_PORT=8502

echo Starting SkyRate AI on http://localhost:%SKYRATE_PORT%
cd /d "%REPO_ROOT%skyrate-ai"
start "SkyRate AI" python -m streamlit run "%APP_FILE%" --server.port %SKYRATE_PORT% --server.headless true

endlocal
