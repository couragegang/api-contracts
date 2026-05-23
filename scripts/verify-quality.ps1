# Quality gate: Redocly lint + зеркала OpenAPI (contracts-sync.json).
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

if (-not (Test-Path "node_modules/@redocly/cli")) {
    Write-Host "Run: npm ci"
    exit 1
}

Write-Host "=== Redocly lint ==="
npx --no-install redocly lint

Write-Host "=== Contract mirrors ==="
if (-not $env:SERVICES_ROOT) {
    $env:SERVICES_ROOT = (Resolve-Path (Join-Path $root "..")).Path
}
if ($env:GITHUB_ACTIONS -eq "true") {
    $env:REQUIRE_SYNC_CHECK = "1"
}
node scripts/verify-sync.mjs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "=== Quality gate passed ==="
