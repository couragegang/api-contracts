# Копирует канон OpenAPI в зеркало сервиса (contracts-sync.json, поле mirrors[].id).
param(
    [Parameter(Mandatory = $true)]
    [string]$Id
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$manifest = Get-Content (Join-Path $root "contracts-sync.json") -Raw | ConvertFrom-Json
$m = $manifest.mirrors | Where-Object { $_.id -eq $Id } | Select-Object -First 1
if (-not $m) {
    $ids = ($manifest.mirrors | ForEach-Object { $_.id }) -join ", "
    throw "Unknown mirror id: $Id (known: $ids)"
}
$src = Join-Path $root ($m.canonical -replace "/", "\")
$dest = Join-Path (Join-Path $root "..") (Join-Path $m.serviceDir ($m.serviceCopy -replace "/", "\"))
$destDir = Split-Path $dest -Parent
if (-not (Test-Path $src)) { throw "Source not found: $src" }
New-Item -ItemType Directory -Force -Path $destDir | Out-Null
Copy-Item -LiteralPath $src -Destination $dest -Force
Write-Host "Synced $($m.id): $src -> $dest"
