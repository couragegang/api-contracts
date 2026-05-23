# Копирует канон OpenAPI в зеркало сервиса (contracts-sync.json).
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("iam", "config", "mcp")]
    [string]$Id
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$manifest = Get-Content (Join-Path $root "contracts-sync.json") -Raw | ConvertFrom-Json
$m = $manifest.mirrors | Where-Object { $_.id -eq $Id } | Select-Object -First 1
if (-not $m) { throw "Unknown mirror id: $Id" }
$src = Join-Path $root ($m.canonical -replace "/", "\")
$dest = Join-Path (Join-Path $root "..") (Join-Path $m.serviceDir ($m.serviceCopy -replace "/", "\"))
$destDir = Split-Path $dest -Parent
if (-not (Test-Path $src)) { throw "Source not found: $src" }
New-Item -ItemType Directory -Force -Path $destDir | Out-Null
Copy-Item -LiteralPath $src -Destination $dest -Force
Write-Host "Synced $($m.id): $src -> $dest"
