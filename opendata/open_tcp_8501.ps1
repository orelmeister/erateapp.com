<#
.SYNOPSIS
  Opens inbound TCP port 8502 in Windows Firewall (for Streamlit).

.DESCRIPTION
  Creates (or updates) an inbound allow rule for TCP 8502.
  By default, applies to the Private profile only (recommended for LAN).

  Run this script in an elevated (Run as Administrator) PowerShell.

.PARAMETER Port
  TCP port to open. Default: 8502

.PARAMETER RuleName
  Firewall rule display name. Default: "Streamlit TCP 8502"

.PARAMETER Profile
  Firewall profile(s) to apply: Private, Domain, Public, or Any. Default: Private

.EXAMPLE
  .\open_tcp_8502.ps1

.EXAMPLE
  .\open_tcp_8502.ps1 -Profile Any
#>

[CmdletBinding()]
param(
  [ValidateRange(1, 65535)]
  [int]$Port = 8502,

  [string]$RuleName = "Streamlit TCP 8502",

  [ValidateSet('Private','Domain','Public','Any')]
  [string]$Profile = 'Private'
)

function Test-IsAdmin {
  $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
  return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
  Write-Error "This script must be run as Administrator. Right-click PowerShell and choose 'Run as administrator'."
  exit 1
}

# Map friendly profile to New-NetFirewallRule -Profile values
$profileArg = switch ($Profile) {
  'Any'     { 'Any' }
  'Private' { 'Private' }
  'Domain'  { 'Domain' }
  'Public'  { 'Public' }
}

Write-Host "Configuring Windows Firewall rule..." -ForegroundColor Cyan
Write-Host "  RuleName : $RuleName"
Write-Host "  Port     : $Port"
Write-Host "  Profile  : $Profile" 

# If a rule with the same display name exists, remove it (to avoid duplicates/mismatched settings)
$existing = Get-NetFirewallRule -DisplayName $RuleName -ErrorAction SilentlyContinue
if ($existing) {
  Write-Host "Existing rule found. Replacing it..." -ForegroundColor Yellow
  $existing | Remove-NetFirewallRule | Out-Null
}

$ruleParams = @{
  DisplayName = $RuleName
  Direction   = 'Inbound'
  Action      = 'Allow'
  Enabled     = 'True'
  Protocol    = 'TCP'
  LocalPort   = $Port
  Profile     = $profileArg
}

New-NetFirewallRule @ruleParams | Out-Null

Write-Host "✅ Firewall rule created." -ForegroundColor Green

Write-Host "\nCurrent matching rules:" -ForegroundColor Cyan

Get-NetFirewallRule -DisplayName $RuleName |
  Select-Object DisplayName, Enabled, Direction, Action, Profile |
  Format-Table -AutoSize

Get-NetFirewallRule -DisplayName $RuleName |
  Get-NetFirewallPortFilter |
  Select-Object Protocol, LocalPort |
  Format-Table -AutoSize

Write-Host "\nTip: If you want other machines to reach Streamlit, run Streamlit bound to 0.0.0.0 and use http://<your-ip>:$Port" -ForegroundColor DarkGray
