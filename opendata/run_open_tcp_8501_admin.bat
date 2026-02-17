@echo off
setlocal

REM Runs open_tcp_8501.ps1 with Administrator privileges (UAC prompt expected)

set "SCRIPT=%~dp0open_tcp_8501.ps1"

if not exist "%SCRIPT%" (
  echo ERROR: PowerShell script not found: "%SCRIPT%"
  exit /b 1
)

REM Launch an elevated PowerShell that runs the script
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process PowerShell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%SCRIPT%""'"

echo If you clicked 'Yes' on the UAC prompt, the firewall rule should be created in the new admin window.
endlocal
