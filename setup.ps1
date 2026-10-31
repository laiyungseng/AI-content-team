# Windows bootstrap: install uv if missing, then run the cross-platform setup.
# Usage (from this folder):  powershell -ExecutionPolicy Bypass -File setup.ps1
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Host 'uv (Python manager) not found. Installing it...'
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install --id astral-sh.uv -e --accept-package-agreements --accept-source-agreements
  } else {
    powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
  }
  # Make uv visible in this window without reopening it.
  $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') + ";$env:USERPROFILE\.local\bin"
}

uv run python .claude/skills/installation-setup/scripts/setup.py all
